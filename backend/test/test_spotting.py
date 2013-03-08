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
            "GET", self.url + '/templates/latest/10', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 2)

        (status, reason, data) = httpcall.call(
            "GET", self.url + '/templates/latest/1', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 1)

        # Add two pictures for the first template
        req = {
            "template_id": template1_id,
            "title": "picture 1.1",
            "ip": "3.2.3.4",
            "description": "pic 1 desc",
            "url": "http://www.google.com"
            }

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/pictures/', cjson.encode(req))
        picture1_id = cjson.decode(data)['id']
        self.assertEqual((status, reason), (200, 'OK'))

        req = {
            "template_id": template1_id,
            "title": "picture 1.2",
            "ip": "3.2.3.4",
            "description": "pic 2 desc",
            "url": "http://www.google.com"
            }

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/pictures/', cjson.encode(req))
        picture2_id = cjson.decode(data)['id']
        self.assertEqual((status, reason), (200, 'OK'))

        # And one picture for the second template
        req = {
            "template_id": template2_id,
            "title": "picture 2.2",
            "ip": "3.2.3.4",
            "description": "pic 3 desc",
            "url": "http://www.amazon.com"
            }

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/pictures/', cjson.encode(req))
        picture3_id = cjson.decode(data)['id']
        self.assertEqual((status, reason), (200, 'OK'))

        # Get a list of the pictures
        (status, reason, data) = httpcall.call(
            "GET", self.url + '/pictures/latest/10', cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 3)


        return


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    unittest.main(verbosity=2)
