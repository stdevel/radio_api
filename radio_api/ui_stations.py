#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
radio_api /stations UI blueprint
"""
from flask import (
    Blueprint, request, render_template
)
from radio_api.api_stations import station_get, station_set, station_delete, station_play

BP = Blueprint('ui_stations', __name__, url_prefix='/stations')

@BP.route("/", methods=["GET"])
def ui_form_stations():
    """
    This function lists all stations
    """
    # get _all_ the stations
    stations = station_get(0)
    # render stations in HTML template
    return render_template("stations.html", result=stations)

@BP.route("/create", methods=["GET", "POST"])
def ui_form_create_station():
    """
    This function presents the form to create stations
    and returns the API result
    """
    if request.method == "POST":
        # create station
        msg = {}
        msg['link'] = "/stations"
        msg['link_text'] = "back"
        msg['text'] = "Station could not be created!"
        if station_set(
                request.form["name"],
                request.form["url"],
            ):
            msg['text'] = "Station created!"
        result = render_template("message.html", message=msg)
    else:
        # show form
        result = render_template("station_create.html")
    return result

@BP.route("/delete/<int:station_id>", methods=["GET"])
def ui_form_delete_station(station_id):
    """
    This function deletes a particular station

    :param station_id: station ID
    :type station_id: int
    """
    # try to delete station
    msg = {}
    msg['link'] = "/stations"
    msg['link_text'] = "back"
    msg['text'] = "Station could not be deleted!"
    if station_delete(station_id):
        msg['text'] = "Station deleted!"
    return render_template("message.html", message=msg)

@BP.route("/edit/<int:station_id>", methods=["GET", "POST"])
def ui_form_edit_station(station_id):
    """
    This function presents the form to edit stations and returns form
    data to the API

    :param station_id: station ID
    :type station_id: int
    """
    if request.method == "POST":
        # edit station
        msg = {}
        msg['link'] = "/stations"
        msg['link_text'] = "back"
        msg['text'] = "Station could not be edited!"
        if station_set(
                request.form["station_name"],
                request.form["station_url"],
                station_id,
                station_newid=request.form["station_id"]
            ):
            msg['text'] = "Station edited!"
        result = render_template("message.html", message=msg)
    else:
        # show form, preselect values
        try:
            result = station_get(station_id)["results"][0]
            result = render_template("station_edit.html", station=result)
        except IndexError:
            result = render_template("station_nonexist.html")
    return result

@BP.route("/play/<int:station_id>", methods=["GET"])
def ui_form_play_station(station_id):
    """
    This function plays a particular station

    :param station_id: station ID
    :type station_id: int
    """
    # try to play station
    msg = {}
    msg['link'] = "/stations"
    msg['link_text'] = "back"
    msg['text'] = "Play request could not be sent!"
    if station_play(station_id):
        msg['text'] = "Play request sent!"
    return render_template("message.html", message=msg)
