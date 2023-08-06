""" AppOptics APM instrumentation for SQLAlchemy.

 Copyright (C) 2016 by SolarWinds, LLC.
 All rights reserved.
"""
import logging

from appoptics_apm import config, util

logger = logging.getLogger(__name__)


def main():
    dialect_wrappers = {
        'do_commit': do_commit_cb,
        'do_rollback': do_rollback_cb,
    }

    module_class_mappings = (
        (
            'sqlalchemy.engine.default',
            'DefaultDialect',
            {
                'do_commit': do_commit_cb,
                'do_execute': do_execute_cb,
                'do_executemany': do_execute_cb,
                'do_rollback': do_rollback_cb
            },
        ),
        (
            'sqlalchemy.dialects.mysql.base',
            'MySQLDialect',
            dialect_wrappers,
        ),
        (
            'sqlalchemy.dialects.postgresql.base',
            'PGDialect',
            dialect_wrappers,
        ),
    )

    for mod, classname, mappings in module_class_mappings:
        try:
            cls = getattr(__import__(mod, fromlist=[classname]), classname)
        except (AttributeError, ImportError):
            pass
        else:
            wrap_methods(cls, mappings)


def wrap_methods(cls, mappings):
    for name, fn in mappings.items():
        try:
            base_method = getattr(cls, name)
        except AttributeError:
            logger.error('Failed to patch %s on %s', name, cls.__name__)
        else:
            appoptics_apm_fn = util.log_method(
                'sqlalchemy', store_backtrace=util._collect_backtraces('sqlalchemy'), callback=fn)(base_method)
            setattr(cls, name, appoptics_apm_fn)


def do_commit_cb(_f, args, _kwargs, _ret):
    self, conn = args[:2]
    return base_info(self.name, conn, 'COMMIT')


def do_execute_cb(_f, args, _kwargs, _ret):
    self, cursor, stmt, params = args[:4]
    info = base_info(self.name, cursor.connection, stmt)
    if not config.get('enable_sanitize_sql', True):
        info['QueryArgs'] = str(params)
    return info


def do_rollback_cb(_f, args, _kwargs, _ret):
    self, conn = args[:2]
    return base_info(self.name, conn, 'ROLLBACK')


def base_info(flavor_name, conn, query):
    # This could be a real connection object, or a connection fairy (proxy)
    conn = getattr(conn, 'connection', conn)
    info = {
        'Flavor': flavor_name,
        'Query': query,
    }
    try:
        info['RemoteHost'] = remotehost_from_connection(flavor_name, conn)
    except Exception:
        pass
    return info


def remotehost_from_connection(flavor_name, conn):
    if flavor_name == 'mysql':
        host_info = conn.get_host_info()

        # "127.0.0.1 via TCP/IP" (MySQLdb)
        if host_info.endswith('TCP/IP'):
            return host_info.split()[0].lower()

        # "socket 127.0.0.1:3306" (pymysql)
        if host_info.startswith('socket'):
            return host_info.split()[1].split(':')[0]

    if flavor_name == 'postgresql':
        host_part = [part for part in conn.dsn.split() if part.startswith('host=')]
        if host_part:
            return host_part[0].split('=')[1]
    return None


if util.ready():
    main()
