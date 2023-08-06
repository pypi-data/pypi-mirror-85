#
# Copyright (c) 2018 Eric Faurot <eric@faurot.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import base64
import hashlib
import importlib
import json
import logging
import os
import time

import bottle


def _logger(logger):
    return logger if logger is not None else logging.getLogger(__name__)


def run_bottle(app, **kwargs):
    bottle.run(app = app, quiet = True, **kwargs)


_apis = {}
def api(path):
    def _(setup):
        _apis[setup] = API(path, setup)
    return _


class API:

    stack = None
    app = None

    def __init__(self, prefix, setup):
        self.prefix = prefix
        self.setup = setup

    def install(self, stack):
        assert self.stack is None
        mount_point = os.path.join(stack.prefix, self.prefix)
        if not mount_point.endswith('/'):
            mount_point += '/'
        app = stack.app_factory()
        self.setup(app)
        stack.app.mount(mount_point, self)
        self.app = app
        self.stack = stack

    def __call__(self, environ, handler):
        environ['udon.api'] = self
        return self.app(environ, handler)


class APIStack(object):

    def __init__(self, prefix = "/", **options):
        self.prefix = prefix
        self.options = options
        self.app = self.app_factory()

    def app_factory(self):
        return bottle.Bottle(**self.options)

    def _install(self, mount_point, setup):
        # TODO deprecate
        return self.install_func(mount_point, setup)

    def install_func(self, prefix, setup):
        api = API(prefix, setup)
        api.install(self)

    def install(self, module_name):
        # TODO deprecate
        return self.install_module(module_name)

    def install_module(self, module_name):
        importlib.import_module(module_name)
        for api in _apis.values():
            if not api.stack:
                api.install(self)

    def __call__(self, environ, handler):
        return self.app(environ, handler)


class WSGIErrorStream:

    def __init__(self, stream, autoflush = False, logger = None):
        self.stream = stream
        self.autoflush = autoflush
        self.logger = _logger(logger)

    def write(self, err):
        try:
            self.stream.write("WSGI ERROR ---- %s\n%s" % (time.ctime(), err))
            if self.autoflush:
                self.stream.flush()
        except:
            self.logger.exception("Failed to write WSGI error")

    def flush(self):
        try:
            self.stream.flush()
        except:
            self.logger.exception("Failed to flush WSGI error")


class WSGIErrorLogger:

    def __init__(self, logger = None):
        self.logger = _logger(logger)

    def write(self, err):
        try:
            self.logger.error("WSGI ERROR: %s", err)
        except:
            self.logger.exception("Failed to write WSGI error")

    def flush(self):
        pass


class EnvMiddleware:

    def __init__(self, app, environ = None):
        self.app = app
        self.environ = {} if environ is None else environ

    def setenv(self, key, value):
        self.environ[key] = value

    def __call__(self, environ, handler):
        environ.update(self.environ)
        return self.app(environ, handler)


class LogMiddleware:

    def __init__(self, app, logger = None):
        self.app = app
        self.logger = _logger(logger)

    def __call__(self, environ, handler):
        t0 = time.time()
        ret = self.app(environ, handler)
        try:
            self.log(environ, ret, time.time() - t0)
        except:
            self.logger.exception("Failed to log result")
        return ret

    def log(self, environ, ret, dt):
        msg = self.format_message(environ, ret, dt)
        self.logger.info(msg)

    def format_message(self, environ, ret, dt):
        request = bottle.request
        response = bottle.response
        _scheme, host, _path, _query_string, _fragment = request.urlparts
        return "%.3f %s %s %s %d %d %s %s" % (dt,
                                              environ["REMOTE_ADDR"],
                                              environ.get("HTTP_X_FORWARDED_FOR", "-"),
                                              request.method,
                                              response.status_code,
                                              response.content_length,
                                              host,
                                              request.path)


def abort(code, message):
    bottle.abort(code, message)


class Form(object):

    def __init__(self, request = None):
        if request is None:
            request = bottle.request
        self.request = request

    def raw(self, name):
        return self.request.forms.get(name)

    def string(self, name):
        return self.raw(name)

    def integer(self, name):
        return int(self.raw(name))

    def float(self, name):
        return float(self.raw(name))

    def date(self, name, fmt = "%d/%m/%Y"):
        return datetime.datetime.strptime(self.raw(name), fmt)

    def file(self, name):
        if name not in self.request.files:
            return None, None
        value = self.request.files[name]
        filename = os.path.basename(value.filename)
        return value.file, filename

