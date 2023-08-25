import json
import logging
import os
from datetime import datetime, timedelta

import requests
from lib.arguments import setup_args
from lib.utils import setup_logger
from packaging import version


def read_json_file(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def get_macos_product_versions():
    """Returns the macOS product versions from the GDMF API."""
    if test_mode:
        local_gdmf = os.path.join(script_dir, "resources/gdfm.json")

        try:
            json = read_json_file(local_gdmf)
            local_asset_sets = json["PublicAssetSets"]["macOS"]
            return local_asset_sets
        except FileNotFoundError:
            logging.error("Local GDMF file not found, falling back to remote GDMF.")

    apple_root_ca = os.path.join(script_dir, "resources/apple_root_ca.pem")

    url = "https://gdmf.apple.com/v2/pmv"
    response = requests.get(url, verify=apple_root_ca)
    macos_product_versions = response.json()["PublicAssetSets"]["macOS"]

    logging.debug(f"Return: {macos_product_versions}")
    return macos_product_versions


def get_nudge_json_file_path():
    """Returns the nudge json file path either from the command line argument or assumes a nudge.json file in the current working directory."""

    json_file_path = (
        args.nudge_json_file
        if args.nudge_json_file
        else os.path.join(execution_dir, "nudge.json")
    )

    if not os.path.exists(json_file_path):
        json_file_path = os.path.join(script_dir, "resources/template.json")

    logging.debug(f"Return: {json_file_path}")
    return json_file_path


def get_latest_major_version(macos_product_versions):
    """Returns the latest major version of macOS from the GDMF API."""
    latest_major_version = str(
        max(
            version.parse(ver["ProductVersion"]).major for ver in macos_product_versions
        )
    )

    logging.debug(f"Return: {latest_major_version}")
    return latest_major_version


def get_product_version_by_major(macos_product_versions, major_version):
    """Returns the latest product version for the specified major version."""

    filtered_versions = [
        version_info["ProductVersion"]
        for version_info in macos_product_versions
        if version.parse(version_info["ProductVersion"]).major
        == version.parse(major_version).major
    ]

    product_version_by_major = max(filtered_versions, default=None)

    logging.debug(f"Return: {product_version_by_major}")
    return product_version_by_major


def get_default_min_major_os_version(macos_product_versions):
    """
    If the minimum version is not specified, this function returns a default minimum version of n-1.
    """

    default_min_version = str(
        max(
            version.parse(ver["ProductVersion"]).major for ver in macos_product_versions
        )
        - 1
    )

    logging.debug(f"Return: {default_min_version}")
    return default_min_version


def get_required_install_date(install_delay=14):
    """Calculates the required installation date based on the current date and the specified install delay."""
    current_date = datetime.utcnow()
    future_date = current_date + timedelta(days=install_delay)
    future_date = future_date.replace(hour=12, minute=0, second=0, microsecond=0)
    required_install_date = future_date.isoformat() + "Z"

    logging.debug(f"Return: {required_install_date}")
    return required_install_date


def get_required_minimum_os_version(
    macos_product_versions, version_requirement, org_min_version
):
    """Returns the required minimum OS version based on the targeted OS versions rule and the organization's minimum supported OS version."""

    targeted_os_versions_rule = version_requirement["targetedOSVersionsRule"]
    required_minimum_os_version = version_requirement["requiredMinimumOSVersion"]

    logging.info(f"Targeted OS Versions Rule: {targeted_os_versions_rule}")
    logging.info(f"Current Minimum OS Version: {required_minimum_os_version}")

    major_version = (
        targeted_os_versions_rule
        if version.parse(targeted_os_versions_rule) >= version.parse(org_min_version)
        else get_latest_major_version(macos_product_versions)
    )

    product_version = get_product_version_by_major(
        macos_product_versions, major_version
    )

    if product_version is None:
        return None

    if version.parse(required_minimum_os_version) == version.parse(product_version):
        return None

    logging.info(f"Updated Minimum OS Version: {product_version}")
    return product_version


def save_nudge_json(nudge_json):
    """Saves the updated osVersionRequirements array to disk."""

    nudge_json_file_path = (
        args.nudge_json_file
        if args.nudge_json_file
        else os.path.join(execution_dir, "nudge.json")
    )

    with open(nudge_json_file_path, "w") as json_file:
        json.dump(nudge_json, json_file, indent=4)

    logging.info(f"Updated: {nudge_json_file_path}")


def main():
    macos_product_versions = get_macos_product_versions()
    required_installation_date = get_required_install_date()
    nudge_json = read_json_file(get_nudge_json_file_path())

    min_major_os_version = (
        args.min_major_os_version
        if args.min_major_os_version
        else get_default_min_major_os_version(macos_product_versions)
    )

    nudge_json["osVersionRequirements"] = [
        {
            **version_requirement,
            "requiredInstallationDate": required_installation_date,
            "requiredMinimumOSVersion": required_minimum_os_version,
        }
        if (
            required_minimum_os_version := get_required_minimum_os_version(
                macos_product_versions, version_requirement, min_major_os_version
            )
        )
        else version_requirement
        for version_requirement in nudge_json["osVersionRequirements"]
    ]

    if test_mode:
        logging.debug(f"nudge.json: {json.dumps(nudge_json, indent=4)}")
        return

    return save_nudge_json(nudge_json)


if __name__ == "__main__":
    args = setup_args()
    test_mode = args.test_mode if args.test_mode else False
    debug = test_mode or args.debug if not test_mode else True

    script_dir = os.path.dirname(__file__)
    execution_dir = os.getcwd()

    setup_logger(debug)
    logging.debug("Debug mode enabled")
    logging.debug(args)

    main()
