r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["MonitoredFileVolume", "MonitoredFileVolumeSchema"]
__pdoc__ = {
    "MonitoredFileVolumeSchema.resource": False,
    "MonitoredFileVolume": False,
}


class MonitoredFileVolumeSchema(ResourceSchema):
    """The fields of the MonitoredFileVolume object"""

    name = fields.Str(data_key="name")
    r""" The name of the volume.

Example: volume1 """

    uuid = fields.Str(data_key="uuid")
    r""" The UUID of the volume.

Example: 028baa66-41bd-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return MonitoredFileVolume

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class MonitoredFileVolume(Resource):

    _schema = MonitoredFileVolumeSchema
