r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["VolumeSpace", "VolumeSpaceSchema"]
__pdoc__ = {
    "VolumeSpaceSchema.resource": False,
    "VolumeSpace": False,
}


class VolumeSpaceSchema(ResourceSchema):
    """The fields of the VolumeSpace object"""

    available = Size(data_key="available")
    r""" The available space, in bytes. """

    block_storage_inactive_user_data = Size(data_key="block_storage_inactive_user_data")
    r""" The size that is physically used in the block storage of the volume and has a cold temperature. In bytes. This parameter is only supported if the volume is in an aggregate that is either attached to a cloud store or could be attached to a cloud store. """

    capacity_tier_footprint = Size(data_key="capacity_tier_footprint")
    r""" Space used by capacity tier for this volume in the FabricPool aggregate, in bytes. """

    footprint = Size(data_key="footprint")
    r""" Data used for this volume in the aggregate, in bytes. """

    local_tier_footprint = Size(data_key="local_tier_footprint")
    r""" Space used by the local tier for this volume in the aggregate, in bytes. """

    logical_space = fields.Nested("netapp_ontap.models.volume_space_logical_space.VolumeSpaceLogicalSpaceSchema", unknown=EXCLUDE, data_key="logical_space")
    r""" The logical_space field of the volume_space. """

    metadata = Size(data_key="metadata")
    r""" Space used by the volume metadata in the aggregate, in bytes. """

    over_provisioned = Size(data_key="over_provisioned")
    r""" The amount of space not available for this volume in the aggregate, in bytes. """

    performance_tier_footprint = Size(data_key="performance_tier_footprint")
    r""" Space used by the performance tier for this volume in the FabricPool aggregate, in bytes. """

    size = Size(data_key="size")
    r""" Total provisioned size. The default size is equal to the minimum size of 20MB, in bytes. """

    snapshot = fields.Nested("netapp_ontap.models.volume_space_snapshot.VolumeSpaceSnapshotSchema", unknown=EXCLUDE, data_key="snapshot")
    r""" The snapshot field of the volume_space. """

    total_footprint = Size(data_key="total_footprint")
    r""" Data and metadata used for this volume in the aggregate, in bytes. """

    used = Size(data_key="used")
    r""" The virtual space used (includes volume reserves) before storage efficiency, in bytes. """

    @property
    def resource(self):
        return VolumeSpace

    gettable_fields = [
        "available",
        "block_storage_inactive_user_data",
        "capacity_tier_footprint",
        "footprint",
        "local_tier_footprint",
        "logical_space",
        "metadata",
        "over_provisioned",
        "performance_tier_footprint",
        "size",
        "snapshot",
        "total_footprint",
        "used",
    ]
    """available,block_storage_inactive_user_data,capacity_tier_footprint,footprint,local_tier_footprint,logical_space,metadata,over_provisioned,performance_tier_footprint,size,snapshot,total_footprint,used,"""

    patchable_fields = [
        "logical_space",
        "size",
        "snapshot",
    ]
    """logical_space,size,snapshot,"""

    postable_fields = [
        "logical_space",
        "size",
        "snapshot",
    ]
    """logical_space,size,snapshot,"""


class VolumeSpace(Resource):

    _schema = VolumeSpaceSchema
