from base64 import urlsafe_b64encode
from uuid import uuid1

from abei.interfaces import (
    IProcedure,
    IProcedureData,
    IProcedureFactory,
    IProcedureDetail,
)

from .procedure_data_basic import (
    ProcedureDataBasic,
    ProcedureDataBool,
    ProcedureDataInt,
    ProcedureDataFloat,
)
from .procedure_joint_basic import (
    joint_validate,
    joint_run,
)


class ProcedureBasic(IProcedure):
    signature = 'doNothing'
    docstring = ''
    input_signatures = []
    output_signatures = []

    def get_signature(self):
        return self.signature

    def get_input_signatures(self):
        return self.input_signatures

    def get_output_signatures(self):
        return self.output_signatures

    def get_docstring(self):
        return self.docstring

    def set_docstring(self, docstring):
        self.docstring = docstring

    def run(self, procedure_data_list, **kwargs):
        # assert isinstance(kwargs.setdefault('procedure_cache', {}), dict)
        return (
            self.run_normally(procedure_data_list, **kwargs) if
            self.run_validation(
                procedure_data_list, self.input_signatures) else
            self.run_exceptionally(procedure_data_list, **kwargs)
        )

    @staticmethod
    def run_validation(procedure_data_list, signatures):
        if len(procedure_data_list) != len(signatures):
            raise AssertionError('invalid data list')

        has_missing_params = False
        for d, sig in zip(procedure_data_list, signatures):
            if d is None:
                has_missing_params = True
                continue
            if not isinstance(d, IProcedureData):
                raise AssertionError('invalid data list')
            if d.get_signature() != sig:
                raise AssertionError('data signature miss match')

        return not has_missing_params

    def run_normally(self, procedure_data_list, **kwargs):
        return [None] * len(self.output_signatures)

    def run_exceptionally(self, procedure_data_list, **kwargs):
        return [None] * len(self.output_signatures)


class ProcedureComposite(IProcedureDetail, ProcedureBasic):
    name = 'composite'
    output_joints = []
    output_indices = []

    def __init__(
            self,
            signature=None,
            docstring=None,
            input_signatures=None,
            output_signatures=None,
    ):
        self.signature = signature or urlsafe_b64encode(
            uuid1().bytes).strip(b'=').decode('utf8')
        self.docstring = docstring or self.docstring
        self.input_signatures = input_signatures or self.input_signatures
        self.output_signatures = output_signatures or self.output_signatures

    def get_joints(self):
        return [(f, i) for f, i in zip(
            self.output_joints, self.output_indices)]

    def set_joints(self, joints, indices):
        joint_validate(
            joints,
            indices,
            self,
            self.output_signatures,
        )
        self.output_joints = joints
        self.output_indices = indices

    def run_normally(self, procedure_data_list, **kwargs):
        return [
            joint_run(joint, procedure_data_list, **kwargs)[i] if
            joint else procedure_data_list[i]
            for joint, i in self.get_joints()
        ]


class ProcedureBuiltin(ProcedureBasic):
    name = 'builtin'

    def __init__(self, data_class):
        self.signature = '{}[{}]'.format(
            self.name,
            data_class.signature,
        )


class ProcedureUnaryOperator(ProcedureBuiltin):
    name = 'unaryOperator'
    native_function = staticmethod(lambda x: x)

    def __init__(self, data_class=ProcedureDataBasic):
        super().__init__(data_class)
        self.input_signatures = [data_class.signature]
        self.output_signatures = [data_class.signature]

    def run_normally(self, procedure_data_list, **kwargs):
        ret = procedure_data_list[0].clone()
        ret.set_value(self.native_function(
            procedure_data_list[0].get_value()))
        return [ret]


class ProcedureBinaryOperator(ProcedureBuiltin):
    name = 'binaryOperator'
    native_function = staticmethod(lambda x, y: x)

    def __init__(self, data_class=ProcedureDataBasic):
        super().__init__(data_class)
        self.input_signatures = [
            data_class.signature,
            data_class.signature,
        ]
        self.output_signatures = [data_class.signature]

    def run_normally(self, procedure_data_list, **kwargs):
        ret = procedure_data_list[0].clone()
        ret.set_value(self.native_function(
            procedure_data_list[0].get_value(),
            procedure_data_list[1].get_value(),
        ))
        return [ret]


