import sys
import requests
from optional_django import six
from .conf import settings
from .exceptions import BuildServerConnectionError, BuildServerUnexpectedResponse


class BuildServer(object):
    def __init__(self, url):
        self.url = url

    def is_running(self):
        try:
            res = requests.get(self.url)
        except requests.ConnectionError:
            return False

        return res.status_code == 200 and 'webpack-build' in res.text

    def build(self, options):
        try:
            res = requests.post('{}/build'.format(self.url), json=options)
        except requests.ConnectionError as e:
            raise six.reraise(BuildServerConnectionError, BuildServerConnectionError(*e.args), sys.exc_info()[2])

        if res.status_code != 200:
            raise BuildServerUnexpectedResponse(res.text)

        return res.json()


server = BuildServer(settings.BUILD_SERVER_URL)
