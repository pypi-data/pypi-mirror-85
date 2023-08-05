r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["VdiOnSanNewIgroups", "VdiOnSanNewIgroupsSchema"]
__pdoc__ = {
    "VdiOnSanNewIgroupsSchema.resource": False,
    "VdiOnSanNewIgroups": False,
}


class VdiOnSanNewIgroupsSchema(ResourceSchema):
    """The fields of the VdiOnSanNewIgroups object"""

    initiators = fields.List(fields.Str, data_key="initiators")
    r""" The initiators field of the vdi_on_san_new_igroups. """

    name = fields.Str(data_key="name")
    r""" The name of the new initiator group. """

    protocol = fields.Str(data_key="protocol")
    r""" The protocol of the new initiator group.

Valid choices:

* fcp
* iscsi
* mixed """

    @property
    def resource(self):
        return VdiOnSanNewIgroups

    gettable_fields = [
        "initiators",
    ]
    """initiators,"""

    patchable_fields = [
        "initiators",
        "name",
        "protocol",
    ]
    """initiators,name,protocol,"""

    postable_fields = [
        "initiators",
        "name",
        "protocol",
    ]
    """initiators,name,protocol,"""


class VdiOnSanNewIgroups(Resource):

    _schema = VdiOnSanNewIgroupsSchema
