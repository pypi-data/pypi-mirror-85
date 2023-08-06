import unittest

from .logon import session_build
from .nova import NovaDriver, NovaObserver, ServerState
from .glance import GlanceDriver
from .neutron import NeutronDriver
from .types import Undefined

_DEFAULT_FLAVOR = 'cirros256'
_DEFAULT_IMAGE = 'cirros-0.4.0-x86_64-disk'
_DEFAULT_NETWORK = 'private'
_DEFAULT_FLAVOR_ALT = 'm1.tiny'


class NovaTests(unittest.TestCase):
    def setUp(self):
        self.created_images = []
        self.created_flavors = []
        self.created_servers = []
        self.session = session_build(
            'http://192.168.56.61/identity/',
            'admin',
            'supersecret',
            'admin',
            'Default',
            'Default'
        )
        self.glance_driver = GlanceDriver(session=self.session)
        self.neutron_driver = NeutronDriver(session=self.session)
        self.nova_driver = NovaDriver(session=self.session, glance_driver=self.glance_driver,
                                      neutron_driver=self.neutron_driver)
        self.nova_observer = NovaObserver(nova_driver=self.nova_driver)
        self.image_default = self.glance_driver.image_get(_DEFAULT_IMAGE)
        self.flavor_default = self.nova_driver.flavor_get(_DEFAULT_FLAVOR)
        self.flavor_default_alt = self.nova_driver.flavor_get(_DEFAULT_FLAVOR_ALT)

    def _server_create(self, server_name):
        server = self.nova_driver.server_create(server_name, _DEFAULT_FLAVOR, _DEFAULT_IMAGE, _DEFAULT_NETWORK)
        self.created_servers.append(server)
        result = self.nova_observer.server_observe(server_name, [
            ServerState.of('ACTIVE', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)
        return server

    def test_server_create(self):
        self._server_create('test_server_1')

    def test_server_pause_unpause(self):
        self._server_create('test_server_1')
        self.nova_driver.server_pause('test_server_1')
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('PAUSED', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)
        self.nova_driver.server_unpause('test_server_1')
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('ACTIVE', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)

    def test_server_suspend_resume(self):
        self._server_create('test_server_1')
        self.nova_driver.server_suspend('test_server_1')
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('SUSPENDED', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)
        self.nova_driver.server_resume('test_server_1')
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('ACTIVE', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)

    def test_server_shelve_unshelve(self):
        self._server_create('test_server_1')
        self.nova_driver.server_shelve('test_server_1')
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('SHELVED_OFFLOADED', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)

    def test_server_stop_start(self):
        self._server_create('test_server_1')
        self.nova_driver.server_stop('test_server_1')
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('SHUTOFF', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)
        self.nova_driver.server_start('test_server_1')
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('ACTIVE', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)

    def test_server_rebuild(self):
        self._server_create('test_server_1')
        self.nova_driver.server_rebuild('test_server_1', _DEFAULT_IMAGE)
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('REBUILD', Undefined(), Undefined(), Undefined()),
            ServerState.of('ACTIVE', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)

    def test_server_confirm_resize(self):
        self._server_create('test_server_1')
        self.nova_driver.server_resize('test_server_1', _DEFAULT_FLAVOR_ALT)
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('VERIFY_RESIZE', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)
        self.nova_driver.server_confirm_resize('test_server_1')
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('ACTIVE', flavor_id=self.flavor_default_alt.id)
        ])
        self.assertTrue(result)

    def test_server_revert_resize(self):
        self._server_create('test_server_1')
        self.nova_driver.server_resize('test_server_1', _DEFAULT_FLAVOR_ALT)
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('VERIFY_RESIZE', Undefined(), Undefined(), Undefined())
        ])
        self.assertTrue(result)
        self.nova_driver.server_revert_resize('test_server_1')
        result = self.nova_observer.server_observe('test_server_1', [
            ServerState.of('ACTIVE', flavor_id=self.flavor_default.id)
        ])
        self.assertTrue(result)

    def tearDown(self):
        for server in self.created_servers:
            self.nova_driver.server_delete(server.name)

