# -*- coding:utf-8 -*-
import distutils
import subprocess
import sys


class ProtocCommand(distutils.cmd.Command):
    """A custom command to run protoc generator."""

    description = "Compile protoc definitions."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run command."""
        commands = (
            [
                "protoc",
                "-I",
                ".",
                "--python_out",
                ".",
                "tests/protobuf3_models_tests.proto",
            ],
        )

        for command in commands:
            self.announce(f'Running command: {" ".join(command)}', level=distutils.log.INFO)
            try:
                subprocess.check_call(command)
            except subprocess.CalledProcessError as ex:
                sys.exit(ex.returncode)
