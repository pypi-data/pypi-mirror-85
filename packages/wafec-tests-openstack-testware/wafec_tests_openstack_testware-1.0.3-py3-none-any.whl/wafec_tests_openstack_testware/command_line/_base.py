
__all__ = [
    'ScriptBase'
]


class ScriptBase(object):
    def __init__(self, subparser, name):
        self.subparser = subparser
        self.parser = subparser.add_parser(name)
        self.parser.set_defaults(func=self.run)
        self.parser_subparsers = self.parser.add_subparsers()

    def command(self, cls):
        cls(self.parser_subparsers)

    def run(self, arg_list):
        pass
