#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
radio_api / UI blueprint
"""
from flask import (
    Blueprint, render_template, send_from_directory
)
from radio_api.api import radio_stop, radio_next, radio_previous

BP = Blueprint('ui', __name__, url_prefix='/')

@BP.route("/")
def index():
    """
    This function simply presents the main page
    """
    return render_template("index.html")

@BP.route("/stop")
def ui_stop_radio():
    """
    This function stops the radio
    """
    msg = {}
    msg['link'] = "/"
    msg['link_text'] = "back"
    msg['text'] = "Stop request could not be sent!"
    if radio_stop():
        msg['text'] = "Stop request sent!"
    return render_template("message.html", message=msg)

@BP.route("/next")
def ui_next_station():
    """
    This function plays the next station
    """
    msg = {}
    msg['link'] = "/"
    msg['link_text'] = "back"
    msg['text'] = "Station request could not be sent!"
    if radio_next():
        msg['text'] = "Station request sent!"
    return render_template("message.html", message=msg)

@BP.route("/previous")
def ui_previous_station():
    """
    This function plays the previous station
    """
    msg = {}
    msg['link'] = "/"
    msg['link_text'] = "back"
    msg['text'] = "Station request could not be sent!"
    if radio_previous():
        msg['text'] = "Station request sent!"
    return render_template("message.html", message=msg)

@BP.route('/css/<path:path>')
def send_js(path):
    """
    This function returns the CSS
    """
    return send_from_directory('templates/css', path)
