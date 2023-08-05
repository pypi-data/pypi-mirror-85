from .base import (
    abstractmethod,
    IService,
)


class IProcedureDetail(IService):
    @abstractmethod
    def get_joints(self):
        """
        get procedure flow joints
        :return: list of procedure flow and index pair
        """

    @abstractmethod
    def set_joints(self, joints, indices):
        """
        set procedure joints
        :param joints:
        :param indices:
        :return:
        """


class IProcedureJoint(IProcedureDetail):
    @abstractmethod
    def get_signature(self):
        """
        get signature of procedure joint
        :return:
        """

    @abstractmethod
    def has_breakpoint(self):
        """
        get if breakpoint is set
        :return:
        """

    @abstractmethod
    def enable_breakpoint(self, has_breakpoint):
        """
        set whether has breakpoint or not
        :param has_breakpoint:
        :return:
        """

    @abstractmethod
    def has_cache(self):
        """
        get if cache is used
        :return:
        """

    @abstractmethod
    def enable_cache(self, has_cache):
        """
        set whether use cache or not
        :param has_cache:
        :return:
        """


class IProcedureJointFactory(IService):

    @abstractmethod
    def create(self, inner_procedure, outer_procedure, **kwargs):
        """
        :param inner_procedure:
        :param outer_procedure:
        :param kwargs:
        :return:
        """
