#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gtfs_thebus_managers import TheBusStopManager
from gtfs_thebus_managers import TheBusTripManager
from multigtfs.models import Stop
from multigtfs.models import Trip


class TheBusStop(Stop):

    class Meta:
        proxy = True

    objects = TheBusStopManager()

    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name,
            'latitude': self.point.y,
            'longitude': self.point.x,
            'url': self.url
        }


class TheBusTrip(Trip):

    class Meta:
        proxy = True

    objects = TheBusTripManager()

    def __init__(self, *args, **kwargs):
        super(TheBusTrip, self).__init__(*args, **kwargs)

    def get_stop_times(self):
        return [x for x in self.stoptime_set.all()]

    def get_stops(self):
        return [x.stop for x in self.stoptime_set.all().only('stop')]

    def get_previous_stop(self, stop_id):
        stop_id_index = self._get_index_of_stop_id_in_trip(stop_id)
        if stop_id_index is not None and stop_id_index != 0:
            return list(self.stoptime_set.all())[stop_id_index - 1].stop
        else:
            return None

    def get_next_stop(self, stop_id):
        stop_id_index = self._get_index_of_stop_id_in_trip(stop_id)
        if stop_id_index is not None \
                and stop_id_index != self.stoptime_set.all().count() - 1:
            return list(self.stoptime_set.all())[stop_id_index + 1].stop
        else:
            return None

    def _get_index_of_stop_id_in_trip(self, stop_id):
        stop_id_index = [
            i for i, stop_time in enumerate(self.stoptime_set.all())
            if stop_time.stop.stop_id == stop_id]

        if len(stop_id_index) == 1:
            return stop_id_index[0]
        else:
            return None

# vim: filetype=python
