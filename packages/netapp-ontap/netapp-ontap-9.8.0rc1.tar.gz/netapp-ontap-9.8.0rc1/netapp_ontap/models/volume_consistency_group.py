r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["VolumeConsistencyGroup", "VolumeConsistencyGroupSchema"]
__pdoc__ = {
    "VolumeConsistencyGroupSchema.resource": False,
    "VolumeConsistencyGroup": False,
}


class VolumeConsistencyGroupSchema(ResourceSchema):
    """The fields of the VolumeConsistencyGroup object"""

    name = fields.Str(data_key="name")
    r""" Name of the consistency group.

Example: consistency_group_1 """

    @property
    def resource(self):
        return VolumeConsistencyGroup

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class VolumeConsistencyGroup(Resource):

    _schema = VolumeConsistencyGroupSchema
