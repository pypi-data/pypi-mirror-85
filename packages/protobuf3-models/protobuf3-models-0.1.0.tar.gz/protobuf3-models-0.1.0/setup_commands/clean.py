# -*- coding:utf-8 -*-
import distutils
import subprocess
import sys


class CleanCommand(distutils.cmd.Command):
    """A custom command to clean build / test artifacts."""

    description = "Clean artifacts (reports, builds...)."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run command."""
        commands = (
            ["rm", "-Rf", ".pytest_cache"],
            ["rm", "-Rf", "htmlcov"],
            ["rm", "-Rf", "htmltest"],
            ["rm", "-f", ".coverage"],
            ["rm", "-f", "coverage.xml"],
            ["rm", "-f", "report.xml"],
            ["rm", "-Rf", "build"],
            ["rm", "-Rf", "dist"],
            ["rm", "-Rf", ".mypy_cache"],
        )

        for command in commands:
            self.announce(f'Running command: {" ".join(command)}', level=distutils.log.INFO)
            try:
                subprocess.check_call(command)
            except subprocess.CalledProcessError as ex:
                sys.exit(ex.returncode)
