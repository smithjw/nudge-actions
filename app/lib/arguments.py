import argparse
import os

from lib.utils import check_env_var


def setup_args():
    parser = argparse.ArgumentParser(description="My script description")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=check_env_var("UNOS_DEBUG", "bool", False),
        help="Enable more verbose logging",
    )

    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        default=check_env_var("UNOS_TEST", "bool", False),
        help="Uses test data and doesn't write any data to disk",
    )

    parser.add_argument(
        "-v",
        "--version",
        dest="min_major_os_version",
        default=check_env_var("UNOS_MIN_MAJOR_OS_VERSION", "str", None),
        help="Defines the minimum major OS version to use for the requiredMinimumOSVersion. Defaults to n-1.",
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="nudge_json_file",
        default=check_env_var("UNOS_NUDGE_JSON_FILE", "str", None),
        help="Path to your json file containing a Nudge osVersionRequirements array. If not defined, a file named nudge.json will be created in the current working directory.",
        type=os.path.abspath,
    )

    return parser.parse_args()
