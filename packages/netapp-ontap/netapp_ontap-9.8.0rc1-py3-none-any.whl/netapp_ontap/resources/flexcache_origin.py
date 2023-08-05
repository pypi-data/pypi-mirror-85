r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
FlexCache is a persistent cache of an origin volume. An origin volume can only be a FlexVol while a FlexCache is always a FlexGroup.</br>
The following relationship configurations are supported:

* Intra-Vserver where FlexCache and the corresponding origin volume reside in the same Vserver.
* Cross-Vserver but intra-cluster where FlexCache and the origin volume reside in the same cluster but belong to different Vservers.
* Cross-cluster where FlexCache and the origin volume reside in different clusters.</br>
FlexCache supports fan-out and more than one FlexCache can be created from one origin volume.
This API retrieves the origin of FlexCache onfigurations in the origin cluster.
## FlexCache APIs
The following APIs can be used to perform operations related to the origin of a FlexCache:

* GET       /api/storage/flexcache/origins
* GET       /api/storage/flexcache/origins/{uuid}
## Examples
### Retrieving origins of FlexCache attributes
The GET request is used to retrieve the origins of FlexCache attributes.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FlexcacheOrigin

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(FlexcacheOrigin.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    FlexcacheOrigin(
        {
            "uuid": "2bc957dd-2617-4afb-8d2f-66ac6070d313",
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/origins/2bc957dd-2617-4afb-8d2f-66ac6070d313"
                }
            },
            "name": "vol_o1",
        }
    ),
    FlexcacheOrigin(
        {
            "uuid": "80fcaee4-0dc2-488b-afb8-86d28a34cda8",
            "_links": {
                "self": {
                    "href": "/api/storage/flexcache/origins/80fcaee4-0dc2-488b-afb8-86d28a34cda8"
                }
            },
            "name": "vol_1",
        }
    ),
]

```
</div>
</div>

### Retrieving the attributes of an origin volume
The GET request is used to retrieve the attributes of an origin volume.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import FlexcacheOrigin

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = FlexcacheOrigin(uuid="80fcaee4-0dc2-488b-afb8-86d28a34cda8")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
FlexcacheOrigin(
    {
        "uuid": "80fcaee4-0dc2-488b-afb8-86d28a34cda8",
        "_links": {
            "self": {
                "href": "/api/storage/flexcache/origins/80fcaee4-0dc2-488b-afb8-86d28a34cda8"
            }
        },
        "svm": {"name": "vs_3", "uuid": "8aa2cd28-0e92-11e9-b391-0050568e4115"},
        "name": "vol_1",
        "flexcaches": [
            {
                "ip_address": "10.140.103.183",
                "cluster": {
                    "name": "node4",
                    "uuid": "c32f16b8-0e90-11e9-aed0-0050568eddbe",
                },
                "create_time": "2019-01-02T19:27:22+05:30",
                "volume": {
                    "name": "fc_42",
                    "uuid": "4e7f9d49-0e96-11e9-aed0-0050568eddbe",
                },
                "svm": {
                    "name": "vs_1_4",
                    "uuid": "36f68322-0e93-11e9-aed0-0050568eddbe",
                },
            },
            {
                "ip_address": "10.140.103.183",
                "cluster": {
                    "name": "node4",
                    "uuid": "c32f16b8-0e90-11e9-aed0-0050568eddbe",
                },
                "create_time": "2019-01-02T21:08:34+05:30",
                "volume": {
                    "name": "fc_421",
                    "uuid": "71ee8f36-0ea4-11e9-aed0-0050568eddbe",
                },
                "svm": {
                    "name": "vs_1_4",
                    "uuid": "36f68322-0e93-11e9-aed0-0050568eddbe",
                },
            },
            {
                "ip_address": "10.140.103.183",
                "cluster": {
                    "name": "node4",
                    "uuid": "c32f16b8-0e90-11e9-aed0-0050568eddbe",
                },
                "create_time": "2019-01-03T11:14:38+05:30",
                "volume": {"name": "fc_422"},
                "svm": {
                    "name": "vs_1_4",
                    "uuid": "36f68322-0e93-11e9-aed0-0050568eddbe",
                },
            },
            {
                "ip_address": "10.140.103.179",
                "cluster": {
                    "name": "node3",
                    "uuid": "8eb21b3b-0e90-11e9-8180-0050568e0b79",
                },
                "create_time": "2019-01-02T19:24:14+05:30",
                "volume": {
                    "name": "fc_32",
                    "uuid": "ddb42bbc-0e95-11e9-8180-0050568e0b79",
                },
                "svm": {"name": "vs_1", "uuid": "e708fbe2-0e92-11e9-8180-0050568e0b79"},
                "size": 4294967296,
                "state": "online",
            },
            {
                "ip_address": "10.140.103.179",
                "cluster": {
                    "name": "node3",
                    "uuid": "8eb21b3b-0e90-11e9-8180-0050568e0b79",
                },
                "create_time": "2019-01-02T21:07:23+05:30",
                "volume": {
                    "name": "fc_321",
                    "uuid": "47902654-0ea4-11e9-8180-0050568e0b79",
                },
                "svm": {"name": "vs_1", "uuid": "e708fbe2-0e92-11e9-8180-0050568e0b79"},
                "size": 4294967296,
                "state": "online",
            },
            {
                "ip_address": "10.140.103.179",
                "cluster": {
                    "name": "node3",
                    "uuid": "8eb21b3b-0e90-11e9-8180-0050568e0b79",
                },
                "create_time": "2019-01-03T00:11:38+05:30",
                "volume": {
                    "name": "fc_322",
                    "uuid": "04d5e07b-0ebe-11e9-8180-0050568e0b79",
                },
                "svm": {"name": "vs_1", "uuid": "e708fbe2-0e92-11e9-8180-0050568e0b79"},
                "size": 4294967296,
                "state": "online",
            },
            {
                "ip_address": "10.140.103.179",
                "cluster": {
                    "name": "node3",
                    "uuid": "8eb21b3b-0e90-11e9-8180-0050568e0b79",
                },
                "create_time": "2019-01-03T00:14:52+05:30",
                "volume": {
                    "name": "fc_323",
                    "uuid": "77e911ff-0ebe-11e9-8180-0050568e0b79",
                },
                "svm": {"name": "vs_1", "uuid": "e708fbe2-0e92-11e9-8180-0050568e0b79"},
                "size": 4294967296,
                "state": "online",
            },
        ],
    }
)

```
</div>
</div>

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


