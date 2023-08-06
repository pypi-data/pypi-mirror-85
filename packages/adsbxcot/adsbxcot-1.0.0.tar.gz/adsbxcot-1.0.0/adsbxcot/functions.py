#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ADS-B Exchange Cursor-on-Target Gateway Functions."""

import datetime

import pycot
import pytak

import adsbxcot.constants

__author__ = "Greg Albrecht W2GMD <oss@undef.net>"
__copyright__ = "Copyright 2020 Orion Labs, Inc."
__license__ = "Apache License, Version 2.0"


def adsbx_to_cot(craft: dict, stale: int = None,
                 classifier = None) -> pycot.Event:
    """
    Transforms an ADS-B Exchange Aircraft Object to a Cursor-on-Target PLI.
    """
    time = datetime.datetime.now(datetime.timezone.utc)
    stale = stale or adsbxcot.constants.DEFAULT_STALE

    lat = craft.get('lat')
    lon = craft.get('lon')

    if lat is None or lon is None:
        return None

    icao_hex = craft.get("hex").upper()
    name = f"ICAO-{icao_hex}"
    flight = craft.get("flight", "").strip()
    if flight:
        callsign = flight
    else:
        callsign = icao_hex

    cot_type = classifier(
        craft.get("hex"), craft.get("category"), flight)

    point = pycot.Point()
    point.lat = lat
    point.lon = lon
    point.ce = craft.get("nac_p", "9999999.0")
    point.le = craft.get("nac_v", "9999999.0")

    # alt_geom: geometric (GNSS / INS) altitude in feet referenced to the
    #           WGS84 ellipsoid
    alt_geom = int(craft.get("alt_geom", 0))
    if alt_geom:
        point.hae = alt_geom * 0.3048
    else:
        point.hae = "9999999.0"

    uid = pycot.UID()
    uid.Droid = name

    contact = pycot.Contact()
    contact.callsign = callsign
    # Not supported by FTS 1.1?
    # if flight:
    #    contact.hostname = f'https://flightaware.com/live/flight/{flight}'

    track = pycot.Track()
    track.course = craft.get("track", "9999999.0")

    # gs: ground speed in knots
    gs = int(craft.get("gs", 0))
    if gs:
        track.speed = gs * 0.514444
    else:
        track.speed = "9999999.0"

    remarks = pycot.Remarks()
    _remark = (f"ICAO24: {icao_hex} Squawk: {craft.get('squawk')}")
    if flight:
        remarks.value = f"Flight: {flight} " + _remark
    else:
        remarks.value = _remark

    detail = pycot.Detail()
    detail.uid = uid
    detail.contact = contact
    detail.track = track
    # Not supported by FTS 1.1?
    # detail.remarks = remarks

    event = pycot.Event()
    event.version = "2.0"
    event.event_type = cot_type
    event.uid = name
    event.time = time
    event.start = time
    event.stale = time + datetime.timedelta(seconds=stale)
    event.how = "m-g"
    event.point = point
    event.detail = detail

    return event


def hello_event():
    time = datetime.datetime.now(datetime.timezone.utc)
    name = 'adsbxcot'
    callsign = 'adsbxcot'

    point = pycot.Point()
    point.lat = 0.0
    point.lon = 0.0

    # FIXME: These values are static, should be dynamic.
    point.ce = '9999999.0'
    point.le = '9999999.0'
    point.hae = '9999999.0'

    uid = pycot.UID()
    uid.Droid = name

    contact = pycot.Contact()
    contact.callsign = callsign

    detail = pycot.Detail()
    detail.uid = uid
    detail.contact = contact

    event = pycot.Event()
    event.version = '2.0'
    event.event_type = 'a-u-G'
    event.uid = name
    event.time = time
    event.start = time
    event.stale = time + datetime.timedelta(hours=1)
    event.how = 'h-g-i-g-o'
    event.point = point
    event.detail = detail

    return event
