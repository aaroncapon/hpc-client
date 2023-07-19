#!/usr/bin/env bash
unset CDPATH; cd "$( dirname "${BASH_SOURCE[0]}" )"; cd "$(pwd -P)"
cd ..

#
# Place any cluster-specific commands here...
#


#
# End cluster-specific block
#

source "settings/credentials.sh"

# Logfile location
logfile="$PWD/logs/cast.log"

# Launch cast
# Using "timeout" prevents the script hanging when launched automatically.
# This time limit may need to be adjusted based on the speed of your system.
cd src_code
timeout 5m python -m pipenv run ./cast.py "$@" 2>&1 | tee -a "$logfile"
