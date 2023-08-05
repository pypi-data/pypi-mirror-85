r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["VolumeSnapmirror", "VolumeSnapmirrorSchema"]
__pdoc__ = {
    "VolumeSnapmirrorSchema.resource": False,
    "VolumeSnapmirror": False,
}


class VolumeSnapmirrorSchema(ResourceSchema):
    """The fields of the VolumeSnapmirror object"""

    is_protected = fields.Boolean(data_key="is_protected")
    r""" Specifies whether a volume is a SnapMirror source volume, using SnapMirror to protect its data. """

    @property
    def resource(self):
        return VolumeSnapmirror

    gettable_fields = [
        "is_protected",
    ]
    """is_protected,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class VolumeSnapmirror(Resource):

    _schema = VolumeSnapmirrorSchema
