#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response

from ..models import Stop


def route_map(request, route, direction):
    stops = Stop.objects.get_stops(str(route), 0 if direction == 'west' else 1)
    output = {'stops': stops}
    return render_to_response('route_map.html', output,
                              context_instance=RequestContext(request))

# vim: filetype=python
