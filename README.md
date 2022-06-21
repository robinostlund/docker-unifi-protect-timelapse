[![Docker Image CI](https://github.com/robinostlund/docker-unifi-protect-timelapse/actions/workflows/docker-build.yaml/badge.svg)](https://github.com/robinostlund/docker-unifi-protect-timelapse/actions/workflows/docker-build.yaml)

# docker-unifi-protect-timelapse
This tool collects snapshots from your ubiquiti cameras on schedule so you will be able to create a timelapse from it.

## Usage

### Requirements
Each camera needs to have anonymous snapshots enabled. This can be enabled by logging into each camera and enabling it.

### Config file
All of your ubiquti cameras needs their own section inside the configuration file, example:
```
[Camera-Back]
name = Back
ip = 192.168.0.100

[Camera-Front]
name = Front
ip = 192.168.0.101
```
This file needs to be mounted to /app.conf in the docker container, check Start chapter here below on how to mount that file.

### Environment variables
* `CRON` crontab schedule `0 * * * *` to perform image capture every hour
* `CHECK_URL` [healthchecks.io](https://healthchecks.io) url or similar cron monitoring to perform a `GET` after a successful image capture
* `TZ` set the [timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) to use for the cron and log `Europe/Stockholm`

### Start
```sh
docker pull robostlund/unifi-protect-timelapse:latest
docker run -dt \
    --name unifi-protect-timelapse \
    --env CRON="0 * * * *" \
    --env CHECK_URL="https://hc-ping.com/hchk_uuid" \
    --env TZ="Europe/Stockholm" \
    --volume /path/to/config:/app.conf:ro \
    --volume /path/to/storage:/storage:rw \
    --label com.centurylinklabs.watchtower.enable='true' \
    robostlund/unifi-protect-timelapse:latest
```