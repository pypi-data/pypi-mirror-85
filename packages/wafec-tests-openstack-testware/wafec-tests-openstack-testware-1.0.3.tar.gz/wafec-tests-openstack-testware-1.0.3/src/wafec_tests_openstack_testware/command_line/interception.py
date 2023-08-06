from ..testd.interception_agent import start_agent_server
from ._base import ScriptBase

__all__ = [
    'InterceptionScript',
    'InterceptionAgentScript'
]


class InterceptionScript(ScriptBase):
    def __init__(self, subparser):
        ScriptBase.__init__(self, subparser, 'interception')
        self.command(InterceptionAgentScript)


class InterceptionAgentScript(ScriptBase):
    def __init__(self, subparser):
        ScriptBase.__init__(self, subparser, 'agent')

    def run(self, arg_list):
        start_agent_server()
