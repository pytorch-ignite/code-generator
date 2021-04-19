"""
This script is for maintainers only.
`semver` and `inquirer` need to be installed beforehand.
pip install semver==2.13.0 inquirer==2.7.0
"""

import subprocess

from semver import VersionInfo
import inquirer


with open("version.txt", "r") as f:
    version = f.read()


questions = [
    inquirer.List(
        "part",
        message="Choose version bump",
        choices=["major", "minor", "patch"],
    )
]

part = inquirer.prompt(questions=questions)

version = VersionInfo.parse(version).next_version(part=part["part"])

with open("version.txt", "w") as f:
    f.write(str(version) + "\n")


subprocess.run(["git", "add", "version.txt"])
subprocess.run(["git", "commit", "-m", f"release: v{version}"])
subprocess.run(["git", "tag", f"v{version}"])
subprocess.run(["git", "push", "origin", f"v{version}"])
subprocess.run(["git", "push"])
