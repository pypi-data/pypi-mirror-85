r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["ServiceProcessor", "ServiceProcessorSchema"]
__pdoc__ = {
    "ServiceProcessorSchema.resource": False,
    "ServiceProcessor": False,
}


class ServiceProcessorSchema(ResourceSchema):
    """The fields of the ServiceProcessor object"""

    dhcp_enabled = fields.Boolean(data_key="dhcp_enabled")
    r""" Set to "true" to use DHCP to configure an IPv4 interface. """

    firmware_version = fields.Str(data_key="firmware_version")
    r""" The version of firmware installed. """

    ipv4_interface = fields.Nested("netapp_ontap.models.ip_interface_and_gateway.IpInterfaceAndGatewaySchema", unknown=EXCLUDE, data_key="ipv4_interface")
    r""" The ipv4_interface field of the service_processor. """

    ipv6_interface = fields.Nested("netapp_ontap.models.ipv6_interface_and_gateway.Ipv6InterfaceAndGatewaySchema", unknown=EXCLUDE, data_key="ipv6_interface")
    r""" The ipv6_interface field of the service_processor. """

    link_status = fields.Str(data_key="link_status")
    r""" The link_status field of the service_processor.

Valid choices:

* up
* down
* disabled
* unknown """

    mac_address = fields.Str(data_key="mac_address")
    r""" The mac_address field of the service_processor. """

    state = fields.Str(data_key="state")
    r""" The state field of the service_processor.

Valid choices:

* online
* offline
* degraded
* rebooting
* unknown
* updating
* node_offline
* sp_daemon_offline """

    @property
    def resource(self):
        return ServiceProcessor

    gettable_fields = [
        "dhcp_enabled",
        "firmware_version",
        "ipv4_interface",
        "ipv6_interface",
        "link_status",
        "mac_address",
        "state",
    ]
    """dhcp_enabled,firmware_version,ipv4_interface,ipv6_interface,link_status,mac_address,state,"""

    patchable_fields = [
        "dhcp_enabled",
        "ipv4_interface",
        "ipv6_interface",
    ]
    """dhcp_enabled,ipv4_interface,ipv6_interface,"""

    postable_fields = [
        "ipv4_interface",
    ]
    """ipv4_interface,"""


class ServiceProcessor(Resource):

    _schema = ServiceProcessorSchema
