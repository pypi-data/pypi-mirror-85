r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["ZappS3BucketApplicationComponentsExcludeAggregates", "ZappS3BucketApplicationComponentsExcludeAggregatesSchema"]
__pdoc__ = {
    "ZappS3BucketApplicationComponentsExcludeAggregatesSchema.resource": False,
    "ZappS3BucketApplicationComponentsExcludeAggregates": False,
}


class ZappS3BucketApplicationComponentsExcludeAggregatesSchema(ResourceSchema):
    """The fields of the ZappS3BucketApplicationComponentsExcludeAggregates object"""

    name = fields.Str(data_key="name")
    r""" The name of the aggregate to exclude. Usage: &lt;aggregate name&gt; """

    uuid = fields.Str(data_key="uuid")
    r""" The ID of the aggregate to exclude. Usage: &lt;UUID&gt; """

    @property
    def resource(self):
        return ZappS3BucketApplicationComponentsExcludeAggregates

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class ZappS3BucketApplicationComponentsExcludeAggregates(Resource):

    _schema = ZappS3BucketApplicationComponentsExcludeAggregatesSchema
