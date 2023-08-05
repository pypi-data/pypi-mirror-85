r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["EventRemediationsSource", "EventRemediationsSourceSchema"]
__pdoc__ = {
    "EventRemediationsSourceSchema.resource": False,
    "EventRemediationsSource": False,
}


class EventRemediationsSourceSchema(ResourceSchema):
    """The fields of the EventRemediationsSource object"""

    object_id = Size(data_key="object_id")
    r""" The object_id field of the event_remediations_source.

Example: 5666 """

    object_type = fields.Str(data_key="object_type")
    r""" The object_type field of the event_remediations_source.

Valid choices:

* inventory.ontap.fas.Cluster """

    @property
    def resource(self):
        return EventRemediationsSource

    gettable_fields = [
        "object_id",
        "object_type",
    ]
    """object_id,object_type,"""

    patchable_fields = [
        "object_id",
        "object_type",
    ]
    """object_id,object_type,"""

    postable_fields = [
        "object_id",
        "object_type",
    ]
    """object_id,object_type,"""


class EventRemediationsSource(Resource):

    _schema = EventRemediationsSourceSchema
