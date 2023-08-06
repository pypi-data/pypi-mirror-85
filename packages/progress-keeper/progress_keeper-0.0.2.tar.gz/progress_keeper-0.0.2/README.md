# progress-keeper

This module is for keeping track of progress.  It's useful for idempotent multi-part processes.  If a process is interrupted or quits unexpectantly this can be used to keep track of the progress so that the next time the process is run, it can pick up where it left off.

## Install

```
pip install progress_keeper
```

## Usage

To create a progress object you need to define the following args:
- fp (str): file path of file to save progress into
- vars (list(str), optional): list of variables to include in progress file and keep track of. If undefined then it will assume only one var and use the default name - 'last_index_processed'.

When you create a progress object the module will check if the 'fp' exists and either use the values in that file if it does exist or create a new file (and set progress values to 0) if it does not exist.

```
fp = 'tmp/my-progress.cfg'
vars = ['process_abc','sub_process_a']

# create progress object
progress = Progress(fp, vars)

# increment progress 'var' by 1
progress.increment('process_abc')

# get value of progress 'var'
progress.values['progress_abc']

# reset value of progress
progress.reset('process_abc')

# delete progress file
progress.delete()
```