r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

try:
    CLICHE_INSTALLED = False
    import cliche
    from cliche.arg_types.choices import Choices
    from cliche.commands import ClicheCommandError
    from netapp_ontap.resource_table import ResourceTable
    CLICHE_INSTALLED = True
except ImportError:
    pass

from marshmallow import fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["IgroupInitiator", "IgroupInitiatorSchema"]
__pdoc__ = {
    "IgroupInitiatorSchema.resource": False,
    "IgroupInitiator.igroup_initiator_show": False,
    "IgroupInitiator.igroup_initiator_create": False,
    "IgroupInitiator.igroup_initiator_modify": False,
    "IgroupInitiator.igroup_initiator_delete": False,
}


class IgroupInitiatorSchema(ResourceSchema):
    """The fields of the IgroupInitiator object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the igroup_initiator. """

    igroup = fields.Nested("netapp_ontap.models.igroup_initiator_igroup.IgroupInitiatorIgroupSchema", data_key="igroup", unknown=EXCLUDE)
    r""" The igroup field of the igroup_initiator. """

    name = fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=96),
    )
    r""" The FC WWPN, iSCSI IQN, or iSCSI EUI that identifies the host initiator. Valid in POST only and not allowed when the `records` property is used.<br/>
An FC WWPN consist of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters.


Example: iqn.1998-01.com.corp.iscsi:name1 """

    records = fields.List(fields.Nested("netapp_ontap.models.igroup_initiator_no_records.IgroupInitiatorNoRecordsSchema", unknown=EXCLUDE), data_key="records")
    r""" An array of initiators specified to add multiple initiators to an initiator group in a single API call. Valid in POST only and not allowed when the `name` property is used. """

    @property
    def resource(self):
        return IgroupInitiator

    gettable_fields = [
        "links",
        "igroup",
        "name",
    ]
    """links,igroup,name,"""

    patchable_fields = [
        "igroup",
    ]
    """igroup,"""

    postable_fields = [
        "igroup",
        "name",
        "records",
    ]
    """igroup,name,records,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in IgroupInitiator.get_collection(fields=field)]
    return getter

async def _wait_for_job(response: NetAppResponse) -> None:
    """Examine the given response. If it is a job, asynchronously wait for it to
    complete. While polling, prints the current status message of the job.
    """

    if not response.is_job:
        return
    from netapp_ontap.resources import Job
    job = Job(**response.http_response.json()["job"])
    while True:
        job.get(fields="state,message")
        if hasattr(job, "message"):
            print("[%s]: %s" % (job.state, job.message))
        if job.state == "failure":
            raise NetAppRestError("IgroupInitiator modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class IgroupInitiator(Resource):
    """Allows interaction with IgroupInitiator objects on the host"""

    _schema = IgroupInitiatorSchema
    _path = "/api/protocols/san/igroups/{igroup[uuid]}/initiators"
    _keys = ["igroup.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves initiators of an initiator group.
### Related ONTAP commands
* `lun igroup show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="igroup initiator show")
        def igroup_initiator_show(
            igroup_uuid,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["name", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of IgroupInitiator resources

            Args:
                name: The FC WWPN, iSCSI IQN, or iSCSI EUI that identifies the host initiator. Valid in POST only and not allowed when the `records` property is used.<br/> An FC WWPN consist of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters. 
            """

            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return IgroupInitiator.get_collection(
                igroup_uuid,
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves initiators of an initiator group.
### Related ONTAP commands
* `lun igroup show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)


    @classmethod
    def delete_collection(
        cls,
        *args,
        body: Union[Resource, dict] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an initiator from an initiator group.
### Related ONTAP commands
* `lun igroup remove`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves initiators of an initiator group.
### Related ONTAP commands
* `lun igroup show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an initiator of an initiator group.
### Related ONTAP commands
* `lun igroup show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Adds one or more initiators to an initiator group.
### Required properties
* `name` or `records.name` - Initiator name(s) to add to the initiator group.
### Related ONTAP commands
* `lun igroup add`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="igroup initiator create")
        async def igroup_initiator_create(
            igroup_uuid,
            links: dict = None,
            igroup: dict = None,
            name: str = None,
            records: dict = None,
        ) -> ResourceTable:
            """Create an instance of a IgroupInitiator resource

            Args:
                links: 
                igroup: 
                name: The FC WWPN, iSCSI IQN, or iSCSI EUI that identifies the host initiator. Valid in POST only and not allowed when the `records` property is used.<br/> An FC WWPN consist of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters. 
                records: An array of initiators specified to add multiple initiators to an initiator group in a single API call. Valid in POST only and not allowed when the `name` property is used. 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if igroup is not None:
                kwargs["igroup"] = igroup
            if name is not None:
                kwargs["name"] = name
            if records is not None:
                kwargs["records"] = records

            resource = IgroupInitiator(
                igroup_uuid,
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create IgroupInitiator: %s" % err)
            return [resource]


    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an initiator from an initiator group.
### Related ONTAP commands
* `lun igroup remove`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="igroup initiator delete")
        async def igroup_initiator_delete(
            igroup_uuid,
            name: str = None,
        ) -> None:
            """Delete an instance of a IgroupInitiator resource

            Args:
                name: The FC WWPN, iSCSI IQN, or iSCSI EUI that identifies the host initiator. Valid in POST only and not allowed when the `records` property is used.<br/> An FC WWPN consist of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters. 
            """

            kwargs = {}
            if name is not None:
                kwargs["name"] = name

            if hasattr(IgroupInitiator, "find"):
                resource = IgroupInitiator.find(
                    igroup_uuid,
                    **kwargs
                )
            else:
                resource = IgroupInitiator(igroup_uuid,)
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete IgroupInitiator: %s" % err)


