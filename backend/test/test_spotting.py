#!/usr/bin/python

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import unittest
import subprocess
import time
import cjson

from .. import httpcall

# For some reason, I need to do the monkey patch before importing logging,
# or an exception is thrown on exit
import logging


def wait_for_startup(server, url):

    # A bit ugly, but we ping the server until it comes up
    for i in range(0, 20):
        time.sleep(0.2)
        try:
            (status, reason, data) = httpcall.call("GET", url + '/ping', '')
            if data == "pong":
                return
        except:
            pass

    server.terminate()

    raise Exception("Server not responding.")


class TestSimpleNetworked(unittest.TestCase):

    def setUp(self):
        self.url = "http://localhost:8200"
        self.server = subprocess.Popen("./drunkspotting.py")
        wait_for_startup(self.server, self.url)

        (status, reason, data) = httpcall.call(
            "GET", self.url + '/nuke_it_all')
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

    def tearDown(self):
        self.server.terminate()

    def test_basics(self):

        # Add a template
        req = {
            "title": "template 1",
            "ip": "1.2.3.4",
            "latitude": 12.34,
            "longitude": 23.34,
            "description": "template 1 desc",
            "url": "http://www.google.com"
            }

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/templates/', cjson.encode(req))
        template1_id = cjson.decode(data)['id']
        self.assertEqual((status, reason), (200, 'OK'))

        # Add another template
        req = {
            "title": "template r2",
            "ip": "1.2.3.4",
            "latitude": 32.34,
            "longitude": 33.34,
            "description": "template 2 desc",
            "url": "http://www.yahoo.com"
            }

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/templates/', cjson.encode(req))
        template2_id = cjson.decode(data)['id']
        self.assertEqual((status, reason), (200, 'OK'))

        # Get a list of the templates
        (status, reason, data) = httpcall.call(
            "GET", self.url + '/templates/', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))


        return

        # Create a new user
        req = {
            "email": "gandalf.hernandez@gmail.com",
            "password": "testtest",
            "type": "recipient",
            "name": "gandalf hernandez",
            "address": "144 sullivan st #13 New York NY 10012 USA",
            "max_purchase_amount": 0,
            "max_volume": 0,
            "max_weight": 0,
            "pickup_leeway": 0,
            "delivery_leeway": 0,
            "telephone": "646-468-5742"}

        # Create new user is ok
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_user', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

        req = {
            "email": "ericaswallow@gmail.com",
            "password": "test2",
            "type": "casual",
            "name": "Erika Swallow",
            "address": "144 sullivan st #13 New York NY 10012 USA",
            "max_purchase_amount": 150,
            "max_volume": 0.5,
            "max_weight": 20,
            "pickup_leeway": 0.5,
            "delivery_leeway": 1.0,
            "telephone": "1-800-DELIVERISH"}

        # Another user is ok
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_user', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

        # Duplicate email not ok
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_user', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK',
                         '{"error": "email already in use."}'))

        # Create another new user
        req = {
            "email": "rui.dacosta@gmail.com",
            "password": "test",
            "type": "recipient",
            "name": "Rui DaCosta",
            "address": "144 sullivan st #13 New York NY 10012 USA",
            "max_purchase_amount": 0,
            "max_volume": 0,
            "max_weight": 0,
            "pickup_leeway": 0,
            "delivery_leeway": 0,
            "telephone": "1234567890"}

        # Fail a login
        req = {
            "email": "wrong@gmail.com",
            "password": "testtest"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/login', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK',
                         '{"error": "email does not exist."}'))

        req = {
            "email": "gandalf.hernandez@gmail.com",
            "password": "wrong"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/login', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK',
                         '{"error": "invalid password."}'))

        # Succeed a login
        req = {
            "email": "ericaswallow@gmail.com",
            "password": "test2"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/login', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        session_key = cjson.decode(data)['session_key']
        self.assertEqual(len(session_key), 40)

        # And another one
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/login', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        session_key2 = cjson.decode(data)['session_key']
        self.assertEqual(len(session_key2), 40)
        self.assertNotEqual(session_key, session_key2)

        # Read back the user
        req = {"session_key": session_key2}
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/get_user', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(data['email'], 'ericaswallow@gmail.com')
        self.assertEqual(data['max_purchase_amount'], 150)
        self.assertAlmostEqual(data['pickup_leeway'], 0.5)
        self.assertAlmostEqual(data['delivery_leeway'], 1.0)
        self.assertEqual(data['telephone'], '1-800-DELIVERISH')

        # Call a restricted api with a bad token
        req = {"session_key": session_key}
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone', cjson.encode(req))
        self.assertEqual((status, reason, data), (403, 'Access denied', ''))

        # Add a delivery zone
        req = {
            "session_key": session_key2,
            "latitude": 40.7142,
            "longitude": -74.0064,
            "radius": 3.3,
            "name": "downtown manhattan"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        zone_id1 = cjson.decode(data)['zone_id']

        # Add another one
        req = {
            "session_key": session_key2,
            "latitude": 40.9142,
            "longitude": -74.0564,
            "radius": 3.3,
            "name": "midtown manhattan"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        zone_id2 = cjson.decode(data)['zone_id']

        # Read back the zones
        req = {"session_key": session_key2}
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/get_zones', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 2)
        if data[0]['name'] == 'midtown manhattan':
            (data[0], data[1]) = (data[1], data[0])
        self.assertAlmostEqual(data[0]['longitude'], -74.0064)
        self.assertAlmostEqual(data[1]['latitude'], 40.9142)
        self.assertAlmostEqual(data[1]['radius'], 3.3)
        self.assertEqual(data[1]['name'], 'midtown manhattan')

        # Add an invalid zone schedule
        req = {
            "session_key": session_key2,
            "zone_id": str(zone_id1 + 100)}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone_schedule', cjson.encode(req))
        self.assertEqual((status, reason, data), (404, 'Item not found', ''))

        # Add a zone schedule
        req = {
            "session_key": session_key2,
            "zone_id": zone_id1,
            "schedules": [
            {"begin": "2013-03-09 08:00", "end": "2013-03-10 17:00"},
            {"begin": "2013-03-10 12:00", "end": "2013-03-10 14:45"}
            ]}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone_schedule', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))

        # Add another one
        req = '{ \
            "session_key": "' + session_key2 + '", \
            "zone_id": ' + str(zone_id2) + ', \
            "schedules": [ \
            { "begin": "2013-03-09 09:20", "end": "2013-03-10 18:20" }, \
            { "begin": "2013-03-10 12:20", "end": "2013-03-10 14:25" } \
            ]}'

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone_schedule', req)
        self.assertEqual((status, reason), (200, 'OK'))

        # Read back the zone schedules
        req = {"session_key": session_key2}
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/get_zone_schedules', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 4)
        data.sort(key=lambda row: row['id'])
        self.assertEqual(data[1]['begin_time'], '2013-03-10T12:00:00-04:00')

        # Add an invalid constraint
        req = '{ \
            "session_key": "' + session_key2 + '", \
            "zone_id1": ' + str(zone_id1 + 100) + ', \
            "zone_id2": ' + str(zone_id2 + 100) + '}'

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone_constraints', req)
        self.assertEqual((status, reason, data), (404, 'Item not found', ''))

        # Add a valid constraint
        req = {
            "session_key": session_key2,
            "zone_id1":  zone_id1,
            "zone_id2": zone_id2,
            "price": 25}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone_constraints', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

        # Add another valid constraint
        req = {
            "session_key": session_key2,
            "zone_id1": zone_id1,
            "zone_id2": zone_id1,
            "price": 15}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone_constraints', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

        # Read back the zone constraints
        # TODO: For this (and the zone schedules, should really have
        # more data in the database to make sure we don't leak
        req = {"session_key": session_key2}
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/get_zone_constraints', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 2)
        data.sort(key=lambda row: row['id'])
        self.assertEqual(data[0]['price'], '$25.00')
        self.assertEqual(data[1]['price'], '$15.00')

        # Log in the shipper
        req = {
            "email": "gandalf.hernandez@gmail.com",
            "password": "testtest"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/login', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        requester_session_key = cjson.decode(data)['session_key']
        self.assertEqual(len(session_key), 40)

        # Do a search for matching deliveries
        req = {
            "shipper_session_key": requester_session_key,
            "pickup_address": "pickup address",
            "pickup_latitude": 40.72,
            "pickup_longitude": -74.01,
            "delivery_address": "delivery address",
            "delivery_latitude": 40.69,
            "delivery_longitude": -74.0464,
            "pickup_time": "2013-03-09 09:30",
            "delivery_time": "2013-03-10 14:30",
            "shopping_total": 150,
            "shopping_notes": "swedish fish $5\ngold fish $10",
            "type_of_package": "box",
            "weight": 2.2,
            "volume": 0.2,
            "notes": "Go buy me Swedish fish at this store, bring it to me"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/find_delivery_matches', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['price'], '$15.00')

        deliverer_user_id = data[0]['user_id']
        pickup_zone_id = data[0]['pickup_zone_id']
        delivery_zone_id = data[0]['delivery_zone_id']
        price = data[0]['price']

        # Read the deliverer info
        req = {
            "session_key": requester_session_key,
            "user_id": deliverer_user_id}
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/get_user', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(data['email'], 'ericaswallow@gmail.com')
        self.assertEqual(data['max_purchase_amount'], 150)
        self.assertAlmostEqual(data['pickup_leeway'], 0.5)
        self.assertAlmostEqual(data['delivery_leeway'], 1.0)
        self.assertEqual(data['telephone'], '1-800-DELIVERISH')

        # Create the delivery
        req = {
            "session_key": requester_session_key,
            "delivery_user_id": deliverer_user_id,
            "pickup_zone_id": pickup_zone_id,
            "delivery_zone_id": delivery_zone_id,
            "price": price,
            "pickup_address": "pickup address",
            "pickup_latitude": 40.72,
            "pickup_longitude": -74.01,
            "delivery_address": "delivery address",
            "delivery_latitude": 40.69,
            "delivery_longitude": -74.0464,
            "pickup_time": "2013-03-09 09:30",
            "delivery_time": "2013-03-10 14:30",
            "shopping_total": 150,
            "shopping_notes": "swedish fish $5\ngold fish $10",
            "type_of_package": "box",
            "weight": 2.2,
            "volume": 0.2,
            "notes": "Go buy me Swedish fish at this store, bring it to me",
            "deliverer_notes": "I'll be happy to do this for you"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_delivery', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))

        # Read back the delivery as the person asking for it
        req = {"session_key": requester_session_key}
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/get_deliveries', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)[0]

        self.assertEqual(data['logged_in_user_is'], 'recipient')
        self.assertEqual(data['price'], '$15.00')
        self.assertEqual(data['status'], 'accepted')

        # Update the status of the delivery
        req = {"session_key": session_key2,
               'delivery_id': data['delivery_user_id'],
               'status': 'pickup'}
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/update_delivery_status', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))

        # Read back the delivery as the person asking for it
        # checking the new status
        req = {"session_key": requester_session_key}
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/get_deliveries', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)[0]

        self.assertEqual(data['logged_in_user_is'], 'recipient')
        self.assertEqual(data['price'], '$15.00')
        self.assertEqual(data['status'], 'pickup')

        # Have the shipper put in a mission to deliver
        req = {
            "session_key": session_key2,
            "title": "Costco run",
            "price": 20,
            "pickup_address": "pickup address",
            "pickup_latitude": 40.72,
            "pickup_longitude": -74.01,
            "delivery_latitude": 40.69,
            "delivery_longitude": -74.0464,
            "delivery_radius": 4.0,
            "pickup_time": "2013-03-09 09:30",
            "delivery_time": "2013-03-10 14:30",
            "shopping_total": 150,
            "shopping_notes": "swedish fish $5\ngold fish $10",
            "type_of_package": "box",
            "weight": 2.2,
            "volume": 0.2,
            "deliverer_notes": "I will go to Costco. I'll pick up some stuff."}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_delivery_proposal', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))

        # Read back the delivery proposals that are close by
        req = {
            "session_key": requester_session_key,
            "keywords": "costco",
            "delivery_latitude": 40.72,
            "delivery_longitude": -74.0}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/get_delivery_proposals', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))

        data = cjson.decode(data)[0]
        self.assertEqual(data['logged_in_user_is'], 'deliverer')
        self.assertAlmostEqual(data['delivery_radius'], 4.0)

        # Make sure that if we are outside the area we find nothing
        req = {
            "session_key": requester_session_key,
            "keywords": "costco",
            "delivery_latitude": 42.72,
            "delivery_longitude": -74.0}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/get_delivery_proposals', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 0)

        # -------------- NICER TEST DATA -----------------

        (status, reason, data) = httpcall.call(
            "GET", self.url + '/nuke_it_all')
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

        # Two test users
        req = {
            "email": "sam@deliverish.me",
            "password": "test",
            "type": "recipient",
            "name": "Sam Francisco",
            "address": "144 Broadway New York NY 10012 USA",
            "max_purchase_amount": 0,
            "max_volume": 0,
            "max_weight": 0,
            "pickup_leeway": 0,
            "delivery_leeway": 0,
            "telephone": "1-800-BUSYNYC"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_user', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

        req = {
            "email": "bob@deliverish.me",
            "password": "test",
            "type": "casual",
            "name": "Bob Tractor",
            "address": "300 E 20 ST New York NY 10020 USA",
            "max_purchase_amount": 100000,
            "max_volume": 1000,
            "max_weight": 1000,
            "pickup_leeway": 0.5,
            "delivery_leeway": 1.0,
            "telephone": "1-800-IDELIVER"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_user', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

        # Login both users
        req = {
            "email": "sam@deliverish.me",
            "password": "test"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/login', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        buyer_session_key = cjson.decode(data)['session_key']

        req = {
            "email": "bob@deliverish.me",
            "password": "test"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/login', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        shipper_session_key = cjson.decode(data)['session_key']

        # Put in a big delivery zone for the shipper
        # Add a delivery zone
        req = {
            "session_key": shipper_session_key,
            "latitude": 40.7142,
            "longitude": -74.0064,
            "radius": 100,
            "name": "NYC"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        zone_id = cjson.decode(data)['zone_id']

        # And a generous schedule for it
        req = {
            "session_key": shipper_session_key,
            "zone_id": zone_id,
            "schedules": [
                {"begin": "2013-01-01 00:00", "end": "2013-12-31 23:59"},
            ]}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone_schedule', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

        # And a price
        req = {
            "session_key": shipper_session_key,
            "zone_id1": zone_id,
            "zone_id2": zone_id,
            "price": 25}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_zone_constraints', cjson.encode(req))
        self.assertEqual((status, reason, data), (200, 'OK', '{}'))

        # Add in an offer to go to Costco
        req = {
            "session_key": shipper_session_key,
            "title": "Costco trip",
            "price": 20,
            "pickup_address": "pickup address",
            "pickup_latitude": 40.72,
            "pickup_longitude": -74.01,
            "delivery_latitude": 40.69,
            "delivery_longitude": -74.0464,
            "delivery_radius": 100.0,
            "pickup_time": "2013-01-01 00:00",
            "delivery_time": "2013-12-31 23:59",
            "shopping_total": 1500,
            "shopping_notes": "Please keep the bulk of the items down a bit.",
            "type_of_package": "box",
            "weight": 200,
            "volume": 000,
            "deliverer_notes": "I will go to Costco and am willing ' + \
                'to pick up other items."}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/add_delivery_proposal', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))

        # Do a search for matching deliveries
        req = {
            "shipper_session_key": buyer_session_key,
            "pickup_address": "pickup address",
            "pickup_latitude": 40.72,
            "pickup_longitude": -74.01,
            "delivery_address": "delivery address",
            "delivery_latitude": 40.69,
            "delivery_longitude": -74.0464,
            "pickup_time": "2013-03-09 09:30",
            "delivery_time": "2013-03-10 14:30",
            "shopping_total": 150,
            "shopping_notes": "swedish fish $5\ngold fish $10",
            "type_of_package": "box",
            "weight": 2.2,
            "volume": 0.2,
            "notes": "Go buy me Swedish fish at this store, bring it to me"}

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/find_delivery_matches', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['price'], '$25.00')

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    unittest.main(verbosity=2)
