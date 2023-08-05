r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["ChassisUsbs", "ChassisUsbsSchema"]
__pdoc__ = {
    "ChassisUsbsSchema.resource": False,
    "ChassisUsbs": False,
}


class ChassisUsbsSchema(ResourceSchema):
    """The fields of the ChassisUsbs object"""

    enabled = fields.Boolean(data_key="enabled")
    r""" Indicates whether or not the USB ports are enabled. """

    ports = fields.List(fields.Nested("netapp_ontap.models.chassis_usbs_ports.ChassisUsbsPortsSchema", unknown=EXCLUDE), data_key="ports")
    r""" The ports field of the chassis_usbs. """

    supported = fields.Boolean(data_key="supported")
    r""" Indicates whether or not USB ports are supported on the current platform. """

    @property
    def resource(self):
        return ChassisUsbs

    gettable_fields = [
        "enabled",
        "ports",
        "supported",
    ]
    """enabled,ports,supported,"""

    patchable_fields = [
        "enabled",
        "ports",
        "supported",
    ]
    """enabled,ports,supported,"""

    postable_fields = [
        "enabled",
        "ports",
        "supported",
    ]
    """enabled,ports,supported,"""


class ChassisUsbs(Resource):

    _schema = ChassisUsbsSchema
