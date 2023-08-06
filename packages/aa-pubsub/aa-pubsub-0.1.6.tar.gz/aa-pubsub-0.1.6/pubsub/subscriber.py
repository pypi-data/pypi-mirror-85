import logging
import threading
import time

import redis

gitem = None


def skip_frame(callback):
    global gitem
    while 1:
        if callback and gitem is not None:
            callback(gitem['data'], 'robot_reids_sub', '', time.time())


class Subscriber(object):
    _instance_lock = threading.Lock()

    def __init__(self,
                 name='robot_reids_sub',
                 host='127.0.0.1',
                 port='6379',
                 db=3,
                 health_check_interval=1):
        self.name = name
        self.host, self.port = host, port
        self.db, self.health_check_interval = db, health_check_interval
        self.pool = redis.ConnectionPool(host=host, port=port, db=self.db)
        logging.debug('create a redis pool at {}:{} for subscriber {}'.format(
            host, port, name))

    def __new__(cls, *args, **kwargs):
        if not hasattr(Subscriber, '_instance'):
            with Subscriber._instance_lock:
                if not hasattr(Subscriber, '_instance'):
                    Subscriber._instance = object.__new__(cls)
        return Subscriber._instance

    def get_connection(self):
        return redis.StrictRedis(connection_pool=self.pool,
                                 db=self.db,
                                 socket_connect_timeout=4,
                                 retry_on_timeout=True,
                                 socket_timeout=4)

    def recv(self, topic, callback=None):
        global gitem
        t = threading.Thread(target=skip_frame, args=[
            callback,
        ])
        t.start()
        rc = Subscriber._instance.get_connection()
        name = Subscriber._instance.name
        ps = rc.pubsub()
        ps.subscribe(topic)
        try:
            for item in ps.listen():
                gitem = item
                logging.debug(
                    'Redis server {}\'s top {} subscribe a data at {}.'.format(
                        name, topic, time.time()))
        except redis.exceptions.ConnectionError:
            logging.error('connect close by server, retry...')
            host, port = \
                Subscriber._instance.host, Subscriber._instance.port
            Subscriber._instance.rc = Subscriber._instance.get_connection()
            logging.error('reconnect at {}:{}'.format(host, port))
            self.recv(topic, callback=callback)
