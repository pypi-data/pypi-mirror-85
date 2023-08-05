r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["NvmeNamespaceLocation", "NvmeNamespaceLocationSchema"]
__pdoc__ = {
    "NvmeNamespaceLocationSchema.resource": False,
    "NvmeNamespaceLocation": False,
}


class NvmeNamespaceLocationSchema(ResourceSchema):
    """The fields of the NvmeNamespaceLocation object"""

    namespace = fields.Str(data_key="namespace")
    r""" The base name component of the NVMe namespace. Valid in POST.<br/>
If properties `name` and `location.namespace` are specified in the same request, they must refer to the base name.<br/>
NVMe namespaces do not support rename.


Example: namespace1 """

    qtree = fields.Nested("netapp_ontap.resources.qtree.QtreeSchema", unknown=EXCLUDE, data_key="qtree")
    r""" The qtree field of the nvme_namespace_location. """

    volume = fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume")
    r""" The volume field of the nvme_namespace_location. """

    @property
    def resource(self):
        return NvmeNamespaceLocation

    gettable_fields = [
        "namespace",
        "qtree.links",
        "qtree.id",
        "qtree.name",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """namespace,qtree.links,qtree.id,qtree.name,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "namespace",
        "qtree.id",
        "qtree.name",
        "volume.name",
        "volume.uuid",
    ]
    """namespace,qtree.id,qtree.name,volume.name,volume.uuid,"""


class NvmeNamespaceLocation(Resource):

    _schema = NvmeNamespaceLocationSchema
