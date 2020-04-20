#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
radio_api shared functions
"""
import json
import logging
import subprocess
import sqlite3
import re
from radio_api.db import get_db

def station_get(station_id):
    """
    This function retrieves a station's information

    :param station_id: station ID
    :type station_id: int
    """
    database = get_db()
    try:
        if station_id > 0:
            # return one particular station
            stations = database.execute(
                "SELECT * FROM stations WHERE station_id=?;",
                (station_id,)
            )
        else:
            # return all stations
            stations = database.execute("SELECT * FROM stations;")

        # prepare result
        result = {}
        result["results"] = [dict(row) for row in stations.fetchall()]
        return result
    except sqlite3.Error as err:
        logging.error('Unable to get station: %s', err)
        return False

def station_play(station_id):
    """
    Plays a radio station.

    :param station_id: station ID
    :type station_id: int
    """
    # stop previously running radio first
    radio_stop()
    # get station information
    station = station_get(station_id)
    logging.info(
        "About to play station: %s", station["results"][0]['station_url']
    )
    result = False
    try:
        command = "mplayer " + station["results"][0]['station_url'] + " &"
        subprocess.call(command, shell=True)
        with open("/tmp/radio.lock", "w") as lockfile:
            lockfile.write(str(station_id))
        result = True
    except FileNotFoundError as exc:
        logging.error("Looks like player is not installed: %s", exc)
    except subprocess.CalledProcessError as exc:
        logging.error("Unable to play station: %s %s", exc.stderr, exc.stdout)
    return result

def radio_stop():
    """
    This function stops the radio
    """
    logging.info("Stopping radio")
    with open("/tmp/radio.lock", "w") as lockfile:
        lockfile.write("")
    return run_command("killall mplayer")

def return_result(result):
    """
    This function simply returns an operation's status in result

    :param result: boolean whether successful
    :type result: bool
    """
    ret = {}
    if result:
        ret["code"] = 0
        ret["message"] = "SUCCESS"
    else:
        ret["code"] = 1
        ret["message"] = "FAILURE"
    return json.dumps(ret)

def run_command(command):
    """
    This function runs a command

    :param command: command
    :type command: str
    """
    result = False
    try:
        subprocess.call(command, shell=True)
        result = True
    except FileNotFoundError as exc:
        logging.error("Looks like command is not available: %s", exc)
    except subprocess.CalledProcessError as exc:
        logging.error("Unable to execute command: %s %s", exc.stderr, exc.stdout)
    return result

def get_command(command):
    """
    This functions runs a command and returns the output

    :param command: command
    :type command: str
    """
    try:
        command = subprocess.run(command, shell=True, capture_output=True, check=True)
    except FileNotFoundError as exc:
        logging.error("Looks like command is not available: %s", exc)
    except subprocess.CalledProcessError as exc:
        logging.error("Unable to execute command: %s %s", exc.stderr, exc.stdout)
    logging.info("Output: %s", command.stdout)
    return command

def get_station_id_by_name(station_name):
    """
    Returns a station ID by name.

    :param station_name: station name
    :type station_name: str
    """
    database = get_db()

    try:
        stations = database.execute(
            "SELECT station_id FROM stations WHERE station_name=?;",
            (station_name,)
        )
        # prepare result
        result = {}
        result["results"] = [dict(row) for row in stations.fetchall()]
        return result
    except IndexError:
        logging.error('Station not found')
        return False
    except sqlite3.Error as err:
        logging.error('Unable to find station: %s', err)
        return False

def volume_get():
    """
    This function returns the current volume level
    """
    logging.info("Get volume level")
    #volume = get_command(["echo", "'90%'"])
    volume = get_command(["amixer", "-M", "get", "PCM"])
    hits = re.search('[0-9]{1,2}%', str(volume.stdout))
    result = {}
    result['volume_level'] = hits.group(0).replace('%', '')
    return result

def volume_up():
    """
    This function increases the volume
    """
    logging.info("Increase volume level")
    return run_command("amixer -M set PCM 10%+")

def volume_down():
    """
    This function decreases the volume
    """
    logging.info("Decrease volume level")
    return run_command("amixer -M set PCM 10%-")

def volume_set(volume_level):
    """
    This function sets the volume to a specific level

    :param volume_level: volume level
    :type volume_level: int
    """
    logging.info('Set volume to station %s', volume_level)
    return run_command("amixer -M set PCM " + str(volume_level) + "%")
