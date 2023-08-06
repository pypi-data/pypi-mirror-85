from dataclasses import dataclass
import logging
import subprocess
from typing import List, Optional

import yaml

from .command_parser import CommandLineOptions, parse_command_line


def print_warning_message(message: str) -> None:
    print("\033[93m" + message + "\033[0m")


@dataclass
class Crime:
    pattern: str  # Search pattern
    directory: str  # directory where the search should take place
    message: str  # Message to display when a crimes is found
    excluded_files: Optional[List[str]] = None  # Files to be excluded from the search


def load_crimes(config_file_path: str) -> List[Crime]:
    with open(config_file_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return [Crime(**crime) for crime in config["crimes"]]


def detect_crimes(crimes: List[Crime]) -> bool:
    success = True
    for crime in crimes:
        result = subprocess.run(
            f"ag {crime.pattern} {crime.directory} -l",
            shell=True,
            capture_output=True,
        )
        # print(result.stdout, result.stderr)
        if result.returncode == 0:
            matched_files = result.stdout.decode("utf-8").strip().split("\n")
            violation_files = sorted(
                set(matched_files) - set(crime.excluded_files or [])
            )
            if violation_files:
                print(f"Found crime pattern '{crime.pattern}' in {violation_files}")
                print_warning_message(crime.message)
                print()
                success = False

    return success


def main() -> int:
    options = parse_command_line()
    # Config logging
    logging.basicConfig(level=getattr(logging, options.loglevel.upper()))

    # Load config file
    crimes = load_crimes(options.config_file)
    logging.debug(f"Defined crimes: {crimes}")

    # Execute
    success = detect_crimes(crimes)
    return 0 if success else 1


if __name__ == "__main__":
    main()
