#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ..gtfs_thebus_models import TheBusTrip
import json


def trip_details(request, trip_id):
    t = get_object_or_404(TheBusTrip, trip_id=trip_id)
    return HttpResponse(json.dumps(t.to_dict()), mimetype="application/json")

# vim: filetype=python
