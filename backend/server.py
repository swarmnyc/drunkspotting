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

    def get_latest_templates(self, count):
        count = int(count)

        sql = 'select id, title, latitude, longitude, description, rating, ' \
              'rating_count, url, time_posted from templates order by ' \
              'time_posted desc limit %s'

        rows = database.execute_all_rows(self._conn, sql, (count, ))

        templates = []
        for row in rows:
            templates.append({
                'id': row[0], 'title': row[1],
                'latitude': row[2], 'longitude': row[3],
                'description': row[4], 'rating': row[5],
                'rating_count': row[6], 'url': row[7],
                'time_posted': row[8].isoformat()})

        return cjson.encode(templates)

    def get_latest_pictures(self, count):
        count = int(count)

        sql = 'select pictures.id, template_id, latitude, longitude, ' \
              'pictures.title, pictures.description,' \
              'pictures.rating, pictures.rating_count,' \
              'pictures.url, pictures.time_posted from pictures, templates ' \
              'where template_id = templates.id ' \
              'order by pictures.time_posted desc limit %s'

        rows = database.execute_all_rows(self._conn, sql, (count, ))

        templates = []
        for row in rows:
            templates.append({
                'id': row[0], 'template_id': row[1],
                'latitude': row[2], 'longitude': row[3],
                'title': row[4],
                'description': row[5], 'rating': row[6],
                'rating_count': row[7], 'url': row[8],
                'time_posted': row[9].isoformat()})

        return cjson.encode(templates)

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

        params = (data['title'], '1.2.3.4',
                data['latitude'], data['longitude'],
                data['description'], 0, 0, data['url'])

        id = database.execute_non_query_returning_id(
            self._conn, sql, params)

        return '{"id": %d}' % (id, )

    def post_comment(self, data):
        pass

    def post_tag(self, data):
        pass

    def post_picture(self, data):
        # TODO: Verify that the template ID is ok
        data = cjson.decode(data)
        sql = 'insert into pictures(template_id, title, ip, ' \
              'description, rating, rating_count, url, time_posted) ' \
              'values(%s, %s, %s, %s, 0, 0, %s, now()) ' \
              'returning id'

        params = (data['template_id'], data['title'], '1.2.3.4',
                  data['description'], data['url'])

        id = database.execute_non_query_returning_id(
            self._conn, sql, params)

        return '{"id": %d}' % (id, )

    def nuke_it_all(self):
        database.execute_non_query(self._conn, 'truncate table comments')
        database.execute_non_query(self._conn, 'truncate table pictures')
        database.execute_non_query(self._conn, 'truncate table tags')
        database.execute_non_query(self._conn, 'truncate table templates')
        return '{}'
