r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
Event remediations is the initial implementation of ONTAP self healing proof of concept.<p/>
This endpoint supports GET calls. GET is used to retrieve details about the event.
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


__all__ = ["EventRemediations", "EventRemediationsSchema"]
__pdoc__ = {
    "EventRemediationsSchema.resource": False,
    "EventRemediations.event_remediations_show": False,
    "EventRemediations.event_remediations_create": False,
    "EventRemediations.event_remediations_modify": False,
    "EventRemediations.event_remediations_delete": False,
}


class EventRemediationsSchema(ResourceSchema):
    """The fields of the EventRemediations object"""

    cluster = fields.Nested("netapp_ontap.models.event_remediations_cluster.EventRemediationsClusterSchema", data_key="cluster", unknown=EXCLUDE)
    r""" The cluster field of the event_remediations. """

    completion_time = ImpreciseDateTime(
        data_key="completion_time",
    )
    r""" Completion time of the event """

    description = fields.Str(
        data_key="description",
    )
    r""" Description for the event

Example: Disable Telnet """

    event_remediation_action = fields.Str(
        data_key="event_remediation_action",
        validate=enum_validation(['perform', 'dismiss']),
    )
    r""" Event remediation action

Valid choices:

* perform
* dismiss """

    event_remediation_action_type = fields.Str(
        data_key="event_remediation_action_type",
        validate=enum_validation(['manual', 'automatic']),
    )
    r""" Type of remediation action

Valid choices:

* manual
* automatic """

    event_remediation_state = fields.Str(
        data_key="event_remediation_state",
        validate=enum_validation(['waiting', 'in_progress', 'completed', 'failed', 'obsolete', 'dismissed']),
    )
    r""" State of the event remediation

Valid choices:

* waiting
* in_progress
* completed
* failed
* obsolete
* dismissed """

    event_type_name = fields.Str(
        data_key="event_type_name",
        validate=enum_validation(['cluster_telnet_enabled']),
    )
    r""" Type of the event

Valid choices:

* cluster_telnet_enabled """

    id = Size(
        data_key="id",
    )
    r""" Event Identifier

Example: 198 """

    solution = fields.Str(
        data_key="solution",
    )
    r""" Corrective action for the event

Example: Continue to disable telnet on the selected cluster using the 'security protocol modify -application telnet -enabled false’ ontap cli command. """

    source = fields.Nested("netapp_ontap.models.event_remediations_source.EventRemediationsSourceSchema", data_key="source", unknown=EXCLUDE)
    r""" The source field of the event_remediations. """

    source_full_name = fields.Str(
        data_key="source_full_name",
    )
    r""" Source of the event

Example: shrey-vsim1 """

    source_resource_type = fields.Str(
        data_key="source_resource_type",
        validate=enum_validation(['cluster']),
    )
    r""" Type of source of the event

Valid choices:

* cluster """

    start_time = ImpreciseDateTime(
        data_key="start_time",
    )
    r""" Start time of the event """

    @property
    def resource(self):
        return EventRemediations

    gettable_fields = [
        "cluster",
        "completion_time",
        "description",
        "event_remediation_action",
        "event_remediation_action_type",
        "event_remediation_state",
        "event_type_name",
        "id",
        "solution",
        "source",
        "source_full_name",
        "source_resource_type",
        "start_time",
    ]
    """cluster,completion_time,description,event_remediation_action,event_remediation_action_type,event_remediation_state,event_type_name,id,solution,source,source_full_name,source_resource_type,start_time,"""

    patchable_fields = [
        "cluster",
        "completion_time",
        "description",
        "event_remediation_action",
        "event_remediation_action_type",
        "event_remediation_state",
        "event_type_name",
        "id",
        "solution",
        "source",
        "source_full_name",
        "source_resource_type",
        "start_time",
    ]
    """cluster,completion_time,description,event_remediation_action,event_remediation_action_type,event_remediation_state,event_type_name,id,solution,source,source_full_name,source_resource_type,start_time,"""

    postable_fields = [
        "cluster",
        "completion_time",
        "description",
        "event_remediation_action_type",
        "event_remediation_state",
        "event_type_name",
        "solution",
        "source",
        "source_full_name",
        "source_resource_type",
        "start_time",
    ]
    """cluster,completion_time,description,event_remediation_action_type,event_remediation_state,event_type_name,solution,source,source_full_name,source_resource_type,start_time,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in EventRemediations.get_collection(fields=field)]
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
            raise NetAppRestError("EventRemediations modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class EventRemediations(Resource):
    """Allows interaction with EventRemediations objects on the host"""

    _schema = EventRemediationsSchema
    _path = "/api/private/manage/event-remediations"
    _keys = ["id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Event remediation and management action collection GET
### Learn more
* [`DOC /private/manage/event-remediations`](#docs-manage-private_manage_event-remediations)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="event remediations show")
        def event_remediations_show(
            completion_time: Choices.define(_get_field_list("completion_time"), cache_choices=True, inexact=True)=None,
            description: Choices.define(_get_field_list("description"), cache_choices=True, inexact=True)=None,
            event_remediation_action: Choices.define(_get_field_list("event_remediation_action"), cache_choices=True, inexact=True)=None,
            event_remediation_action_type: Choices.define(_get_field_list("event_remediation_action_type"), cache_choices=True, inexact=True)=None,
            event_remediation_state: Choices.define(_get_field_list("event_remediation_state"), cache_choices=True, inexact=True)=None,
            event_type_name: Choices.define(_get_field_list("event_type_name"), cache_choices=True, inexact=True)=None,
            id: Choices.define(_get_field_list("id"), cache_choices=True, inexact=True)=None,
            solution: Choices.define(_get_field_list("solution"), cache_choices=True, inexact=True)=None,
            source_full_name: Choices.define(_get_field_list("source_full_name"), cache_choices=True, inexact=True)=None,
            source_resource_type: Choices.define(_get_field_list("source_resource_type"), cache_choices=True, inexact=True)=None,
            start_time: Choices.define(_get_field_list("start_time"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["completion_time", "description", "event_remediation_action", "event_remediation_action_type", "event_remediation_state", "event_type_name", "id", "solution", "source_full_name", "source_resource_type", "start_time", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of EventRemediations resources

            Args:
                completion_time: Completion time of the event
                description: Description for the event
                event_remediation_action: Event remediation action
                event_remediation_action_type: Type of remediation action
                event_remediation_state: State of the event remediation
                event_type_name: Type of the event
                id: Event Identifier
                solution: Corrective action for the event
                source_full_name: Source of the event
                source_resource_type: Type of source of the event
                start_time: Start time of the event
            """

            kwargs = {}
            if completion_time is not None:
                kwargs["completion_time"] = completion_time
            if description is not None:
                kwargs["description"] = description
            if event_remediation_action is not None:
                kwargs["event_remediation_action"] = event_remediation_action
            if event_remediation_action_type is not None:
                kwargs["event_remediation_action_type"] = event_remediation_action_type
            if event_remediation_state is not None:
                kwargs["event_remediation_state"] = event_remediation_state
            if event_type_name is not None:
                kwargs["event_type_name"] = event_type_name
            if id is not None:
                kwargs["id"] = id
            if solution is not None:
                kwargs["solution"] = solution
            if source_full_name is not None:
                kwargs["source_full_name"] = source_full_name
            if source_resource_type is not None:
                kwargs["source_resource_type"] = source_resource_type
            if start_time is not None:
                kwargs["start_time"] = start_time
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return EventRemediations.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Event remediation and management action collection GET
### Learn more
* [`DOC /private/manage/event-remediations`](#docs-manage-private_manage_event-remediations)
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
        r"""Perform an event management action.
### Learn more
* [`DOC /private/manage/event-remediations`](#docs-manage-private_manage_event-remediations)
"""
        return super()._patch_collection(body, *args, connection=connection, **kwargs)

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Event remediation and management action collection GET
### Learn more
* [`DOC /private/manage/event-remediations`](#docs-manage-private_manage_event-remediations)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Event remediation and management action
### Learn more
* [`DOC /private/manage/event-remediations`](#docs-manage-private_manage_event-remediations)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Perform an event management action.
### Learn more
* [`DOC /private/manage/event-remediations`](#docs-manage-private_manage_event-remediations)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="event remediations modify")
        async def event_remediations_modify(
            completion_time: datetime = None,
            query_completion_time: datetime = None,
            description: str = None,
            query_description: str = None,
            event_remediation_action: str = None,
            query_event_remediation_action: str = None,
            event_remediation_action_type: str = None,
            query_event_remediation_action_type: str = None,
            event_remediation_state: str = None,
            query_event_remediation_state: str = None,
            event_type_name: str = None,
            query_event_type_name: str = None,
            id: Size = None,
            query_id: Size = None,
            solution: str = None,
            query_solution: str = None,
            source_full_name: str = None,
            query_source_full_name: str = None,
            source_resource_type: str = None,
            query_source_resource_type: str = None,
            start_time: datetime = None,
            query_start_time: datetime = None,
        ) -> ResourceTable:
            """Modify an instance of a EventRemediations resource

            Args:
                completion_time: Completion time of the event
                query_completion_time: Completion time of the event
                description: Description for the event
                query_description: Description for the event
                event_remediation_action: Event remediation action
                query_event_remediation_action: Event remediation action
                event_remediation_action_type: Type of remediation action
                query_event_remediation_action_type: Type of remediation action
                event_remediation_state: State of the event remediation
                query_event_remediation_state: State of the event remediation
                event_type_name: Type of the event
                query_event_type_name: Type of the event
                id: Event Identifier
                query_id: Event Identifier
                solution: Corrective action for the event
                query_solution: Corrective action for the event
                source_full_name: Source of the event
                query_source_full_name: Source of the event
                source_resource_type: Type of source of the event
                query_source_resource_type: Type of source of the event
                start_time: Start time of the event
                query_start_time: Start time of the event
            """

            kwargs = {}
            changes = {}
            if query_completion_time is not None:
                kwargs["completion_time"] = query_completion_time
            if query_description is not None:
                kwargs["description"] = query_description
            if query_event_remediation_action is not None:
                kwargs["event_remediation_action"] = query_event_remediation_action
            if query_event_remediation_action_type is not None:
                kwargs["event_remediation_action_type"] = query_event_remediation_action_type
            if query_event_remediation_state is not None:
                kwargs["event_remediation_state"] = query_event_remediation_state
            if query_event_type_name is not None:
                kwargs["event_type_name"] = query_event_type_name
            if query_id is not None:
                kwargs["id"] = query_id
            if query_solution is not None:
                kwargs["solution"] = query_solution
            if query_source_full_name is not None:
                kwargs["source_full_name"] = query_source_full_name
            if query_source_resource_type is not None:
                kwargs["source_resource_type"] = query_source_resource_type
            if query_start_time is not None:
                kwargs["start_time"] = query_start_time

            if completion_time is not None:
                changes["completion_time"] = completion_time
            if description is not None:
                changes["description"] = description
            if event_remediation_action is not None:
                changes["event_remediation_action"] = event_remediation_action
            if event_remediation_action_type is not None:
                changes["event_remediation_action_type"] = event_remediation_action_type
            if event_remediation_state is not None:
                changes["event_remediation_state"] = event_remediation_state
            if event_type_name is not None:
                changes["event_type_name"] = event_type_name
            if id is not None:
                changes["id"] = id
            if solution is not None:
                changes["solution"] = solution
            if source_full_name is not None:
                changes["source_full_name"] = source_full_name
            if source_resource_type is not None:
                changes["source_resource_type"] = source_resource_type
            if start_time is not None:
                changes["start_time"] = start_time

            if hasattr(EventRemediations, "find"):
                resource = EventRemediations.find(
                    **kwargs
                )
            else:
                resource = EventRemediations()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify EventRemediations: %s" % err)



