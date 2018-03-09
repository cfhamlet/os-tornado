import traceback
import wrapt
from tornado.web import RequestHandler


def _jsonify_common_operations(method):
    def _exec(instance, *args, **kwargs):
        response = method(instance, *args, **kwargs)
        if response is not None:
            instance.write(response)
    return _exec


def _jsonify_write_error(method):
    def _exec(instance, status_code, **kwargs):
        if instance.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            instance.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                instance.write(line)
            instance.finish()
        else:
            response = {'status_code': status_code}
            if instance._reason is not None:
                response['reason'] = instance._reason

            instance.finish(response)
    return _exec


_OPERATION_WRAPPER = dict.fromkeys(['head', 'get', 'post', 'delete', 'patch', 'put', 'options'],
                                   _jsonify_common_operations)
_OPERATION_WRAPPER['write_error'] = _jsonify_write_error

_WRAPPED_CLASSES = set([])


@wrapt.decorator
def jsonify(wrapped, instance, args, kwargs):
    if not issubclass(wrapped, RequestHandler):
        raise TypeError('%s is not subclass of tornado.web.RequestHandler'
                        % wrapped.__name__)
    if wrapped in _WRAPPED_CLASSES:
        return wrapped(*args, **kwargs)
    for operation in _OPERATION_WRAPPER:
        if hasattr(wrapped, operation):
            method = getattr(wrapped, operation)
            wrapped_method = _OPERATION_WRAPPER[operation](method)
            setattr(wrapped, operation, wrapped_method)
    _WRAPPED_CLASSES.add(wrapped)

    return wrapped(*args, **kwargs)
