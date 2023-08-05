r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["FileMoveFilesToMove", "FileMoveFilesToMoveSchema"]
__pdoc__ = {
    "FileMoveFilesToMoveSchema.resource": False,
    "FileMoveFilesToMove": False,
}


class FileMoveFilesToMoveSchema(ResourceSchema):
    """The fields of the FileMoveFilesToMove object"""

    destination = fields.Nested("netapp_ontap.models.file.FileSchema", unknown=EXCLUDE, data_key="destination")
    r""" The destination field of the file_move_files_to_move. """

    source = fields.Nested("netapp_ontap.models.file.FileSchema", unknown=EXCLUDE, data_key="source")
    r""" The source field of the file_move_files_to_move. """

    @property
    def resource(self):
        return FileMoveFilesToMove

    gettable_fields = [
        "destination.path",
        "destination.svm",
        "destination.volume",
        "source.path",
        "source.svm",
        "source.volume",
    ]
    """destination.path,destination.svm,destination.volume,source.path,source.svm,source.volume,"""

    patchable_fields = [
        "destination.path",
        "destination.svm",
        "destination.volume",
        "source.path",
        "source.svm",
        "source.volume",
    ]
    """destination.path,destination.svm,destination.volume,source.path,source.svm,source.volume,"""

    postable_fields = [
        "destination.path",
        "destination.svm",
        "destination.volume",
        "source.path",
        "source.svm",
        "source.volume",
    ]
    """destination.path,destination.svm,destination.volume,source.path,source.svm,source.volume,"""


class FileMoveFilesToMove(Resource):

    _schema = FileMoveFilesToMoveSchema
