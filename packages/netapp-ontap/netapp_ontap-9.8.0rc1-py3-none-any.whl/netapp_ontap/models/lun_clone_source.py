r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["LunCloneSource", "LunCloneSourceSchema"]
__pdoc__ = {
    "LunCloneSourceSchema.resource": False,
    "LunCloneSource": False,
}


class LunCloneSourceSchema(ResourceSchema):
    """The fields of the LunCloneSource object"""

    name = fields.Str(data_key="name")
    r""" The fully qualified path name of the clone source LUN composed of a "/vol" prefix, the volume name, the (optional) qtree name, and base name of the LUN. Valid in POST and PATCH.


Example: /vol/volume1/lun1 """

    uuid = fields.Str(data_key="uuid")
    r""" The unique identifier of the clone source LUN. Valid in POST and PATCH.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return LunCloneSource

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class LunCloneSource(Resource):

    _schema = LunCloneSourceSchema
