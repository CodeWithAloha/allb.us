#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import time
import re
from datetime import datetime
from datetime import timedelta

from bs4 import BeautifulSoup

from django.core.cache import cache
from allbus.utilities.cache.decorators import cacheable
from allbus.thebus.utilities.xml2json import elem_to_internal

import gtfs_realtime_pb2
import xml.etree.cElementTree as ET


class TheBusException(Exception):
    pass


DATE_MATCHER = re.compile(
    r"^(?P<title>.*)\s*,?-?\s*(?P<date>\d{1,2}/\d{1,2}/\d{4})$")


class TheBusClient(object):
    """ Thin wrapper into theBus API """

    GTFS_SERVICE_ALERT_ENDPOINT = \
        'http://webapps.thebus.org/transitdata/production/servicealerts/'

    GTFS_TRIP_UPDATE_ENDPOINT = \
        'http://webapps.thebus.org/transitdata/production/tripupdates/'

    GTFS_VEHICLE_LOCATION_ENDPOINT = \
        'http://webapps.thebus.org/transitdata/production/vehloc/'

    def __init__(self, api_key, domain='api.thebus.org', timeout=60):
        self.api_key = api_key
        self.domain = domain
        self.timeout = timeout

    @cacheable(cache=cache, key=None, ttl=10)
    def get_arrivals(self, stop_id, callback=None):
        query_params = {'key': self.api_key, 'stop': stop_id}
        endpoint = self._get_endpoint('/arrivals', query_params)
        return self._call_endpoint(endpoint, callback)

    def track_vehicle(self, vehicle_id, callback=None):
        query_params = {'key': self.api_key, 'num': vehicle_id}
        endpoint = self._get_endpoint('/vehicle', query_params)
        return self._call_endpoint(endpoint, callback)

    def get_gtfs_service_alerts(self):
        return self._get_gtfs_data(self.GTFS_SERVICE_ALERT_ENDPOINT)

    def get_gtfs_trip_updates(self):
        return self._get_gtfs_data(self.GTFS_TRIP_UPDATE_ENDPOINT)

    def get_gtfs_vehicle_location(self):
        return self._get_gtfs_data(self.GTFS_VEHICLE_LOCATION_ENDPOINT)

    def _get_gtfs_data(self, endpoint):
        gtfs_data = self._call_endpoint(endpoint)

        gtfs_message = gtfs_realtime_pb2.FeedMessage()
        gtfs_message.ParseFromString(gtfs_data)
        return gtfs_message

    def _get_endpoint(self, path='', query_params=None):
        normalized_path = path + '/' if path and path[-1] != '/' else path
        endpoint = "{0[scheme]}://{0[domain]}{0[path]}".format(
            {'scheme': 'http',
             'domain': self.domain,
             'path': normalized_path})
        if query_params:
            endpoint = endpoint + '?' + urllib.urlencode(query_params)
        return endpoint

    def _call_endpoint(self, endpoint, callback=None):
        request = urllib2.Request(endpoint)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            raise TheBusException("Unable to contact %s" % endpoint)

        payload = callback(response) if callback else response.read()
        response.close()
        return payload

    def __str__(self):
        return "TheBus Client"


def tags_to_dict(soup, tags):
    """ tags should be a list of tuples -> ('route', 'route_key').  If tuple
        only contains tag, then tag name is used as dict key. """
    output = {}
    for tag in tags:
        xml_node = soup.find(tag[0])
        if xml_node:
            key = tag[1] if len(tag) > 1 else tag[0]
            output[key] = xml_node.text.strip()
    return output


def parse_arrival_xml_to_dict(response):
    soup = BeautifulSoup(response.read(), "html.parser")
    output = tags_to_dict(soup, [('stop',), ('timestamp',), ('errorMessage',)])

    try:
        server_ts_date = output['timestamp'].split()[0]
        output['server_ts'] = datetime.fromtimestamp(
            time.mktime(time.strptime(output['timestamp'], "%m/%d/%Y %I:%M:%S %p")))

        arrivals = []

        arrivals_xml = soup.findAll('arrival')

        for arrival_xml in arrivals_xml:
            arrival = tags_to_dict(
                arrival_xml,
                [('route',), ('headsign',), ('vehicle',), ('direction',),
                 ('stoptime', 'stop_time'), ('estimated',), ('longitude',),
                 ('latitude',)])

            arrival_server_time = time.strptime(
                "%s %s" % (
                    server_ts_date, arrival['stop_time']), "%m/%d/%Y %I:%M %p")
            arrival['server_ts'] = datetime.fromtimestamp(
                time.mktime(arrival_server_time))

            # HACK - Need to do this because of API. If the server_ts is PM,
            # and the arrivals are coming in AM, this indicates that it's
            # overnight.  Need to add one day to the server_ts, otherwise, all
            # these arrivals will look late.
            if output['server_ts'].hour > 12 \
                    and arrival['server_ts'].hour < 12:
                arrival['server_ts'] = arrival['server_ts'] + timedelta(days=1)

            # Adding nicety
            arrival['can_track'] = False \
                if arrival['vehicle'] == '???' else True

            arrivals.append(arrival)

        output['arrivals'] = arrivals
    except:
        pass
    return output


def parse_vehicle_xml_to_dict(response):
    soup = BeautifulSoup(response.read())
    output = tags_to_dict(soup, [('timestamp',), ('errorMessage',)])

    output['server_ts'] = datetime.fromtimestamp(
        time.mktime(time.strptime(output['timestamp'], "%m/%d/%Y %I:%M:%S %p")))

    vehicles = []

    vehicles_xml = soup.findAll('vehicles')

    for vehicle_xml in vehicles_xml:
        vehicle = tags_to_dict(
            vehicle_xml,
            [('number',), ('driver',), ('latitude',), ('longitude',), ('adherence',), ('last_message',)])

        vehicles.append(vehicle)

    output['vehicles'] = vehicles
    return output


def parse_xml_to_dict(response):
    options = {
        'strip_ns': True,
        'strip_nl': True,
        'pretty': True,
        'strip_text': True
    }
    elem = ET.fromstring(response.read())
    if hasattr(elem, 'getroot'):
        elem = elem.getroot()
    return elem_to_internal(elem, options)


def main():
    pass


def test_client():
    client = TheBusClient('')
    print client.get_gtfs_service_alerts()
    print client.get_gtfs_trip_updates()
    locations = client.get_gtfs_vehicle_location()
    for e in locations.entity:
        value = datetime.fromtimestamp(e.vehicle.timestamp)
        print(value.strftime('%Y-%m-%d %H:%M:%S'))
    print client.track_vehicle(917, parse_xml_to_dict)
    print client.get_arrivals(125, parse_arrival_xml_to_dict)
    print client.get_rider_alerts()


if __name__ == '__main__':
    main()

# vim: filetype=python
