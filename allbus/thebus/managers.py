#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q
from itertools import chain
from multigtfs.models.base import BaseManager
import operator
import pytz


class TheBusStopManager(BaseManager):

    STRIP_CONNECTORS = ['or', 'and', 'near', '+', '&']

    def get_route_names(self, stop_id):
        return self.\
            get(stop_id=stop_id).\
            stoptime_set.\
            all().\
            values_list('trip__route__short_name', flat=True).distinct()

    def nearby(self, latitude, longitude, distance_in_miles=1):
        pt = Point(longitude, latitude)
        return self.filter(
            point__distance_lte=(pt, D(mi=distance_in_miles))).distance(
                pt).order_by('distance')

    def search(self, search_term):
        normalized_search = search_term.lower().strip()
        normalized_terms = [term for term in normalized_search.split(' ')
                            if term not in self.STRIP_CONNECTORS]
        queries = []
        for normalized_term in normalized_terms:
            queries.append(self.filter(Q(name__icontains=normalized_term)))
        return chain.from_iterable(queries)


class TheBusTripManager(BaseManager):

    DIRECTION = {"west": 0, "east": 1}

    def get_trips(
            self,
            route_shortname,
            direction,
            utc_dt=None,
            local_timezone=None):
        """ Returns the trips for a route given a direction and time. Useful to
        determine what stops a bus will be stopping at in a given direction on
        a certain date/time. Does not take into exception schedules at this
        point, but probably should. """
        utc_dt = utc_dt or datetime.datetime.utcnow()
        local_timezone = local_timezone or 'Pacific/Honolulu'

        local_tz = pytz.timezone(local_timezone)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        local_time = local_tz.normalize(local_dt)
        local_day_lower = local_time.strftime('%A').lower()

        predicates = [
            ('route__short_name', route_shortname),
            ('service__start_date__lt', local_time),
            ('service__end_date__gt', local_time),
            ('direction', self.DIRECTION[direction.lower()]),
            ("service__{0}".format(local_day_lower), True)
        ]

        q_list = [Q(x) for x in predicates]
        return self.filter(reduce(operator.and_, q_list))

# vim: filetype=python
