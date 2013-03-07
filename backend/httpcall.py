#!/usr/bin/python

import gevent
import gevent.monkey
gevent.monkey.patch_all()

import urllib2
import array
import cStringIO
import time
import argparse

class Request(urllib2.Request):
    """Subclass of urllib2.Request to support PUT and binary content

    We have to subclass Request, because we want to be able to control the verb.
    A PUT will otherwise turn into a POST. Additionally, passing data straight
    to urllib2 in the constructor only works if it is propery string data,
    while our data is binary. httplib will then sometimes complain if
    there are bytes like 0xFF in there. We use cStringIO, to get httplib
    to read the raw bytes instead."""

    def __init__(self, verb, url, data):
        """Initialize the class, with a http verb, URL and data

        The data is streamed to the request, to be able to use binary data."""

        self.verb = verb

        if data:
            urllib2.Request.__init__(self, url, None)
            self.add_header("Content-Length", str(len(data)))
            self.add_header("Content-Type", "binary/octet-stream")

            output = cStringIO.StringIO(data)
            self.add_data(output)          
        else:
            urllib2.Request.__init__(self, url, None)


    def get_method(self):
        """Function override to supply verb"""

        return self.verb

def call(verb, url, data = None):
    """Call to send a http request with given verb, url and data.

    This function is used throughout the system any time a peer
    needs initiate communications with another peer.

    Any errors, including connection errors are transformed
    into a http 500 response, with the exception as the reason

    This way any errors can be treated in the same way, no matter
    if they are network errors or unexpected errors from the peer"""

    if verb in ["GET", "HEAD", "DELETE"]:
        request = Request(verb, url, None)
    elif verb in ["PUT", "POST"]:
        request = Request(verb, url, data)

    response = None
    try:
        response = urllib2.urlopen(request)

        data = response.read()
        rc = (response.code, response.msg, data)
    except urllib2.HTTPError, e:
        rc = (e.code, e.msg, "")
    except urllib2.URLError, e:
        rc = (500, e, "")
    finally:
        if response:
            response.close()
    
    return rc


def run():
    """Call this function to use issue httpcalls from the command line"""

    print

    parser = argparse.ArgumentParser(description="httpcall")
    parser.add_argument("verb", choices=["GET", "PUT", "POST", "HEAD", "DELETE"])
    parser.add_argument("url")
    parser.add_argument("data", nargs="?", default="")

    args = parser.parse_args()

    [status, reason, data] = call(args.verb, args.url, args.data)
    print("Status %d, reason: %s, data:" % (status, reason))
    print(data)
            

if __name__ == '__main__':
    run()

