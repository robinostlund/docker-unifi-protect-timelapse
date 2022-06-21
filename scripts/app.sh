#!/bin/bash

set -e

echo "INFO: Starting app.sh pid $$ $(date)"

if [ `lsof | grep $0 | wc -l | tr -d ' '` -gt 1 ]
then
  echo "WARNING: A previous process is still running. Waiting for it to complete."
else
  echo $$ > /tmp/app.pid

  echo "INFO: Starting app"
  python3 /root/app.py
  exit_code=$?

  if [ -z "$CHECK_URL" ]; then
    echo "INFO: Define CHECK_URL with https://healthchecks.io to monitor the app"
  else
    # only update healtcheck if we have a valid exit code
    if [ $exit_code -eq 0 ]; then
      wget --quiet $CHECK_URL -O /dev/null
    fi
    
  fi

  rm -f /tmp/app.pid
fi