from __future__ import absolute_import, division, print_function, unicode_literals

import os
import platform
import time

import requests
import requests.exceptions

import json
from . import __version__
from .errors import ConnectionError, Error


class Client(object):
    USER_AGENT = 'Tinify/{0} Python/{1} ({2})'.format(__version__,
                                                      platform.python_version(),
                                                      platform.python_implementation())

    def __init__(self, key, tinify, app_identifier=None, proxy=None):
        self.session = requests.sessions.Session()
        if proxy:
            self.session.proxies = {'https': proxy}
        self.session.auth = ('api', key)
        self.session.headers = {
            'user-agent': self.USER_AGENT + ' ' + app_identifier if app_identifier else self.USER_AGENT,
        }
        self.session.verify = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'cacert.pem')
        self.tinify = tinify

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.session.close()

    def request(self, method, url, body=None):
        url = url if url.lower().startswith('https://') else self.tinify.endpoint + url
        params = {}
        if isinstance(body, dict):
            if body:
                # Dump without whitespace.
                params['headers'] = {'Content-Type': 'application/json'}
                params['data'] = json.dumps(body, separators=(',', ':'))
        elif body:
            params['data'] = body

        for retries in range(self.tinify.retry_count, -1, -1):
            if retries < self.RETRY_COUNT:
                time.sleep(self.tinify.retry_delay / 1000.0)

            try:
                response = self.session.request(method, url, **params)
            except requests.exceptions.Timeout as err:
                if retries > 0:
                    continue
                raise ConnectionError('Timeout while connecting', cause=err)
            except Exception as err:
                if retries > 0:
                    continue
                raise ConnectionError('Error while connecting: {0}'.format(err), cause=err)

            count = response.headers.get('compression-count')
            if count:
                self.tinify.compression_count = int(count)

            if response.ok:
                return response

            details = None
            try:
                details = response.json()
            except Exception as err:
                details = {'message': 'Error while parsing response: {0}'.format(err), 'error': 'ParseError'}
            if retries > 0 and response.status_code >= 500: continue
            raise Error.create(details.get('message'), details.get('error'), response.status_code)
