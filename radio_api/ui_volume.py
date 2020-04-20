#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
radio_api /volume UI blueprint
"""
from flask import (
    Blueprint, render_template
)
from radio_api.api_volume import volume_get, volume_up, volume_down

BP = Blueprint('ui_volume', __name__, url_prefix='/volume')

@BP.route("/", methods=["GET"])
def ui_volume():
    """
    This function shows volume control
    """
    # get current volume
    volume = volume_get()
    # render stations in HTML template
    return render_template("volume.html", result=volume)

@BP.route("/up", methods=["GET"])
def ui_volume_up():
    """
    This function increases the volume
    """
    msg = {}
    msg['link'] = "/volume"
    msg['link_text'] = "back"
    msg['text'] = "Volume could not be increased!"
    if volume_up():
        msg['text'] = "Volume increased!"
    return render_template("message.html", message=msg)

@BP.route("/down", methods=["GET"])
def ui_volume_down():
    """
    This function decreases the volume
    """
    msg = {}
    msg['link'] = "/volume"
    msg['link_text'] = "back"
    msg['text'] = "Volume could not be decreased!"
    if volume_down():
        msg['text'] = "Volume decreased!"
    return render_template("message.html", message=msg)
