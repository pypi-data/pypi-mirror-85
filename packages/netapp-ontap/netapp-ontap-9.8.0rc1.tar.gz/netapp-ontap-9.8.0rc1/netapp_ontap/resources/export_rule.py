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


__all__ = ["ExportRule", "ExportRuleSchema"]
__pdoc__ = {
    "ExportRuleSchema.resource": False,
    "ExportRule.export_rule_show": False,
    "ExportRule.export_rule_create": False,
    "ExportRule.export_rule_modify": False,
    "ExportRule.export_rule_delete": False,
}


class ExportRuleSchema(ResourceSchema):
    """The fields of the ExportRule object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the export_rule. """

    anonymous_user = fields.Str(
        data_key="anonymous_user",
    )
    r""" User ID To Which Anonymous Users Are Mapped. """

    clients = fields.List(fields.Nested("netapp_ontap.resources.export_client.ExportClientSchema", unknown=EXCLUDE), data_key="clients")
    r""" Array of client matches """

    index = Size(
        data_key="index",
    )
    r""" Index of the rule within the export policy. """

    protocols = fields.List(fields.Str, data_key="protocols")
    r""" The protocols field of the export_rule. """

    ro_rule = fields.List(fields.Str, data_key="ro_rule")
    r""" Authentication flavors that the read-only access rule governs """

    rw_rule = fields.List(fields.Str, data_key="rw_rule")
    r""" Authentication flavors that the read/write access rule governs """

    superuser = fields.List(fields.Str, data_key="superuser")
    r""" Authentication flavors that the superuser security type governs """

    @property
    def resource(self):
        return ExportRule

    gettable_fields = [
        "links",
        "anonymous_user",
        "clients",
        "index",
        "protocols",
        "ro_rule",
        "rw_rule",
        "superuser",
    ]
    """links,anonymous_user,clients,index,protocols,ro_rule,rw_rule,superuser,"""

    patchable_fields = [
        "anonymous_user",
        "clients",
        "protocols",
        "ro_rule",
        "rw_rule",
        "superuser",
    ]
    """anonymous_user,clients,protocols,ro_rule,rw_rule,superuser,"""

    postable_fields = [
        "anonymous_user",
        "clients",
        "protocols",
        "ro_rule",
        "rw_rule",
        "superuser",
    ]
    """anonymous_user,clients,protocols,ro_rule,rw_rule,superuser,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in ExportRule.get_collection(fields=field)]
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
            raise NetAppRestError("ExportRule modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class ExportRule(Resource):
    """Allows interaction with ExportRule objects on the host"""

    _schema = ExportRuleSchema
    _path = "/api/protocols/nfs/export-policies/{policy[id]}/rules"
    _keys = ["policy.id", "index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves export policy rules.
### Related ONTAP commands
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="export rule show")
        def export_rule_show(
            policy_id,
            anonymous_user: Choices.define(_get_field_list("anonymous_user"), cache_choices=True, inexact=True)=None,
            index: Choices.define(_get_field_list("index"), cache_choices=True, inexact=True)=None,
            protocols: Choices.define(_get_field_list("protocols"), cache_choices=True, inexact=True)=None,
            ro_rule: Choices.define(_get_field_list("ro_rule"), cache_choices=True, inexact=True)=None,
            rw_rule: Choices.define(_get_field_list("rw_rule"), cache_choices=True, inexact=True)=None,
            superuser: Choices.define(_get_field_list("superuser"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["anonymous_user", "index", "protocols", "ro_rule", "rw_rule", "superuser", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of ExportRule resources

            Args:
                anonymous_user: User ID To Which Anonymous Users Are Mapped.
                index: Index of the rule within the export policy. 
                protocols: 
                ro_rule: Authentication flavors that the read-only access rule governs 
                rw_rule: Authentication flavors that the read/write access rule governs 
                superuser: Authentication flavors that the superuser security type governs 
            """

            kwargs = {}
            if anonymous_user is not None:
                kwargs["anonymous_user"] = anonymous_user
            if index is not None:
                kwargs["index"] = index
            if protocols is not None:
                kwargs["protocols"] = protocols
            if ro_rule is not None:
                kwargs["ro_rule"] = ro_rule
            if rw_rule is not None:
                kwargs["rw_rule"] = rw_rule
            if superuser is not None:
                kwargs["superuser"] = superuser
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return ExportRule.get_collection(
                policy_id,
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves export policy rules.
### Related ONTAP commands
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of an export policy rule to change an export policy rule's index or fields.
### Related ONTAP commands
* `vserver export-policy rule modify`
* `vserver export-policy rule setindex`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._patch_collection(body, *args, connection=connection, **kwargs)

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        body: Union[Resource, dict] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an export policy rule.
### Related ONTAP commands
* `vserver export-policy rule delete`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves export policy rules.
### Related ONTAP commands
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an export policy rule
### Related ONTAP commands
* `vserver export-policy rule show`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
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
        r"""Creates an export policy rule.
### Required properties
* `policy.id`  - Existing export policy for which to create an export rule.
* `clients.match`  - List of clients (hostnames, ipaddresses, netgroups, domains) to which the export rule applies.
* `ro_rule`  - Used to specify the security type for read-only access to volumes that use the export rule.
* `rw_rule`  - Used to specify the security type for read-write access to volumes that use the export rule.
### Default property values
If not specified in POST, the following default property values are assigned:
* `protocols` - _any_
* `anonymous_user` - _none_
* `superuser` - _any_
### Related ONTAP commands
* `vserver export-policy rule create`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="export rule create")
        async def export_rule_create(
            policy_id,
            links: dict = None,
            anonymous_user: str = None,
            clients: dict = None,
            index: Size = None,
            protocols = None,
            ro_rule: List[str] = None,
            rw_rule: List[str] = None,
            superuser: List[str] = None,
        ) -> ResourceTable:
            """Create an instance of a ExportRule resource

            Args:
                links: 
                anonymous_user: User ID To Which Anonymous Users Are Mapped.
                clients: Array of client matches
                index: Index of the rule within the export policy. 
                protocols: 
                ro_rule: Authentication flavors that the read-only access rule governs 
                rw_rule: Authentication flavors that the read/write access rule governs 
                superuser: Authentication flavors that the superuser security type governs 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if anonymous_user is not None:
                kwargs["anonymous_user"] = anonymous_user
            if clients is not None:
                kwargs["clients"] = clients
            if index is not None:
                kwargs["index"] = index
            if protocols is not None:
                kwargs["protocols"] = protocols
            if ro_rule is not None:
                kwargs["ro_rule"] = ro_rule
            if rw_rule is not None:
                kwargs["rw_rule"] = rw_rule
            if superuser is not None:
                kwargs["superuser"] = superuser

            resource = ExportRule(
                policy_id,
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create ExportRule: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of an export policy rule to change an export policy rule's index or fields.
### Related ONTAP commands
* `vserver export-policy rule modify`
* `vserver export-policy rule setindex`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="export rule modify")
        async def export_rule_modify(
            policy_id,
            anonymous_user: str = None,
            query_anonymous_user: str = None,
            index: Size = None,
            query_index: Size = None,
            protocols=None,
            query_protocols=None,
            ro_rule: List[str] = None,
            query_ro_rule: List[str] = None,
            rw_rule: List[str] = None,
            query_rw_rule: List[str] = None,
            superuser: List[str] = None,
            query_superuser: List[str] = None,
        ) -> ResourceTable:
            """Modify an instance of a ExportRule resource

            Args:
                anonymous_user: User ID To Which Anonymous Users Are Mapped.
                query_anonymous_user: User ID To Which Anonymous Users Are Mapped.
                index: Index of the rule within the export policy. 
                query_index: Index of the rule within the export policy. 
                protocols: 
                query_protocols: 
                ro_rule: Authentication flavors that the read-only access rule governs 
                query_ro_rule: Authentication flavors that the read-only access rule governs 
                rw_rule: Authentication flavors that the read/write access rule governs 
                query_rw_rule: Authentication flavors that the read/write access rule governs 
                superuser: Authentication flavors that the superuser security type governs 
                query_superuser: Authentication flavors that the superuser security type governs 
            """

            kwargs = {}
            changes = {}
            if query_anonymous_user is not None:
                kwargs["anonymous_user"] = query_anonymous_user
            if query_index is not None:
                kwargs["index"] = query_index
            if query_protocols is not None:
                kwargs["protocols"] = query_protocols
            if query_ro_rule is not None:
                kwargs["ro_rule"] = query_ro_rule
            if query_rw_rule is not None:
                kwargs["rw_rule"] = query_rw_rule
            if query_superuser is not None:
                kwargs["superuser"] = query_superuser

            if anonymous_user is not None:
                changes["anonymous_user"] = anonymous_user
            if index is not None:
                changes["index"] = index
            if protocols is not None:
                changes["protocols"] = protocols
            if ro_rule is not None:
                changes["ro_rule"] = ro_rule
            if rw_rule is not None:
                changes["rw_rule"] = rw_rule
            if superuser is not None:
                changes["superuser"] = superuser

            if hasattr(ExportRule, "find"):
                resource = ExportRule.find(
                    policy_id,
                    **kwargs
                )
            else:
                resource = ExportRule(policy_id,)
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify ExportRule: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an export policy rule.
### Related ONTAP commands
* `vserver export-policy rule delete`
### Learn more
* [`DOC /protocols/nfs/export-policies`](#docs-NAS-protocols_nfs_export-policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="export rule delete")
        async def export_rule_delete(
            policy_id,
            anonymous_user: str = None,
            index: Size = None,
            protocols=None,
            ro_rule: List[str] = None,
            rw_rule: List[str] = None,
            superuser: List[str] = None,
        ) -> None:
            """Delete an instance of a ExportRule resource

            Args:
                anonymous_user: User ID To Which Anonymous Users Are Mapped.
                index: Index of the rule within the export policy. 
                protocols: 
                ro_rule: Authentication flavors that the read-only access rule governs 
                rw_rule: Authentication flavors that the read/write access rule governs 
                superuser: Authentication flavors that the superuser security type governs 
            """

            kwargs = {}
            if anonymous_user is not None:
                kwargs["anonymous_user"] = anonymous_user
            if index is not None:
                kwargs["index"] = index
            if protocols is not None:
                kwargs["protocols"] = protocols
            if ro_rule is not None:
                kwargs["ro_rule"] = ro_rule
            if rw_rule is not None:
                kwargs["rw_rule"] = rw_rule
            if superuser is not None:
                kwargs["superuser"] = superuser

            if hasattr(ExportRule, "find"):
                resource = ExportRule.find(
                    policy_id,
                    **kwargs
                )
            else:
                resource = ExportRule(policy_id,)
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete ExportRule: %s" % err)


