r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Retrieving storage disk information
The storage disk GET API retrieves all of the disks in the cluster.
<br/>
---
## Examples
### 1) Retrieve a list of disks from the cluster.
#### The following example shows the response with a list of disks in the cluster:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Disk.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Disk({"name": "1.24.4"}),
    Disk({"name": "1.24.3"}),
    Disk({"name": "1.24.5"}),
    Disk({"name": "1.24.0"}),
    Disk({"name": "1.24.2"}),
    Disk({"name": "1.24.1"}),
]

```
</div>
</div>

---
### 2) Retrieve a specific disk from the cluster.
#### The following example shows the response of the requested disk. If there is no disk with the requested name, an error is returned:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk(name="1.24.3")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Disk(
    {
        "shelf": {"uid": "10318311901725526608"},
        "serial_number": "EC47PC5021SW",
        "usable_size": 438304768000,
        "uid": "50000394:0808AA88:00000000:00000000:00000000:00000000:00000000:00000000:00000000:00000000",
        "name": "1.24.3",
        "container_type": "aggregate",
        "rpm": 10000,
        "node": {
            "name": "node-2",
            "uuid": "3a89ed49-8c6d-11e8-93bc-00a0985a64b6",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/3a89ed49-8c6d-11e8-93bc-00a0985a64b6"
                }
            },
        },
        "type": "sas",
        "aggregates": [
            {
                "uuid": "3fd9c345-ba91-4949-a7b1-6e2b898d74e3",
                "_links": {
                    "self": {
                        "href": "/api/storage/aggregates/3fd9c345-ba91-4949-a7b1-6e2b898d74e3"
                    }
                },
                "name": "node_2_SAS_1",
            }
        ],
        "state": "present",
        "model": "X421_FAL12450A10",
        "home_node": {
            "name": "node-2",
            "uuid": "3a89ed49-8c6d-11e8-93bc-00a0985a64b6",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/3a89ed49-8c6d-11e8-93bc-00a0985a64b6"
                }
            },
        },
        "firmware_version": "NA02",
        "pool": "pool0",
        "bay": 3,
        "vendor": "NETAPP",
        "class": "performance",
    }
)

```
</div>
</div>

---
## Modifying storage disk
The storage disk PATCH API modifies disk ownership or encrypting drive authentication keys (AKs) in the cluster.
### Updating the disk ownership for a specified disk
### 1. When the disk is not assigned
When the disk is a spare (or unowned) disk and node name is specified, the PATCH opertaion assigns the disk to the specified node.
### 2. When the disk is already assigned
When the disk is already assigned (aleady has a owner), and a new node is specified, the PATCH operation changes the ownership to the new node.
<br/>
---
## Examples
### 1. Update the disk ownership for an unowned disk
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk(name="<disk-name>")
    resource.node.name = "node-name"
    resource.patch()

```

---
### 2. Update the disk ownership for an already owned disk.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk(name="<disk-name>")
    resource.node.name = "node-name"
    resource.patch()

```

---
### 3. Rekey the data AK of all encrypting drives to an AK selected automatically by the system.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Disk

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Disk()
    resource.patch(hydrate=True, name="*", encryption_operation="rekey_data_auto_id")

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


__all__ = ["Disk", "DiskSchema"]
__pdoc__ = {
    "DiskSchema.resource": False,
    "Disk.disk_show": False,
    "Disk.disk_create": False,
    "Disk.disk_modify": False,
    "Disk.disk_delete": False,
}


