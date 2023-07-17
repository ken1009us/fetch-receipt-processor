"""
This script sets up a virtual environment, installs required packages,
and performs linting using Flake8.

"""

import nox
import sys


from pathlib import Path

VERSION = '3.11.4'


@nox.session(python=VERSION, reuse_venv=True)
def setup(session):
    """
    Sets up the virtual environment and installs the required packages.

    Args:
        session (nox.Session): The Nox session object.

    Raises:
        nox.command.CommandFailed: If the installation of requirements fails.
    """
    session_name = "setup"
    activate_venv(session, session_name)
    session.log("Virtual environment activated.")
    try:
        session.run("pip3", "install", "-r", "requirements.txt")
    except nox.command.CommandFailed:
        session.error("Failed to install requirements.")


@nox.session(python=VERSION, reuse_venv=True)
def lint(session) -> None:
    """
    Performs linting using Flake8.

    Args:
        session (nox.Session): The Nox session object.

    Raises:
        nox.command.CommandFailed: If the linting process fails.
    """
    session_name = "lint"
    activate_venv(session, session_name)
    try:
        session.install("flake8")
        session.run("flake8", ".", silent=True, external=True)
    except nox.command.CommandFailed:
        session.error("Linting failed.")


def activate_venv(session, session_name):
    """
    Activates the virtual environment based on the platform.

    Args:
        session (nox.Session): The Nox session object.
        session_name (str): The name of the session.

    Raises:
        nox.command.CommandFailed: If the virtual environment activation fails.
    """
    nox_path = Path(".nox")
    if sys.platform.startswith('win'):
        p = nox_path / session_name / 'Scripts' / 'activate'
        try:
            session.run(str(p), silent=True, external=True)
        except nox.command.CommandFailed:
            session.error("Failed to activate virtual environment.")
    else:
        p = nox_path / session_name / 'bin' / 'activate'
        try:
            session.run("bash", "-c", f"source {p}",
                        silent=True,
                        external=True)
        except nox.command.CommandFailed:
            session.error("Failed to activate virtual environment.")