__all__ = ["FlexcacheOrigin", "FlexcacheOriginSchema"]
__pdoc__ = {
    "FlexcacheOriginSchema.resource": False,
    "FlexcacheOrigin.flexcache_origin_show": False,
    "FlexcacheOrigin.flexcache_origin_create": False,
    "FlexcacheOrigin.flexcache_origin_modify": False,
    "FlexcacheOrigin.flexcache_origin_delete": False,
}


class FlexcacheOriginSchema(ResourceSchema):
    """The fields of the FlexcacheOrigin object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the flexcache_origin. """

    flexcaches = fields.List(fields.Nested("netapp_ontap.models.flexcache_relationship.FlexcacheRelationshipSchema", unknown=EXCLUDE), data_key="flexcaches")
    r""" The flexcaches field of the flexcache_origin. """

    name = fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=203),
    )
    r""" Origin volume name

Example: vol1, vol_2 """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the flexcache_origin. """

    uuid = fields.Str(
        data_key="uuid",
    )
    r""" Origin volume UUID. Unique identifier for origin of FlexCache.

Example: 1cd8a442-86d1-11e0-ae1c-123478563512 """

    @property
    def resource(self):
        return FlexcacheOrigin

    gettable_fields = [
        "links",
        "flexcaches",
        "name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,flexcaches,name,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "flexcaches",
        "name",
        "svm.name",
        "svm.uuid",
    ]
    """flexcaches,name,svm.name,svm.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in FlexcacheOrigin.get_collection(fields=field)]
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
            raise NetAppRestError("FlexcacheOrigin modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class FlexcacheOrigin(Resource):
    r""" Defines the origin endpoint of FlexCache. """

    _schema = FlexcacheOriginSchema
    _path = "/api/storage/flexcache/origins"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves origin of FlexCache in the cluster.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `flexcaches.ip_address` - IP address of FlexCache.
* `flexcaches.size` - Physical size of FlexCache.
* `flexcaches.guarantee.type` - Space guarantee style of FlexCache.
* `flexcaches.state` - State of FlexCache.
### Related ONTAP commands
* `volume flexcache origin show-caches`
### Learn more
* [`DOC /storage/flexcache/origins`](#docs-storage-storage_flexcache_origins)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="flexcache origin show")
        def flexcache_origin_show(
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["name", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of FlexcacheOrigin resources

            Args:
                name: Origin volume name
                uuid: Origin volume UUID. Unique identifier for origin of FlexCache.
            """

            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return FlexcacheOrigin.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves origin of FlexCache in the cluster.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `flexcaches.ip_address` - IP address of FlexCache.
* `flexcaches.size` - Physical size of FlexCache.
* `flexcaches.guarantee.type` - Space guarantee style of FlexCache.
* `flexcaches.state` - State of FlexCache.
### Related ONTAP commands
* `volume flexcache origin show-caches`
### Learn more
* [`DOC /storage/flexcache/origins`](#docs-storage-storage_flexcache_origins)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves origin of FlexCache in the cluster.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `flexcaches.ip_address` - IP address of FlexCache.
* `flexcaches.size` - Physical size of FlexCache.
* `flexcaches.guarantee.type` - Space guarantee style of FlexCache.
* `flexcaches.state` - State of FlexCache.
### Related ONTAP commands
* `volume flexcache origin show-caches`
### Learn more
* [`DOC /storage/flexcache/origins`](#docs-storage-storage_flexcache_origins)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves attributes of the origin of a FlexCache in the cluster.
### Expensive properties
There is an added cost to retrieving values for these properties. They are included by default in GET results. The recommended method to use this API is to filter and retrieve only the required fields. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `flexcaches.ip_address` - IP address of FlexCache.
* `flexcaches.size` - Physical size of FlexCache.
* `flexcaches.guarantee.type` - Space guarantee style of FlexCache.
* `flexcaches.state` - State of FlexCache.
### Related ONTAP commands
* `volume flexcache origin show-caches`
### Learn more
* [`DOC /storage/flexcache/origins`](#docs-storage-storage_flexcache_origins)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