class DiskSchema(ResourceSchema):
    """The fields of the Disk object"""

    aggregates = fields.List(fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE), data_key="aggregates")
    r""" List of aggregates sharing this disk """

    bay = Size(
        data_key="bay",
    )
    r""" Disk shelf bay

Example: 1 """

    class_ = fields.Str(
        data_key="class",
        validate=enum_validation(['unknown', 'capacity', 'performance', 'archive', 'solid_state', 'array', 'virtual']),
    )
    r""" Disk class

Valid choices:

* unknown
* capacity
* performance
* archive
* solid_state
* array
* virtual """

    container_type = fields.Str(
        data_key="container_type",
        validate=enum_validation(['aggregate', 'broken', 'foreign', 'labelmaint', 'maintenance', 'shared', 'spare', 'unassigned', 'unknown', 'unsupported', 'remote', 'mediator']),
    )
    r""" Type of overlying disk container

Valid choices:

* aggregate
* broken
* foreign
* labelmaint
* maintenance
* shared
* spare
* unassigned
* unknown
* unsupported
* remote
* mediator """

    dr_node = fields.Nested("netapp_ontap.models.dr_node.DrNodeSchema", data_key="dr_node", unknown=EXCLUDE)
    r""" The dr_node field of the disk. """

    drawer = fields.Nested("netapp_ontap.models.disk_drawer.DiskDrawerSchema", data_key="drawer", unknown=EXCLUDE)
    r""" The drawer field of the disk. """

    encryption_operation = fields.Str(
        data_key="encryption_operation",
    )
    r""" Encryption operation to apply to the drives. Possible values are:
- rekey_data_default
- rekey_data_auto_id """

    fips_certified = fields.Boolean(
        data_key="fips_certified",
    )
    r""" The fips_certified field of the disk. """

    firmware_version = fields.Str(
        data_key="firmware_version",
    )
    r""" The firmware_version field of the disk.

Example: NA51 """

    home_node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="home_node", unknown=EXCLUDE)
    r""" The home_node field of the disk. """

    key_id = fields.Nested("netapp_ontap.models.disk_key_id.DiskKeyIdSchema", data_key="key_id", unknown=EXCLUDE)
    r""" The key_id field of the disk. """

    model = fields.Str(
        data_key="model",
    )
    r""" The model field of the disk.

Example: X421_HCOBE450A10 """

    name = fields.Str(
        data_key="name",
    )
    r""" Cluster-wide disk name

Example: 1.0.1 """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE)
    r""" The node field of the disk. """

    pool = fields.Str(
        data_key="pool",
        validate=enum_validation(['pool0', 'pool1', 'failed', 'none']),
    )
    r""" Pool to which disk is assigned

Valid choices:

* pool0
* pool1
* failed
* none """

    protection_mode = fields.Str(
        data_key="protection_mode",
        validate=enum_validation(['open', 'data', 'part', 'full']),
    )
    r""" Mode of drive data protection and FIPS compliance. Possible values are:
- _open_ - Disk is unprotected
- _data_ - Data protection only without FIPS compliance
- _part_ - Partial protection with FIPS compliance only
- _full_ - Full data and FIPS compliance protection


Valid choices:

* open
* data
* part
* full """

    rated_life_used_percent = Size(
        data_key="rated_life_used_percent",
    )
    r""" Percentage of rated life used

Example: 10 """

    rpm = Size(
        data_key="rpm",
    )
    r""" Revolutions per minute

Example: 15000 """

    self_encrypting = fields.Boolean(
        data_key="self_encrypting",
    )
    r""" The self_encrypting field of the disk. """

    serial_number = fields.Str(
        data_key="serial_number",
    )
    r""" The serial_number field of the disk.

Example: KHG2VX8R """

    shelf = fields.Nested("netapp_ontap.resources.shelf.ShelfSchema", data_key="shelf", unknown=EXCLUDE)
    r""" The shelf field of the disk. """

    state = fields.Str(
        data_key="state",
        validate=enum_validation(['broken', 'copy', 'maintenance', 'partner', 'pending', 'present', 'reconstructing', 'removed', 'spare', 'unfail', 'zeroing']),
    )
    r""" State

Valid choices:

* broken
* copy
* maintenance
* partner
* pending
* present
* reconstructing
* removed
* spare
* unfail
* zeroing """

    type = fields.Str(
        data_key="type",
        validate=enum_validation(['ata', 'bsas', 'fcal', 'fsas', 'lun', 'sas', 'msata', 'ssd', 'vmdisk', 'unknown', 'ssd_cap', 'ssd_nvm']),
    )
    r""" Disk interface type

Valid choices:

* ata
* bsas
* fcal
* fsas
* lun
* sas
* msata
* ssd
* vmdisk
* unknown
* ssd_cap
* ssd_nvm """

    uid = fields.Str(
        data_key="uid",
    )
    r""" The unique identifier for a disk

Example: 002538E5:71B00B2F:00000000:00000000:00000000:00000000:00000000:00000000:00000000:00000000 """

    usable_size = Size(
        data_key="usable_size",
    )
    r""" The usable_size field of the disk.

Example: 959934889984 """

    vendor = fields.Str(
        data_key="vendor",
    )
    r""" The vendor field of the disk.

Example: NETAPP """

    @property
    def resource(self):
        return Disk

    gettable_fields = [
        "aggregates.links",
        "aggregates.name",
        "aggregates.uuid",
        "bay",
        "class_",
        "container_type",
        "dr_node.name",
        "dr_node.uuid",
        "drawer",
        "fips_certified",
        "firmware_version",
        "home_node.links",
        "home_node.name",
        "home_node.uuid",
        "key_id",
        "model",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "pool",
        "protection_mode",
        "rated_life_used_percent",
        "rpm",
        "self_encrypting",
        "serial_number",
        "shelf.links",
        "shelf.uid",
        "state",
        "type",
        "uid",
        "usable_size",
        "vendor",
    ]
    """aggregates.links,aggregates.name,aggregates.uuid,bay,class_,container_type,dr_node.name,dr_node.uuid,drawer,fips_certified,firmware_version,home_node.links,home_node.name,home_node.uuid,key_id,model,name,node.links,node.name,node.uuid,pool,protection_mode,rated_life_used_percent,rpm,self_encrypting,serial_number,shelf.links,shelf.uid,state,type,uid,usable_size,vendor,"""

    patchable_fields = [
        "drawer",
        "encryption_operation",
        "key_id",
        "node.name",
        "node.uuid",
    ]
    """drawer,encryption_operation,key_id,node.name,node.uuid,"""

    postable_fields = [
        "drawer",
        "key_id",
    ]
    """drawer,key_id,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Disk.get_collection(fields=field)]
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
            raise NetAppRestError("Disk modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Disk(Resource):
    """Allows interaction with Disk objects on the host"""

    _schema = DiskSchema
    _path = "/api/storage/disks"
    _keys = ["name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of disks.
### Related ONTAP commands
* `storage disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="disk show")
        def disk_show(
            bay: Choices.define(_get_field_list("bay"), cache_choices=True, inexact=True)=None,
            class_: Choices.define(_get_field_list("class_"), cache_choices=True, inexact=True)=None,
            container_type: Choices.define(_get_field_list("container_type"), cache_choices=True, inexact=True)=None,
            encryption_operation: Choices.define(_get_field_list("encryption_operation"), cache_choices=True, inexact=True)=None,
            fips_certified: Choices.define(_get_field_list("fips_certified"), cache_choices=True, inexact=True)=None,
            firmware_version: Choices.define(_get_field_list("firmware_version"), cache_choices=True, inexact=True)=None,
            model: Choices.define(_get_field_list("model"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            pool: Choices.define(_get_field_list("pool"), cache_choices=True, inexact=True)=None,
            protection_mode: Choices.define(_get_field_list("protection_mode"), cache_choices=True, inexact=True)=None,
            rated_life_used_percent: Choices.define(_get_field_list("rated_life_used_percent"), cache_choices=True, inexact=True)=None,
            rpm: Choices.define(_get_field_list("rpm"), cache_choices=True, inexact=True)=None,
            self_encrypting: Choices.define(_get_field_list("self_encrypting"), cache_choices=True, inexact=True)=None,
            serial_number: Choices.define(_get_field_list("serial_number"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            type: Choices.define(_get_field_list("type"), cache_choices=True, inexact=True)=None,
            uid: Choices.define(_get_field_list("uid"), cache_choices=True, inexact=True)=None,
            usable_size: Choices.define(_get_field_list("usable_size"), cache_choices=True, inexact=True)=None,
            vendor: Choices.define(_get_field_list("vendor"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["bay", "class_", "container_type", "encryption_operation", "fips_certified", "firmware_version", "model", "name", "pool", "protection_mode", "rated_life_used_percent", "rpm", "self_encrypting", "serial_number", "state", "type", "uid", "usable_size", "vendor", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Disk resources

            Args:
                bay: Disk shelf bay
                class_: Disk class
                container_type: Type of overlying disk container
                encryption_operation: Encryption operation to apply to the drives. Possible values are: - rekey_data_default - rekey_data_auto_id 
                fips_certified: 
                firmware_version: 
                model: 
                name: Cluster-wide disk name
                pool: Pool to which disk is assigned
                protection_mode: Mode of drive data protection and FIPS compliance. Possible values are: - _open_ - Disk is unprotected - _data_ - Data protection only without FIPS compliance - _part_ - Partial protection with FIPS compliance only - _full_ - Full data and FIPS compliance protection 
                rated_life_used_percent: Percentage of rated life used
                rpm: Revolutions per minute
                self_encrypting: 
                serial_number: 
                state: State
                type: Disk interface type
                uid: The unique identifier for a disk
                usable_size: 
                vendor: 
            """

            kwargs = {}
            if bay is not None:
                kwargs["bay"] = bay
            if class_ is not None:
                kwargs["class_"] = class_
            if container_type is not None:
                kwargs["container_type"] = container_type
            if encryption_operation is not None:
                kwargs["encryption_operation"] = encryption_operation
            if fips_certified is not None:
                kwargs["fips_certified"] = fips_certified
            if firmware_version is not None:
                kwargs["firmware_version"] = firmware_version
            if model is not None:
                kwargs["model"] = model
            if name is not None:
                kwargs["name"] = name
            if pool is not None:
                kwargs["pool"] = pool
            if protection_mode is not None:
                kwargs["protection_mode"] = protection_mode
            if rated_life_used_percent is not None:
                kwargs["rated_life_used_percent"] = rated_life_used_percent
            if rpm is not None:
                kwargs["rpm"] = rpm
            if self_encrypting is not None:
                kwargs["self_encrypting"] = self_encrypting
            if serial_number is not None:
                kwargs["serial_number"] = serial_number
            if state is not None:
                kwargs["state"] = state
            if type is not None:
                kwargs["type"] = type
            if uid is not None:
                kwargs["uid"] = uid
            if usable_size is not None:
                kwargs["usable_size"] = usable_size
            if vendor is not None:
                kwargs["vendor"] = vendor
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Disk.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves a collection of disks.
### Related ONTAP commands
* `storage disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
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
        r"""Updates disk ownership or authentication keys.
### Related ONTAP commands
* `storage disk assign`
* `storage encryption disk modify -data-key-id`
* `security key-manager key query -key-type NSE-AK`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
        return super()._patch_collection(body, *args, connection=connection, **kwargs)

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)


    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of disks.
### Related ONTAP commands
* `storage disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific disk.
### Related ONTAP commands
* `storage disk show`
### Learn more
* [`DOC /storage/disks`](#docs-storage-storage_disks)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





