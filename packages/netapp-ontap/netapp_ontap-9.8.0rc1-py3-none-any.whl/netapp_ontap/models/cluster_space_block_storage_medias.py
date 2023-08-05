r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["ClusterSpaceBlockStorageMedias", "ClusterSpaceBlockStorageMediasSchema"]
__pdoc__ = {
    "ClusterSpaceBlockStorageMediasSchema.resource": False,
    "ClusterSpaceBlockStorageMedias": False,
}


class ClusterSpaceBlockStorageMediasSchema(ResourceSchema):
    """The fields of the ClusterSpaceBlockStorageMedias object"""

    available = Size(data_key="available")
    r""" Available space """

    efficiency = fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", unknown=EXCLUDE, data_key="efficiency")
    r""" The efficiency field of the cluster_space_block_storage_medias. """

    size = Size(data_key="size")
    r""" Total space """

    type = fields.Str(data_key="type")
    r""" The type of media being used

Valid choices:

* hdd
* hybrid
* lun
* ssd
* vmdisk """

    used = Size(data_key="used")
    r""" Used space """

    @property
    def resource(self):
        return ClusterSpaceBlockStorageMedias

    gettable_fields = [
        "available",
        "efficiency",
        "size",
        "type",
        "used",
    ]
    """available,efficiency,size,type,used,"""

    patchable_fields = [
        "available",
        "efficiency",
        "size",
        "type",
        "used",
    ]
    """available,efficiency,size,type,used,"""

    postable_fields = [
        "available",
        "efficiency",
        "size",
        "type",
        "used",
    ]
    """available,efficiency,size,type,used,"""


class ClusterSpaceBlockStorageMedias(Resource):

    _schema = ClusterSpaceBlockStorageMediasSchema
