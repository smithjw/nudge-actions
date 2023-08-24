import hashlib
import logging


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
