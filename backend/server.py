#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import json
import hashlib
import binascii
import psycopg2
import os
import datetime
import azure.storage

import database
import drunkspotting_exceptions
from config import config


class Server:
    def __init__(self):
        """Create a new server
        """

        import gevent
        import gevent.wsgi
        import gevent.monkey
        gevent.monkey.patch_all()

        self._conn = psycopg2.connect(
            database=config['database'],
            user=config['database_user'],
            password=config['database_password'])

        logging.info("Server initialized.")

    def ping(self, env):
        return 'pong'

    def upload(self, data, env):
        salt = binascii.b2a_hex(os.urandom(20))
        sha1 = hashlib.sha1()
        sha1.update(salt)
        sha1.update(str(datetime.datetime.now()))
        img = sha1.hexdigest() + ".jpg"

        if 'azure_account' in config and config['azure_account']:
            blob_service = azure.storage.BlobService(
                account_name=config['azure_account'],
                account_key=config['azure_key'])
            blob_service.create_container('pictures',
                                          x_ms_blob_public_access='blob')
            blob_service.put_blob('pictures', img,
                                  data, x_ms_blob_type='BlockBlob',
                                  x_ms_blob_content_type='image/jpeg')
        elif 'upload_folder' in config and config['upload_folder']:
            with open(os.path.join(config['upload_folder'], img), 'wb') as f:
                f.write(data)

        url = config['upload_url'] + 'pictures/ ' + img
        print url
        return json.dumps({'url': url})

    def get_picture(self, picture_id, env):
        picture_id = int(picture_id)

        sql = 'select template_id, is_template, title, description, ' \
              'latitude, longitude, rating, rating_count, url, ' \
              'time_posted from pictures where id = %s'

        rows = database.execute_all_rows(self._conn, sql, (picture_id, ))
        if not rows:
            raise drunkspotting_exceptions.NotFoundException('Not found')

        row = rows[0]
        return json.dumps({
            'template_id': row[0], 'is_template': row[1],
            'title': row[2], 'description': row[3],
            'latitude': row[4], 'longitude': row[5],
            'rating': row[6], 'rating_count': row[7],
            'url': row[8], 'time_posted': row[9].isoformat()})

    def _get_latest_pictures(self, count, is_template, env):
        count = int(count)
        is_template = bool(is_template)

        sql = 'select id, template_id, title, latitude, longitude, ' \
              'description, rating, rating_count, url, time_posted from ' \
              'pictures where is_template = %s order by time_posted desc ' \
              'limit %s'

        rows = database.execute_all_rows(self._conn, sql, (is_template, count))

        templates = []
        for row in rows:
            templates.append({
                'id': row[0], 'template_id': row[1],
                'title': row[2],
                'latitude': row[3], 'longitude': row[4],
                'description': row[5], 'rating': row[6],
                'rating_count': row[7], 'url': row[8],
                'time_posted': row[9].isoformat()})

        return json.dumps(templates)

    def get_latest_templates(self, count, env):
        return self._get_latest_pictures(count, True, env)

    def get_latest_pictures(self, count, env):
        return self._get_latest_pictures(count, False, env)

    def get_latest_comments(self, picture_id, count, env):
        picture_id = int(picture_id)
        count = int(count)

        sql = 'select id, nick, title, description, up_votes, down_votes, ' \
              'time_posted from comments where picture_id = %s ' \
              'order by time_posted desc limit %s'

        rows = database.execute_all_rows(self._conn, sql,
                                         (picture_id, count))

        comments = []
        for row in rows:
            comments.append({
                'id': row[0], 'nick': row[1],
                'title': row[2], 'description': row[3],
                'up_votes': row[4], 'down_votes': row[5],
                'time_posted': row[6].isoformat()})

        return json.dumps(comments)

    def _post_picture(self, data, env):
        sql = 'insert into pictures(template_id, is_template, title, ip, ' \
              'description, latitude, longitude, rating, rating_count, ' \
              'url, time_posted) ' \
              'values(%s, %s, %s, %s, %s, %s, %s, 0, 0, %s, now()) ' \
              'returning id'

        params = (data.get('template_id', None),
                data['is_template'],
                data.get('title', ''),
                env['REMOTE_ADDR'],
                data.get('decription', ''),
                data.get('latitude', None),
                data.get('longitude', None),
                data['url'])

        id = database.execute_non_query_returning_id(
            self._conn, sql, params)

        return '{"id": %d}' % (id, )

    def post_template(self, data, env):
        data = json.loads(data)
        if 'is_template' not in data:
            data['is_template'] = True
        return self._post_picture(data, env)

    def post_picture(self, data, env):
        data = json.loads(data)
        if 'is_template' not in data:
            data['is_template'] = False
        return self._post_picture(data, env)

    def post_comment(self, picture_id, data, env):
        data = json.loads(data)
        picture_id = int(picture_id)
        sql = 'insert into comments(picture_id, ip, nick,' \
              'title, description, up_votes, down_votes, time_posted) ' \
              'values(%s, %s, %s, %s, %s, 0, 0, now()) ' \
              'returning id'

        params = (picture_id, env['REMOTE_ADDR'],
                data['nick'], data['title'],
                data['description'])

        id = database.execute_non_query_returning_id(
            self._conn, sql, params)

        return '{"id": %d}' % (id, )

    def post_tag(self, data, env):
        pass

    def get_tags(self, env):
        pass

    def find_by_tags(self, env):
        pass

    def nuke_it_all(self, env):
        if 'allow-nuking-database' in config:
            if config['allow-nuking-database'] == 'yes-be-careful':
                database.execute_non_query(
                    self._conn, 'truncate table comments')
                database.execute_non_query(
                    self._conn, 'truncate table pictures')
                database.execute_non_query(
                    self._conn, 'truncate table tags')
                return '{}'

        raise drunkspotting_exceptions.NotFoundException('Not found')
