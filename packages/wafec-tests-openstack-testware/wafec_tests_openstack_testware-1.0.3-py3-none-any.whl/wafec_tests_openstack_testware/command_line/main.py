import argparse

from .interception import InterceptionScript


def run():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers()
    InterceptionScript(sub)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    run()
