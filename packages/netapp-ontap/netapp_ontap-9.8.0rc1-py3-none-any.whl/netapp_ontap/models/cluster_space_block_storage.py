r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["ClusterSpaceBlockStorage", "ClusterSpaceBlockStorageSchema"]
__pdoc__ = {
    "ClusterSpaceBlockStorageSchema.resource": False,
    "ClusterSpaceBlockStorage": False,
}


class ClusterSpaceBlockStorageSchema(ResourceSchema):
    """The fields of the ClusterSpaceBlockStorage object"""

    inactive_data = Size(data_key="inactive_data")
    r""" Inactive data across all aggregates """

    medias = fields.List(fields.Nested("netapp_ontap.models.cluster_space_block_storage_medias.ClusterSpaceBlockStorageMediasSchema", unknown=EXCLUDE), data_key="medias")
    r""" The medias field of the cluster_space_block_storage. """

    size = Size(data_key="size")
    r""" Total space across the cluster """

    used = Size(data_key="used")
    r""" Space used (includes volume reserves) """

    @property
    def resource(self):
        return ClusterSpaceBlockStorage

    gettable_fields = [
        "inactive_data",
        "medias",
        "size",
        "used",
    ]
    """inactive_data,medias,size,used,"""

    patchable_fields = [
        "inactive_data",
        "medias",
        "size",
        "used",
    ]
    """inactive_data,medias,size,used,"""

    postable_fields = [
        "inactive_data",
        "medias",
        "size",
        "used",
    ]
    """inactive_data,medias,size,used,"""


class ClusterSpaceBlockStorage(Resource):

    _schema = ClusterSpaceBlockStorageSchema
