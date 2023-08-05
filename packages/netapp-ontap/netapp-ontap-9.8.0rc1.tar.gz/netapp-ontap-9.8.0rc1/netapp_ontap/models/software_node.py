r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["SoftwareNode", "SoftwareNodeSchema"]
__pdoc__ = {
    "SoftwareNodeSchema.resource": False,
    "SoftwareNode": False,
}


class SoftwareNodeSchema(ResourceSchema):
    """The fields of the SoftwareNode object"""

    firmware = fields.Nested("netapp_ontap.models.firmware.FirmwareSchema", unknown=EXCLUDE, data_key="firmware")
    r""" The firmware field of the software_node. """

    name = fields.Str(data_key="name")
    r""" Name of the node.

Example: node1 """

    version = fields.Str(data_key="version")
    r""" ONTAP version of the node.

Example: ONTAP_X """

    @property
    def resource(self):
        return SoftwareNode

    gettable_fields = [
        "firmware",
        "name",
        "version",
    ]
    """firmware,name,version,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SoftwareNode(Resource):

    _schema = SoftwareNodeSchema
