from argparse import (
    ArgumentParser,
    SUPPRESS,
)

from abei.interfaces import IStorage


class Storage(IStorage):

    def __init__(self, service_site, **kwargs):
        parser = ArgumentParser()
        parser.add_argument('--debug', nargs="?", default=SUPPRESS)
        parser.add_argument('--config_file', nargs="?", default=SUPPRESS)
        parser.add_argument('--unittest', nargs="?", default=SUPPRESS)
        args = parser.parse_args()
        self.args = {
            'config_file': getattr(args, 'config_file', None),
            'debug': hasattr(args, 'debug'),
            'unittest': hasattr(args, 'unittest')
        }
        print('----storage argv service initialized----')

    def get_value(self, key):
        return self.args.get(key)

    def set_value(self, key, value):
        return False  # can not set value

    def del_value(self, key):
        return False  # can not delete value
