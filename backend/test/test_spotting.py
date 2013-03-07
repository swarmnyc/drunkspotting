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
        data = cjson.decode(data)
        self.assertEqual(len(data), 2)

        return


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    unittest.main(verbosity=2)
