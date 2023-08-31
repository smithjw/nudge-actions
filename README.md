# nudge-actions

Reusable Workflow and stand-alone Python script for updating a Nudge osVersionRequirements array using Apple's gdfm service (https://gdmf.apple.com/v2/pmv).

## Reusable Workflow

To call this workflow from your own repo, create a GitHub Actions Workflow file with the following `jobs` block:

``` yaml
name: "Test workflow_call"

on:
  workflow_dispatch:
  # schedule: # Uncomment to run this on a schedule
  #   - cron: '0 1 * * *' # Runs at 01:00am each day UTC

permissions:
  contents: write
  pull-requests: write

jobs:
  call_workflow:
    uses: smithjw/nudge-actions/.github/workflows/update-nudge-version.yml@main
    with:
      unos_test_mode: true
```

- The permissions block is required so that the Reusable Workflow is able to write changes to the json file in your repo and open a new PR before those changes are merged into your main branch.
- If you would like to specify the minimum os version, add `unos_min_major_os_version` to your Workflow
- If you would like to specify location (relative to the working directory of your repo) of the nudge.json file, add `unos_nudge_json_file` to your Workflow
- To write an updated file, and create a new in your repo, set `unos_test_mode` to `false`

## Python Script

To run the Python script independly of the GitHub Actions Reusable Workflow, [please see the documentation here](app/README.md)

### Notes

If https://gdmf.apple.com/v2/pmv changes format in the future or can no longer be used, an alternative could be https://jamf-patch.jamfcloud.com/v1/software/
