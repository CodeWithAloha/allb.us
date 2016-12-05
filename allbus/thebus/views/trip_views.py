#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from ..models import TheBusTrip


def trip_details(request, trip_id):
    t = get_object_or_404(TheBusTrip, trip_id=trip_id)
    return HttpResponse(json.dumps(t.to_dict()), content_type="application/json")

# vim: filetype=python