class ProcedureComparator(ProcedureBuiltin):
    name = 'compare'
    native_function = staticmethod(lambda x, y: True)

    def __init__(self, data_class=ProcedureDataBasic):
        super().__init__(data_class)
        self.input_signatures = [
            data_class.signature,
            data_class.signature,
        ]
        self.output_signatures = [
            ProcedureDataBool.signature,
        ]

    def run_normally(self, procedure_data_list, **kwargs):
        ret = ProcedureDataBool(value=self.native_function(
            procedure_data_list[0].get_value(),
            procedure_data_list[1].get_value(),
        ))
        return [ret]


# class ProcedureFilter(ProcedureBuiltin):
#     name = 'filter@py'
#
#     def __init__(
#             self,
#             data_class=ProcedureDataBasic,
#             data_count=1,
#     ):
#         super().__init__(data_class)
#         self.data_signature = data_class.signature
#         signatures = [data_class.signature] * data_count
#         self.input_signatures = ['int@py', *signatures]
#         self.output_signatures = signatures
#
#     def run_normally(self, procedure_data_list, **kwargs):
#         flag = procedure_data_list[0].get_value()
#         assert isinstance(flag, int)
#
#         return [
#             (flag & (1 >> i)) and
#             procedure_data_list[i + 1] or None
#             for i in range(len(self.output_signatures))
#         ]
#
#     def run_exceptionally(self, procedure_data_list, **kwargs):
#         return self.run_normally(procedure_data_list, **kwargs)


class ProcedureDiverge(ProcedureBuiltin):
    name = 'diverge2'

    def __init__(
            self,
            data_class=ProcedureDataBasic,
            # data_count=2,
    ):
        super().__init__(data_class)
        self.input_signatures = [
            ProcedureDataBool.signature,
            data_class.signature,
        ]
        self.output_signatures = [
            data_class.signature,
            data_class.signature,
        ]

    def run_normally(self, procedure_data_list, **kwargs):
        flag = procedure_data_list[0].get_value()
        ret = procedure_data_list[1]
        return flag and [ret, None] or [None, ret]

    def run_exceptionally(self, procedure_data_list, **kwargs):
        return self.run_normally(procedure_data_list, **kwargs)


class ProcedureConverge(ProcedureBuiltin):
    name = 'converge2'

    def __init__(
            self,
            data_class=ProcedureDataBasic,
            # data_count=2,
    ):
        super().__init__(data_class)
        self.input_signatures = [
            ProcedureDataBool.signature,
            data_class.signature,
            data_class.signature,
        ]
        self.output_signatures = [
            data_class.signature,
        ]

    def run_normally(self, procedure_data_list, **kwargs):
        flag = procedure_data_list[0].get_value()
        ret = procedure_data_list[flag and 1 or 2]
        return [ret]

    def run_exceptionally(self, procedure_data_list, **kwargs):
        return self.run_normally(procedure_data_list, **kwargs)


class ProcedureProbe(ProcedureBuiltin):
    name = 'probe'

    def __init__(self, data_class=ProcedureDataBasic):
        super().__init__(data_class)
        self.input_signatures = [data_class.signature]
        self.output_signatures = [ProcedureDataBool.signature]

    def run_normally(self, procedure_data_list, **kwargs):
        ret = ProcedureDataBool(
            value=bool(procedure_data_list[0] is not None))
        return [ret]

    def run_exceptionally(self, procedure_data_list, **kwargs):
        return self.run_normally(procedure_data_list, **kwargs)


class ProcedureCast(ProcedureBuiltin):
    name = 'cast'
    to_data_class = ProcedureDataBasic

    def __init__(self, data_class=ProcedureDataBasic):
        super().__init__(data_class)
        self.input_signatures = [data_class.signature]
        self.output_signatures = [self.to_data_class.signature]

    def run_normally(self, procedure_data_list, **kwargs):
        ret = self.to_data_class()
        ret.set_value(self.to_data_class.value_type(
            procedure_data_list[0].get_value()))
        return [ret]


