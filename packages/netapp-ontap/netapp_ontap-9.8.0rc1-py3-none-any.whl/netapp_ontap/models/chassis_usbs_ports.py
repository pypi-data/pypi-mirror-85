r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["ChassisUsbsPorts", "ChassisUsbsPortsSchema"]
__pdoc__ = {
    "ChassisUsbsPortsSchema.resource": False,
    "ChassisUsbsPorts": False,
}


class ChassisUsbsPortsSchema(ResourceSchema):
    """The fields of the ChassisUsbsPorts object"""

    connected = fields.Boolean(data_key="connected")
    r""" Indicates whether or not the USB port has a device connected to it. """

    @property
    def resource(self):
        return ChassisUsbsPorts

    gettable_fields = [
        "connected",
    ]
    """connected,"""

    patchable_fields = [
        "connected",
    ]
    """connected,"""

    postable_fields = [
        "connected",
    ]
    """connected,"""


class ChassisUsbsPorts(Resource):

    _schema = ChassisUsbsPortsSchema
