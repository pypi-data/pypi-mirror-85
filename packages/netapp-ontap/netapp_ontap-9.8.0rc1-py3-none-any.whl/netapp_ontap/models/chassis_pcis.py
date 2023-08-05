r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["ChassisPcis", "ChassisPcisSchema"]
__pdoc__ = {
    "ChassisPcisSchema.resource": False,
    "ChassisPcis": False,
}


class ChassisPcisSchema(ResourceSchema):
    """The fields of the ChassisPcis object"""

    cards = fields.List(fields.Nested("netapp_ontap.models.chassis_pcis_cards.ChassisPcisCardsSchema", unknown=EXCLUDE), data_key="cards")
    r""" The cards field of the chassis_pcis. """

    @property
    def resource(self):
        return ChassisPcis

    gettable_fields = [
        "cards",
    ]
    """cards,"""

    patchable_fields = [
        "cards",
    ]
    """cards,"""

    postable_fields = [
        "cards",
    ]
    """cards,"""


class ChassisPcis(Resource):

    _schema = ChassisPcisSchema
