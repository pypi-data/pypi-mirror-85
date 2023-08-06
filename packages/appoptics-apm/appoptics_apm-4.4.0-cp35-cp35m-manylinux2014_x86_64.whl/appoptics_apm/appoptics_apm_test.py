#_*_ coding: utf-8 _*_
""" AppOptics APM instrumentation API for Python.

Copyright (C) 2016 by SolarWinds, LLC.
All rights reserved.

appoptics_apm_test defines test mock classes for:
a) running unit test
"""
import pprint
import random
import socket
import string

import appoptics_apm

# objects pickle unpickle with HAC(hash authentication)
try:
    import cPickle as pickle
except ImportError:
    import pickle

# global set of registered event reporting listeners
listeners = []


class Metadata(object):
    def __init__(self, flag=None):
        if flag:
            int_randomer = random.Random()
            id_list = [string.hexdigits[int_randomer.randint(0, len(string.hexdigits) - 1)] for _ in range(56)]
            self.id = "2B" + ''.join(id_list).upper() + '01'
        else:
            self.id = ''

    @staticmethod
    def fromString(strv):
        md = Metadata()
        md.id = strv
        return md

    def createEvent(self):
        return Event()

    @staticmethod
    def makeRandom(flag=True):
        return Metadata(flag)

    def copy(self):
        return self

    def isValid(self):
        return True

    def isSampled(self):
        return True

    def toString(self):
        return self.id


class Context(object):
    md = None

    @staticmethod
    def setTracingMode(_):
        return False

    @staticmethod
    def setDefaultSampleRate(_):
        return False

    @staticmethod
    def getDecisions(*args, **kwargs):
        """
        This is the stub method in test mode. The corresponding method in the
        `normal` mode (when the instrumentation is working) is actually a wrapper
        of the `getDecisions` method of the Context class in swig/oboe.hpp.

        There are multiple return values in this method, which are:
        do_metrics, do_sample, sample_rate, sample_source, typ, auth, status_msg, auth_msg, status

        Go to oboe.hpp to see the descriptions of all the return values.
        """
        return 1, 1, 1000000, 6, 0, -1, "ok", "", 0

    @classmethod
    def get(cls):
        return cls.md

    @classmethod
    def set(cls, md):
        cls.md = md

    @staticmethod
    def fromString(_):
        return Context()

    @staticmethod
    def copy():
        return Context()

    @classmethod
    def clear(cls):
        cls.md = None

    @classmethod
    def isValid(cls):
        return cls.md is not None

    @classmethod
    def isSampled(cls):
        return cls.md is not None

    @staticmethod
    def toString():
        return str(Context.md.id) if Context.md else ''

    @staticmethod
    def createEvent():
        return Event()

    @staticmethod
    def startTrace(_=None):
        return Event()


class Event(object):
    def __init__(self, _=None, __=None):
        ''' initialize event. Props for checking properties,
            evt for compatible with oboe SwigEvent. Otherwise
            complaints come from _reporter().sendReport(event.evt)
            etc.
        '''
        self.props = {}
        self.evt = self

    def addInfo(self, name, value):
        self.props[name] = value

    def addEdge(self, _):
        pass

    def addEdgeStr(self, _):
        pass

    def getMetadata(self):
        return Metadata()

    def metadataString(self):
        return ''

    def is_valid(self):
        return True

    @staticmethod
    def startTrace(_=None):
        return Event()

    def __repr__(self):
        return '<Event(' + str(self.props) + ')>'


