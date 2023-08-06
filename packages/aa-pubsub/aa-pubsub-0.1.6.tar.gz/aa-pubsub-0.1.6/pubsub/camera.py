import logging
import struct
import time

import cv2
import numpy as np

from pubsub.publisher import Publisher
from pubsub.subscriber import Subscriber


def packImage(img, timestamp=None):
    h, w = img.shape[:2]
    shape = struct.pack('>II', h, w)
    img_time = struct.pack('>d', timestamp or time.time())
    encoded = shape + img_time + img.tobytes()
    return encoded


def unpackImage(encoded):
    h, w = struct.unpack('>II', encoded[:8])
    img_time = struct.unpack('>d', encoded[8:16])
    img = np.frombuffer(encoded, dtype=np.uint8, offset=16).reshape(h, w, 3)
    return img, img_time[0]


class CameraPub(object):
    def __init__(self,
                 pipe=0,
                 name='robot_mono',
                 host='127.0.0.1',
                 port='6379',
                 db=3):
        self.cap = cv2.VideoCapture(pipe)  # video capture object
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        w = int(self.cap.get(3))
        h = int(self.cap.get(4))
        logging.debug('camera param: fps {}, weight {}, height {}'.format(fps, w, h))
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)  # set buffer size
        self.pub = Publisher(name='{}_pub'.format(name),
                             host=host,
                             port=port,
                             db=db)

    def publish(self, topic='robot_mono', flip=2):
        while self.cap.isOpened():
            ret_val, img = self.cap.read()
            timestamp = time.time()
            pdata = packImage(img, timestamp)
            self.pub.send(topic, pdata)
        self.cap.release()


class CameraSub(object):
    def __init__(self,
                 pipe=0,
                 name='robot_mono',
                 host='127.0.0.1',
                 port='6379',
                 db=3):
        self.sub = Subscriber(name='{}_sub'.format(name),
                              host=host,
                              port=port,
                              db=db)

    def subscribe(self, topic='robot_mono', callback=None):
        self.sub.recv(topic, callback or self.process)

    def process(self, pdata, *arg):
        if 1 == pdata:
            logging.debug('not a stable connection, pass that message')
        else:
            img, _ = unpackImage(pdata)
            # do what you want in your own process
            cv2.imshow('process', img)
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
