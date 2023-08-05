from abei.interfaces import (
    IProcedureData,
    IProcedureDataFactory,
)


class ProcedureDataBasic(IProcedureData):
    signature = 'none'
    label = 'none'
    value_type = type(None)
    value = None

    def __init__(self, value=None):
        if value is not None:
            self.set_value(value)

    def clone(self):
        instance = self.__class__()
        instance.value = self.value
        return instance

    def get_signature(self):
        return self.signature

    def get_label(self):
        return self.label

    def get_value(self):
        return self.value

    def set_value(self, value):
        try:
            self.value = (
                value if
                isinstance(value, self.value_type) else
                self.value_type(value)
            )
            return True
        except (ValueError, TypeError):
            return False


class ProcedureDataBool(ProcedureDataBasic):
    signature = 'bool'
    label = 'bool'
    value_type = bool
    value = True


class ProcedureDataInt(ProcedureDataBasic):
    signature = 'int'
    label = 'int'
    value_type = int
    value = 0


class ProcedureDataFloat(ProcedureDataBasic):
    signature = 'float'
    label = 'float'
    value_type = float
    value = 0.0


class ProcedureDataString(ProcedureDataBasic):
    signature = 'string'
    label = 'string'
    value_type = str
    value = ''


class ProcedureDataArray(ProcedureDataBasic):
    signature = 'array'
    label = 'array'
    value_type = list
    value = list()


class ProcedureDataMap(ProcedureDataBasic):
    signature = 'map'
    label = 'map'
    value_type = dict
    value = dict()


class ProcedureDataFactory(IProcedureDataFactory):
    def __init__(self, service_site, **kwargs):
        self.data_classes = dict([
            (ProcedureDataBool.signature, ProcedureDataBool),
            (ProcedureDataInt.signature, ProcedureDataInt),
            (ProcedureDataFloat.signature, ProcedureDataFloat),
            (ProcedureDataString.signature, ProcedureDataString),
            (ProcedureDataArray.signature, ProcedureDataArray),
            (ProcedureDataMap.signature, ProcedureDataMap),
        ])

    def create(self, signature, **kwargs):
        return self.get_class(signature)(**kwargs)

    def get_class(self, signature):
        data_class = self.query_class(signature)
        if not data_class:
            raise LookupError('data class not found')
        return data_class

    def query_class(self, signature):
        return self.data_classes.get(signature)

    def register_class(self, signature, procedure_data_class, **kwargs):
        assert signature not in self.data_classes
        self.data_classes[signature] = procedure_data_class

    def iterate_classes(self):
        return self.data_classes.keys()
