r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Managing SnapMirror policies
This API is used to manage SnapMirror policies of type "async" and "sync". When applied to a SnapMirror relationship, the SnapMirror policy controls the behavior of the relationship and specifies the configuration attributes for that relationship.<br>The policy type "async" can be associated with a SnapMirror relationship that has either the FlexVol volume or FlexGroup volume or SVM as the endpoint.<br>The policy type "sync" can be associated with a SnapMirror relationship that has FlexVol volume or a Consistency Group as the endpoint. The policy type "sync" can have a "sync_type" of either "sync", "strict_sync" or "automated_failover". If the "sync_type" is "sync" then a write success is returned to the client after writing the data to the primary endpoint and before writing the data to the secondary endpoint. If the "sync_type" is "strict_sync" then a write success is returned to the client after writing the data to the both primary and secondary endpoints.<br>The "sync_type" of "automated_failover" can be associated with a SnapMirror relationship that has Consistency Group as the endpoint.<\br>
Mapping of SnapMirror policies from CLI to REST
|--------------------|----------------------------|
|        CLI         |            REST            |
|--------------------|----------------------------|
|mirror-vault        | async                      |
|--------------------|----------------------------|
|                    |       |  sync_type         |
|                    |       |--------------------|
|sync-mirror         | sync  | sync               |
|strict-sync-mirror  | sync  | strict_sync        |
|automated-failover  | sync  | automated_failover |
|--------------------|----------------------------|
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


__all__ = ["SnapmirrorPolicy", "SnapmirrorPolicySchema"]
__pdoc__ = {
    "SnapmirrorPolicySchema.resource": False,
    "SnapmirrorPolicy.snapmirror_policy_show": False,
    "SnapmirrorPolicy.snapmirror_policy_create": False,
    "SnapmirrorPolicy.snapmirror_policy_modify": False,
    "SnapmirrorPolicy.snapmirror_policy_delete": False,
}


class SnapmirrorPolicySchema(ResourceSchema):
    """The fields of the SnapmirrorPolicy object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the snapmirror_policy. """

    comment = fields.Str(
        data_key="comment",
    )
    r""" Comment associated with the policy. """

    identity_preservation = fields.Str(
        data_key="identity_preservation",
        validate=enum_validation(['full', 'exclude_network_config', 'exclude_network_and_protocol_config']),
    )
    r""" Specifies which configuration of the source SVM is replicated to the destination SVM. This property is applicable only for SVM data protection with "async" policy type.

Valid choices:

* full
* exclude_network_config
* exclude_network_and_protocol_config """

    name = fields.Str(
        data_key="name",
    )
    r""" The name field of the snapmirror_policy.

Example: Asynchronous """

    network_compression_enabled = fields.Boolean(
        data_key="network_compression_enabled",
    )
    r""" Specifies whether network compression is enabled for transfers. This is applicable only to the policies of type "async". """

    retention = fields.List(fields.Nested("netapp_ontap.models.snapmirror_policy_rule.SnapmirrorPolicyRuleSchema", unknown=EXCLUDE), data_key="retention")
    r""" Policy on Snapshot copy retention. """

    scope = fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
    )
    r""" Set to "svm" for policies owned by an SVM, otherwise set to "cluster".

Valid choices:

* svm
* cluster """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the snapmirror_policy. """

    sync_common_snapshot_schedule = fields.Nested("netapp_ontap.resources.schedule.ScheduleSchema", data_key="sync_common_snapshot_schedule", unknown=EXCLUDE)
    r""" The sync_common_snapshot_schedule field of the snapmirror_policy. """

    sync_type = fields.Str(
        data_key="sync_type",
        validate=enum_validation(['sync', 'strict_sync', 'automated_failover']),
    )
    r""" The sync_type field of the snapmirror_policy.

Valid choices:

* sync
* strict_sync
* automated_failover """

    throttle = Size(
        data_key="throttle",
    )
    r""" Throttle in KB/s. Default to unlimited. """

    transfer_schedule = fields.Nested("netapp_ontap.resources.schedule.ScheduleSchema", data_key="transfer_schedule", unknown=EXCLUDE)
    r""" The transfer_schedule field of the snapmirror_policy. """

    type = fields.Str(
        data_key="type",
        validate=enum_validation(['async', 'sync']),
    )
    r""" The type field of the snapmirror_policy.

