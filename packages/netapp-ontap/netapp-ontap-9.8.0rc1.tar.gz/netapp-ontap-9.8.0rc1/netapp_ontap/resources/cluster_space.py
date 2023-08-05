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


__all__ = ["ClusterSpace", "ClusterSpaceSchema"]
__pdoc__ = {
    "ClusterSpaceSchema.resource": False,
    "ClusterSpace.cluster_space_show": False,
    "ClusterSpace.cluster_space_create": False,
    "ClusterSpace.cluster_space_modify": False,
    "ClusterSpace.cluster_space_delete": False,
}


class ClusterSpaceSchema(ResourceSchema):
    """The fields of the ClusterSpace object"""

    block_storage = fields.Nested("netapp_ontap.models.cluster_space_block_storage.ClusterSpaceBlockStorageSchema", data_key="block_storage", unknown=EXCLUDE)
    r""" The block_storage field of the cluster_space. """

    cloud_storage = fields.Nested("netapp_ontap.models.cluster_space_cloud_storage.ClusterSpaceCloudStorageSchema", data_key="cloud_storage", unknown=EXCLUDE)
    r""" The cloud_storage field of the cluster_space. """

    efficiency = fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", data_key="efficiency", unknown=EXCLUDE)
    r""" The efficiency field of the cluster_space. """

    efficiency_without_snapshots = fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", data_key="efficiency_without_snapshots", unknown=EXCLUDE)
    r""" The efficiency_without_snapshots field of the cluster_space. """

    @property
    def resource(self):
        return ClusterSpace

    gettable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,"""

    patchable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,"""

    postable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in ClusterSpace.get_collection(fields=field)]
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
            raise NetAppRestError("ClusterSpace modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class ClusterSpace(Resource):
    """Allows interaction with ClusterSpace objects on the host"""

    _schema = ClusterSpaceSchema
    _path = "/api/storage/cluster"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Reports cluster wide storage details across different tiers. By default, this endpoint returns all fields.
Supports the following roles: admin, and readonly.
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cluster space show")
        def cluster_space_show(
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single ClusterSpace resource

            Args:
            """

            kwargs = {}
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            resource = ClusterSpace(
                **kwargs
            )
            resource.get()
            return [resource]





