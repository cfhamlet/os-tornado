from os_tornado.extension import Extension


class ExampleExtension(Extension):
    def setup(self):
        super(ExampleExtension, self).setup()
        self._logger.debug('setup')
        self._logger.debug('extension settings: %s' % str(self.ext_settings))

    def run(self):
        super(ExampleExtension, self).run()
        self._logger.debug('run')

    def cleanup(self):
        super(ExampleExtension, self).cleanup()
        self._logger.debug('cleanup')
    