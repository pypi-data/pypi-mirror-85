r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["SnapmirrorDestinationCreation", "SnapmirrorDestinationCreationSchema"]
__pdoc__ = {
    "SnapmirrorDestinationCreationSchema.resource": False,
    "SnapmirrorDestinationCreation": False,
}


class SnapmirrorDestinationCreationSchema(ResourceSchema):
    """The fields of the SnapmirrorDestinationCreation object"""

    enabled = fields.Boolean(data_key="enabled")
    r""" Optional property to create the destination endpoint when establishing a SnapMirror relationship. It is assumed to be "false" if no other property is set and assumed to be "true" if any other property is set. """

    storage_service = fields.Nested("netapp_ontap.models.snapmirror_destination_creation_storage_service.SnapmirrorDestinationCreationStorageServiceSchema", unknown=EXCLUDE, data_key="storage_service")
    r""" The storage_service field of the snapmirror_destination_creation. """

    tiering = fields.Nested("netapp_ontap.models.snapmirror_destination_creation_tiering.SnapmirrorDestinationCreationTieringSchema", unknown=EXCLUDE, data_key="tiering")
    r""" The tiering field of the snapmirror_destination_creation. """

    @property
    def resource(self):
        return SnapmirrorDestinationCreation

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "enabled",
        "storage_service",
        "tiering",
    ]
    """enabled,storage_service,tiering,"""


class SnapmirrorDestinationCreation(Resource):

    _schema = SnapmirrorDestinationCreationSchema
