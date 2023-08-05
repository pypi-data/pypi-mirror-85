from os import getenv

from configparser import (
    ConfigParser,
    NoOptionError,
    NoSectionError,
)

from abei.interfaces import (
    IStorage,
    service_entry as _
)


class Storage(IStorage):
    def __init__(self, service_site, **kwargs):
        service = service_site.query_service(_(IStorage, 'argv'))
        self.filename = (
            service and service.get_value('config_file') or
            getenv('CONFIG_FILE') or 'app.ini'
        )
        self.config = ConfigParser()
        self.config.read(self.filename, encoding='utf8')
        print('----storage ini file service initialized----')

    def get_value(self, key):
        try:
            keys = key.split(':', 1)
            return (
                self.config.get(keys[0], keys[1]) if
                len(keys) > 1 else
                self.config.get('common', keys[0])
            )
        except (NoOptionError, NoSectionError):
            return None

    def set_value(self, key, value):
        try:
            keys = key.split(':', 1)
            (
                self.config.set(keys[0], keys[1], value) if
                len(keys) > 1 else
                self.config.set('common', keys[0], value)
            )
            return True
        except NoSectionError:
            return False

    def del_value(self, key):
        return False  # can not delete value
