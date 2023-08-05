r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["MonitoredFileSvm", "MonitoredFileSvmSchema"]
__pdoc__ = {
    "MonitoredFileSvmSchema.resource": False,
    "MonitoredFileSvm": False,
}


class MonitoredFileSvmSchema(ResourceSchema):
    """The fields of the MonitoredFileSvm object"""

    name = fields.Str(data_key="name")
    r""" The name of the svm.

Example: svm1 """

    uuid = fields.Str(data_key="uuid")
    r""" The UUID of the svm.

Example: 028baa66-41bd-11e9-81d5-00a0986138f7 """

    @property
    def resource(self):
        return MonitoredFileSvm

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class MonitoredFileSvm(Resource):

    _schema = MonitoredFileSvmSchema
