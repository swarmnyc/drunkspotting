#!/usr/bin/python
"""This module implements a wsgi handler calling into its server
"""

import re
import logging
import sys
import argparse
import daemon
#import lockfile


import drunkspotting_exceptions
import server


class Gateway:
    """ This class contains a wsgi handler function as well as a list
    of urls (as compiled regular expressions) and the associated server
    functions they map to """

    def __init__(self, server):
        """Initialize the gateway. It will forward calls to the attached server """
        self._CONTENT_TYPE = "application/json"
        self._server = server
        self._gets = [
            [re.compile("/templates/(\w+)/*$"), self._server.get_template],
            [re.compile("/pictures/(\w+)/*$"), self._server.get_picture],
            [re.compile("/templates/(\w+)/comments/latest/(\w+)/*$"), self._server.get_latest_template_comments],
            [re.compile("/pictures/(\w+)/comments/latest/(\w+)/*$"), self._server.get_latest_picture_comments],

            [re.compile("/nuke_it_all/*$"), self._server.nuke_it_all],

            [re.compile("/ping/*$"), self._server.ping],
            [re.compile("/templates/latest/(\w+)$"), self._server.get_latest_templates],
            [re.compile("/pictures/latest/(\w+)$"), self._server.get_latest_pictures],
            [re.compile("/tags/*$"), self._server.get_tags],
            [re.compile("/find_by_tags/*$"), self._server.find_by_tags]]

        self._posts = [
            [re.compile("/templates/*$"), self._server.post_template],
            [re.compile("/tags/(\w+)/*$"), self._server.post_tag],
            [re.compile("/templates/(\w+)/comments/*$"), self._server.post_template_comment],
            [re.compile("/pictures/(\w+)/comments/*$"), self._server.post_picture_comment],
            [re.compile("/pictures/*$"), self._server.post_picture]]

    def process_without_data(self, path, calls):
        """Process http requests that do not have data (GET/HEAD/DELETE)

        The incoming path is matched against the calls (for example self.heads)
        and if the path matches, the corresponding function will be called,
        with any match groups as additional parameters"""
        print 'GET: ' + path
        for call in calls:
            match = call[0].match(path)
            if match:
                return call[1](*match.groups())
        raise drunkspotting_exceptions.UnknownMethodException(path)

    def process_with_data(self, path, calls, data):
        """Process http requests that have data (PUT/POST)

        The incoming path is matched against the calls (for example self.heads)
        and if the path matches, the corresponding function will be called,
        with any match groups as additional parameters"""

        print 'PUT/POST ' + path + ' data: ' + data
        for call in calls:
            match = call[0].match(path)
            if match:
                # A bit of a pain, but I want the key before the data in the calls
                params = list(match.groups())
                params.append(data)
                return call[1](*params)
        raise drunkspotting_exceptions.UnknownMethodException(path)

    def handler(self, env, start_response):
        """ WSGI handler function, called whenever a http request is received

        The path and http verb is used to distinguish against what
        list of regular expression function pairs the request should be run against

        The incoming path is matched against the calls
        and if the path matches, the corresponding function will be called,
        with any match groups as additional parameters

        Exceptions are caught and turned into http return codes"""
        try:
            if env["REQUEST_METHOD"] == "GET":
                response = self.process_without_data(env["PATH_INFO"], self._gets)
            elif env["REQUEST_METHOD"] == "HEAD":
                response = self.process_without_data(env["PATH_INFO"], self._heads)
            elif env["REQUEST_METHOD"] == "DELETE":
                response = self.process_without_data(env["PATH_INFO"], self._deletes)
            elif env["REQUEST_METHOD"] in ("PUT", "POST"):

                content_length = int(env.get('CONTENT_LENGTH', 0))
                data = env['wsgi.input'].read(content_length)

                if env["REQUEST_METHOD"] == "PUT":
                    response = self.process_with_data(env["PATH_INFO"], self._puts, data)
                else:
                    response = self.process_with_data(env["PATH_INFO"], self._posts, data)

            else:
                start_response('500 Unknown verb', [("Content-Type", self._CONTENT_TYPE),
                    ('Access-Control-Allow-Origin', '*'),
                    ('Access-Control-Allow-Methods' ,'GET, POST')])
                return[response]

            start_response("200 OK", [("Content-Type", self._CONTENT_TYPE),
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods' ,'GET, POST')])
            return [response]

        except drunkspotting_exceptions.NotFoundException:
            start_response('404 Item not found', [("Content-Type", self._CONTENT_TYPE),
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods' ,'GET, POST')])
            return[""]
        except drunkspotting_exceptions.AcccessDeniedException:
            start_response('403 Access denied', [("Content-Type", self._CONTENT_TYPE),
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods' ,'GET, POST')])
            return[""]
        except Exception:
            response = str(sys.exc_info())
            logging.exception("Error handling request.")

            start_response('500 Server error', [("Content-Type", self._CONTENT_TYPE),
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods' ,'GET, POST')])
            return[response]


def run(log):
    import gevent
    import gevent.monkey
    import gevent.wsgi
    gevent.monkey.patch_all()

    if log != "":
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG, filename=args.log, filemode="w")
    else:
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    deliverish_server = server.Server()
    deliverish_gateway = Gateway(deliverish_server)

    httpd = gevent.wsgi.WSGIServer(('', 8200), deliverish_gateway.handler,
                                   log=None)
    httpd.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="deliverish")
    parser.add_argument('--daemon', dest="daemon", action='store_true', default=False,
        help="Run as daemon.")
    parser.add_argument('--log', action="store", dest="log", default="",
        help="Log file location")

    # Will exit out on error
    args = parser.parse_args()

    if args.daemon:
        context = daemon.DaemonContext(working_directory='.', umask=0o002,
             stdout=file("stdout.txt", "w"), stderr=file("stderr.txt", "w"))
#             pidfile=lockfile.FileLock('concerts.pid'))

        with context:
            run(args.log)
    else:
        run(args.log)
