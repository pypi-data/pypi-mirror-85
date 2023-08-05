r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["SvmNfs", "SvmNfsSchema"]
__pdoc__ = {
    "SvmNfsSchema.resource": False,
    "SvmNfs": False,
}


class SvmNfsSchema(ResourceSchema):
    """The fields of the SvmNfs object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the svm_nfs. """

    enabled = fields.Boolean(data_key="enabled")
    r""" Enable NFS? Setting to true creates a service if not already created. """

    @property
    def resource(self):
        return SvmNfs

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


class SvmNfs(Resource):

    _schema = SvmNfsSchema
