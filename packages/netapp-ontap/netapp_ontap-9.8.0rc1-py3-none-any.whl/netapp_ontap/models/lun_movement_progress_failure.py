r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["LunMovementProgressFailure", "LunMovementProgressFailureSchema"]
__pdoc__ = {
    "LunMovementProgressFailureSchema.resource": False,
    "LunMovementProgressFailure": False,
}


class LunMovementProgressFailureSchema(ResourceSchema):
    """The fields of the LunMovementProgressFailure object"""

    code = fields.Str(data_key="code")
    r""" The error code.


Example: 4 """

    message = fields.Str(data_key="message")
    r""" The error message.


Example: Destination volume is offline. """

    @property
    def resource(self):
        return LunMovementProgressFailure

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class LunMovementProgressFailure(Resource):

    _schema = LunMovementProgressFailureSchema
