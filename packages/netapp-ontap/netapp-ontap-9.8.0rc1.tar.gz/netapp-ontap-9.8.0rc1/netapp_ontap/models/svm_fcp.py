r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["SvmFcp", "SvmFcpSchema"]
__pdoc__ = {
    "SvmFcpSchema.resource": False,
    "SvmFcp": False,
}


class SvmFcpSchema(ResourceSchema):
    """The fields of the SvmFcp object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the svm_fcp. """

    enabled = fields.Boolean(data_key="enabled")
    r""" Enable Fiber Channel Protocol (FCP)? Setting to true creates a service if not already created. """

    @property
    def resource(self):
        return SvmFcp

    gettable_fields = [
        "links",
        "enabled",
    ]
    """links,enabled,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""


class SvmFcp(Resource):

    _schema = SvmFcpSchema
