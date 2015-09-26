#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ..gtfs_thebus_models import TheBusStop
import json
from ..utilities.thebus.client import parse_xml_to_dict
from ..utilities.thebus.client import TheBusClient


def stop_details(request, stop, route=None):
    c = TheBusClient(settings.THEBUS_API_CLIENT_TOKEN)
    s = get_object_or_404(TheBusStop, code=stop)
    a = c.get_arrivals(int(stop), parse_xml_to_dict)

    stopTimes = a.get('stopTimes', None)
    arrivals = stopTimes.get('arrival', None) if stopTimes else None

    if route:
        route = route.upper()
        if arrivals:
            arrivals = filter(lambda x: x['route'] == route, arrivals)

    output = {
        'stop': s.to_dict(),
        'arrivals': arrivals,
    }

    if route:
        output['route'] = route

    return HttpResponse(json.dumps(output), mimetype="application/json")

# vim: filetype=python
