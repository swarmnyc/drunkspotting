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
            "title": "template 2",
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

        # Get one of the templates
        (status, reason, data) = httpcall.call(
            "GET", self.url + '/templates/%d' % (template2_id, ),
            cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(data['title'], 'template 2')

        # Add two pictures for the first template
        req = {
            "template_id": template1_id,
            "title": "picture 1.1",
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

        # Get one of the pictures
        (status, reason, data) = httpcall.call(
            "GET", self.url + '/pictures/%d' % (picture2_id, ),
            cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(data['title'], 'picture 1.2')
        self.assertEqual(data['latitude'], 12.34)
        self.assertEqual(data['longitude'], 23.34)

        # Add a comment to one of the template
        req = {
            "nick": "gandalf",
            "title": "template 1 comment title",
            "description": "template 1 comment description"
            }

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/templates/%d/comments' % (template1_id, ),
            cjson.encode(req))
        comment1_id = cjson.decode(data)['id']
        self.assertEqual((status, reason), (200, 'OK'))

        # And to one of the pictures
        req = {
            "nick": "drunkspotting",
            "title": "picture 3 comment title",
            "description": "picture 3 comment description"
            }

        (status, reason, data) = httpcall.call(
            "POST", self.url + '/pictures/%d/comments' % (picture3_id, ),
            cjson.encode(req))
        comment1_id = cjson.decode(data)['id']
        self.assertEqual((status, reason), (200, 'OK'))

        # Read back the template comments
        (status, reason, data) = httpcall.call(
            "GET", self.url + '/templates/%d/comments/latest/10' %
            (template1_id, ),
            cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nick'], 'gandalf')
        self.assertEqual(data[0]['title'], 'template 1 comment title')

        # Read back the picture comments
        (status, reason, data) = httpcall.call(
            "GET", self.url + '/pictures/%d/comments/latest/10' %
            (picture3_id, ),
            cjson.encode(req))
        self.assertEqual((status, reason), (200, 'OK'))
        data = cjson.decode(data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nick'], 'drunkspotting')
        self.assertEqual(data[0]['description'],
                         'picture 3 comment description')

        # Upload a picture
        logo = open('data/logo.jpg', 'r').read()
        (status, reason, data) = httpcall.call(
            "POST", self.url + '/upload_template', logo)
        self.assertEqual((status, reason), (200, 'OK'))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    unittest.main(verbosity=2)
