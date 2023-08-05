r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["SvmIscsi", "SvmIscsiSchema"]
__pdoc__ = {
    "SvmIscsiSchema.resource": False,
    "SvmIscsi": False,
}


class SvmIscsiSchema(ResourceSchema):
    """The fields of the SvmIscsi object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the svm_iscsi. """

    enabled = fields.Boolean(data_key="enabled")
    r""" Enable iSCSI? Setting to true creates a service if not already created. """

    @property
    def resource(self):
        return SvmIscsi

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


class SvmIscsi(Resource):

    _schema = SvmIscsiSchema
