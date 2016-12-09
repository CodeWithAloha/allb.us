#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
import datetime
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from ..models import TheBusStop
from ..models import TheBusTrip
import json
from ..utilities.client import parse_vehicle_xml_to_dict
from ..utilities.client import parse_xml_to_dict
from ..utilities.client import TheBusClient
from ..utilities.time_utilities import naive_to_timestamp


STRIP_CONNECTORS = ['or', 'and', 'near', '+', '&']


def stop_details(request, stop_id, route=None):
    c = TheBusClient(settings.THEBUS_API_CLIENT_TOKEN)
    s = get_object_or_404(TheBusStop, stop_id=stop_id)
    a = c.get_arrivals(int(stop_id), parse_xml_to_dict)

    stopTimes = a.get('stopTimes', None)
    arrivals = stopTimes.get('arrival', None) if stopTimes else None

    if route:
        route = route.upper()
        if arrivals:
            arrivals = filter(lambda x: x['route'] == route, arrivals)

    output = {
        'stop': s.to_dict(),
        'arrivals': arrivals,
        'servertime': stopTimes.get('timestamp')
    }

    try:
        naive_datetime = datetime.datetime.strptime(
            output['servertime'],
            "%m/%d/%Y %I:%M:%S %p")
        output['servertime_ts'] = naive_to_timestamp(
            naive_datetime, tz='Pacific/Honolulu')
    except:
        pass

    if route:
        output['route'] = route

    output['route_names'] = list(TheBusStop.objects.get_route_names(stop_id))

    # return render(request, 'stops/details.html', output)
    return HttpResponse(json.dumps(output), content_type="application/json")


def stop_nearby(request, latitude, longitude):
    stops = TheBusStop.objects.nearby(float(latitude), float(longitude))
    stops_as_json = [s.to_dict() for s in stops] if stops else []
    return HttpResponse(json.dumps(stops_as_json), content_type="application/json")


def stop_search(request):
    query = request.GET.get('q', None)
    stops = TheBusStop.objects.search(query) if query else None
    counter = Counter(stops)

    output = {
        'stops': [s.to_dict() for s, c in counter.most_common()],
        'query': query
    }

    return HttpResponse(json.dumps(output), content_type="application/json")


def stop_bus_map(request, stop_id, route, trip_id, bus = None):
    s = get_object_or_404(TheBusStop, stop_id=stop_id)
    trip = TheBusTrip.objects.get(trip_id=trip_id)
    stops = trip.get_stops()

    if bus:
        c = TheBusClient(settings.THEBUS_API_CLIENT_TOKEN)
        v = c.track_vehicle(int(bus), parse_vehicle_xml_to_dict)
        vehicle = v.get('vehicles', None)
        vehicle = vehicle[0] if len(vehicle) == 1 else vehicle
    else:
        vehicle = None

    output = {'stop': s.to_dict(),
              'vehicle': vehicle,
              'trip': trip.to_dict(),
              'stops': [{'stop_id': s.stop_id, 'name': s.name, 'point': { 'x': s.point.x, 'y': s.point.y}} for s in stops]}
    return HttpResponse(json.dumps(output), content_type="application/json")


# vim: filetype=python
