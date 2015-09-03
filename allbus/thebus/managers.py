#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

from math import radians
from math import sin
from math import cos
from math import asin
from math import sqrt

import operator
import datetime

GREAT_CIRCLE_RADIUS_MILES = 3956
GREAT_CIRCLE_RADIUS_FEET = GREAT_CIRCLE_RADIUS_MILES * 5280


def haversine(latlong1, latlong2, radius):
    """ http://en.wikipedia.org/wiki/Haversine_formula """

    lat1, lng1 = latlong1
    lat2, lng2 = latlong2

    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])

    # Actual haversine - rough approximations since Earth is not round
    lat_dist = lat2 - lat1
    lng_dist = lng2 - lng1

    a = sin(lat_dist/2)**2 + cos(lat1) * cos(lat2) * sin(lng_dist/2)**2
    return 2 * asin(sqrt(a)) * radius


class StopManager(models.Manager):

    def nearby(self, latitude=None, longitude=None, distance=500):
        """ Returns all stops nearby to latitude/longitude ordered by distance  """

        nearby = []

        # Explicit check for None since 0 is a valid coordinate
        if latitude is None and longitude is None:
            return nearby

        # Note: If this takes too long, winnow the data set by performing a
        # range filter on lat/long.  The Earth is not round, so the
        # bounding box changes as you near equator.  This is just a rough
        # estimate for coordinates in Hawaii, so not a big deal.
        qs = super(StopManager, self).get_query_set()

        for stop in qs:
            if stop.latitude and stop.longitude:
                d = haversine(
                    (latitude, longitude),
                    (stop.latitude, stop.longitude),
                    GREAT_CIRCLE_RADIUS_FEET)

                if distance >= d:
                    nearby.append((d, stop))

        return [stop for _, stop in sorted(nearby, key=operator.itemgetter(0))]

    def get_stops(self, route_shortname, direction):
        curr_time = datetime.datetime.utcnow()
        day_str = 'thebus_service.' + curr_time.strftime('%a').upper()

        return self.raw(
            "SELECT thebus_stop.id, thebus_stop.latitude, thebus_stop.longitude \
            FROM thebus_stoptime \
            JOIN thebus_stop on thebus_stoptime.stop_id = thebus_stop.id \
            WHERE thebus_stoptime.trip_id = \
            (SELECT thebus_trip.id \
                FROM thebus_trip \
                JOIN thebus_service ON thebus_trip.service_id = thebus_service.id \
                JOIN thebus_route ON thebus_route.id = thebus_trip.route_id \
                WHERE thebus_route.short_name = %(route)s \
                AND %(curr_time)s > start_date \
                AND %(curr_time)s < end_date AND " + day_str + " = 1 \
                AND thebus_trip.direction = %(direction)s \
                GROUP BY service_id) \
            ORDER BY thebus_stoptime.sequence",
            {'route': str(route_shortname),
             'direction': bool(direction),
             'curr_time': curr_time.strftime('%Y-%m-%d %H:%M:%S')})


class RouteManager(models.Manager):

    def get_routes(self, stop_code):
        return self.raw("SELECT distinct(r.id) \
            FROM thebus_stoptime as st \
            JOIN thebus_trip as t on st.trip_id = t.id \
            JOIN thebus_route as r on t.route_id = r.id \
            JOIN thebus_stop as ts on ts.id = st.stop_id \
            WHERE ts.code=%s \
            ORDER BY r.id", [stop_code])