# Agent reporter_instance is initialized the first time it is used
# By design, it uses polymorphism to initialize corresponding reporter
# instance for oboe. For python, it should use factory or like this
# use proxy to address that
class Reporter(object):
    """ Mock the Reporter; no-op for unsupported platforms, or unit test harness
        if in APPOPTICS_TEST mode. """
    def __init__(self, *args, **kwargs):
        """ initialize a udp reporter and helper functions for
            network data processing if it's configured appropriately.
            The arguments are extracted from `kwargs`.
        :param reporter: the reporter type, normally it's `udp` for testing.
        :param host: the collector address in the format of `host:port`.
        """
        reporter_type = kwargs.get("reporter", "udp")
        if reporter_type == "udp":
            try:
                host_str = kwargs.get("host")
                host, port = host_str.split(":")[0], int(host_str.split(":")[1])
                self.proxy = UdpReporter((host, port))
            except Exception:
                self.proxy = None
        else:
            self.proxy = None

        self.init_status = 0

    def sendReport(self, event, __=None):
        if self.proxy:
            self.proxy.sendReport(event)
            return
        for listener in listeners:
            listener.send(event)

    def sendStatus(self, event, __=None):
        if self.proxy:
            self.proxy.sendStatus(event)
            return
        for listener in listeners:
            listener.send(event)

    def sendSpan(self, event, __=None):
        if self.proxy:
            self.proxy.sendSpan(event)
            return
        for listener in listeners:
            listener.send(event)


class UdpReporter(object):
    """ Reporter for no-op for unsupported platforms, or unit test harness
        if in APPOPTICS_TEST mode. """
    def __init__(self, server_tuple=('localhost', 7835), timeout=30):
        ''' initialize a upd reporter and helper functions for
        network data processing
        :param server_tuple:tuple, server address and port, default 7835 is defined
               in net_utils.py
        :param timeout:int timeout for reading data
        '''
        self.listener = (server_tuple[0], server_tuple[1])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(timeout)

    def _pickle_message(self, obj):
        '''encode an object for network transfer'''
        return pickle.dumps(obj)

    def sendReport(self, event, __=None):
        self.socket.sendto(self._pickle_message(event), self.listener)

    def sendStatus(self, event, __=None):
        self.socket.sendto(self._pickle_message(event), self.listener)

    def sendSpan(self, event, __=None):
        self.socket.sendto(self._pickle_message(event), self.listener)


class Span(object):
    @staticmethod
    def createHttpSpan(*args):
        # util._reporter() guarantees reporter instance
        reporter = appoptics_apm.util._reporter()
        if reporter:
            reporter.sendSpan({'SPAN_REPORT': args})

    @staticmethod
    def createSpan(*args):
        # util._reporter() guarantees reporter instance
        reporter = appoptics_apm.util._reporter()
        if reporter:
            reporter.sendSpan({'SPAN_REPORT': args})


class MetricTags(object):
    @staticmethod
    def add(*args, **kwargs):
        pass


class CustomMetrics(object):
    @staticmethod
    def summary(*args, **kwargs):
        pass

    @staticmethod
    def increment(*args, **kwargs):
        pass


class AppOpticsApmListener(object):
    """ Simple test harness for intercepting event reports. """
    def __init__(self):
        self.events = []
        self.spans = []
        self.listeners = listeners
        listeners.append(self)

    def send(self, event):
        if isinstance(event, Event):
            self.events.append(event)
        else:
            self.spans.append(event)

    def get_events(self, *filters):
        """ Returns all events matching the filters passed """
        events = self.events
        for _filter in filters:
            events = [ev for ev in events if _filter(ev)]
        return events

    def get_spans(self, *filters):
        """ Returns all spans matching the filters passed """
        spans = self.spans
        for _filter in filters:
            spans = [sp for sp in spans if _filter(sp)]
        return spans

    def str_events(self, *filters):
        return pprint.pformat(self.get_events(*filters))

    def str_spans(self, *filters):
        return pprint.pformat(self.get_spans(*filters))

    def pop_events(self, *filters):
        """ Returns all events matching the filters passed,
        and also removes those events from the Trace so that
        they will not be returned by future calls to
        pop_events or events. """
        matched = self.get_events(*filters)
        for match in matched:
            self.events.remove(match)
        return matched

    def pop_spans(self, *filters):
        """ Returns all spans matching the filters passed,
        and also removes those spans from the Trace so that
        they will not be returned by future calls to
        pop_spans or spans. """
        matched = self.get_spans(*filters)
        for match in matched:
            self.spans.remove(match)
        return matched

    def __del__(self):
        self.listeners.remove(self)


# add a default listener to collect init messages
initListener = AppOpticsApmListener()
