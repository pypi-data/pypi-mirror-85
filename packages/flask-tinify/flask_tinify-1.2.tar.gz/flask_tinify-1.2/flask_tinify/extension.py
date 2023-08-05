import threading

from flask_tinify.source import Source
from flask_tinify.client import Client
from flask_tinify.errors import AccountError, ClientError


class Tinify(object):
    def __init__(self, app=None):
        self._lock = threading.RLock()

        self._client = None
        self._key = None
        self._app_identifier = None
        self._proxy = None
        self._compression_count = None

        self.endpoint = None
        self.retry_count = None
        self.retry_delay = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        self.key = app.config.get('TINIFY_KEY')
        self.proxy = app.config.get('TINIFY_PROXY', None)
        self.endpoint = app.config.get('TINIFY_ENDPOINT', 'https://api.tinify.com')
        self.retry_count = app.config.get('TINIFY_RETRY_COUNT', 1)
        self.retry_delay = app.config.get('TINIFY_RETRY_DELAY', 500)

        app.extensions['tinify'] = self

    @property
    def key(self):
        if self._key and len(self._key) > 0:
            return self._key

    @key.setter
    def key(self, value):
        self._key = value
        self._client = None

    @property
    def app_identifier(self):
        return self._app_identifier

    @app_identifier.setter
    def app_identifier(self, value):
        self._app_identifier = value
        self._client = None

    @property
    def proxy(self):
        return self._key

    @proxy.setter
    def proxy(self, value):
        self._proxy = value
        self._client = None

    @property
    def compression_count(self):
        return self._compression_count

    @compression_count.setter
    def compression_count(self, value):
        self._compression_count = value

    def get_client(self):
        if not self._key:
            raise AccountError('Provide an API key with tinify.key = ...')

        if not self._client:
            with self._lock:
                if not self._client:
                    self._client = Client(self._key, self, self._app_identifier, self._proxy)

        return self._client

    def validate(self):
        try:
            self.get_client().request('post', '/shrink')
        except AccountError as err:
            if err.status == 429:
                return True
            raise err
        except ClientError:
            return True

    def from_file(self, path):
        if hasattr(path, 'read'):
            return self._shrink(path)
        else:
            with open(path, 'rb') as f:
                return self._shrink(f.read())

    def from_buffer(self, string):
        return self._shrink(string)

    def from_url(self, url):
        return self._shrink({"source": {"url": url}})

    def _shrink(self, obj):
        response = self.get_client().request('POST', '/shrink', obj)
        return Source(response.headers.get('location'), self)