Valid choices:

* async
* sync """

    uuid = fields.Str(
        data_key="uuid",
    )
    r""" The uuid field of the snapmirror_policy.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return SnapmirrorPolicy

    gettable_fields = [
        "links",
        "comment",
        "identity_preservation",
        "name",
        "network_compression_enabled",
        "retention",
        "scope",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "sync_common_snapshot_schedule.links",
        "sync_common_snapshot_schedule.name",
        "sync_common_snapshot_schedule.uuid",
        "sync_type",
        "throttle",
        "transfer_schedule.links",
        "transfer_schedule.name",
        "transfer_schedule.uuid",
        "type",
        "uuid",
    ]
    """links,comment,identity_preservation,name,network_compression_enabled,retention,scope,svm.links,svm.name,svm.uuid,sync_common_snapshot_schedule.links,sync_common_snapshot_schedule.name,sync_common_snapshot_schedule.uuid,sync_type,throttle,transfer_schedule.links,transfer_schedule.name,transfer_schedule.uuid,type,uuid,"""

    patchable_fields = [
        "comment",
        "identity_preservation",
        "network_compression_enabled",
        "retention",
        "sync_common_snapshot_schedule.name",
        "sync_common_snapshot_schedule.uuid",
        "throttle",
        "transfer_schedule.name",
        "transfer_schedule.uuid",
    ]
    """comment,identity_preservation,network_compression_enabled,retention,sync_common_snapshot_schedule.name,sync_common_snapshot_schedule.uuid,throttle,transfer_schedule.name,transfer_schedule.uuid,"""

    postable_fields = [
        "comment",
        "identity_preservation",
        "name",
        "network_compression_enabled",
        "retention",
        "svm.name",
        "svm.uuid",
        "sync_common_snapshot_schedule.name",
        "sync_common_snapshot_schedule.uuid",
        "sync_type",
        "throttle",
        "transfer_schedule.name",
        "transfer_schedule.uuid",
        "type",
    ]
    """comment,identity_preservation,name,network_compression_enabled,retention,svm.name,svm.uuid,sync_common_snapshot_schedule.name,sync_common_snapshot_schedule.uuid,sync_type,throttle,transfer_schedule.name,transfer_schedule.uuid,type,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in SnapmirrorPolicy.get_collection(fields=field)]
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
            raise NetAppRestError("SnapmirrorPolicy modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class SnapmirrorPolicy(Resource):
    r""" SnapMirror policy information. SnapMirror policy can either be of type "async" or "sync".<br>The policy type "async" can be associated with a SnapMirror relationship that has either the FlexVol volume or FlexGroup volume or SVM as the endpoint.<br>The policy type "sync" along with "sync_type" as "sync" or "strict_sync" can be associated with a SnapMirror relationship that has FlexVol volume as the endpoint. The policy type "sync" can have a "sync_type" of either "sync", "strict_sync" or "automated_failover". If the "sync_type" is "sync" then a write success is returned to the client after writing the data to the source endpoint and before writing the data to the destination endpoint. If the "sync_type" is "strict_sync" then a write success is returned to the client after writing the data to the both source and destination endpoints.<br>If the "sync_type" is "automated_failover" then the policy can be associated with a SnapMirror relationship that has Consistency Group as the endpoint. Use the "sync" policy with "sync_type" as "automated_failover" to establish SnapMirror relationships for business continuity usecases. SnapMirror relationships with policy type as "sync" and "sync_type" as "automated_failover" can be monitored by the Mediator, if configured. In case the source Consistency Group endpoint is not reachable, the Mediator may trigger a failover to the destination Consistency Group endpoint. """

    _schema = SnapmirrorPolicySchema
    _path = "/api/snapmirror/policies"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves SnapMirror policies of type "async" and "sync".
### Related ONTAP commands
* `snapmirror policy show`
### Example
The following example shows how to retrieve a collection of SnapMirror policies.
<br/>
```
GET "/api/snapmirror/policies"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="snapmirror policy show")
        def snapmirror_policy_show(
            comment: Choices.define(_get_field_list("comment"), cache_choices=True, inexact=True)=None,
            identity_preservation: Choices.define(_get_field_list("identity_preservation"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            network_compression_enabled: Choices.define(_get_field_list("network_compression_enabled"), cache_choices=True, inexact=True)=None,
            scope: Choices.define(_get_field_list("scope"), cache_choices=True, inexact=True)=None,
            sync_type: Choices.define(_get_field_list("sync_type"), cache_choices=True, inexact=True)=None,
            throttle: Choices.define(_get_field_list("throttle"), cache_choices=True, inexact=True)=None,
            type: Choices.define(_get_field_list("type"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["comment", "identity_preservation", "name", "network_compression_enabled", "scope", "sync_type", "throttle", "type", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of SnapmirrorPolicy resources

            Args:
                comment: Comment associated with the policy.
                identity_preservation: Specifies which configuration of the source SVM is replicated to the destination SVM. This property is applicable only for SVM data protection with \"async\" policy type.
                name: 
                network_compression_enabled: Specifies whether network compression is enabled for transfers. This is applicable only to the policies of type \"async\".
                scope: Set to \"svm\" for policies owned by an SVM, otherwise set to \"cluster\".
                sync_type: 
                throttle: Throttle in KB/s. Default to unlimited.
                type: 
                uuid: 
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if identity_preservation is not None:
                kwargs["identity_preservation"] = identity_preservation
            if name is not None:
                kwargs["name"] = name
            if network_compression_enabled is not None:
                kwargs["network_compression_enabled"] = network_compression_enabled
            if scope is not None:
                kwargs["scope"] = scope
            if sync_type is not None:
                kwargs["sync_type"] = sync_type
            if throttle is not None:
                kwargs["throttle"] = throttle
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return SnapmirrorPolicy.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves SnapMirror policies of type "async" and "sync".
### Related ONTAP commands
* `snapmirror policy show`
### Example
The following example shows how to retrieve a collection of SnapMirror policies.
<br/>
```
GET "/api/snapmirror/policies"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
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
        r"""Updates the SnapMirror policy.
