import argparse
import os

from lib.utils import string_to_bool


def setup_args():
    parser = argparse.ArgumentParser(description="My script description")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=string_to_bool(os.getenv("UNOS_DEBUG", False)),
        help="Enable more verbose logging",
    )

    parser.add_argument(
        "-t",
        "--test",
        default=string_to_bool(os.getenv("UNOS_TEST", False)),
        action="store_true",
        help="Uses test data and doesn't write any data to disk",
    )

    parser.add_argument(
        "-v",
        "--version",
        dest="min_major_os_version",
        default=os.getenv("UNOS_MIN_MAJOR_OS_VERSION", None),
        help="Defines the minimum major OS version to use for the requiredMinimumOSVersion. Defaults to n-1.",
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="nudge_json_file",
        default=os.getenv("UNOS_NUDGE_JSON_FILE", None),
        help="Path to your json file containing a Nudge osVersionRequirements array. If not defined, a file named nudge.json will be created in the current working directory.",
        type=os.path.abspath,
    )

    return parser.parse_args()
