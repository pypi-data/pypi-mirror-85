r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
You can use this API to retrieve and display relevant information pertaining to MetroCluster interconnect status. The ```/cluster/metrocluster/interconnects``` endpoint returns a list of all the interconnects in MetroCluster and their status. Each individual interconnect can be queried individually using the ```/cluster/metrocluster/interconnects/{node.uuid}/{partner_type}/{adapter}``` endpoint.
####
---
### Examples
### Retrieving MetroCluster interconnects
```
GET https://<mgmt-ip>/api/cluster/metrocluster/interconnects
{
    "records": [
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "ha",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/ha/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "ha",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/ha/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "dr",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/dr/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "dr",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/dr/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "aux",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/aux/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_01",
                "uuid": "6fead8fe-8d81-11e9-b5a9-005056826931",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/6fead8fe-8d81-11e9-b5a9-005056826931"
                    }
                }
            },
            "partner_type": "aux",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/6fead8fe-8d81-11e9-b5a9-005056826931/aux/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "ha",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/ha/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "ha",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/ha/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "dr",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/dr/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "dr",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/dr/e0g"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "aux",
            "adapter": "e0f",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/aux/e0f"
                }
            }
        },
        {
            "node": {
                "name": "cluster1_02",
                "uuid": "f5435191-8d81-11e9-9d4b-00505682dc8b",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/f5435191-8d81-11e9-9d4b-00505682dc8b"
                    }
                }
            },
            "partner_type": "aux",
            "adapter": "e0g",
            "_links": {
                "self": {
                    "href": "/api/cluster/metrocluster/interconnects/f5435191-8d81-11e9-9d4b-00505682dc8b/aux/e0g"
                }
            }
        }
    ],
    "num_records": 12,
    "_links": {
        "self": {
            "href": "/api/cluster/metrocluster/interconnects"
        }
    }
}
```
### Retrieves information about a specific MetroCluster interconnect
```
https://<mgmt-ip>/api/cluster/metrocluster/interconnects/774b4fbc-86f9-11e9-9051-005056825c71/aux/e0f
{
    "node": {
        "name": "cluster1_01",
        "uuid": "46147363-9857-11e9-9a55-005056828eb9",
        "_links": {
            "self": {
                "href": "/api/cluster/nodes/46147363-9857-11e9-9a55-005056828eb9"
            }
        }
    },
    "partner_type": "ha",
    "adapter": "e0f",
    "state": "up",
    "type": "iwarp",
    "_links": {
        "self": {
            "href": "/api/cluster/metrocluster/interconnects/46147363-9857-11e9-9a55-005056828eb9/ha/e0f"
        }
    }
}
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


__all__ = ["MetroclusterInterconnect", "MetroclusterInterconnectSchema"]
__pdoc__ = {
    "MetroclusterInterconnectSchema.resource": False,
    "MetroclusterInterconnect.metrocluster_interconnect_show": False,
    "MetroclusterInterconnect.metrocluster_interconnect_create": False,
    "MetroclusterInterconnect.metrocluster_interconnect_modify": False,
    "MetroclusterInterconnect.metrocluster_interconnect_delete": False,
}


class MetroclusterInterconnectSchema(ResourceSchema):
    """The fields of the MetroclusterInterconnect object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the metrocluster_interconnect. """

    adapter = fields.Str(
        data_key="adapter",
    )
    r""" Adapter """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE)
    r""" The node field of the metrocluster_interconnect. """

    partner_type = fields.Str(
        data_key="partner_type",
        validate=enum_validation(['aux', 'dr', 'ha']),
    )
    r""" Partner type

Valid choices:

* aux
* dr
* ha """

    state = fields.Str(
        data_key="state",
        validate=enum_validation(['down', 'up']),
    )
    r""" Adapter status

Valid choices:

* down
* up """

    type = fields.Str(
        data_key="type",
        validate=enum_validation(['roce', 'iwarp', 'unknown']),
    )
    r""" Adapter type

Valid choices:

* roce
* iwarp
* unknown """

    @property
    def resource(self):
        return MetroclusterInterconnect

    gettable_fields = [
        "links",
        "adapter",
        "node.links",
        "node.name",
        "node.uuid",
        "partner_type",
        "state",
        "type",
    ]
    """links,adapter,node.links,node.name,node.uuid,partner_type,state,type,"""

    patchable_fields = [
        "node.name",
        "node.uuid",
    ]
    """node.name,node.uuid,"""

    postable_fields = [
        "node.name",
        "node.uuid",
    ]
    """node.name,node.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in MetroclusterInterconnect.get_collection(fields=field)]
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
            raise NetAppRestError("MetroclusterInterconnect modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class MetroclusterInterconnect(Resource):
    r""" Data for a MetroCluster interconnect. REST: /api/cluster/metrocluster/interconnects """

    _schema = MetroclusterInterconnectSchema
    _path = "/api/cluster/metrocluster/interconnects"
    _keys = ["node.uuid", "partner_type", "adapter"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a list of interconnect adapter information for nodes in the MetroCluster.
### Related ONTAP Commands
* `metrocluster interconnect show`
### Learn more
* [`DOC /cluster/metrocluster/interconnects`](#docs-cluster-cluster_metrocluster_interconnects)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="metrocluster interconnect show")
        def metrocluster_interconnect_show(
            adapter: Choices.define(_get_field_list("adapter"), cache_choices=True, inexact=True)=None,
            partner_type: Choices.define(_get_field_list("partner_type"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            type: Choices.define(_get_field_list("type"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["adapter", "partner_type", "state", "type", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of MetroclusterInterconnect resources

            Args:
                adapter: Adapter
                partner_type: Partner type
                state: Adapter status
                type: Adapter type
            """

            kwargs = {}
            if adapter is not None:
                kwargs["adapter"] = adapter
            if partner_type is not None:
                kwargs["partner_type"] = partner_type
            if state is not None:
                kwargs["state"] = state
            if type is not None:
                kwargs["type"] = type
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return MetroclusterInterconnect.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves a list of interconnect adapter information for nodes in the MetroCluster.
### Related ONTAP Commands
* `metrocluster interconnect show`
### Learn more
* [`DOC /cluster/metrocluster/interconnects`](#docs-cluster-cluster_metrocluster_interconnects)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a list of interconnect adapter information for nodes in the MetroCluster.
### Related ONTAP Commands
* `metrocluster interconnect show`
### Learn more
* [`DOC /cluster/metrocluster/interconnects`](#docs-cluster-cluster_metrocluster_interconnects)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves information about a MetroCluster Interconnect for a specific partner type and adapter.
### Related ONTAP Commands
* `metrocluster interconnect show`

### Learn more
* [`DOC /cluster/metrocluster/interconnects`](#docs-cluster-cluster_metrocluster_interconnects)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