class ProcedureNot(ProcedureUnaryOperator):
    name = 'not'
    native_function = staticmethod(lambda x: not x)


class ProcedureNegate(ProcedureUnaryOperator):
    name = 'neg'
    native_function = staticmethod(lambda x: -x)


class ProcedureSquare(ProcedureUnaryOperator):
    name = 'sq'
    native_function = staticmethod(lambda x: x * x)


class ProcedureAnd(ProcedureBinaryOperator):
    name = 'and'
    native_function = staticmethod(lambda x, y: x and y)


class ProcedureOr(ProcedureBinaryOperator):
    name = 'or'
    native_function = staticmethod(lambda x, y: x or y)


class ProcedureAdd(ProcedureBinaryOperator):
    name = 'add'
    native_function = staticmethod(lambda x, y: x + y)


class ProcedureSubtract(ProcedureBinaryOperator):
    name = 'sub'
    native_function = staticmethod(lambda x, y: x - y)


class ProcedureMultiply(ProcedureBinaryOperator):
    name = 'mul'
    native_function = staticmethod(lambda x, y: x * y)


class ProcedureDivide(ProcedureBinaryOperator):
    name = 'div'
    native_function = staticmethod(lambda x, y: x / y)


class ProcedureModulo(ProcedureBinaryOperator):
    name = 'mod'
    native_function = staticmethod(lambda x, y: x % y)


class ProcedureModDivide(ProcedureBinaryOperator):
    name = 'modDiv'
    native_function = staticmethod(lambda x, y: x // y)


class ProcedurePower(ProcedureBinaryOperator):
    name = 'pow'
    native_function = staticmethod(lambda x, y: x ** y)


class ProcedureEqual(ProcedureComparator):
    name = 'eq'
    native_function = staticmethod(lambda x, y: x == y)


class ProcedureNotEqual(ProcedureComparator):
    name = 'ne'
    native_function = staticmethod(lambda x, y: x != y)


class ProcedureLessThan(ProcedureComparator):
    name = 'lt'
    native_function = staticmethod(lambda x, y: x < y)


class ProcedureLessThanOrEqual(ProcedureComparator):
    name = 'lte'
    native_function = staticmethod(lambda x, y: x <= y)


class ProcedureGreaterThan(ProcedureComparator):
    name = 'gt'
    native_function = staticmethod(lambda x, y: x > y)


class ProcedureGreaterThanEqual(ProcedureComparator):
    name = 'gte'
    native_function = staticmethod(lambda x, y: x >= y)


class ProcedureCastToBool(ProcedureCast):
    name = 'castToBool'
    to_data_class = ProcedureDataBool


class ProcedureCastToInt(ProcedureCast):
    name = 'castToInt'
    to_data_class = ProcedureDataInt


class ProcedureCastToFloat(ProcedureCast):
    name = 'castToFloat'
    to_data_class = ProcedureDataFloat


class ProcedureFactory(IProcedureFactory):

    def __init__(self, service_site, **kwargs):
        self.procedure_classes = {p.name: p for p in [
            ProcedureComposite,
            ProcedureProbe,
            ProcedureNot,
            ProcedureNegate,
            ProcedureSquare,
            ProcedureAnd,
            ProcedureOr,
            ProcedureAdd,
            ProcedureSubtract,
            ProcedureMultiply,
            ProcedureDivide,
            ProcedureModulo,
            ProcedureModDivide,
            ProcedurePower,
            ProcedureEqual,
            ProcedureNotEqual,
            ProcedureLessThan,
            ProcedureLessThanOrEqual,
            ProcedureGreaterThan,
            ProcedureGreaterThanEqual,
            # ProcedureFilter,
            ProcedureDiverge,
            ProcedureConverge,
            ProcedureCastToBool,
            ProcedureCastToInt,
            ProcedureCastToFloat,
        ]}

    def create(self, class_name, **kwargs):
        procedure_class = self.procedure_classes.get(class_name)
        return procedure_class and procedure_class(**kwargs)

    def register_class(self, class_name, procedure_class, **kwargs):
        assert class_name not in self.procedure_classes
        self.procedure_classes[class_name] = procedure_class

    def iterate_classes(self):
        return self.procedure_classes.keys()
