from .service import (
    abstractmethod,
    IService,
)


class ICache(IService):

    @abstractmethod
    def get_value(self, key):
        """
        get value by key in cache
        """

    @abstractmethod
    def set_value(self, key, value, expire):
        """
        set value with key and expire time to cache
        """

    @abstractmethod
    def set_value_if_match(self, key, value, match, expire):
        """
        set value with key and expire time to cache
        if previous value match the given one
        note that this is an atomic operation
        """

    @abstractmethod
    def del_value(self, key):
        """
        delete key value pair in cache
        """

    @abstractmethod
    def del_value_if_match(self, key, value):
        """
        delete key value pair in cache if the input is matched
        note that this is an atomic operation
        """

    @abstractmethod
    def swp_value(self, key, value, expire):
        """
        swap value, if there is already key value pair in cache
        note that this is an atomic operation
        """
