EXTENSIONS = [
    {
        "name": "Temp",
        "extension_class": "tests.test_commands.temp_extension.TempExtension",
        "key1": "value1",
    }
]

PORT = 9999
REQUEST_HANDLERS = [
    {
        "pattern": r"/",
        "handler_class": "tests.test_commands.temp_handler.TempHandler",
        "key1": "value1"
    }
]
