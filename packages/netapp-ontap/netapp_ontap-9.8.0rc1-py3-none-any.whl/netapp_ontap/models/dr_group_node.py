r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["DrGroupNode", "DrGroupNodeSchema"]
__pdoc__ = {
    "DrGroupNodeSchema.resource": False,
    "DrGroupNode": False,
}


class DrGroupNodeSchema(ResourceSchema):
    """The fields of the DrGroupNode object"""

    dr_ha_partners = fields.List(fields.Nested("netapp_ontap.models.dr_group_node_dr_ha_partners.DrGroupNodeDrHaPartnersSchema", unknown=EXCLUDE), data_key="dr_ha_partners")
    r""" The dr_ha_partners field of the dr_group_node. """

    dr_node = fields.Nested("netapp_ontap.models.dr_group_node_dr_ha_partners.DrGroupNodeDrHaPartnersSchema", unknown=EXCLUDE, data_key="dr_node")
    r""" The dr_node field of the dr_group_node. """

    ha_partners = fields.List(fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE), data_key="ha_partners")
    r""" The ha_partners field of the dr_group_node. """

    ip_interfaces = fields.List(fields.Nested("netapp_ontap.models.dr_group_node_ip_interfaces.DrGroupNodeIpInterfacesSchema", unknown=EXCLUDE), data_key="ip_interfaces")
    r""" The ip_interfaces field of the dr_group_node. """

    mirroring_enabled = fields.Boolean(data_key="mirroring_enabled")
    r""" The mirroring_enabled field of the dr_group_node. """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node")
    r""" The node field of the dr_group_node. """

    state = fields.Str(data_key="state")
    r""" The state field of the dr_group_node.

Valid choices:

* normal
* switchover_in_progress
* switchover_failed
* switchover_completed
* heal_aggrs_in_progress
* heal_aggrs_failed
* heal_aggrs_completed
* heal_roots_in_progress
* heal_roots_failed
* heal_roots_completed
* switchback_in_progress
* switchback_failed """

    @property
    def resource(self):
        return DrGroupNode

    gettable_fields = [
        "dr_ha_partners",
        "dr_node",
        "ha_partners.links",
        "ha_partners.name",
        "ha_partners.uuid",
        "ip_interfaces",
        "mirroring_enabled",
        "node.links",
        "node.name",
        "node.uuid",
        "state",
    ]
    """dr_ha_partners,dr_node,ha_partners.links,ha_partners.name,ha_partners.uuid,ip_interfaces,mirroring_enabled,node.links,node.name,node.uuid,state,"""

    patchable_fields = [
        "ip_interfaces",
    ]
    """ip_interfaces,"""

    postable_fields = [
        "dr_node",
        "ip_interfaces",
        "node.name",
        "node.uuid",
    ]
    """dr_node,ip_interfaces,node.name,node.uuid,"""


class DrGroupNode(Resource):

    _schema = DrGroupNodeSchema
