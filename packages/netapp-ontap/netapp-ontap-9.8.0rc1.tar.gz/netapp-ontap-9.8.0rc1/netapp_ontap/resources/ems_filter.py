r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
Manages a specific filter instance.
See the documentation for [/support/ems/filters](#/docs/support/support_ems_filters) for details on the various properties.
## Examples
### Retrieving a specific filter instance
```JSON
# API
GET /api/support/ems/filters/no-info-debug-events
# Response
200 OK
# JSON Body
{
  "name": "no-info-debug-events",
  "rules": [
    {
      "index": 1,
      "type": "include",
      "message_criteria": {
        "name_pattern": "*",
        "severities": "emergency,alert,error,notice",
        "snmp_trap_types": "*",
        "_links": {
          "related": {
            "href": "/api/support/ems/messages?name=*&severity=emergency,alert,error,notice&snmp_trap_type=*"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/support/ems/filters/no-info-debug-events/rules/1"
        }
      }
    },
    {
      "index": 2,
      "type": "exclude",
      "message_criteria": {
        "name_pattern": "*",
        "severities": "*",
        "snmp_trap_types": "*",
        "_links": {
          "related": {
            "href": "/api/support/ems/messages?name=*&severity=*&snmp_trap_type=*"
          }
        }
      },
      "_links": {
        "self": {
          "href": "/api/support/ems/filters/no-info-debug-events/rules/2"
        }
      }
    }
  ],
  "_links": {
    "self": {
      "href": "/api/support/ems/filters/no-info-debug-events"
    }
  }
}
```
### Updating an existing filter with a new rule
```JSON
# API
PATCH /api/support/ems/filters/test-filter
# JSON Body
{
  "rules": [
    {
      "type": "include",
      "message_criteria": {
        "name_pattern": "wafl.*",
        "severities": "error"
      }
    }
  ]
}
# Response
200 OK
```
### Deleting an existing filter
```JSON
# API
DELETE /api/support/ems/filters/test-filter
# Response
200 OK
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


__all__ = ["EmsFilter", "EmsFilterSchema"]
__pdoc__ = {
    "EmsFilterSchema.resource": False,
    "EmsFilter.ems_filter_show": False,
    "EmsFilter.ems_filter_create": False,
    "EmsFilter.ems_filter_modify": False,
    "EmsFilter.ems_filter_delete": False,
}


class EmsFilterSchema(ResourceSchema):
    """The fields of the EmsFilter object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the ems_filter. """

    name = fields.Str(
        data_key="name",
    )
    r""" Filter name

Example: snmp-traphost """

    rules = fields.List(fields.Nested("netapp_ontap.resources.ems_filter_rule.EmsFilterRuleSchema", unknown=EXCLUDE), data_key="rules")
    r""" Array of event filter rules on which to match. """

    @property
    def resource(self):
        return EmsFilter

    gettable_fields = [
        "links",
        "name",
        "rules",
    ]
    """links,name,rules,"""

    patchable_fields = [
        "name",
        "rules",
    ]
    """name,rules,"""

    postable_fields = [
        "name",
        "rules",
    ]
    """name,rules,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in EmsFilter.get_collection(fields=field)]
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
            raise NetAppRestError("EmsFilter modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class EmsFilter(Resource):
    """Allows interaction with EmsFilter objects on the host"""

    _schema = EmsFilterSchema
    _path = "/api/support/ems/filters"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of event filters.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ems filter show")
        def ems_filter_show(
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["name", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of EmsFilter resources

            Args:
                name: Filter name
            """

            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return EmsFilter.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves a collection of event filters.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
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
        r"""Updates an event filter.
### Recommended optional properties
* `new_name` - New string that uniquely identifies a filter.
* `rules` - New list of criteria used to match the filter with an event. The existing list is discarded.
### Related ONTAP commands
* `event filter create`
* `event filter delete`
* `event filter rename`
* `event filter rule add`
* `event filter rule delete`
* `event filter rule reorder`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
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
        r"""Deletes an event filter.
### Related ONTAP commands
* `event filter delete`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of event filters.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an event filter.
### Related ONTAP commands
* `event filter show`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
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
        r"""Creates an event filter.
### Required properties
* `name` - String that uniquely identifies the filter.
### Recommended optional properties
* `rules` - List of criteria which is used to match a filter with an event.
### Related ONTAP commands
* `event filter create`

### Learn more
* [`DOC /support/ems/filters`](#docs-support-support_ems_filters)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ems filter create")
        async def ems_filter_create(
            links: dict = None,
            name: str = None,
            rules: dict = None,
        ) -> ResourceTable:
            """Create an instance of a EmsFilter resource

            Args:
                links: 
                name: Filter name
                rules: Array of event filter rules on which to match.
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if name is not None:
                kwargs["name"] = name
            if rules is not None:
                kwargs["rules"] = rules

            resource = EmsFilter(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create EmsFilter: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an event filter.
### Recommended optional properties
* `new_name` - New string that uniquely identifies a filter.
* `rules` - New list of criteria used to match the filter with an event. The existing list is discarded.
### Related ONTAP commands
* `event filter create`
* `event filter delete`
* `event filter rename`
* `event filter rule add`
* `event filter rule delete`
* `event filter rule reorder`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ems filter modify")
        async def ems_filter_modify(
            name: str = None,
            query_name: str = None,
        ) -> ResourceTable:
            """Modify an instance of a EmsFilter resource

            Args:
                name: Filter name
                query_name: Filter name
            """

            kwargs = {}
            changes = {}
            if query_name is not None:
                kwargs["name"] = query_name

            if name is not None:
                changes["name"] = name

            if hasattr(EmsFilter, "find"):
                resource = EmsFilter.find(
                    **kwargs
                )
            else:
                resource = EmsFilter()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify EmsFilter: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an event filter.
### Related ONTAP commands
* `event filter delete`

### Learn more
* [`DOC /support/ems/filters/{name}`](#docs-support-support_ems_filters_{name})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ems filter delete")
        async def ems_filter_delete(
            name: str = None,
        ) -> None:
            """Delete an instance of a EmsFilter resource

            Args:
                name: Filter name
            """

            kwargs = {}
            if name is not None:
                kwargs["name"] = name

            if hasattr(EmsFilter, "find"):
                resource = EmsFilter.find(
                    **kwargs
                )
            else:
                resource = EmsFilter()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete EmsFilter: %s" % err)


