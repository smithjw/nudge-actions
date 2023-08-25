# nudge-action
Reusable Workflow and stand-alone Python script for updating a Nudge osVersionRequirements array using Apple's gdfm service (https://gdmf.apple.com/v2/pmv).

## Python Script
This has been written and tested on Python 3.11. The script can be run independtly of the GitHub Action and takes the following input:

- `--debug` OR `-d` OR `UNOS_DEBUG` (environment variable)
- `--test` OR `-t` OR `UNOS_TEST` (environment variable)
- `--version` OR `-v` OR `UNOS_MIN_MAJOR_OS_VERSION` (environment variable)
- `--file` OR `-f` OR `UNOS_NUDGE_JSON_FILE` (environment variable)

