#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

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

# vim: filetype=python