_mandatory = object()
_unset = object()
class Parameters(object):

    def __init__(self, params):
        if not isinstance(params, dict):
            abort(400, 'Expect parameter object')
        self.params = params

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if (type, value, traceback) == (None, None, None):
            if self.params:
                abort(400, 'Unexpected parameter(s): %s' % ', '.join(self.params.keys()))

    def get(self, name, default, validate):
        value = self.params.pop(name, _unset)

        if value is _unset:
            if default is not _mandatory:
                return default
            abort(400, 'Missing parameter %s' % (name, ))

        if validate:
            try:
                validate(value)
            except TypeError as e:
                abort(400, 'Invalid parameter type: %s: %s' % (name, str(e)))
            except ValueError as e:
                abort(400, 'Invalid parameter value: %s: %s' % (name, str(e)))
        return value

    def get_list(self, name, default, validate, maxlen):
        def _(v):
            if not isinstance(v, list):
                raise TypeError('expect list')
            if maxlen is not None and len(v) > maxlen:
                raise ValueError('list too long')
            if validate:
                for e in v:
                    validate(e)
        return self.get(name, default, _)

    def any(self, name, default = _mandatory, validate = None):
        return self.get(name, default, validate)

    def string(self, name, default = _mandatory, choice = None, validate = None):
        def _(v):
            if not isinstance(v, str):
                raise TypeError('expect string')
            if choice is not None and v not in choice:
                raise ValueError('not in set of possible values')
            if validate:
                validate(v)
        return self.get(name, default, _)

    def binary(self, name, default = _mandatory, maxlen = None, validate = None):
        def _(v):
            if not isinstance(v, str):
                raise TypeError('expect base64 string')
            if maxlen is not None and len(v) > maxlen * 4:
                raise ValueError('too long')
        v = self.get(name, default, _)
        try:
            v = base64.b64decode(v)
        except:
            raise ValueError('not properly base64-encoded')
        if maxlen is not None and len(v) > maxlen:
            raise ValueError('too long')
        if validate:
            validate(v)
        return v

    def integer(self, name, default = _mandatory, min = None, max = None):
        def _(v):
            if not isinstance(v, int):
                raise TypeError('expect integer')
            if min is not None and v < min:
                raise ValueError('too small')
            if max is not None and v > max:
                raise ValueError('too large')
        return self.get(name, default, _)

    def float(self, name, default = _mandatory, min = None, max = None):
        def _(v):
            if not isinstance(v, float):
                raise TypeError('expect float')
            if min is not None and v < min:
                raise ValueError('too small')
            if max is not None and v > max:
                raise ValueError('too large')
        return self.get(name, default, _)

    def boolean(self, name, default = _mandatory):
        def _(v):
            if not isinstance(v, bool):
                raise TypeError('expect boolean')
        return self.get(name, default, _)

    def string_list(self, name, default = _mandatory, maxlen = None, choice = None, validate =
 None):
        def _(v):
            if not isinstance(v, str):
                raise TypeError('expect list of strings')
            if choice is not None and v not in choice:
                raise ValueError('not in set of possible values')
            if validate:
                validate(v)
        return self.get_list(name, default, _, maxlen)

    def integer_list(self, name, default = _mandatory, maxlen = None):
        def _(v):
            if not isinstance(v, int):
                raise TypeError('expect list of integers')
        return self.get_list(name, default, _, maxlen)

    def any_list(self, name, default = _mandatory, validate = None, maxlen = None):
        return self.get_list(name, default, validate, maxlen)

    def timestamp(self, name, default = _mandatory, min = 0, max = None):
        if max is None:
            max = int(time.time()) + 3600 * 24 * 365
        return self.integer(name, default, min = min, max = max)

    def email(self, name, default = _mandatory):
        v = self.string(name, default)
        if v is not None:
            # XXX validate email?
            return v.strip().lower()

def _request_json(request):
    try:
        return request.json
    except ValueError:
        abort(400, 'Invalid JSON content')

def params(request = None, data = None):
    if data is None:
        if request is None:
            request = bottle.request
        data = _request_json(request) or {}
    return Parameters(data)

def no_params(request = None):
    if request is None:
        request = bottle.request
    if _request_json(request):
        abort(400, 'No parameter expected')

def _fmt_time(timestamp = None):
    if timestamp is None:
        timestamp = time.time()
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(timestamp))

def _make_etag(*parts):
    hash = hashlib.sha1()
    for part in parts:
        hash.update(str(part).encode('utf-8'))
    return hash.hexdigest()


def response_ok(status = 204):
    response = bottle.HTTPResponse(status = status)
    return response

