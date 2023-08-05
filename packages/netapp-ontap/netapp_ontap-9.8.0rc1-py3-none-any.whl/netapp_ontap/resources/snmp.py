r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
Cluster wide SNMP configuration. You can configure or retrieve the following SNMP parameters using this endpoint:

* enable or disable SNMP
* enable or disable SNMP authentication traps
## Examples
### Disables SNMP protocol in the cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.enabled = False
    resource.patch()

```

### Enables SNMP authentication traps in the cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.auth_traps_enabled = True
    resource.patch()

```

### Enables SNMP protocol and SNMP authentication traps in the cluster.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Snmp

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Snmp()
    resource.enabled = True
    resource.auth_traps_enabled = True
    resource.patch()

```

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


__all__ = ["Snmp", "SnmpSchema"]
__pdoc__ = {
    "SnmpSchema.resource": False,
    "Snmp.snmp_show": False,
    "Snmp.snmp_create": False,
    "Snmp.snmp_modify": False,
    "Snmp.snmp_delete": False,
}


class SnmpSchema(ResourceSchema):
    """The fields of the Snmp object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the snmp. """

    auth_traps_enabled = fields.Boolean(
        data_key="auth_traps_enabled",
    )
    r""" Specifies whether to enable or disable SNMP authentication traps.

Example: true """

    enabled = fields.Boolean(
        data_key="enabled",
    )
    r""" Specifies whether to enable or disable SNMP.

Example: true """

    @property
    def resource(self):
        return Snmp

    gettable_fields = [
        "links",
        "auth_traps_enabled",
        "enabled",
    ]
    """links,auth_traps_enabled,enabled,"""

    patchable_fields = [
        "auth_traps_enabled",
        "enabled",
    ]
    """auth_traps_enabled,enabled,"""

    postable_fields = [
    ]
    """"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Snmp.get_collection(fields=field)]
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
            raise NetAppRestError("Snmp modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Snmp(Resource):
    r""" Cluster-wide SNMP configuration. """

    _schema = SnmpSchema
    _path = "/api/support/snmp"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cluster wide SNMP configuration.
### Related ONTAP commands
* `options snmp.enable`
* `system snmp show`
### Learn more
* [`DOC /support/snmp`](#docs-support-support_snmp)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="snmp show")
        def snmp_show(
            auth_traps_enabled: Choices.define(_get_field_list("auth_traps_enabled"), cache_choices=True, inexact=True)=None,
            enabled: Choices.define(_get_field_list("enabled"), cache_choices=True, inexact=True)=None,
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single Snmp resource

            Args:
                auth_traps_enabled: Specifies whether to enable or disable SNMP authentication traps.
                enabled: Specifies whether to enable or disable SNMP.
            """

            kwargs = {}
            if auth_traps_enabled is not None:
                kwargs["auth_traps_enabled"] = auth_traps_enabled
            if enabled is not None:
                kwargs["enabled"] = enabled
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            resource = Snmp(
                **kwargs
            )
            resource.get()
            return [resource]


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the cluster wide SNMP configuration, such as enabling or disabling SNMP and enabling or disabling authentication traps.
### Related ONTAP commands
* `options snmp.enable`
* `system snmp authtrap`
### Learn more
* [`DOC /support/snmp`](#docs-support-support_snmp)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="snmp modify")
        async def snmp_modify(
            auth_traps_enabled: bool = None,
            query_auth_traps_enabled: bool = None,
            enabled: bool = None,
            query_enabled: bool = None,
        ) -> ResourceTable:
            """Modify an instance of a Snmp resource

            Args:
                auth_traps_enabled: Specifies whether to enable or disable SNMP authentication traps.
                query_auth_traps_enabled: Specifies whether to enable or disable SNMP authentication traps.
                enabled: Specifies whether to enable or disable SNMP.
                query_enabled: Specifies whether to enable or disable SNMP.
            """

            kwargs = {}
            changes = {}
            if query_auth_traps_enabled is not None:
                kwargs["auth_traps_enabled"] = query_auth_traps_enabled
            if query_enabled is not None:
                kwargs["enabled"] = query_enabled

            if auth_traps_enabled is not None:
                changes["auth_traps_enabled"] = auth_traps_enabled
            if enabled is not None:
                changes["enabled"] = enabled

            if hasattr(Snmp, "find"):
                resource = Snmp.find(
                    **kwargs
                )
            else:
                resource = Snmp()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify Snmp: %s" % err)



