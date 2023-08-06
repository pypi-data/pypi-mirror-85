from dataclasses import dataclass
import subprocess
from typing import List


def print_warning_message(message: str) -> None:
    print("\033[93m" + message + "\033[0m")


@dataclass
class Crime:
    pattern: str  # Search pattern
    directory: str  # directory where the search should take place
    message: str  # Message to display when a crimes is found
    excluded_files: List[str]  # Files to be excluded from the search


CRIMES = [
    Crime(
        pattern="UserLogin.objects.create",
        directory="apps",
        message="Should not directly ORM to create UserLogin. Use UserAnalyticsService instead.",
        excluded_files=["apps/analytics/backends.py"],
    ),
    Crime(
        pattern="UserRegister.objects.create",
        directory="apps",
        message="Should not directly ORM to create UserRegister. Use UserAnalyticsService instead.",
        excluded_files=["apps/analytics/backends.py"],
    ),
    Crime(
        pattern="UserEmail.objects.get",
        directory="apps",
        message="Should not directly ORM to get UserEmail. Use UserEmailService.get_by_email instead.",
        excluded_files=[
            "apps/wave_auth/backends.py",
            "apps/wave_auth/tests/models_tests.py",
        ],
    ),
    Crime(
        pattern="Site.objects",
        directory="apps",
        message=(
            "The `sites` framework is not needed for retrieving the current domain."
            "Check out the functions in 'core.utils' for your need."
        ),
        excluded_files=["apps/wave_auth/migrations/0003_default_fixtures.py"],
    ),
]


def detect_crimes() -> bool:
    success = True
    for crime in CRIMES:
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
    success = detect_crimes()
    return 0 if success else 1
