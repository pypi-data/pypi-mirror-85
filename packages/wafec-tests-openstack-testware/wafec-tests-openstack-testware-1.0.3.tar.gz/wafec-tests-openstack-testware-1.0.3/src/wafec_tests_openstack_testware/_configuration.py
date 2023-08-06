import configparser

from .utils import first_existent_path

__all__ = [
    'interception_config',
    'BASE_CONF_DIR'
]

BASE_CONF_DIR = '/usr/wafec'


class InterceptionConfiguration(object):
    _sources = [
        "interception.ini",
        "resources/interception.ini",
        f"{BASE_CONF_DIR}/interception.ini"
    ]

    def __init__(self):
        self.connection_string = "mysql+pymysql://testd:testd@localhost/testd?charset=utf8mb4"
        self.port = 7654
        self.dat_file = f'{BASE_CONF_DIR}/interception.dat'
        self.controller_port = 8765
        self.agent_port = 7654

    def auto_initialize(self):
        source = first_existent_path(InterceptionConfiguration._sources)
        if source:
            config = configparser.ConfigParser()
            config.read(source)
            self.connection_string = config.get('database', 'connection_string', fallback=self.connection_string)
            self.port = config.getint('DEFAULT', 'port', fallback=self.port)
            self.dat_file = config.get('agent', 'dat_file', fallback=self.dat_file)
            self.agent_port = config.getint('agent', 'port', fallback=self.agent_port)
            self.controller_port = config.getint('controller', 'port', fallback=self.controller_port)


interception_config = InterceptionConfiguration()
interception_config.auto_initialize()
