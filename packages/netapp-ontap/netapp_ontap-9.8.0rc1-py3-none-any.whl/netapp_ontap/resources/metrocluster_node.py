r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
Retrieves the configuration information for the nodes in the MetroCluster configuration.
####
---
### Example
```
GET https://<mgmt-ip>/api/cluster/metrocluster/nodes
{
    "records": [
        {
            "dr_group_id": 1,
            "cluster": {
                "name": "cluster1",
                "uuid": "8f77de32-9857-11e9-9a55-005056828eb9",
                "_links": {
                    "self": {
                        "href": "/api/cluster/8f77de32-9857-11e9-9a55-005056828eb9"
                    }
                }
            },
            "node": {
                "name": "cluster1_01",
                "uuid": "46147363-9857-11e9-9a55-005056828eb9",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/46147363-9857-11e9-9a55-005056828eb9"
                    }
                }
            },
            "dr_mirroring_state": "enabled",
            "configuration_state": "configured",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/nodes/46147363-9857-11e9-9a55-005056828eb9"
                }
            }
        },
        {
            "dr_group_id": 1,
            "cluster": {
                "name": "cluster1",
                "uuid": "8f77de32-9857-11e9-9a55-005056828eb9",
                "_links": {
                    "self": {
                        "href": "/api/cluster/8f77de32-9857-11e9-9a55-005056828eb9"
                    }
                }
            },
            "node": {
                "name": "cluster1_02",
                "uuid": "cf1dc67f-9857-11e9-bf80-005056829db6",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/cf1dc67f-9857-11e9-bf80-005056829db6"
                    }
                }
            },
            "dr_mirroring_state": "enabled",
            "configuration_state": "configured",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/nodes/cf1dc67f-9857-11e9-bf80-005056829db6"
                }
            }
        },
        {
            "dr_group_id": 1,
            "cluster": {
                "name": "cluster3",
                "uuid": "aa8aa15a-9857-11e9-80c9-00505682e684",
                "_links": {
                    "self": {
                        "href": "/api/cluster/aa8aa15a-9857-11e9-80c9-00505682e684"
                    }
                }
            },
            "node": {
                "name": "cluster3_01",
                "uuid": "5b3b983b-9857-11e9-80c9-00505682e684",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/5b3b983b-9857-11e9-80c9-00505682e684"
                    }
                }
            },
            "dr_mirroring_state": "enabled",
            "configuration_state": "configured",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/nodes/5b3b983b-9857-11e9-80c9-00505682e684"
                }
            }
        },
        {
            "dr_group_id": 1,
            "cluster": {
                "name": "cluster3",
                "uuid": "aa8aa15a-9857-11e9-80c9-00505682e684",
                "_links": {
                    "self": {
                        "href": "/api/cluster/aa8aa15a-9857-11e9-80c9-00505682e684"
                    }
                }
            },
            "node": {
                "name": "cluster3_02",
                "uuid": "45bff538-9858-11e9-a624-005056820377",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/45bff538-9858-11e9-a624-005056820377"
                    }
                }
            },
            "dr_mirroring_state": "enabled",
            "configuration_state": "configured",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/nodes/45bff538-9858-11e9-a624-005056820377"
                }
            }
        }
    ],
    "num_records": 4,
    "_links": {
        "self": {
            "href": "/api/cluster/metrocluster/nodes?fields=%2A"
        }
    }
}
```
---
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


__all__ = ["MetroclusterNode", "MetroclusterNodeSchema"]
__pdoc__ = {
    "MetroclusterNodeSchema.resource": False,
    "MetroclusterNode.metrocluster_node_show": False,
    "MetroclusterNode.metrocluster_node_create": False,
    "MetroclusterNode.metrocluster_node_modify": False,
    "MetroclusterNode.metrocluster_node_delete": False,
}


class MetroclusterNodeSchema(ResourceSchema):
    """The fields of the MetroclusterNode object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the metrocluster_node. """

    cluster = fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", data_key="cluster", unknown=EXCLUDE)
    r""" The cluster field of the metrocluster_node. """

    configuration_state = fields.Str(
        data_key="configuration_state",
        validate=enum_validation(['unreachable', 'configured']),
    )
    r""" Configuration state of the node.

Valid choices:

* unreachable
* configured """

    dr_group_id = Size(
        data_key="dr_group_id",
    )
    r""" DR Group ID. """

    dr_mirroring_state = fields.Str(
        data_key="dr_mirroring_state",
        validate=enum_validation(['enabled', 'disabled', 'unreachable', 'configured']),
    )
    r""" State of the DR mirroring configuration.

Valid choices:

* enabled
* disabled
* unreachable
* configured """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE)
    r""" The node field of the metrocluster_node. """

    @property
    def resource(self):
        return MetroclusterNode

    gettable_fields = [
        "links",
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "configuration_state",
        "dr_group_id",
        "dr_mirroring_state",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """links,cluster.links,cluster.name,cluster.uuid,configuration_state,dr_group_id,dr_mirroring_state,node.links,node.name,node.uuid,"""

    patchable_fields = [
        "cluster.name",
        "cluster.uuid",
        "node.name",
        "node.uuid",
    ]
    """cluster.name,cluster.uuid,node.name,node.uuid,"""

    postable_fields = [
        "cluster.name",
        "cluster.uuid",
        "node.name",
        "node.uuid",
    ]
    """cluster.name,cluster.uuid,node.name,node.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in MetroclusterNode.get_collection(fields=field)]
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
            raise NetAppRestError("MetroclusterNode modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class MetroclusterNode(Resource):
    r""" Data for a node in a MetroCluster. REST: /api/cluster/metrocluster/nodes """

    _schema = MetroclusterNodeSchema
    _path = "/api/cluster/metrocluster/nodes"
    _keys = ["node.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves MetroCluster nodes and their configurations.
### Related ONTAP Commands
* `metrocluster node show`
### Learn more
* [`DOC /cluster/metrocluster/nodes`](#docs-cluster-cluster_metrocluster_nodes)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="metrocluster node show")
        def metrocluster_node_show(
            configuration_state: Choices.define(_get_field_list("configuration_state"), cache_choices=True, inexact=True)=None,
            dr_group_id: Choices.define(_get_field_list("dr_group_id"), cache_choices=True, inexact=True)=None,
            dr_mirroring_state: Choices.define(_get_field_list("dr_mirroring_state"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["configuration_state", "dr_group_id", "dr_mirroring_state", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of MetroclusterNode resources

            Args:
                configuration_state: Configuration state of the node.
                dr_group_id: DR Group ID.
                dr_mirroring_state: State of the DR mirroring configuration.
            """

            kwargs = {}
            if configuration_state is not None:
                kwargs["configuration_state"] = configuration_state
            if dr_group_id is not None:
                kwargs["dr_group_id"] = dr_group_id
            if dr_mirroring_state is not None:
                kwargs["dr_mirroring_state"] = dr_mirroring_state
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return MetroclusterNode.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves MetroCluster nodes and their configurations.
### Related ONTAP Commands
* `metrocluster node show`
### Learn more
* [`DOC /cluster/metrocluster/nodes`](#docs-cluster-cluster_metrocluster_nodes)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves MetroCluster nodes and their configurations.
### Related ONTAP Commands
* `metrocluster node show`
### Learn more
* [`DOC /cluster/metrocluster/nodes`](#docs-cluster-cluster_metrocluster_nodes)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the node configuration in the MetroCluster.
### Related ONTAP Commands
* `metrocluster node show`

### Learn more
* [`DOC /cluster/metrocluster/nodes`](#docs-cluster-cluster_metrocluster_nodes)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





