#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse

import json
from ..utilities.thebus.client import TheBusClient
from ..utilities.thebus.client import parse_vehicle_xml_to_dict

THEBUS_API_KEY = getattr(settings, 'THEBUS_API_KEY', None)


def bus_details(request, bus):
    c = TheBusClient(THEBUS_API_KEY)
    v = c.track_vehicle(int(bus), parse_vehicle_xml_to_dict)
    vehicle = v.get('vehicles', None)
    vehicle = vehicle[0] if len(vehicle) == 1 else vehicle

    return HttpResponse(json.dumps(vehicle), mimetype="application/json")

# vim: filetype=python
