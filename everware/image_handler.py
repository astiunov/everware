from tornado import gen
from tornado.locks import Event


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class ImageHandler():

    def __init__(self):
        self._images = {}

    @gen.coroutine
    def start_building(self, image_name):
        if image_name in self._images:
            yield self._images[image_name].wait()
        else:
            self._images[image_name] = Event()

    def finish_building(self, image_name):
        if image_name not in self._images:
            raise NameError('%s not found' % image_name)
        self._images[image_name].set()
