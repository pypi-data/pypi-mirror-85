import logging
import threading
import time

import redis


class Publisher(object):
    _instance_lock = threading.Lock()

    def __init__(self,
                 name='robot_reids_pub',
                 host='127.0.0.1',
                 port='6379',
                 db=3,
                 health_check_interval=1):
        self.name = name
        self.db = db
        self.pool = redis.ConnectionPool(host=host, port=port)
        logging.debug('create a redis pool at {}:{} for publisher {}'.format(
            host, port, name))

    def __new__(cls, *args, **kwargs):
        if not hasattr(Publisher, '_instance'):
            with Publisher._instance_lock:
                if not hasattr(Publisher, '_instance'):
                    Publisher._instance = object.__new__(cls)
        return Publisher._instance

    def get_connection(self):
        return redis.StrictRedis(connection_pool=self.pool,
                                 db=self.db,
                                 socket_connect_timeout=4,
                                 retry_on_timeout=True,
                                 socket_timeout=4)

    def send(self, topic, dpack):
        rc = Publisher._instance.get_connection()
        name = Publisher._instance.name
        rc.publish(topic, dpack)

        logging.debug('Redis server {}\'s top {} publish a data at {}.'.format(
            name, topic, time.time()))
