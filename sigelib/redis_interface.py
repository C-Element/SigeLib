# Copyright (C) 2015 Clemente Junior
#
# This file is part of SigeLib
#
# SigeLib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.


import pickle
from datetime import timedelta
from uuid import uuid4

from redis import Redis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin

PORT = 6669


class RedisData(object):
    """
    Class to manipulate data into Redis Server.
    """
    def __init__(self, connection_pool=None):
        if connection_pool:
            self.redis = Redis(connection_pool=connection_pool)
        else:
            self.redis = Redis(port=PORT)

    def delete(self, key, prefix='SigeCore:'):
        """
        Delete key from Redis Server
        """
        self.redis.delete(prefix + key)

    def delete_all(self, key_part, prefix='SigeCore:'):
        """
        Delete all keys starting with key from Redis Server.
        """
        for key in self.get_all(key_part, prefix):
            self.redis.delete(key)

    def get(self, key, prefix='SigeCore:'):
        """
        Get value of key from Redis Server
        """
        to_return = value = self.redis.get(prefix + key)
        if value is not None:
            to_return = pickle.loads(value)
        return to_return

    def get_all(self, key_part, prefix='SigeCore:'):
        """
        Get all values from Redis Server where this key starts with key.
        """
        to_return = {}
        for entry in self.redis.keys():
            this_key = entry.decode()
            if this_key.startswith(prefix + key_part):
                to_return[this_key] = pickle.loads(self.redis.get(entry))
        return to_return

    def set(self, key, value, prefix='SigeCore:', expire=timedelta(hours=23)):
        """
        Get this key-values into Redis Server.
        """
        value = pickle.dumps(value)
        self.redis.setex(prefix + key, value, expire)


class RedisSession(CallbackDict, SessionMixin):
    """
    Redis session to Flask Server.
    :param initial:
    :param sid:
    :param new:
    """

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


def generate_sid():
    """
    Generate the session id.
    """
    return str(uuid4())


def get_redis_expiration_time(app, session):
    """
    Generate the session id.
    """
    if session.permanent:
        return app.permanent_session_lifetime
    return timedelta(days=1)


class RedisSessionInterface(SessionInterface):
    """
    Redis Session interface to Flask Server.
    """

    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session_SigeWeb:'):
        if redis is None:
            redis = Redis(port=PORT)
        self.redis = redis
        self.prefix = prefix

    def open_session(self, app, request):
        """
        Get session from Redis Server
        :param app:
        :param request:
        :return:
        """
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        """
        Save session into Redis Server
        :param app:
        :param session:
        :param response:
        :return:
        """
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
                         int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)
