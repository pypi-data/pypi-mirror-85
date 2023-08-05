r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["NasFlexcache", "NasFlexcacheSchema"]
__pdoc__ = {
    "NasFlexcacheSchema.resource": False,
    "NasFlexcache": False,
}


class NasFlexcacheSchema(ResourceSchema):
    """The fields of the NasFlexcache object"""

    origin = fields.Nested("netapp_ontap.models.nas_flexcache_origin.NasFlexcacheOriginSchema", unknown=EXCLUDE, data_key="origin")
    r""" The origin field of the nas_flexcache. """

    @property
    def resource(self):
        return NasFlexcache

    gettable_fields = [
        "origin",
    ]
    """origin,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "origin",
    ]
    """origin,"""


class NasFlexcache(Resource):

    _schema = NasFlexcacheSchema
