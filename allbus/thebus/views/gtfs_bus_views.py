#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from django.conf import settings
from django.http import HttpResponse

import json
import pytz
from ..utilities.thebus.client import TheBusClient
from ..utilities.thebus.client import parse_vehicle_xml_to_dict


def bus_details(request, bus):
    c = TheBusClient(settings.THEBUS_API_CLIENT_TOKEN)
    v_dict = c.track_vehicle(int(bus), parse_vehicle_xml_to_dict)
    v_list = v_dict.get('vehicles', None)
    vehicle = v_list[0] if v_list and len(v_list) == 1 else {}

    if 'last_message' in vehicle:
        hst = pytz.timezone('Pacific/Honolulu')
        naive_datetime = datetime.datetime.strptime(
            vehicle['last_message'],
            "%m/%d/%Y %I:%M:%S %p")
        hst_datetime = hst.localize(naive_datetime, is_dst=None)
        utc_epoch_datetime = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)
        vehicle['last_message_ts'] = \
            int((hst_datetime - utc_epoch_datetime).total_seconds())

    return HttpResponse(json.dumps(vehicle), mimetype="application/json")

# vim: filetype=python
