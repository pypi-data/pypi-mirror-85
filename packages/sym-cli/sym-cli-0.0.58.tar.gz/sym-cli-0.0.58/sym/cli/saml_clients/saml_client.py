import re
import shlex
import sys
from abc import ABC, abstractmethod
from configparser import ConfigParser
from datetime import datetime, timedelta
from operator import attrgetter
from pathlib import Path
from typing import ClassVar, Optional, Sequence, Type
from urllib.parse import urlsplit

from ..errors import CliError
from ..helpers import segment, validations
from ..helpers.config import SymConfigFile
from ..helpers.keywords_to_options import keywords_to_options
from ..helpers.os import read_write_lock
from ..helpers.params import Profile, get_aws_saml_url, get_profile


class SAMLClient(ABC):
    binary: ClassVar[str]
    option_value: ClassVar[str]
    priority: ClassVar[int]
    setup_help: ClassVar[Optional[str]] = None

    resource: str
    options: "GlobalOptions"

    config_file: SymConfigFile

    _config: Optional[ConfigParser]
    _session_exists: bool
    _checked_setup: bool

    def __init__(self, resource: str, *, options: "GlobalOptions") -> None:
        self.resource = resource
        self.options = options

        self._config = None
        self._session_exists = False
        self._checked_setup = False

        self.check_is_setup()

    @property
    def _section_name(self):
        return f"sym-{self.resource}"

    @property
    def debug(self):
        return self.options.debug

    @property
    def log_dir(self):
        return self.options.log_dir

    @classmethod
    def validate_resource(cls, resource: str):
        return validations.validate_resource(resource)

    def check_is_setup(self):
        if self._checked_setup:
            return
        self._checked_setup = True

        if self.is_setup():
            return

        print(
            f"Warning: sym might not function correctly until {self.binary} is setup.",
            file=sys.stderr,
        )
        if self.setup_help:
            print(f"Hint: {self.setup_help}", file=sys.stderr)

    @classmethod
    def sorted_subclasses(cls):
        return sorted(cls.__subclasses__(), key=attrgetter("priority"), reverse=True)

    @abstractmethod
    def _exec(self, *args: str, **opts: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def _ensure_config(self, profile: Profile) -> ConfigParser:
        raise NotImplementedError

    @abstractmethod
    def is_setup(self) -> bool:
        raise NotImplementedError

    def _cli_options(self):
        return {
            "saml_client": self.option_value,
            "debug": self.debug,
            "log_dir": self.log_dir,
        }

    @property
    def cli_options(self):
        return shlex.join(keywords_to_options([self._cli_options()]))

    def exec(self, *args: str, **kwargs: str) -> None:
        self.ensure_session()
        self.dprint(f"client: {self.cli_options}")
        return self._exec(*args, **kwargs)

    def _ensure_session(self, *, force: bool):
        self.dprint(f"ensuring session, force={force}")
        self._exec("true", silence_stderr_=False, suppress_=True)

    def ensure_session(self, force=False):
        if not self._session_exists:
            self._ensure_session(force=force or self._creds_expiring())
            self._session_exists = True

    def ensure_config(self) -> ConfigParser:
        if not self._config:
            config = self._ensure_config(self.get_profile())
            with self.config_file as f:
                config.write(f)
            self.dconfig(config)
            self._config = config
        return self._config

    def subconfig(self, file_name, **deps):
        return SymConfigFile(
            **self._cli_options(), resource=self.resource, **deps, file_name=file_name
        )

    def dprint(self, *s: Sequence[str], **kwargs):
        self.options.dprint(*s, **kwargs)

    def dconfig(self, config: ConfigParser):
        if self.debug:
            print("Writing config:", file=sys.stderr)
            config.write(sys.stderr)

    def log_subprocess_event(self, command: tuple):
        segment.track("Subprocess Called", binary=command[0])

    def get_profile(self) -> Profile:
        try:
            profile = get_profile(self.resource)
        except KeyError:
            raise CliError(f"Invalid resource: {self.resource}")

        self.dprint(f"Using profile {profile}")
        return profile

    def get_aws_saml_url(self, bare: bool = False) -> str:
        url = get_aws_saml_url(self.resource)
        if bare:
            url = urlsplit(url).path[1:]
        return url

    @property
    def _cred_env_vars(self):
        return (
            "AWS_REGION",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_SESSION_TOKEN",
            "AWS_SECURITY_TOKEN",
            "AWS_CREDENTIAL_EXPIRATION",
        )

    def get_creds(self):
        output = self._exec("env", capture_output_=True, censor_=True)[-1]
        env_vars = re.findall(r"([\w_]+)=(.+)\n", output)
        return {k: v for k, v in env_vars if k in self._cred_env_vars}

    def _creds_expiring(self, buffer=timedelta(minutes=2)):
        try:
            creds = self.get_creds()
        except Exception:
            return True

        if (expires := creds.get("AWS_CREDENTIAL_EXPIRATION")) :
            parsed = datetime.fromisoformat(expires)
            remaining = parsed - datetime.now(parsed.tzinfo)
            self.dprint(f"{remaining} remaining in creds session")
            return remaining < buffer
        return False

    def write_creds(self, *, path: Path, profile: str):
        self.dprint(f"writing creds, profile={profile}")

        if self._creds_expiring(buffer=timedelta(minutes=5)):
            self._ensure_session(force=True)

        creds = self.get_creds()
        creds["region"] = creds.pop("AWS_REGION", self.get_profile().region)
        creds["x_security_token_expires"] = creds.pop("AWS_CREDENTIAL_EXPIRATION", None)
        creds["x_sym_ansible_bucket"] = self.get_profile().ansible_bucket

        path.parent.mkdir(parents=True, exist_ok=True)

        with read_write_lock(path) as f:
            config = ConfigParser()
            config.read_file(f)

            if config.has_section(profile):
                config.remove_section(profile)
            config.add_section(profile)
            for k, v in creds.items():
                if v:
                    config.set(profile, k.lower(), v)

            f.seek(0)
            f.truncate()
            config.write(f)

    def clone(self, *, klass: Type["SAMLClient"] = None, **overrides):
        kwargs = {
            key: overrides.get(key, getattr(self, key)) for key in ["resource", "options"]
        }
        return (klass or self.__class__)(**kwargs)
