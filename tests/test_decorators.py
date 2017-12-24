import pytest
import json
from tornado.web import RequestHandler, Application
from os_tornado.decorators import jsonify


def test_json_response():
    with pytest.raises(TypeError):
        @jsonify
        class NotRequestHander(object):
            pass
