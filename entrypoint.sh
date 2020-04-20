#!/bin/sh
# move to folder
cd /opt/radio_api
# export variables
export FLASK_APP=radio_api
export FLASK_ENV=prodcution
# create database if not exists
if [ ! -f instance/radio_api.sqlite ]; then
  flask init-db
fi
# clear lockfile
echo "" > /tmp/radio.lock
# set volume level to 70%
amixer -M set PCM 70%
# run application
flask run --host=0.0.0.0
