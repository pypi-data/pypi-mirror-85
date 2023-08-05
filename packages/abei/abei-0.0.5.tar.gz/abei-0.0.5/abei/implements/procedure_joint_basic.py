from base64 import urlsafe_b64encode
from uuid import uuid1

from abei.interfaces import (
    IProcedure,
    IProcedureJoint,
    IProcedureJointFactory,
    IProcedureDetail,
)


def joint_validate(joints, indices, procedure, signatures):
    signatures_in = procedure.get_input_signatures()
    assert len(joints) == len(indices), 'input number miss match'

    for i, joint, sig in zip(
            indices,
            joints,
            signatures,
    ):
        assert isinstance(i, int), 'incorrect input type'

        if not joint:
            input_sig = signatures_in
        elif isinstance(joint, ProcedureJointBasic):
            assert joint.outer_procedure is procedure, \
                'incorrect outer procedure'
            input_sig = joint.inner_procedure.get_output_signatures()
        else:
            raise AssertionError('incorrect flow type')

        if i >= len(input_sig):
            raise AssertionError(
                'input index {} >= {}'.format(i, input_sig))

        if sig != input_sig[i]:
            raise AssertionError(
                'input type {} mismatch {}'.format(sig, input_sig[i]))


def joint_validate_dependents(joint, dependents=None):
    if not isinstance(dependents, frozenset):
        dependents = frozenset()

    signature = joint.get_signature()
    if signature in dependents:
        raise AssertionError(
            'recursive dependency found in joint: {}'.format(signature))

    dependents = dependents.union([signature])
    for j, _ in joint.get_joints():
        if j is not None:
            joint_validate_dependents(j, dependents)


def joint_run(joint, procedure_data_list, **kwargs):
    assert isinstance(joint, ProcedureJointBasic)

    input_data_list = [
        joint_run(joint, procedure_data_list, **kwargs)[i] if
        joint else procedure_data_list[i]
        for joint, i in joint.get_joints()
    ]

    output_data_list = joint.inner_procedure.run(
        input_data_list, **kwargs)

    return output_data_list


class ProcedureJointBasic(IProcedureJoint):
    use_breakpoint = False
    use_cache = False

    def __init__(
            self,
            signature=None,
            inner_procedure=None,
            outer_procedure=None,
    ):
        assert inner_procedure is not outer_procedure
        # outer procedure should be a composite procedure
        assert isinstance(inner_procedure, IProcedure)
        assert (
            isinstance(outer_procedure, IProcedure) and
            isinstance(outer_procedure, IProcedureDetail)
        )
        self.signature = signature or urlsafe_b64encode(
            uuid1().bytes).strip(b'=').decode('utf8')
        self.inner_procedure = inner_procedure
        self.outer_procedure = outer_procedure
        self.input_indices = []
        self.input_flows = []

    def get_signature(self):
        return self.signature

    def get_inner_procedure(self):
        return self.inner_procedure

    def get_outer_procedure(self):
        return self.outer_procedure

    def has_breakpoint(self):
        return self.use_breakpoint

    def enable_breakpoint(self, has_breakpoint):
        self.use_breakpoint = has_breakpoint

    def has_cache(self):
        return self.use_cache

    def enable_cache(self, has_cache):
        self.use_cache = has_cache

    def get_joints(self):
        return [(f, i) for f, i in zip(
            self.input_flows, self.input_indices)]

    def set_joints(
            self,
            joints,
            indices,
    ):
        joint_validate(
            joints,
            indices,
            self.outer_procedure,
            self.inner_procedure.get_input_signatures(),
        )
        self.input_flows = joints
        self.input_indices = indices


class ProcedureJointFactory(IProcedureJointFactory):

    def __init__(self, service_site, **kwargs):
        pass

    def create(self, inner_procedure, outer_procedure, **kwargs):
        return ProcedureJointBasic(
            inner_procedure=inner_procedure,
            outer_procedure=outer_procedure,
            **kwargs
        )
