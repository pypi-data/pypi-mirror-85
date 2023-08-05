r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["DrGroupNodeIpInterfaces", "DrGroupNodeIpInterfacesSchema"]
__pdoc__ = {
    "DrGroupNodeIpInterfacesSchema.resource": False,
    "DrGroupNodeIpInterfaces": False,
}


class DrGroupNodeIpInterfacesSchema(ResourceSchema):
    """The fields of the DrGroupNodeIpInterfaces object"""

    ip = fields.Nested("netapp_ontap.models.ip_info.IpInfoSchema", unknown=EXCLUDE, data_key="ip")
    r""" The ip field of the dr_group_node_ip_interfaces. """

    port = fields.Str(data_key="port")
    r""" The port field of the dr_group_node_ip_interfaces.

Example: e1b """

    @property
    def resource(self):
        return DrGroupNodeIpInterfaces

    gettable_fields = [
        "ip",
        "port",
    ]
    """ip,port,"""

    patchable_fields = [
        "ip",
        "port",
    ]
    """ip,port,"""

    postable_fields = [
        "ip",
        "port",
    ]
    """ip,port,"""


class DrGroupNodeIpInterfaces(Resource):

    _schema = DrGroupNodeIpInterfacesSchema
