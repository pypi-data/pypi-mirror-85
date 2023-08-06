from neutronclient.v2_0 import client

from .base import DriverBase
from .exceptions import NotFoundException


class NeutronDriver(DriverBase):
    def __init__(self, session):
        DriverBase.__init__(self)
        self.session = session
        self.client = client.Client(session=self.session)

    def network_get(self, network_name):
        networks = self.client.list_networks(name=network_name)
        if networks and networks['networks']:
            networks = networks['networks']
            network = networks[0]
            return network
        else:
            raise NotFoundException()
