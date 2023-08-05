r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["AggregateBlockStoragePrimary", "AggregateBlockStoragePrimarySchema"]
__pdoc__ = {
    "AggregateBlockStoragePrimarySchema.resource": False,
    "AggregateBlockStoragePrimary": False,
}


class AggregateBlockStoragePrimarySchema(ResourceSchema):
    """The fields of the AggregateBlockStoragePrimary object"""

    checksum_style = fields.Str(data_key="checksum_style")
    r""" The checksum style used by the aggregate.

Valid choices:

* block
* advanced_zoned
* mixed """

    disk_class = fields.Str(data_key="disk_class")
    r""" The class of disks being used by the aggregate.

Valid choices:

* capacity
* performance
* archive
* solid_state
* array
* virtual
* data_center
* capacity_flash """

    disk_count = Size(data_key="disk_count")
    r""" Number of disks used in the aggregate. This includes parity disks, but excludes disks in the hybrid cache.

Example: 8 """

    disk_type = fields.Str(data_key="disk_type")
    r""" The type of disk being used by the aggregate.

Valid choices:

* fc
* lun
* nl_sas
* nvme_ssd
* sas
* sata
* scsi
* ssd
* ssd_cap
* vm_disk """

    raid_size = Size(data_key="raid_size")
    r""" Option to specify the maximum number of disks that can be included in a RAID group.

Example: 16 """

    raid_type = fields.Str(data_key="raid_type")
    r""" RAID type of the aggregate.

Valid choices:

* raid_dp
* raid_tec
* raid0
* raid4 """

    @property
    def resource(self):
        return AggregateBlockStoragePrimary

    gettable_fields = [
        "checksum_style",
        "disk_class",
        "disk_count",
        "disk_type",
        "raid_size",
        "raid_type",
    ]
    """checksum_style,disk_class,disk_count,disk_type,raid_size,raid_type,"""

    patchable_fields = [
        "disk_count",
        "raid_size",
        "raid_type",
    ]
    """disk_count,raid_size,raid_type,"""

    postable_fields = [
        "checksum_style",
        "disk_class",
        "disk_count",
        "raid_size",
        "raid_type",
    ]
    """checksum_style,disk_class,disk_count,raid_size,raid_type,"""


class AggregateBlockStoragePrimary(Resource):

    _schema = AggregateBlockStoragePrimarySchema
