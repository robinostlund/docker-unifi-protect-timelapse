#!/bin/bash
set -e

# configure timezone
if [ ! -z "$TZ" ]
then
  cp /usr/share/zoneinfo/$TZ /etc/localtime
  echo $TZ > /etc/timezone
fi

# setup cron schedule
if [ -z "$CRON" ]
  then
    echo "INFO: Add CRON=\"0 * * * *\" to perform image capture every hour"
  else
    # setup cron job
    crontab -d
    echo "$CRON /root/app.sh >> /tmp/app.log 2>&1" > /tmp/crontab.tmp
    crontab /tmp/crontab.tmp
    rm /tmp/crontab.tmp

    # start cron
    echo "INFO: Starting crond ..."
    touch /tmp/crond.log
    touch /tmp/app.log
    crond -b -l 0 -L /tmp/crond.log
    echo "INFO: crond started"
    tail -F /tmp/crond.log /tmp/app.log
fi
