import argparse
from dataclasses import dataclass


@dataclass
class CommandLineOptions:
    config_file: str
    loglevel: str


def parse_command_line() -> CommandLineOptions:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        default="./.pyolice.yml",
        help="Provide configuration file.",
    )
    # Log level
    parser.add_argument(
        "--log",
        dest="loglevel",
        default="warning",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Provide logging level. Example --log debug', default='WARNING'",
    )
    options = parser.parse_args()

    return CommandLineOptions(
        config_file=options.config_file, loglevel=options.loglevel
    )
