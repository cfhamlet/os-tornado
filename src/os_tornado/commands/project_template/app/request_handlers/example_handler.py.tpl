import json
from tornado.web import RequestHandler

class ExampleHandler(RequestHandler):
    def initialize(self, **kwargs):
        self.handler_settings = kwargs
    
    def get(self, *args, **kwargs):
        self.write(json.dumps(self.handler_settings))