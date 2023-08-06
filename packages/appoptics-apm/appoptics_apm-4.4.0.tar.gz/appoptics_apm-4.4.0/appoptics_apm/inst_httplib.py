""" AppOptics APM instrumentation for requests.

Instrumentation is done in urllib3.

Copyright (C) 2016 by SolarWinds, LLC.
All rights reserved.
"""
import logging

import appoptics_apm.util as util

logger = logging.getLogger(__name__)

HTTPLIB_LAYER = 'httplib'


def safeindex(_list, index):
    return _list[index] if len(_list) > index else None


def safeget(obj, key):
    return obj.get(key, None) if obj and hasattr(obj, 'get') else None


def wrap_request_putrequest(func, f_args, f_kwargs):
    self = safeindex(f_args, 0)
    if self:
        self.__appoptics_apm_path = safeindex(f_args, 2) or safeget(f_kwargs, 'url')
    return f_args, f_kwargs, {}


def wrap_request_endheaders(func, f_args, f_kwargs):
    if len(f_args) >= 1:
        self = f_args[0]
        self.putheader('X-Trace', util.last_id())
    return f_args, f_kwargs, {}


def wrap_request_getresponse(func, f_args, f_kwargs, res):
    kvs = {
        'IsService': 'yes',
        'RemoteProtocol': 'http',
    }
    self = safeindex(f_args, 0)
    if self:
        kvs['RemoteHost'] = "%s:%s" % (getattr(self, 'host', ''), getattr(self, 'port', '80'))
        if hasattr(self, '__appoptics_apm_path'):
            kvs['ServiceArg'] = getattr(self, '__appoptics_apm_path') or '/'
            delattr(self, '__appoptics_apm_path')
    if hasattr(res, 'status'):
        kvs['HTTPStatus'] = getattr(res, 'status')
    edge_str = res.getheader('x-trace') if res and hasattr(res, 'getheader') else None
    return kvs, edge_str


def wrap(module):
    try:
        # Wrap putrequest.  This marks the beginning of the request, and is also
        # where
        wrapper_putrequest = util.log_method(
            HTTPLIB_LAYER,
            before_callback=wrap_request_putrequest,
            send_exit_event=False,
            store_backtrace=util._collect_backtraces('httplib'))
        setattr(module.HTTPConnection, 'putrequest', wrapper_putrequest(module.HTTPConnection.putrequest))

        wrapper_endheaders = util.log_method(
            HTTPLIB_LAYER,
            before_callback=wrap_request_endheaders,
            send_entry_event=False,
            send_exit_event=False,
            except_send_exit_event=True)
        setattr(module.HTTPConnection, 'endheaders', wrapper_endheaders(module.HTTPConnection.endheaders))

        wrapper_getresponse = util.log_method(HTTPLIB_LAYER, callback=wrap_request_getresponse, send_entry_event=False)
        setattr(module.HTTPConnection, 'getresponse', wrapper_getresponse(module.HTTPConnection.getresponse))
    except Exception as e:
        logger.error("AppOptics APM error: %s" % str(e))


if util.ready():
    try:
        import httplib
        wrap(httplib)
    except ImportError:
        import http.client
        wrap(http.client)
