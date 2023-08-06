from glanceclient import client

from .base import DriverBase
from .exceptions import NotFoundException

_DEFAULT_VERSION = '2'


class GlanceDriver(DriverBase):
    def __init__(self, session, version=_DEFAULT_VERSION):
        DriverBase.__init__(self)
        self.session = session
        self.version = version
        self.client = client.Client(self.version, session=self.session)

    def image_get(self, image_name):
        images = self.client.images.list(filters={'name': image_name})
        images = list(images)
        if images:
            image = images[0]
            return image
        else:
            raise NotFoundException()
