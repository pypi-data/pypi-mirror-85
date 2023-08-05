r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["SvmCifsService", "SvmCifsServiceSchema"]
__pdoc__ = {
    "SvmCifsServiceSchema.resource": False,
    "SvmCifsService": False,
}


class SvmCifsServiceSchema(ResourceSchema):
    """The fields of the SvmCifsService object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the svm_cifs_service. """

    ad_domain = fields.Nested("netapp_ontap.models.ad_domain_svm.AdDomainSvmSchema", unknown=EXCLUDE, data_key="ad_domain")
    r""" The ad_domain field of the svm_cifs_service. """

    enabled = fields.Boolean(data_key="enabled")
    r""" Specifies whether or not the CIFS service is administratively enabled. """

    name = fields.Str(data_key="name")
    r""" The NetBIOS name of the CIFS server.

Example: CIFS1 """

    @property
    def resource(self):
        return SvmCifsService

    gettable_fields = [
        "links",
        "ad_domain",
        "enabled",
        "name",
    ]
    """links,ad_domain,enabled,name,"""

    patchable_fields = [
        "ad_domain",
        "enabled",
        "name",
    ]
    """ad_domain,enabled,name,"""

    postable_fields = [
        "ad_domain",
        "enabled",
        "name",
    ]
    """ad_domain,enabled,name,"""


class SvmCifsService(Resource):

    _schema = SvmCifsServiceSchema
