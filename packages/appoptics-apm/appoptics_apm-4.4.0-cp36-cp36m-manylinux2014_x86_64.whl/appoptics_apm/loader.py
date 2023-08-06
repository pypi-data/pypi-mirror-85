""" AppOptics APM instrumentation loader

Checks appoptics_apm.config['inst_enabled'] and imports as requested. used by middleware
and djangoware.

Copyright (C) 2016 by SolarWinds, LLC.
All rights reserved.
"""
from appoptics_apm import config


def _enabled(m):
    return config['inst_enabled'][m]


def load_inst_modules():
    # TODO_Pylint: Check if disabling warnings here is good
    # pylint: disable-msg=W0611
    if _enabled('memcache'):
        from appoptics_apm import inst_memcache
    if _enabled('pymongo'):
        from appoptics_apm import inst_pymongo
    if _enabled('sqlalchemy'):
        from appoptics_apm import inst_sqlalchemy
    if _enabled('httplib'):
        from appoptics_apm import inst_httplib
    if _enabled('redis'):
        from appoptics_apm import inst_redis
    # additionally, in djangoware.py: 'django_orm', 'django_templates'
