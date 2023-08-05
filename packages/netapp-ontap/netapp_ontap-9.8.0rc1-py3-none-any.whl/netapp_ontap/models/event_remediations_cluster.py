r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["EventRemediationsCluster", "EventRemediationsClusterSchema"]
__pdoc__ = {
    "EventRemediationsClusterSchema.resource": False,
    "EventRemediationsCluster": False,
}


class EventRemediationsClusterSchema(ResourceSchema):
    """The fields of the EventRemediationsCluster object"""

    name = fields.Str(data_key="name")
    r""" The name field of the event_remediations_cluster.

Example: cluster1 """

    uuid = fields.Str(data_key="uuid")
    r""" The uuid field of the event_remediations_cluster.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return EventRemediationsCluster

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class EventRemediationsCluster(Resource):

    _schema = EventRemediationsClusterSchema