### Important notes
* The properties "transfer_schedule" and "throttle" can be modified only if all the SnapMirror relationships associated with the specified SnapMirror policy have the same values.
* The properties "retention.label" and "retention.count" are mandatory if "retention" is provided in the input. The provided "retention.label" is the final list and is replaced with the existing values.
* The value of the "identity_preservation" property cannot be changed if the SnapMirror relationships associated with the policy have different identity_preservation configurations.
* If the SnapMirror policy "identity_preservation" value matches the "identity_preservation" value of the associated SnapMirror relationships, then the "identity_preservation" value can be changed from a higher "identity_preservation" threshold value to a lower "identity_preservation" threshold value but not vice-versa. For example, the threshold value of the "identity_preservation" property can be changed from "full" to "exclude_network_config" to "exclude_network_and_protocol_config", but could not be increased from "exclude_network_and_protocol_config" to "exclude_network_config" to "full".<br/>
### Related ONTAP commands
* `snapmirror policy modify`
### Example
  Updating the "retention" property
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention" : {"label" : ["sm_created", "lab2"], "count": ["1","2"], "creation_schedule": {"name": ["weekly"]}}}'
   ```
   <br/>
  Updating "transfer_schedule", "throttle", and "identity_preservation" properties
   <br/>
   ```
   PATCH "/api/snapmirror/policies/8aef950b-3bef-11e9-80ac-0050568ea591" '{"transfer_schedule.name" : "weekly", "throttle" : "100", "identity_preservation":"exclude_network_and_protocol_config"}'
   ```
   <br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
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
        r"""Deletes a SnapMirror policy.
### Related ONTAP commands
* `snapmirror policy delete`
### Example
<br/>
```
DELETE "/api/snapmirror/policies/510c15d4-f9e6-11e8-bdb5-0050568e12c2"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves SnapMirror policies of type "async" and "sync".
### Related ONTAP commands
* `snapmirror policy show`
### Example
The following example shows how to retrieve a collection of SnapMirror policies.
<br/>
```
GET "/api/snapmirror/policies"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific SnapMirror policy.
### Example
<br/>
```
GET "/api/snapmirror/policies/567aaac0-f863-11e8-a666-0050568e12c2"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
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
        r"""Creates a SnapMirror policy. The property "identity_preservation" is applicable to only SnapMirror relationships with SVM endpoints and it indicates which configuration of the source SVM is replicated to the destination SVM.</br>
It takes the following values:
- `full` - indicates that the source SVM configuration is replicated to the destination SVM endpoint.
- `exclude_network_config` - indicates that the source SVM configuration other than network configuration is replicated to the destination SVM endpoint.
- `exclude_network_and_protocol_config` - indicates that the source SVM configuration is not replicated to the destination SVM endpoint.<br/>
### Important note
- The property "identity_preservation" is applicable to only SnapMirror relationships with SVM endpoints and it indicates which configuration of the source SVM is replicated to the destination SVM.
- The properties "identity_preservation" and "transfer_schedule" are not applicable for "sync" type policies.
- The properties "retention.creation_schedule" and "retention.prefix" are not applicable for "sync" type policies.
- The property "sync_common_snapshot_schedule" is not applicable for an "async" type policy.
- The property "retention.count" specifies the maximum number of Snapshot copies that are retained on the SnapMirror destination volume.
- When the property "retention.label" is specified, the Snapshot copies that have a SnapMirror label matching this property is transferred to the SnapMirror destination.
- When the property "retention.creation_schedule" is specified, Snapshot copies are directly created on the SnapMirror destination. The Snapshot copies created have the same content as the latest Snapshot copy already present on the SnapMirror destination.
### Required properties
* `name` - Name of the new SnapMirror policy.
### Recommended optional properties
* `svm.name` or `svm.uuid` - Name or UUID of the SVM that owns the SnapMirror policy.
### Default property values
If not specified in POST, the following default property values are assigned:
* `type` - _async_
* `sync_type` - _sync_ (when `type` is _sync_)
* `network_compression_enabled` - _false_
* `throttle` - _0_
* `identity_preservation` - `_exclude_network_and_protocol_config_`
### Related ONTAP commands
* `snapmirror policy create`
### Examples
  Creating a SnapMirror policy of type "sync"
   <br/>
   ```
   POST "/api/snapmirror/policies/" '{"name": "policy1", "svm.name": "VS0", "type": "sync", "sync_type": "sync"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async" with retention values
   <br/>
   ```
   POST "/api/snapmirror/policies" '{"name": "policy_ret", "svm": {"name": "vs1"}, "retention": {"label": ["smcreate"], "count": ["2"], "creation_schedule": ["weekly"]}}'
   ```
   <br/>
  Creating a SnapMirror policy of type "async"
   ```
   POST "/api/snapmirror/policies" '{"name": "newPolicy", "svm":{"name" : "vs1"}, "type": "async"}'
   ```
   <br/>
  Creating a SnapMirror policy of type "sync" with sync_type as "automated_failover"
   <br/>
   ```
   POST "/api/snapmirror/policies/" '{"name": "policy1", "svm.name": "VS0", "type": "sync", "sync_type": "automated_failover" }'
   ```
   <br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="snapmirror policy create")
        async def snapmirror_policy_create(
            links: dict = None,
            comment: str = None,
            identity_preservation: str = None,
            name: str = None,
            network_compression_enabled: bool = None,
            retention: dict = None,
            scope: str = None,
            svm: dict = None,
            sync_common_snapshot_schedule: dict = None,
            sync_type: str = None,
            throttle: Size = None,
            transfer_schedule: dict = None,
            type: str = None,
            uuid: str = None,
        ) -> ResourceTable:
            """Create an instance of a SnapmirrorPolicy resource

            Args:
                links: 
                comment: Comment associated with the policy.
                identity_preservation: Specifies which configuration of the source SVM is replicated to the destination SVM. This property is applicable only for SVM data protection with \"async\" policy type.
                name: 
                network_compression_enabled: Specifies whether network compression is enabled for transfers. This is applicable only to the policies of type \"async\".
                retention: Policy on Snapshot copy retention.
                scope: Set to \"svm\" for policies owned by an SVM, otherwise set to \"cluster\".
                svm: 
                sync_common_snapshot_schedule: 
                sync_type: 
                throttle: Throttle in KB/s. Default to unlimited.
                transfer_schedule: 
                type: 
                uuid: 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if comment is not None:
                kwargs["comment"] = comment
            if identity_preservation is not None:
                kwargs["identity_preservation"] = identity_preservation
            if name is not None:
                kwargs["name"] = name
            if network_compression_enabled is not None:
                kwargs["network_compression_enabled"] = network_compression_enabled
            if retention is not None:
                kwargs["retention"] = retention
            if scope is not None:
                kwargs["scope"] = scope
            if svm is not None:
                kwargs["svm"] = svm
            if sync_common_snapshot_schedule is not None:
                kwargs["sync_common_snapshot_schedule"] = sync_common_snapshot_schedule
            if sync_type is not None:
                kwargs["sync_type"] = sync_type
            if throttle is not None:
                kwargs["throttle"] = throttle
            if transfer_schedule is not None:
                kwargs["transfer_schedule"] = transfer_schedule
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid

            resource = SnapmirrorPolicy(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create SnapmirrorPolicy: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the SnapMirror policy.
### Important notes
* The properties "transfer_schedule" and "throttle" can be modified only if all the SnapMirror relationships associated with the specified SnapMirror policy have the same values.
* The properties "retention.label" and "retention.count" are mandatory if "retention" is provided in the input. The provided "retention.label" is the final list and is replaced with the existing values.
* The value of the "identity_preservation" property cannot be changed if the SnapMirror relationships associated with the policy have different identity_preservation configurations.
* If the SnapMirror policy "identity_preservation" value matches the "identity_preservation" value of the associated SnapMirror relationships, then the "identity_preservation" value can be changed from a higher "identity_preservation" threshold value to a lower "identity_preservation" threshold value but not vice-versa. For example, the threshold value of the "identity_preservation" property can be changed from "full" to "exclude_network_config" to "exclude_network_and_protocol_config", but could not be increased from "exclude_network_and_protocol_config" to "exclude_network_config" to "full".<br/>
### Related ONTAP commands
* `snapmirror policy modify`
### Example
  Updating the "retention" property
   <br/>
   ```
   PATCH "/api/snapmirror/policies/fe65686d-00dc-11e9-b5fb-0050568e3f83" '{"retention" : {"label" : ["sm_created", "lab2"], "count": ["1","2"], "creation_schedule": {"name": ["weekly"]}}}'
   ```
   <br/>
  Updating "transfer_schedule", "throttle", and "identity_preservation" properties
   <br/>
   ```
   PATCH "/api/snapmirror/policies/8aef950b-3bef-11e9-80ac-0050568ea591" '{"transfer_schedule.name" : "weekly", "throttle" : "100", "identity_preservation":"exclude_network_and_protocol_config"}'
   ```
   <br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="snapmirror policy modify")
        async def snapmirror_policy_modify(
            comment: str = None,
            query_comment: str = None,
            identity_preservation: str = None,
            query_identity_preservation: str = None,
            name: str = None,
            query_name: str = None,
            network_compression_enabled: bool = None,
            query_network_compression_enabled: bool = None,
            scope: str = None,
            query_scope: str = None,
            sync_type: str = None,
            query_sync_type: str = None,
            throttle: Size = None,
            query_throttle: Size = None,
            type: str = None,
            query_type: str = None,
            uuid: str = None,
            query_uuid: str = None,
        ) -> ResourceTable:
            """Modify an instance of a SnapmirrorPolicy resource

            Args:
                comment: Comment associated with the policy.
                query_comment: Comment associated with the policy.
                identity_preservation: Specifies which configuration of the source SVM is replicated to the destination SVM. This property is applicable only for SVM data protection with \"async\" policy type.
                query_identity_preservation: Specifies which configuration of the source SVM is replicated to the destination SVM. This property is applicable only for SVM data protection with \"async\" policy type.
                name: 
                query_name: 
                network_compression_enabled: Specifies whether network compression is enabled for transfers. This is applicable only to the policies of type \"async\".
                query_network_compression_enabled: Specifies whether network compression is enabled for transfers. This is applicable only to the policies of type \"async\".
                scope: Set to \"svm\" for policies owned by an SVM, otherwise set to \"cluster\".
                query_scope: Set to \"svm\" for policies owned by an SVM, otherwise set to \"cluster\".
                sync_type: 
                query_sync_type: 
                throttle: Throttle in KB/s. Default to unlimited.
                query_throttle: Throttle in KB/s. Default to unlimited.
                type: 
                query_type: 
                uuid: 
                query_uuid: 
            """

            kwargs = {}
            changes = {}
            if query_comment is not None:
                kwargs["comment"] = query_comment
            if query_identity_preservation is not None:
                kwargs["identity_preservation"] = query_identity_preservation
            if query_name is not None:
                kwargs["name"] = query_name
            if query_network_compression_enabled is not None:
                kwargs["network_compression_enabled"] = query_network_compression_enabled
            if query_scope is not None:
                kwargs["scope"] = query_scope
            if query_sync_type is not None:
                kwargs["sync_type"] = query_sync_type
            if query_throttle is not None:
                kwargs["throttle"] = query_throttle
            if query_type is not None:
                kwargs["type"] = query_type
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if comment is not None:
                changes["comment"] = comment
            if identity_preservation is not None:
                changes["identity_preservation"] = identity_preservation
            if name is not None:
                changes["name"] = name
            if network_compression_enabled is not None:
                changes["network_compression_enabled"] = network_compression_enabled
            if scope is not None:
                changes["scope"] = scope
            if sync_type is not None:
                changes["sync_type"] = sync_type
            if throttle is not None:
                changes["throttle"] = throttle
            if type is not None:
                changes["type"] = type
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(SnapmirrorPolicy, "find"):
                resource = SnapmirrorPolicy.find(
                    **kwargs
                )
            else:
                resource = SnapmirrorPolicy()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify SnapmirrorPolicy: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a SnapMirror policy.
