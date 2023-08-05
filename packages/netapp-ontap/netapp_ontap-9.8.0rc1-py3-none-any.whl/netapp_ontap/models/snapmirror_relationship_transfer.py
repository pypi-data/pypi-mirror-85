r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["SnapmirrorRelationshipTransfer", "SnapmirrorRelationshipTransferSchema"]
__pdoc__ = {
    "SnapmirrorRelationshipTransferSchema.resource": False,
    "SnapmirrorRelationshipTransfer": False,
}


class SnapmirrorRelationshipTransferSchema(ResourceSchema):
    """The fields of the SnapmirrorRelationshipTransfer object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the snapmirror_relationship_transfer. """

    bytes_transferred = Size(data_key="bytes_transferred")
    r""" Bytes transferred. """

    state = fields.Str(data_key="state")
    r""" The state field of the snapmirror_relationship_transfer.

Valid choices:

* aborted
* failed
* hard_aborted
* queued
* success
* transferring """

    uuid = fields.Str(data_key="uuid")
    r""" The uuid field of the snapmirror_relationship_transfer.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return SnapmirrorRelationshipTransfer

    gettable_fields = [
        "links",
        "bytes_transferred",
        "state",
        "uuid",
    ]
    """links,bytes_transferred,state,uuid,"""

    patchable_fields = [
        "bytes_transferred",
        "state",
        "uuid",
    ]
    """bytes_transferred,state,uuid,"""

    postable_fields = [
        "bytes_transferred",
        "state",
        "uuid",
    ]
    """bytes_transferred,state,uuid,"""


class SnapmirrorRelationshipTransfer(Resource):

    _schema = SnapmirrorRelationshipTransferSchema
