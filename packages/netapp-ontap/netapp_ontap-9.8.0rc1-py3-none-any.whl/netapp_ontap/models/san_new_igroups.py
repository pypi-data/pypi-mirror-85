r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["SanNewIgroups", "SanNewIgroupsSchema"]
__pdoc__ = {
    "SanNewIgroupsSchema.resource": False,
    "SanNewIgroups": False,
}


class SanNewIgroupsSchema(ResourceSchema):
    """The fields of the SanNewIgroups object"""

    initiators = fields.List(fields.Str, data_key="initiators")
    r""" The initiators field of the san_new_igroups. """

    name = fields.Str(data_key="name")
    r""" The name of the new initiator group. """

    os_type = fields.Str(data_key="os_type")
    r""" The name of the host OS accessing the application. The default value is the host OS that is running the application.

Valid choices:

* aix
* hpux
* hyper_v
* linux
* netware
* openvms
* solaris
* vmware
* windows
* xen """

    protocol = fields.Str(data_key="protocol")
    r""" The protocol of the new initiator group.

Valid choices:

* fcp
* iscsi
* mixed """

    @property
    def resource(self):
        return SanNewIgroups

    gettable_fields = [
        "initiators",
    ]
    """initiators,"""

    patchable_fields = [
        "initiators",
        "name",
        "os_type",
        "protocol",
    ]
    """initiators,name,os_type,protocol,"""

    postable_fields = [
        "initiators",
        "name",
        "os_type",
        "protocol",
    ]
    """initiators,name,os_type,protocol,"""


class SanNewIgroups(Resource):

    _schema = SanNewIgroupsSchema
