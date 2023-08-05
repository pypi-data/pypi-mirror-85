r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["GcpKmsState", "GcpKmsStateSchema"]
__pdoc__ = {
    "GcpKmsStateSchema.resource": False,
    "GcpKmsState": False,
}


class GcpKmsStateSchema(ResourceSchema):
    """The fields of the GcpKmsState object"""

    cluster_state = fields.Boolean(data_key="cluster_state")
    r""" Set to true when Google Cloud KMS key protection is available on all nodes of the cluster. """

    code = Size(data_key="code")
    r""" Error code corresponding to the status message. Returns 0 if Google Cloud KMS key protection is available in all nodes of the cluster.

Example: 346758 """

    message = fields.Str(data_key="message")
    r""" Error message set when cluster availability is false. This field will be empty when cluster availability is true. Cluster availability refers to the cluster-wide state of the embedded KMIP server's client on all nodes.

Example: Google Cloud KMS key protection is unavailable in following nodes - node1, node2. """

    @property
    def resource(self):
        return GcpKmsState

    gettable_fields = [
        "cluster_state",
        "code",
        "message",
    ]
    """cluster_state,code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class GcpKmsState(Resource):

    _schema = GcpKmsStateSchema
