#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
radio_api /api/stations blueprint
"""
import json
import logging

from flask import (
    Blueprint, Response
)
from radio_api.api_shared import station_get, station_play, radio_stop, return_result

BP = Blueprint('api', __name__, url_prefix='/api')

def radio_previous():
    """
    This function plays the previous station
    """
    previous_station = 0
    # get stations
    stations = [x["station_id"] for x in station_get(0)["results"]]
    # get current station
    try:
        with open("/tmp/radio.lock", "r") as lockfile:
            current_station = int(lockfile.read())
    except ValueError:
        current_station = 0
    logging.info("Current station: %d", current_station)
    # get previous or first station
    if current_station and current_station > 0:
        # get position
        position = stations.index(current_station)
        if (position+1) >= 1 and position < len(stations):
            previous_station = stations[stations.index(current_station)-1]
    else:
        # play first station
        previous_station = stations[0]
    logging.info("Previous station: %d", previous_station)
    return station_play(previous_station)

def radio_next():
    """
    This function plays the next station
    """
    next_station = 0
    # get stations
    stations = [x["station_id"] for x in station_get(0)["results"]]
    # get current station
    try:
        with open("/tmp/radio.lock", "r") as lockfile:
            current_station = int(lockfile.read())
    except ValueError:
        current_station = 0
    logging.info("Current station: %d", current_station)
    # get next or last station
    if current_station and current_station > 0:
        # get position
        position = stations.index(current_station)
        if (position+1) < len(stations):
            next_station = stations[stations.index(current_station)+1]
        else:
            next_station = stations[0]
    else:
        # play first station
        next_station = stations[0]
    logging.info("Next station: %d", next_station)
    return station_play(next_station)

def radio_current():
    """
    This function returns the currently played station
    """
    # get current station
    try:
        with open("/tmp/radio.lock", "r") as lockfile:
            current_station = int(lockfile.read())
    except ValueError:
        current_station = 0
    logging.info("Current station: %d", current_station)
    if current_station != 0:
        station_info = station_get(current_station)
    else:
        station_info = {}
    return station_info



@BP.route("/previous", methods=["GET"])
def api_previous():
    """
    This function plays the previous station
    """
    return Response(
        return_result(radio_previous()),
        status=200,
        mimetype="application/json"
    )

@BP.route("/next", methods=["GET"])
def api_next():
    """
    This function plays the next station
    """
    return Response(
        return_result(radio_next()),
        status=200,
        mimetype="application/json"
    )

@BP.route("/stop", methods=["GET"])
def api_stop():
    """
    This function stops the radio
    """
    return Response(
        return_result(radio_stop()),
        status=200,
        mimetype="application/json"
    )

@BP.route("/current", methods=["GET"])
def api_current():
    """
    This function returns the currently played station
    """
    return Response(
        json.dumps(radio_current()),
        status=200,
        mimetype="application/json"
    )
