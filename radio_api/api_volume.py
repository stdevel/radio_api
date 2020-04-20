#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
radio_api /api/volume blueprint
"""
import json

from flask import (
    Blueprint, Response, request
)

from radio_api.api_shared import return_result, volume_get, volume_set, volume_up, volume_down

BP = Blueprint('api_volume', __name__, url_prefix='/api/volume')

@BP.route("/", methods=["GET"])
def api_volume_get():
    """
    This function returns the current volume level
    """
    return Response(
        json.dumps(volume_get()),
        status=200,
        mimetype="application/json"
    )

@BP.route("", methods=["POST"])
def api_volume_set():
    """
    This function sets the volume on a specific level
    """
    # execute and return result
    result_data = json.loads(request.data)
    result = volume_set(result_data["level"])
    return Response(
        return_result(result),
        status=200,
        mimetype="application/json"
    )

@BP.route("/up", methods=["GET"])
def api_volume_up():
    """
    This function increases the volume level
    """
    return Response(
        return_result(volume_up()),
        status=200,
        mimetype="application/json"
    )

@BP.route("/down", methods=["GET"])
def api_volume_down():
    """
    This function decreases the volume level
    """
    return Response(
        return_result(volume_down()),
        status=200,
        mimetype="application/json"
    )
