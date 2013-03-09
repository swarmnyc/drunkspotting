#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import json
import hashlib
import binascii
import psycopg2
import os
import datetime
import cgi
import azure.storage

import database
import drunkspotting_exceptions
import config

class Server:
    def __init__(self):
        """Create a new server
        """

        import gevent
        import gevent.wsgi
        import gevent.monkey
        gevent.monkey.patch_all()

        self._conn = psycopg2.connect(
            database=config.config['database'],
            user=config.config['database_user'],
            password=config.config['database_password'])

        logging.info("Server initialized.")

    def ping(self, env):
        return 'pong'

    def _upload(self, data, folder):
        salt = binascii.b2a_hex(os.urandom(20))
        sha1 = hashlib.sha1()
        sha1.update(salt)
        sha1.update(str(datetime.datetime.now()))
        img = sha1.hexdigest() + ".jpg"

        blob_service = azure.storage.BlobService(
            account_name=config.config['azure_account'],
            account_key=config.config['azure_key'])
        blob_service.create_container(folder,
                                      x_ms_blob_public_access='blob')
        blob_service.put_blob(folder, img,
                              data, x_ms_blob_type='BlockBlob',
                              x_ms_blob_content_type='image/jpeg')

        url = config.config['upload_url'] + folder + '/' + img
        print url
        return json.dumps({'url': url})

    def upload_template(self, data, env):
        return self._upload(data, 'templates')

    def upload_picture(self, data, env):
        return self._upload(data, 'pictures')

    def get_template(self, template, env):
        template = int(template)

        # TODO: Merge with get_latest_templates
        sql = 'select title, latitude, longitude, description, rating, ' \
              'rating_count, url, time_posted from templates ' \
              'where id = %s'

        rows = database.execute_all_rows(self._conn, sql, (template, ))
        if not rows:
            raise drunkspotting_exceptions.NotFoundException('Not found')

        row = rows[0]
        return json.dumps({
            'title': row[0],
            'latitude': row[1], 'longitude': row[2],
            'description': row[3], 'rating': row[4],
            'rating_count': row[5], 'url': row[6],
            'time_posted': row[7].isoformat()})

    def get_picture(self, picture, env):
        picture = int(picture)

        # sql = 'select template_id, latitude, longitude, ' \
        #       'pictures.title, pictures.description,' \
        #       'pictures.rating, pictures.rating_count,' \
        #       'pictures.url, pictures.time_posted from pictures, templates ' \
        #       'where template_id = templates.id ' \
        #       'and pictures.id = %s'

        sql = 'select template_id, 0, 0, ' \
              'pictures.title, pictures.description,' \
              'pictures.rating, pictures.rating_count,' \
              'pictures.url, pictures.time_posted from pictures ' \
              'where pictures.id = %s'

        rows = database.execute_all_rows(self._conn, sql, (picture, ))
        if not rows:
            raise drunkspotting_exceptions.NotFoundException('Not found')
        row = rows[0]

        # return json.dumps({
        #     'template_id': row[0],
        #     'latitude': row[1], 'longitude': row[2],
        #     'title': row[3],
        #     'description': row[4], 'rating': row[5],
        #     'rating_count': row[6], 'url': row[7],
        #     'time_posted': row[8].isoformat()})

        return json.dumps({
            'template_id': row[0],
            'latitude': 12.34, 'longitude': 23.34,
            'title': row[3],
            'description': row[4], 'rating': row[5],
            'rating_count': row[6], 'url': row[7],
            'time_posted': row[8].isoformat()})

    def get_latest_template_comments(self, template, count, env):
        template = int(template)
        count = int(count)

        sql = 'select id, nick, title, description, up_votes, down_votes, ' \
              'time_posted from comments where template_id = %s order by ' \
              'time_posted desc limit %s'

        rows = database.execute_all_rows(self._conn, sql, (template, count, ))

        comments = []
        for row in rows:
            comments.append({
                'id': row[0], 'nick': row[1],
                'title': row[2], 'description': row[3],
                'up_votes': row[4], 'down_votes': row[5],
                'time_posted': row[6].isoformat()})

        return json.dumps(comments)

    def get_latest_picture_comments(self, picture, count, env):
        # TODO: Ugh, near copy of get_latest_template_comments
        picture = int(picture)
        count = int(count)

        sql = 'select id, nick, title, description, up_votes, down_votes, ' \
              'time_posted from comments where picture_id = %s order by ' \
              'time_posted desc limit %s'

        rows = database.execute_all_rows(self._conn, sql, (picture, count, ))

        comments = []
        for row in rows:
            comments.append({
                'id': row[0], 'nick': row[1],
                'title': row[2], 'description': row[3],
                'up_votes': row[4], 'down_votes': row[5],
                'time_posted': row[6].isoformat()})

        return json.dumps(comments)

    def get_latest_templates(self, count, env):
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

        return json.dumps(templates)

    def get_latest_pictures(self, count, env):
        count = int(count)

        # sql = 'select pictures.id, template_id, latitude, longitude, ' \
        #       'pictures.title, pictures.description,' \
        #       'pictures.rating, pictures.rating_count,' \
        #       'pictures.url, pictures.time_posted from pictures, templates ' \
        #       'where template_id = templates.id ' \
        #       'order by pictures.time_posted desc limit %s'

        sql = 'select pictures.id, 0, 0, 0, ' \
              'pictures.title, pictures.description,' \
              'pictures.rating, pictures.rating_count,' \
              'pictures.url, pictures.time_posted from pictures ' \
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

        return json.dumps(templates)

    def get_tags(self, env):
        pass

    def find_by_tags(self, env):
        pass

    def post_template(self, data, env):
        data = json.loads(data)
        sql = 'insert into templates(title, ip, latitude, longitude, ' \
              'description, rating, rating_count, url, time_posted) ' \
              'values(%s, %s, %s, %s, %s, %s, %s, %s, now()) ' \
              'returning id'

        params = (data['title'], env['REMOTE_ADDR'],
                data['latitude'], data['longitude'],
                data['description'], 0, 0, data['url'])

        id = database.execute_non_query_returning_id(
            self._conn, sql, params)

        return '{"id": %d}' % (id, )

    def post_template_comment(self, template, data, env):
        # TODO: Verify template id
        template = int(template)
        data = json.loads(data)
        sql = 'insert into comments(template_id, ip, nick,' \
              'title, description, up_votes, down_votes, time_posted) ' \
              'values(%s, %s, %s, %s, %s, 0, 0, now()) ' \
              'returning id'

        params = (template, env['REMOTE_ADDR'],
                data['nick'], data['title'],
                data['description'])

        id = database.execute_non_query_returning_id(
            self._conn, sql, params)

        return '{"id": %d}' % (id, )

    def post_picture_comment(self, picture, data, env):
        # TODO: Ugh, almost exact copy of post_template_comment - refactor
        picture = int(picture)
        data = json.loads(data)
        sql = 'insert into comments(picture_id, ip, nick,' \
              'title, description, up_votes, down_votes, time_posted) ' \
              'values(%s, %s, %s, %s, %s, 0, 0, now()) ' \
              'returning id'

        params = (picture, env['REMOTE_ADDR'],
                data['nick'], data['title'],
                data['description'])

        id = database.execute_non_query_returning_id(
            self._conn, sql, params)

        return '{"id": %d}' % (id, )

    def post_tag(self, data, env):
        pass

    def post_picture(self, data, env):
        # TODO: Verify that the template ID is ok
        data = json.loads(data)
        sql = 'insert into pictures(template_id, title, ip, ' \
              'description, rating, rating_count, url, time_posted) ' \
              'values(%s, %s, %s, %s, 0, 0, %s, now()) ' \
              'returning id'

        params = (data['template_id'], data['title'], env['REMOTE_ADDR'],
                  data['description'], data['url'])

        id = database.execute_non_query_returning_id(
            self._conn, sql, params)

        salt = binascii.b2a_hex(os.urandom(20))
        sha1 = hashlib.sha1()
        sha1.update(salt)

        return json.dumps({'id': id})

    def nuke_it_all(self, env):
        if 'allow-nuking-database' in config.config:
            if config.config['allow-nuking-database'] == 'yes-be-careful':
                database.execute_non_query(
                    self._conn, 'truncate table comments')
                database.execute_non_query(
                    self._conn, 'truncate table pictures')
                database.execute_non_query(
                    self._conn, 'truncate table tags')
                database.execute_non_query(
                    self._conn, 'truncate table templates')
                return '{}'

        raise drunkspotting_exceptions.NotFoundException('Not found')
