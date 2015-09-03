#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import json
import re
import urllib

from ..utilities.thebus.client import TheBusClient
from ..utilities.thebus.client import parse_arrival_xml_to_dict
from ..utilities.thebus.client import parse_vehicle_xml_to_dict
from ..models import Stop
from ..models import Route

from collections import Counter


THEBUS_API_KEY = getattr(settings, 'THEBUS_API_KEY', None)
STRIP_CONNECTORS = ['or', 'and', '+', '&']

STOP_REG_EX = re.compile('^\s*\d+\s*$')


def stop_near(request):
    return render_to_response('stop_near.html', {},
                              context_instance=RequestContext(request))


@csrf_exempt
def stop_nearby(request, latitude, longitude):
    def _encode_stop(obj):
        if isinstance(obj, Stop):
            return {
                'latitude': obj.latitude,
                'longitude': obj.longitude,
                'code': obj.code,
                'name': obj.name,
            }
    output = {}
    output['stops'] = Stop.objects.nearby(float(latitude), float(longitude))
    return HttpResponse(json.dumps(output, default=_encode_stop), mimetype="application/json")


@csrf_exempt
def stop_search(request):
    if request.method == 'POST':
        s = request.POST.get('stop_or_street', None)
        stop_or_street = '' if s is None else str(s)
        if stop_or_street:
            if STOP_REG_EX.match(stop_or_street):
                s = get_object_or_404(Stop, code=stop_or_street)
                return redirect(s.get_absolute_url())
            else:
                stop_search = reverse('stop_search')
                q = "?q={0}".format(urllib.quote_plus(stop_or_street))
                return HttpResponseRedirect(
                    "{0}{1}".format(stop_search, q).encode('utf-8'))
        else:
            slash = reverse('slash')
            return HttpResponseRedirect(slash)
    else:
        output = {}
        query = request.GET.get('q', None)
        ordered_stops, stops = [], []

        if query:
            normalize = [term for term in query.strip().split(' ') if term not in STRIP_CONNECTORS]
            for street in normalize:
                stops.extend(Stop.objects.filter(name__icontains=street).order_by('code'))

        c = Counter(stops)

        counted_stops = c.most_common()

        # Get occurrences
        occurrences = sorted(list(set(c.values())), reverse=True)

        if counted_stops:
            for o in occurrences:
                vals = [stop for stop, count in counted_stops if count == o]
                ordered_stops.extend(sorted(vals, key=lambda x: int(x.code)))

        output['stops'] = ordered_stops
        output['query'] = query

        return render_to_response('stop_search.html', output,
                                  context_instance=RequestContext(request))


def stop_details(request, stop, route):
    s = get_object_or_404(Stop, code=stop)

    output = {'stop': s}

    c = TheBusClient(THEBUS_API_KEY)
    a = c.get_arrivals(int(stop), parse_arrival_xml_to_dict)
    arrivals = a.get('arrivals', None)
    server_ts = a.get('server_ts', None)

    if route:
        route = route.upper()
        if arrivals:
            arrivals = filter(lambda x: x['route'] == route, arrivals)

    if arrivals:
        for arrival in arrivals:
            arrival['route_len'] = len(arrival['route'])

    output['arrivals'] = arrivals
    output['server_ts'] = server_ts
    output['route'] = route
    output['routes'] = Route.objects.get_routes(stop)

    return render_to_response('stop_details.html', output,
                              context_instance=RequestContext(request))


def stop_map(request, stop):
    s = get_object_or_404(Stop, code=stop)

    output = {'stop': s}
    return render_to_response('stop_map.html', output,
                              context_instance=RequestContext(request))


def stop_bus_map(request, stop, route, bus, direction):
    s = get_object_or_404(Stop, code=stop)
    c = TheBusClient(THEBUS_API_KEY)
    v = c.track_vehicle(int(bus), parse_vehicle_xml_to_dict)
    vehicle = v.get('vehicles', None)
    vehicle = vehicle[0] if len(vehicle) == 1 else vehicle

    stops = Stop.objects.get_stops(str(route), 0 if direction == 'west' else 1)

    output = {'stop': s, 'vehicle': vehicle, 'stops': stops}
    return render_to_response('stop_bus_map.html', output,
                              context_instance=RequestContext(request))

# vim: filetype=python