### Related ONTAP commands
* `snapmirror policy delete`
### Example
<br/>
```
DELETE "/api/snapmirror/policies/510c15d4-f9e6-11e8-bdb5-0050568e12c2"
```
<br/>
### Learn more
* [`DOC /snapmirror/policies`](#docs-snapmirror-snapmirror_policies)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="snapmirror policy delete")
        async def snapmirror_policy_delete(
            comment: str = None,
            identity_preservation: str = None,
            name: str = None,
            network_compression_enabled: bool = None,
            scope: str = None,
            sync_type: str = None,
            throttle: Size = None,
            type: str = None,
            uuid: str = None,
        ) -> None:
            """Delete an instance of a SnapmirrorPolicy resource

            Args:
                comment: Comment associated with the policy.
                identity_preservation: Specifies which configuration of the source SVM is replicated to the destination SVM. This property is applicable only for SVM data protection with \"async\" policy type.
                name: 
                network_compression_enabled: Specifies whether network compression is enabled for transfers. This is applicable only to the policies of type \"async\".
                scope: Set to \"svm\" for policies owned by an SVM, otherwise set to \"cluster\".
                sync_type: 
                throttle: Throttle in KB/s. Default to unlimited.
                type: 
                uuid: 
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if identity_preservation is not None:
                kwargs["identity_preservation"] = identity_preservation
            if name is not None:
                kwargs["name"] = name
            if network_compression_enabled is not None:
                kwargs["network_compression_enabled"] = network_compression_enabled
            if scope is not None:
                kwargs["scope"] = scope
            if sync_type is not None:
                kwargs["sync_type"] = sync_type
            if throttle is not None:
                kwargs["throttle"] = throttle
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid

            if hasattr(SnapmirrorPolicy, "find"):
                resource = SnapmirrorPolicy.find(
                    **kwargs
                )
            else:
                resource = SnapmirrorPolicy()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete SnapmirrorPolicy: %s" % err)


