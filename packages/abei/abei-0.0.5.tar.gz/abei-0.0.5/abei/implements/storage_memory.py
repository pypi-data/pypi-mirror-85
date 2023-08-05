from abei.interfaces import IStorage


class Storage(IStorage):

    def __init__(self, service_site, **kwargs):
        self.mapping = {}
        print('----storage memory service initialized----')

    def get_value(self, key):
        return self.mapping.get(key)

    def set_value(self, key, value):
        self.mapping[key] = value
        return True  # always return true

    def del_value(self, key):
        return bool(self.mapping.pop(key, None))
