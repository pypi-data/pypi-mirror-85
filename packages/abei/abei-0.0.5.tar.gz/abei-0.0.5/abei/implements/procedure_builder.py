from abei.interfaces import (
    IProcedure,
    IProcedureDetail,
    IProcedureFactory,
    IProcedureJointFactory,
    IProcedureBuilder,
    service_entry as _,
)

from abei.implements.service_basic import ServiceBasic
from abei.implements.util import (
    FileLikeWrapper,
    LazyProperty,
)

from .procedure_joint_basic import (
    joint_validate_dependents,
)

keyword_procedure_signature = 'fn'
keyword_procedure_input_signatures = 'args'
keyword_procedure_output_signatures = 'return'
keyword_procedure_outputs = 'out'
keyword_procedure_document = 'doc'
keyword_joints = 'statements'
keyword_joint_name = 'name'
keyword_joint_procedure = 'call'
keyword_joint_inputs = 'in'


class ProcedureJointBuilder(object):
    def __init__(
            self,
            procedure_builder,
            procedure_site,
            procedure,
            data,
    ):
        self.procedure_builder = procedure_builder
        self.procedure_site = procedure_site
        self.procedure = procedure
        assert isinstance(data, dict)
        self.data = data

    @property
    def name(self):
        return self.data.get(keyword_joint_name)

    @property
    def inputs(self):
        return self.data.get(keyword_joint_inputs)

    @LazyProperty
    def instance(self):
        joint_procedure_signature = self.data.get(keyword_joint_procedure)
        joint_procedure_signatures = joint_procedure_signature.split('@')
        if len(joint_procedure_signatures) > 2:
            raise ValueError('invalid joint procedure {}'.format(
                joint_procedure_signature))

        joint_procedure = self.procedure_site.get_procedure(
            joint_procedure_signatures[0],
            site=(
                joint_procedure_signatures[1] if
                len(joint_procedure_signatures) > 1 else None
            )
        )
        return self.procedure_builder.procedure_joint_factory.create(
            joint_procedure,
            self.procedure,
            signature=self.name,
        )


class ProcedureBuilder(ServiceBasic, IProcedureBuilder):

    def __init__(self, service_site, **kwargs):
        self.service_site = service_site

    @LazyProperty
    def procedure_factory(self):
        return self.service_site.get_service(_(IProcedureFactory))

    @LazyProperty
    def procedure_joint_factory(self):
        return self.service_site.get_service(_(IProcedureJointFactory))

    @classmethod
    def get_dependencies(cls):
        return ['PyYAML']

    def load_procedure(self, procedure_site, procedure_object):
        if not isinstance(procedure_object, dict):
            raise ValueError(
                'invalid procedure in configuration file')

        input_signatures = procedure_object.get(
            keyword_procedure_input_signatures, [])
        if not isinstance(input_signatures, list):
            raise ValueError(
                'invalid procedure input signatures')

        input_signatures = [str(sig) for sig in input_signatures]

        output_signatures = procedure_object.get(
            keyword_procedure_output_signatures, [])
        if not isinstance(output_signatures, list):
            raise ValueError(
                'invalid procedure output signatures')

        output_signatures = [str(sig) for sig in output_signatures]

        procedure = self.procedure_factory.create(
            'composite',
            signature=str(procedure_object.get(
                keyword_procedure_signature, '')),
            docstring=str(procedure_object.get(
                keyword_procedure_document, '')),
            input_signatures=input_signatures,
            output_signatures=output_signatures,
        )
        assert (
            isinstance(procedure, IProcedure) and
            isinstance(procedure, IProcedureDetail)
        )

        procedure_joints = procedure_object.get(keyword_joints, [])
        procedure_joints = [
            ProcedureJointBuilder(
                self,
                procedure_site,
                procedure,
                jt
            ) for jt in procedure_joints
        ]
        procedure_joints = {jt.name: jt for jt in procedure_joints}
        self.load_joints(
            procedure_site,
            procedure,
            procedure_joints,
        )

        procedure_output_joints = procedure_object.get(
            keyword_procedure_outputs, [])
        if not isinstance(procedure_output_joints, list):
            raise ValueError('invalid procedure joints')

        output_joints, output_indices = self.load_joint_inputs(
            procedure_output_joints, procedure_joints)
        for j in output_joints:
            if j is not None:
                joint_validate_dependents(j)

        procedure.set_joints(output_joints, output_indices)
        procedure_site.register_procedure(procedure)

    def load_joints(self, procedure_site, procedure, joint_objects):
        if not isinstance(joint_objects, dict):
            raise ValueError('invalid procedure joints')

        # connect joints
        for joint_signature, joint_object in joint_objects.items():
            joint_inputs = joint_object.inputs
            if not isinstance(joint_inputs, list):
                raise ValueError('invalid procedure joint config')

            joint_object.instance.set_joints(
                *self.load_joint_inputs(joint_inputs, joint_objects))

    @staticmethod
    def load_joint_inputs(joint_inputs, joint_objects):
        input_joints = []
        input_indices = []
        for joint_input in joint_inputs:
            if not isinstance(joint_input, str):
                raise ValueError('invalid procedure joint input')

            if joint_input.startswith('$'):
                joint_input = joint_input.strip('$')
                if not joint_input.isdigit():
                    raise ValueError('invalid joint input')
                input_joints.append(None)
                input_indices.append(int(joint_input))
            else:
                joint_input_tokens = joint_input.split('[')
                if len(joint_input_tokens) != 2:
                    raise ValueError('invalid joint input')
                joint_input_joint, joint_input_index = joint_input_tokens
                joint_input_joint = joint_input_joint.strip()
                joint_input_index = joint_input_index.strip(']').strip()
                if joint_input_joint not in joint_objects:
                    raise ValueError('invalid joint')
                if not joint_input_index.isdigit():
                    raise ValueError('invalid joint input')
                input_joints.append(
                    joint_objects[joint_input_joint].instance)
                input_indices.append(int(joint_input_index))
        return input_joints, input_indices

    def load_object(self, procedure_site, config_object):
        if not isinstance(config_object, (tuple, list)):
            raise ValueError('invalid procedure configuration file')

        for config_item in config_object:
            self.load_procedure(procedure_site, config_item)

    def load_json(self, procedure_site, file_or_filename):
        import json

        with FileLikeWrapper(file_or_filename) as file:
            self.load_object(procedure_site, json.loads(file.read()))

    def save_json(self, procedure_site, file_or_filename):
        raise NotImplementedError

    def load_yaml(self, procedure_site, file_or_filename):
        import yaml

        with FileLikeWrapper(file_or_filename) as file:
            self.load_object(procedure_site, yaml.safe_load(file))

    def save_yaml(self, procedure_site, file_or_filename):
        raise NotImplementedError