def response_json(value):
    response = bottle.HTTPResponse()
    response.set_header('Content-Type', 'application/json')
    response.body = json.dumps(value)
    return response


class ResourceView:

    def __init__(self, body, size, mtime, ctype = None, etag = None):
        self.body = body
        self.ctype = ctype if ctype is not None else 'application/octet-stream'
        self.size = size
        self.mtime = mtime
        self.etag = etag


def response_view(view, request = None):
    if request is None:
        request = bottle.request

    def _parse_range():
        value = request.environ.get('HTTP_RANGE', '')
        if not value.startswith("bytes="):
            return None

        for rng in value.split("=", 1)[1].split(","):
            if '-' not in rng:
                continue
            offset, end = rng.split('-', 1)
            if (offset, end) == ('', ''):
                continue
            if not offset:
                offset, end = max(0, view.size - int(end) + 1), view.size
            elif not end:
                offset, end = int(offset), view.size
            else:
                offset, end = int(offset), int(end) + 1
            if 0 <= offset < end <= view.size:
                return offset, end

        return None

    def _modified():
        return True

    def _read(fp, count, bufsize = 1024 * 1024):
        while count:
            data = fp.read(min(count, bufsize))
            if not data:
                break
            yield data
            count -= len(data)

    def _iter_range(body, offset, count, logger):
        try:
            if (offset):
                if body.seekable():
                    body.seek(offset, 1)
                else:
                    for _ in _read(body, offset):
                        pass
            for chunk in _read(body, count):
                yield chunk
        except GeneratorExit:
            # interrupted transfer
            pass
        except:
            _logger(logger).exception("EXCEPTION")
            raise
        finally:
            body.close()

    range = _parse_range()

    response = bottle.HTTPResponse()
    response.set_header("Accept-Ranges", "bytes")
    response.set_header("Content-Type", view.ctype)
    if isinstance(view.mtime, str):
        response.set_header("Last-Modified", view.mtime)
    else:
        response.set_header("Last-Modified", _fmt_time(view.mtime))
    if view.etag is not None:
        # XXX not if Range?
        response.set_header("ETag", view.etag)

    if request.method == "HEAD":
        response.set_header("Content-Length", view.size)
        view.body.close()
    elif not _modified():
        response.set_header("Content-Length", 0)
        response.status = "304 Not modified"
        view.body.close()
    elif range:
        offset, end = range
        response.set_header("Content-Length", end - offset)
        response.set_header("Content-Range",  "bytes %d-%d/%d" % (offset, end - 1, view.size))
        response.status = "206 Partial Content"
        response.body = _iter_range(view.body, offset, end - offset, None)
    else:
        response.set_header("Content-Length", view.size)
        response.body = view.body

    return response


def response_file(path, ctype = None, etag = None):
    fp = open(path, "rb")
    stat = os.fstat(fp.fileno())
    if etag is None:
        etag = _make_etag(path, stat.st_size, stat.st_mtime)
    if ctype is None:
        ctype = guess_content_type(path)
    view = ResourceView(fp,
                        stat.st_size,
                        stat.st_mtime,
                        ctype = ctype,
                        etag = etag)
    return response_view(view)


def response_content(fp):
    headers = { key: val for key, val in fp.info.headers }
    view = ResourceView(fp,
                        fp.info.size,
                        fp.info.timestamp,
                        ctype = headers.get("Content-Type"),
                        etag = headers.get('ETag'))
    return response_view(view)


def response_request(req):
    response = bottle.HTTPResponse()
    response.status = "%d %s" % (req.status_code, req.reason)
    for key, value in req.headers.items():
        if key not in ('Connection', ):
            response.set_header(key, value)
    response.body = req.raw
    return response


DEFAULT_TYPE = {
    'mp3': 'audio/mpeg',
    'mp4': 'video/mp4',
    'aac': 'audio/mp4',
    'webm': 'video/webm',
    'oga': 'audio/ogg',
    'ogg': 'audio/ogg',
    'ogv': 'video/ogg',
    'css': 'text/css',
    'gif': 'image/gif',
    'html': 'text/html',
    'js': 'application/javascript',
    'json': 'application/json',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'otf': 'application/vnd.ms-opentype',
    'pdf': 'application/pdf',
    'png': 'image/png',
    'svg': 'image/svg+xml',
    'ttf': 'application/x-font-ttf',
    'txt': 'text/plain',
    'woff': 'application/font-woff',
    'woff2': 'application/font-woff2',
    'xhtml': 'application/xhtml+xml',
}

def guess_content_type(filename, default = None):
    ext = filename.split('.')[-1].lower()
    return DEFAULT_TYPE.get(ext, default)
