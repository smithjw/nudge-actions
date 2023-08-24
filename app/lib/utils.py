import argparse
import hashlib
import logging
import os


def string_to_bool(value) -> bool:
    """Convert a string representation of truth to true (1) or false (0).

    True values are case insensitive 'y', 'yes', 't', 'true', 'on', and '1'.
    false values are case insensitive 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if 'val' is anything else.
    """

    if type(value) is bool:
        # Return the value if it's already a boolean
        return value

    val = value.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


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


def setup_logger(debug=False):
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(filename)s - %(funcName)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


async def hash_string(string: str):
    hash_obj = hashlib.sha256(string.encode())
    hash_hex = hash_obj.hexdigest()
    short_hash_hex = hash_hex[:6]

    return short_hash_hex
