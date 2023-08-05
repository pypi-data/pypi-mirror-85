r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["DrGroupNodeDrHaPartners", "DrGroupNodeDrHaPartnersSchema"]
__pdoc__ = {
    "DrGroupNodeDrHaPartnersSchema.resource": False,
    "DrGroupNodeDrHaPartners": False,
}


class DrGroupNodeDrHaPartnersSchema(ResourceSchema):
    """The fields of the DrGroupNodeDrHaPartners object"""

    name = fields.Str(data_key="name")
    r""" The name field of the dr_group_node_dr_ha_partners.

Example: node1 """

    uuid = fields.Str(data_key="uuid")
    r""" The uuid field of the dr_group_node_dr_ha_partners.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return DrGroupNodeDrHaPartners

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

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


class DrGroupNodeDrHaPartners(Resource):

    _schema = DrGroupNodeDrHaPartnersSchema
