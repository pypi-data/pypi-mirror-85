from abei.interfaces import (
    IStorage,
    service_entry as _
)

# from .storage_argv import Storage as StorageArgv
from .storage_ini_file import Storage as StorageINI
from .storage_memory import Storage as StorageMem


class Storage(IStorage):

    def __init__(self, service_site, **kwargs):
        # self.storage_argv = service_site.register_service(
        #     [_(IStorage, 'argv')], StorageArgv)

        self.storage_ini = service_site.register_service(
            [_(IStorage, 'ini')], StorageINI)

        self.storage_mem = service_site.register_service(
            [_(IStorage, 'mem')], StorageMem)

    def get_value(self, key):
        return (
            # self.storage_argv.get_value(key) or
            self.storage_ini.get_value(key) or
            self.storage_mem.get_value(key)
        )

    def set_value(self, key, value):
        return self.storage_mem.get_value(key)

    def del_value(self, key):
        return self.storage_mem.del_value(key)
