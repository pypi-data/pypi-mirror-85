r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["ChassisPcisCards", "ChassisPcisCardsSchema"]
__pdoc__ = {
    "ChassisPcisCardsSchema.resource": False,
    "ChassisPcisCards": False,
}


class ChassisPcisCardsSchema(ResourceSchema):
    """The fields of the ChassisPcisCards object"""

    device = fields.Str(data_key="device")
    r""" The description of the PCI card.

Example: Intel Lewisburg series chipset SATA Controller """

    info = fields.Str(data_key="info")
    r""" The info string from the device driver of the PCI card.

Example: Additional Info: 0 (0xaaf00000)   SHM2S86Q120GLM22NP FW1146 114473MB 512B/sect (SPG190108GW) """

    slot = fields.Str(data_key="slot")
    r""" The slot where the PCI card is placed. This can sometimes take the form of "6-1" to indicate slot and subslot.

Example: 0 """

    @property
    def resource(self):
        return ChassisPcisCards

    gettable_fields = [
        "device",
        "info",
        "slot",
    ]
    """device,info,slot,"""

    patchable_fields = [
        "device",
        "info",
        "slot",
    ]
    """device,info,slot,"""

    postable_fields = [
        "device",
        "info",
        "slot",
    ]
    """device,info,slot,"""


class ChassisPcisCards(Resource):

    _schema = ChassisPcisCardsSchema
