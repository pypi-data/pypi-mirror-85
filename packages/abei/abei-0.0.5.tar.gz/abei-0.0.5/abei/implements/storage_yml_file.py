from os import getenv

from abei.interfaces import (
    IStorage,
    service_entry as _
)
from .service_basic import ServiceBasic


class Storage(ServiceBasic, IStorage):
    @classmethod
    def get_dependencies(cls):
        return ['PyYAML']

    def __init__(self, service_site, **kwargs):
        from yaml import (
            safe_load,
            # safe_dump,
        )

        service = service_site.query_service(_(IStorage, 'argv'))
        self.filename = (
            service and service.get_value('config_file') or
            getenv('CONFIG_FILE') or 'app.yml'
        )
        with open(self.filename) as f:
            self.mapping = safe_load(f)

        if not isinstance(self.mapping, dict):
            raise ValueError('invalid yml config file')

        print('----storage yml file service initialized----')

    def get_value_recursive(self, mapping, key):
        keys = key.split(':', 1)
        subs = mapping.get(keys[0])
        if len(keys) <= 1:
            return subs

        if not isinstance(subs, dict):
            return None

        return self.get_value_recursive(subs, keys[1])

    def set_value_recursive(self, mapping, key, value):
        keys = key.split(':', 1)
        if len(keys) <= 1:
            mapping[key[0]] = value
            return True

        subs = mapping.setdefault(keys[0], {})
        if not isinstance(subs, dict):
            return False

        return self.set_value_recursive(subs, keys[1], value)

    def del_value_recursive(self, mapping, key):
        keys = key.split(':', 1)
        if len(keys) <= 1:
            return bool(mapping.pop(key, None))

        subs = mapping.setdefault(keys[0], {})
        if not isinstance(subs, dict):
            return False

        return self.del_value_recursive(subs, keys[1])

    def get_value(self, key):
        return self.get_value_recursive(self.mapping, key)

    def set_value(self, key, value):
        return self.set_value_recursive(self.mapping, key, value)

    def del_value(self, key):
        return self.del_value_recursive(self.mapping, key)
