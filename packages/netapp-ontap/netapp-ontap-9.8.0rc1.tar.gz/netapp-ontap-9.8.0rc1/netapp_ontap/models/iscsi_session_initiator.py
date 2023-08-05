r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["IscsiSessionInitiator", "IscsiSessionInitiatorSchema"]
__pdoc__ = {
    "IscsiSessionInitiatorSchema.resource": False,
    "IscsiSessionInitiator": False,
}


class IscsiSessionInitiatorSchema(ResourceSchema):
    """The fields of the IscsiSessionInitiator object"""

    alias = fields.Str(data_key="alias")
    r""" The initiator alias.


Example: initiator_alias1 """

    name = fields.Str(data_key="name")
    r""" The world wide unique name of the initiator.


Example: iqn.1992-01.example.com:string """

    @property
    def resource(self):
        return IscsiSessionInitiator

    gettable_fields = [
        "alias",
        "name",
    ]
    """alias,name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class IscsiSessionInitiator(Resource):

    _schema = IscsiSessionInitiatorSchema
