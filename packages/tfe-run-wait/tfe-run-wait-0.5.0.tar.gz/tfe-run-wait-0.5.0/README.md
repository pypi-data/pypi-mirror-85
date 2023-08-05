# tfe-run-wait
Command line utility to poll for a Terraform Enterprise run state change and apply a planned run.

## Usage
```
tfe-run-wait [-h] \
        --token TOKEN \
        --organization ORGANIZATION \
        --workspace WORKSPACE \
        --clone-url CLONE\_URL \
        --commit-sha COMMIT\_SHA \
        [--wait-for-status WAIT\_FOR\_STATUS] \
        [--maximum-wait-time MAXIMUM\_WAIT\_TIME]

tfe-run-apply [-h] \
        --token TOKEN \
        --organization ORGANIZATION \
        --workspace WORKSPACE \
        --clone-url CLONE\_URL \
        --commit-sha COMMIT\_SHA \
        --comment COMMENT \
        [--maximum-wait-time MAXIMUM\_WAIT\_TIME]
```

## Options
```
  --token TOKEN         Terraform Enterprise access token, default from TFE\_API\_TOKEN
  --organization ORGANIZATION
                        of the workspace
  --workspace WORKSPACE
                        to inspect runs for
  --clone-url CLONE\_URL
                        of source repository for the run
  --commit-sha COMMIT\_SHA
                        of commit which initiated the run
  --wait-for-status WAIT\_FOR\_STATUS
                        wait state to reach, defaults to 'applied' and 'planned_and_finished'
  --maximum-wait-time MAXIMUM\_WAIT\_TIME
                        for state to be reached in minutes, default 45
  --comment             to use in the apply of the planned run.
  -h, --help            show this help message and exit
```


## Description
Finds a Terraform enterpise run initiated for the specified git commit and either polls for a specific state change or apply the planned changes.

tfe-run-wait will wait until the specified status is reached. By default it will wait for the status `applied` or `planned_and_finished`. When the run 
  reaches a non specified final state, it will exit with an error.

tfe-run-apply will request terraform to apply to plan for the run. If the status of the run is already `applied` or `planned_and_finished`, it will exit without an error.
  It will not check whether the run is in the correct state. The run should be in the state `planned` or `policy_checked`.
