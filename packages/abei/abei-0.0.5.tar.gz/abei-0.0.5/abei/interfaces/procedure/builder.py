from .base import (
    abstractmethod,
    IService,
)


class IProcedureBuilder(IService):

    @abstractmethod
    def load_json(self, procedure_site, file_or_filename):
        """
        :param procedure_site:
        :param file_or_filename:
        :return:
        """

    @abstractmethod
    def save_json(self, procedure_site, file_or_filename):
        """
        :param procedure_site:
        :param file_or_filename:
        :return:
        """

    @abstractmethod
    def load_yaml(self, procedure_site, file_or_filename):
        """
        :param procedure_site:
        :param file_or_filename:
        :return:
        """

    @abstractmethod
    def save_yaml(self, procedure_site, file_or_filename):
        """
        :param procedure_site:
        :param file_or_filename:
        :return:
        """
