#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import cjson
import psycopg2
import hashlib
import binascii
import os
import math
import sendgrid

import database
import drunkspotting_exceptions


class Server:
    def __init__(self):
        """Create a new server
        """

        import gevent
        import gevent.wsgi
        import gevent.monkey
        gevent.monkey.patch_all()

        self._conn = psycopg2.connect(database='drunkspotting',
                                      user='drunkspotting',
                                      password='drunkspotting1234')

        logging.info("Server initialized.")

    def ping(self):
        return 'pong'

    def get_template(self, template):
        pass

    def get_picture(self, picture):
        pass

    def get_comments(self):
        pass

    def get_templates(self):
        return '{}'

    def get_pictures(self):
        pass

    def get_tags(self):
        pass

    def find_by_tags(self):
        pass

    def post_template(self, data):
        data = cjson.decode(data)
        sql = 'insert into templates(title, ip, latitude, longitude, ' \
              'description, rating, rating_count, url, time_posted) ' \
              'values(%s, %s, %s, %s, %s, %s, %s, %s, now()) ' \
              'returning id'

        data = (data['title'], '1.2.3.4', data['latitude'], data['longitude'],
                data['description'], 0, 0, data['url'])

        id = database.execute_non_query_returning_id(
            self._conn, sql, data)

        return '{"id": %d}' % (id, )
        pass

    def post_comment(self, data):
        pass

    def post_tag(self, data):
        pass

    def post_picture(self, data):
        pass

    def nuke_it_all(self):
        database.execute_non_query(self._conn, 'truncate table comments')
        database.execute_non_query(self._conn, 'truncate table pictures')
        database.execute_non_query(self._conn, 'truncate table tags')
        database.execute_non_query(self._conn, 'truncate table templates')
        return '{}'
