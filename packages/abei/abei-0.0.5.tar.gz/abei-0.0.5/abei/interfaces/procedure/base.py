from ..service import (
    abstractmethod,
    IService,
)


class IProcedure(IService):

    @abstractmethod
    def get_signature(self):
        """
        get signature of procedure
        :return:
        """

    @abstractmethod
    def get_input_signatures(self):
        """
        get list of input signatures
        :return:
        """

    @abstractmethod
    def get_output_signatures(self):
        """
        get list of output signatures
        :return:
        """

    @abstractmethod
    def get_docstring(self):
        """
        get document string of procedure
        :return:
        """

    @abstractmethod
    def set_docstring(self, docstring):
        """
        set document string of procedure
        :param docstring:
        :return:
        """

    @abstractmethod
    def run(self, procedure_data_list, **kwargs):
        """
        :param procedure_data_list: input code data list
        :param kwargs: extra arguments
        :return output code data list:
        """


class IProcedureFactory(IService):

    @abstractmethod
    def create(self, class_name, **kwargs):
        """
        create procedure
        :param class_name:
        :param kwargs:
        :return:
        """

    @abstractmethod
    def register_class(self, class_name, procedure_class, **kwargs):
        """
        register procedure class
        :param class_name:
        :param procedure_class:
        :param kwargs:
        :return:
        """

    @abstractmethod
    def iterate_classes(self):
        """
        iterate procedure classes
        :return:
        """
