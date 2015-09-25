#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
import datetime
import operator
import pytz


class TheBusStopManager(models.Manager):
    pass


class TheBusTripManager(models.Manager):

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
