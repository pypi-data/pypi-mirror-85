r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["FileMoveReferenceFile", "FileMoveReferenceFileSchema"]
__pdoc__ = {
    "FileMoveReferenceFileSchema.resource": False,
    "FileMoveReferenceFile": False,
}


class FileMoveReferenceFileSchema(ResourceSchema):
    """The fields of the FileMoveReferenceFile object"""

    path = fields.Str(data_key="path")
    r""" The source reference file. If a reference file is specified, data for other files being moved will be transferred as a difference from the reference file. This can save bandwidth and destination storage if the specified source files share blocks. If provided, this input must match one of the source file paths. This input need not be provided if only one source file is specified. """

    volume = fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume")
    r""" The volume field of the file_move_reference_file. """

    @property
    def resource(self):
        return FileMoveReferenceFile

    gettable_fields = [
        "path",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """path,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "path",
        "volume.name",
        "volume.uuid",
    ]
    """path,volume.name,volume.uuid,"""

    postable_fields = [
        "path",
        "volume.name",
        "volume.uuid",
    ]
    """path,volume.name,volume.uuid,"""


class FileMoveReferenceFile(Resource):

    _schema = FileMoveReferenceFileSchema
