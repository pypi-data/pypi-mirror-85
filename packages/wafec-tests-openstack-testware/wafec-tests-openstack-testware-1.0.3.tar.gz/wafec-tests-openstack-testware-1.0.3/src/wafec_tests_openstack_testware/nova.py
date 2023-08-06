from novaclient import client

from .base import DriverBase, StateBase, ObserverBase, WaitState
from .exceptions import NotFoundException, StateMismatchException
from .types import Undefined

_DEFAULT_VERSION = '2.1'
_UNDEFINED = Undefined()


class NovaDriver(DriverBase):
    def __init__(self, session, glance_driver, neutron_driver, version=_DEFAULT_VERSION):
        DriverBase.__init__(self)
        self.session = session
        self.version = version
        self.client = client.Client(version=self.version, session=self.session)
        self.glance_driver = glance_driver
        self.neutron_driver = neutron_driver

    def server_create(self, server_name, flavor_name, image_name, network_name):
        image = self.glance_driver.image_get(image_name)
        flavor = self.flavor_get(flavor_name)
        network = self.neutron_driver.network_get(network_name)
        server = self.client.servers.create(
            name=server_name,
            image=image.id,
            flavor=flavor.id,
            nics=[{'net-id': network['id']}]
        )
        return server

    def server_get(self, server_name):
        servers = self.client.servers.list(search_opts={'name': server_name})
        servers = list(servers)
        if servers:
            server = servers[0]
            return server
        else:
            raise NotFoundException()

    def server_list(self, name=None):
        search_opts = {}
        if name:
            search_opts['name'] = name
        servers = self.client.servers.list(search_opts=search_opts)
        servers = list(servers)
        return servers

    def server_delete(self, server_name):
        server = self.server_get(server_name)
        server.delete()

    def flavor_get(self, flavor_name):
        flavors = self.client.flavors.list()
        flavors = list(flavors)
        flavors = [flavor for flavor in flavors if flavor.name == flavor_name]
        if flavors:
            flavor = flavors[0]
            return flavor
        else:
            raise NotFoundException()

    def server_pause(self, server_name):
        server = self.server_get(server_name)
        server.pause()
        return server

    def server_unpause(self, server_name):
        server = self.server_get(server_name)
        server.unpause()
        return server

    def server_suspend(self, server_name):
        server = self.server_get(server_name)
        server.suspend()
        return server

    def server_resume(self, server_name):
        server = self.server_get(server_name)
        server.resume()
        return server

    def server_shelve(self, server_name):
        server = self.server_get(server_name)
        server.shelve()
        return server

    def server_unshelve(self, server_name):
        server = self.server_get(server_name)
        server.unshelve()
        return server

    def server_stop(self, server_name):
        server = self.server_get(server_name)
        server.stop()
        return server

    def server_start(self, server_name):
        server = self.server_get(server_name)
        server.start()
        return server

    def server_rebuild(self, server_name, image_name):
        image = self.glance_driver.image_get(image_name)
        server = self.server_get(server_name)
        server.rebuild(image)
        return server

    def server_resize(self, server_name, flavor_name):
        flavor = self.flavor_get(flavor_name)
        server = self.server_get(server_name)
        server.resize(flavor)
        return server

    def server_confirm_resize(self, server_name):
        server = self.server_get(server_name)
        server.confirm_resize()
        return server

    def server_revert_resize(self, server_name):
        server = self.server_get(server_name)
        server.revert_resize()
        return server


class ServerState(StateBase):
    def __init__(self):
        StateBase.__init__(self)
        self.status = None
        self.task_state = None
        self.vm_state = None
        self.power_state = None
        self.image_id = None
        self.flavor_id = None

    @property
    def state_props(self):
        return ['status', 'task_state', 'vm_state', 'power_state', 'image_id', 'flavor_id']

    def __repr__(self):
        return f'<ServerState(status={self.status}, task_state={self.task_state}, ' \
               f'vm_state={self.vm_state}, power_state={self.power_state}, image_id={self.image_id}, ' \
               f'flavor_id={self.flavor_id})> '

    @staticmethod
    def of(status, task_state=_UNDEFINED, vm_state=_UNDEFINED, power_state=_UNDEFINED, image_id=_UNDEFINED,
           flavor_id=_UNDEFINED):
        inst = ServerState()
        inst.status = status
        inst.task_state = task_state
        inst.vm_state = vm_state
        inst.power_state = power_state
        inst.image_id = image_id
        inst.flavor_id = flavor_id
        return inst

    @staticmethod
    def from_server(server):
        if server is None:
            raise ValueError('server is None')
        return ServerState.of(
            server.status,
            getattr(server, 'OS-EXT-STS:task_state'),
            getattr(server, 'OS-EXT-STS:vm_state'),
            getattr(server, 'OS-EXT-STS:power_state'),
            server.image['id'],
            server.flavor['id']
        )


class NovaObserver(ObserverBase):
    _DEFAULT_TIMEOUT = 60

    def __init__(self, nova_driver):
        ObserverBase.__init__(self)
        self.nova_driver = nova_driver

    def server_observe(self, server_name, states, timeout=_DEFAULT_TIMEOUT):
        states_index = 0
        state = None
        server_state = None
        if not states:
            raise ValueError('states is empty')

        def supplier():
            server = self.nova_driver.server_get(server_name)
            return server

        def condition(server):
            nonlocal states_index, state, server_state
            state = states[states_index]
            server_state = ServerState.from_server(server)
            if server_state.compare_with(state):
                states_index += 1
            if states_index >= len(states):
                return True
            return False

        result = WaitState.wait_while(condition, supplier, timeout)
        if not result:
            raise StateMismatchException(f'{server_state} != {state}')
        return result
