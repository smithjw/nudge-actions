# update_nudge_osVersionRequirements.py

This has been written and tested on Python 3.11. The script can be run independtly of the GitHub Action and takes the following inputs:

- `--debug` OR `-d` OR `UNOS_DEBUG` (environment variable)
  - Produces verbose output to the console
- `--test-mode` OR `-t` OR `UNOS_TEST_MODE` (environment variable)
  - Will enable verbose logging and prevent writing anything to disk
- `--version` OR `-v` OR `UNOS_MIN_MAJOR_OS_VERSION` (environment variable)
  - Sets the minimum major OS version supported in your environment
- `--file` OR `-f` OR `UNOS_NUDGE_JSON_FILE` (environment variable)
  - Location of your json file containing the `osVersionRequirements` array. If none is specified the file `nudge.json` is written to the current working directory.

## Running the standalone script

``` shell
# Clone Repo
gh repo clone smithjw/nudge-actions
cd nudge-actions/app

# Create Python Virtual Environment
python -m venv .venv
source .venv/bin/activate

# Install Requirements
pip install -r requirements.txt

# Run Script
python update_nudge_osVersionRequirements.py --test-mode
```

## Updating Requirements Hashes

> *This is really a note for FutureJames*

To ensure that the hashes supplied in `requirements.txt` work across multiple platforms, we're taking advantakge of the Python package [`pip-compile-cross-platform`](https://pypi.org/project/pip-compile-cross-platform/) which can be installed with the command:

`pip install --user pip-compile-cross-platform`

To run, execute the following command:

`pip-compile-cross-platform --min-python-version 3.12 app/requirements.in`
