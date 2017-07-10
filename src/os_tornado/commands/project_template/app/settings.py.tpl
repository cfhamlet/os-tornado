# coding: utf-8

LOG_LEVEL = "DEBUG"
TORNADO_APP_SETTINGS_COOKIE_SECRET = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"

EXTENSIONS = [
    {
        "name":"Example",
        "extension_class":"app.extensions.example_extension.ExampleExtension",
        "key1":"value1",
    }
]

HTTP_PORT = 8080
REQUEST_HANDLERS = [
    {
        "pattern":r"/",
        "handler_class":"app.request_handlers.example_handler.ExampleHandler",
        "key1":"value1"
    }
]
