from typing import Any, Dict

import setuptools

version: Dict[str, Any] = {}
exec(open("sym/cli/version.py").read(), version)

with open("DESCRIPTION.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sym-cli",
    version=version["__version__"],
    author="SymOps, Inc.",
    author_email="pypi@symops.io",
    description="The CLI for Sym",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/symopsio/runtime/sym-cli",
    packages=setuptools.find_namespace_packages(include=["sym.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Click",
        "PyYAML",
        "sentry-sdk>=0.18",
        "validators",
        "analytics-python",
        "boto3>=1.14",
        "click-option-group",
        "immutables",
        "portalocker",
        "SecretStorage>3",
        "keyring",
    ],
    entry_points="""
        [console_scripts]
        sym=sym.cli.sym:sym
    """,
)
