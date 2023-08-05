from base64 import urlsafe_b64encode
from uuid import uuid1

from abei.interfaces import (
    IProcedure,
    IProcedureSite,
    IProcedureSiteFactory,
    IProcedureDataFactory,
    IProcedureFactory,
    service_entry as _
)
from abei.implements.util import LazyProperty


class ProcedureSiteBuiltin(IProcedureSite):
    def __init__(self, procedures_builtin):
        self.procedures = {
            procedure.get_signature(): procedure
            for procedure in procedures_builtin
        }

    def get_signature(self):
        return 'builtin'

    def get_procedure(self, signature, **kwargs):
        procedure = self.query_procedure(signature, **kwargs)
        if not procedure:
            raise LookupError(
                'procedure {} not found'.format(signature))
        return procedure

    def query_procedure(self, signature, site=None, **kwargs):
        site = site and str(site)
        signature = str(signature)
        return (
            (site is None or self.get_signature() == site) and
            self.procedures.get(signature) or None
        )

    def register_procedure(self, procedure, **kwargs):
        return None

    def iterate_procedures(self):
        return self.procedures.keys()

    def get_base_sites(self):
        return []


class ProcedureSiteBasic(IProcedureSite):

    def __init__(self, signature=None, dependencies=None):
        # signature will be set to random string if not specified
        self.signature = signature or urlsafe_b64encode(
            uuid1().bytes).strip(b'=').decode()
        self.dependencies = dependencies or []
        self.procedures = {}

    def get_signature(self):
        return self.signature

    def get_procedure(self, signature, **kwargs):
        procedure = self.query_procedure(signature, **kwargs)
        if not procedure:
            raise LookupError(
                'procedure {} not found'.format(signature))
        return procedure

    def query_procedure(self, signature, depth=-1, site=None, **kwargs):
        site = site and str(site)
        signature = str(signature)

        procedure = (
            (site is None or self.get_signature() == site) and
            self.procedures.get(signature) or None
        )
        if procedure:
            return procedure

        if depth == 0:
            return None

        # try to find in dependent sites
        for s in self.dependencies:
            procedure = s.query_procedure(
                signature, depth=depth - 1, site=site, **kwargs)
            if procedure:
                return procedure

        return None

    def register_procedure(self, procedure, **kwargs):
        assert isinstance(procedure, IProcedure)
        signature = str(procedure.get_signature())
        if (
                not kwargs.get('overwrite') and
                self.query_procedure(signature)
        ):
            raise AssertionError('procedure already registered')

        self.procedures[signature] = procedure
        return procedure

    def iterate_procedures(self):
        return self.procedures.keys()

    def get_base_sites(self):
        return list(self.dependencies)


class ProcedureSiteFactory(IProcedureSiteFactory):

    def __init__(self, service_site, **kwargs):
        self.service_site = service_site

    @LazyProperty
    def builtin(self):
        service = self.service_site.get_service(_(IProcedureFactory))
        service_d = self.service_site.get_service(_(IProcedureDataFactory))

        class_bool = service_d.get_class('bool')
        class_int = service_d.get_class('int')
        class_float = service_d.get_class('float')
        class_string = service_d.get_class('string')

        return ProcedureSiteBuiltin([
            service.create('probe', data_class=class_bool),
            service.create('not', data_class=class_bool),
            service.create('and', data_class=class_bool),
            service.create('or', data_class=class_bool),

            service.create('probe', data_class=class_int),
            service.create('neg', data_class=class_int),
            service.create('sq', data_class=class_int),
            service.create('add', data_class=class_int),
            service.create('sub', data_class=class_int),
            service.create('mul', data_class=class_int),
            service.create('mod', data_class=class_int),
            service.create('modDiv', data_class=class_int),
            service.create('pow', data_class=class_int),
            service.create('eq', data_class=class_int),
            service.create('ne', data_class=class_int),
            service.create('lt', data_class=class_int),
            service.create('lte', data_class=class_int),
            service.create('gt', data_class=class_int),
            service.create('gte', data_class=class_int),
            service.create('diverge2', data_class=class_int),
            service.create('converge2', data_class=class_int),

            service.create('probe', data_class=class_float),
            service.create('neg', data_class=class_float),
            service.create('sq', data_class=class_float),
            service.create('add', data_class=class_float),
            service.create('sub', data_class=class_float),
            service.create('mul', data_class=class_float),
            service.create('div', data_class=class_float),
            service.create('mod', data_class=class_float),
            service.create('modDiv', data_class=class_float),
            service.create('pow', data_class=class_float),
            service.create('eq', data_class=class_float),
            service.create('ne', data_class=class_float),
            service.create('lt', data_class=class_float),
            service.create('lte', data_class=class_float),
            service.create('gt', data_class=class_float),
            service.create('gte', data_class=class_float),
            service.create('diverge2', data_class=class_float),
            service.create('converge2', data_class=class_float),

            service.create('probe', data_class=class_string),
            service.create('add', data_class=class_string),
            service.create('eq', data_class=class_string),
            service.create('ne', data_class=class_string),
            service.create('diverge2', data_class=class_string),
            service.create('converge2', data_class=class_string),
        ])

    def create(self, procedure_sites, signature=None, **kwargs):
        if not procedure_sites and not signature:
            return self.builtin

        return ProcedureSiteBasic(
            signature=signature,
            dependencies=procedure_sites or [self.builtin],
        )
