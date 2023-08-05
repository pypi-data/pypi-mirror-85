r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["BgpPeerGroupPeer", "BgpPeerGroupPeerSchema"]
__pdoc__ = {
    "BgpPeerGroupPeerSchema.resource": False,
    "BgpPeerGroupPeer": False,
}


class BgpPeerGroupPeerSchema(ResourceSchema):
    """The fields of the BgpPeerGroupPeer object"""

    address = fields.Str(data_key="address")
    r""" Peer router address

Example: 10.10.10.7 """

    asn = Size(data_key="asn")
    r""" Autonomous system number of peer """

    @property
    def resource(self):
        return BgpPeerGroupPeer

    gettable_fields = [
        "address",
        "asn",
    ]
    """address,asn,"""

    patchable_fields = [
        "address",
    ]
    """address,"""

    postable_fields = [
        "address",
        "asn",
    ]
    """address,asn,"""


class BgpPeerGroupPeer(Resource):

    _schema = BgpPeerGroupPeerSchema
