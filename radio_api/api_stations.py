#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
radio_api /api/stations blueprint
"""
import json
import logging
import sqlite3

from flask import (
    Blueprint, Response, request
)

from radio_api.db import get_db
from radio_api.api_shared import station_get, station_play, return_result, get_station_id_by_name

BP = Blueprint('api_stations', __name__, url_prefix='/api/stations')

def station_set(station_name, station_url, station_id=None, station_newid=None):
    """
    This function creates/updates a station

    :param station_name: station name
    :type station_name: str
    :param station_url: station URL
    :type station_url: str
    :param station_id: station ID
    :type station_id: int
    :param station_newid: new station ID
    :type station_newid: int
    """
    database = get_db()
    try:
        if station_id:
            # update existing station
            database.execute(
                """UPDATE stations SET station_id=?, station_name=?, station_url=?
                WHERE station_id=?""",
                (station_newid, station_name, station_url, station_id,)
            )
            database.commit()
            logging.info('Updated station %s', station_url)
            result = True
        else:
            # create new station
            database.execute(
                'INSERT INTO stations (station_name, station_url) VALUES (?, ?)',
                (station_name, station_url,)
            )
            database.commit()
            logging.info('Created station %s', station_url)
            result = True
        return result
    except sqlite3.Error as err:
        logging.error('Unable to create/update station: %s', err)
        return False

def station_delete(station_id):
    """
    Deletes a station.

    :param station_id: station ID
    :type station_id: int
    """
    database = get_db()
    try:
        count = database.execute(
            'DELETE FROM stations WHERE station_id=?;',
            (station_id,)
        ).rowcount
        database.commit()
        if count > 0:
            logging.info('Removed station #%s', station_id)
            result = True
        else:
            result = False
        return result
    except sqlite3.Error as err:
        logging.error('Unable to remove station: %s', err)
        return False



@BP.route("/<int:station_id>", methods=["GET"])
def api_station_get(station_id):
    """
    This function shows a particular station

    :param station_id: station ID
    :type station_id: int
    """
    logging.info("Retrieve station #%s", station_id)
    return Response(
        json.dumps(station_get(station_id)),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<station_name>", methods=["GET"])
def api_station_get_by_name(station_name):
    """
    This function shows a particular station by name

    :param station_name: station name
    :type station_name: str
    """
    station = get_station_id_by_name(station_name)
    station_id = next(iter(station['results'][0].values()))
    return api_station_get(station_id)

@BP.route("", methods=["POST"])
def api_station_create():
    """
    This function creates a new station
    """
    # execute and return result
    result_data = json.loads(request.data)
    logging.info('Create station %s', result_data["item"]["name"])
    result = station_set(
        result_data["item"]["name"],
        result_data["item"]["url"]
    )
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<int:station_id>", methods=["PUT", "POST"])
def api_station_update(station_id):
    """
    This function updates an existing station

    :param station_id: station ID
    :type station_id: int
    """
    # execute and return result
    logging.info('Update station %s', station_id)
    result_data = json.loads(request.data)
    result = station_set(
        result_data["item"]["name"],
        result_data["item"]["url"],
        station_id,
        result_data["item"]["id"],
    )
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<station_name>", methods=["PUT", "POST"])
def api_station_update_by_name(station_name):
    """
    This function updates an existing station by name

    :param station_name: station name
    :type station_name: str
    """
    station = get_station_id_by_name(station_name)
    station_id = next(iter(station['results'][0].values()))
    return api_station_update(station_id)

@BP.route("/<int:station_id>", methods=["DELETE"])
def api_station_delete(station_id):
    """
    This function removes a station

    :param station_id: station ID
    :type station_id: int
    """
    logging.info('Delete station %s', station_id)
    result = station_delete(station_id)
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<station_name>", methods=["DELETE"])
def api_station_delete_by_name(station_name):
    """
    This function removes a station by name

    :param station_name: station name
    :type station_name: str
    """
    station = get_station_id_by_name(station_name)
    station_id = next(iter(station['results'][0].values()))
    return api_station_delete(station_id)

@BP.route("/<int:station_id>/play", methods=["GET"])
def api_station_play(station_id):
    """
    This function plays a station

    :param station_id: station ID
    :type station_id: int
    """
    return Response(
        return_result(station_play(station_id)),
        status=200,
        mimetype="application/json"
    )

@BP.route("/<station_name>/play", methods=["GET"])
def api_station_play_by_name(station_name):
    """
    This function plays a station by name

    :param station_name: station name
    :type station_name: str
    """
    station = get_station_id_by_name(station_name)
    station_id = next(iter(station['results'][0].values()))
    return api_station_play(station_id)
