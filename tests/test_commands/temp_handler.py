import json
from tornado.web import RequestHandler


class TempHandler(RequestHandler):
    def initialize(self, **kwargs):
        self.handler_settings = kwargs

    def get(self):
        self.write(json.dumps(self.handler_settings))
