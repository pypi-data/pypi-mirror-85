from .service import (
    abstractmethod,
    IService,
)


class IStorage(IService):
    @abstractmethod
    def get_value(self, key):
        """
        get value by key
        """

    @abstractmethod
    def set_value(self, key, value):
        """
        set value with key
        """

    @abstractmethod
    def del_value(self, key):
        """
        del value by key
        """
