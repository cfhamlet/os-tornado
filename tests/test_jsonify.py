import json
import sys

import pytest
import tornado.ioloop
from os_tornado.decorators import jsonify

_PY3 = sys.version_info[0] >= 3
if _PY3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin


def test_not_request_handler_class():
    @jsonify
    class NotRequestHander(object):
        pass
    with pytest.raises(TypeError):
        NotRequestHander()


@jsonify
class GetOK(tornado.web.RequestHandler):
    def get(self):
        return {'status': 'ok'}


@jsonify
class Get404(tornado.web.RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(404)


application = tornado.web.Application([
    (r"/get/ok", GetOK),
    (r"/get/404", Get404),
])


@pytest.mark.skip(reason="pytest-tornado don't support lastest version")
@pytest.fixture
def app():
    return application


@pytest.mark.skip(reason="pytest-tornado don't support lastest version")
@pytest.mark.gen_test
def test_return_dict(http_client, base_url):
    response = yield http_client.fetch(urljoin(base_url, '/get/ok'))
    assert response.code == 200
    assert json.loads(response.body) == {'status': 'ok'}


@pytest.mark.skip(reason="pytest-tornado don't support lastest version")
@pytest.mark.gen_test
def test_not_found(http_client, base_url):
    response = yield http_client.fetch(urljoin(base_url, '/get/404'), raise_error=False)
    assert response.code == 404
    assert json.loads(response.body)['status_code'] == 404
