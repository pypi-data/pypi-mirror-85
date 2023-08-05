r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["LunClone", "LunCloneSchema"]
__pdoc__ = {
    "LunCloneSchema.resource": False,
    "LunClone": False,
}


class LunCloneSchema(ResourceSchema):
    """The fields of the LunClone object"""

    source = fields.Nested("netapp_ontap.models.lun_clone_source.LunCloneSourceSchema", unknown=EXCLUDE, data_key="source")
    r""" The source field of the lun_clone. """

    @property
    def resource(self):
        return LunClone

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "source",
    ]
    """source,"""

    postable_fields = [
        "source",
    ]
    """source,"""


class LunClone(Resource):

    _schema = LunCloneSchema
