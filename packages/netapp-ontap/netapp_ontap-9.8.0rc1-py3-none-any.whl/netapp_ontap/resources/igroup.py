r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
An initiator group (igroup) is a collection of Fibre Channel (FC) world wide port names (WWPNs), and/or iSCSI Qualified Names (IQNs), and/or iSCSI EUIs (Extended Unique Identifiers) that identify host initiators.<br/>
Initiator groups are used to control which hosts can access specific LUNs. To grant access to a LUN from one or more hosts, create an initiator group containing the host initiator names, then create a LUN map that associates the initiator group with the LUN.<br/>
The initator group REST API allows you to create, update, delete, and discover initiator groups, and add and remove initiators that can access the target and associated LUNs.
An initiator can appear in multiple initiator groups. An initiator group can be mapped to multiple LUNs. A specific initiator can be mapped to a specific LUN only once.<br/>
All initiators in an initiator group must be from the same operating system. The initiator group's operating system is specified when the initiator group is created.<br/>
When an initiator group is created, the `protocol` property is used to restrict member initiators to Fibre Channel (_fcp_), iSCSI (_iscsi_), or both (_mixed_).<br/>
Zero or more initiators can be supplied when the initiator group is created. After creation, initiators can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/initiators` endpoint. See [`POST /protocols/san/igroups/{igroup.uuid}/initiators`](#/SAN/igroup_initiator_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/initiators/{name}`](#/SAN/igroup_initiator_delete) for more details.<br/>
An FC WWPN consist of 16 hexadecimal digits grouped as 8 pairs separated by colons. The format for an iSCSI IQN is _iqn.yyyy-mm.reverse_domain_name:any_. The iSCSI EUI format consists of the _eui._ prefix followed by 16 hexadecimal characters.
## Examples
### Creating an initiator group with no initiators
The example initiator group is for Linux iSCSI initiators only. Note that the `return_records` query parameter is used to obtain the newly created initiator group in the response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup()
    resource.svm.name = "svm1"
    resource.name = "igroup1"
    resource.os_type = "linux"
    resource.protocol = "iscsi"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Igroup(
    {
        "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
        "os_type": "linux",
        "_links": {
            "self": {
                "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
            }
        },
        "protocol": "iscsi",
        "svm": {
            "name": "svm1",
            "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            "_links": {
                "self": {"href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"}
            },
        },
        "name": "igroup1",
    }
)

```
</div>
</div>

---
### Creating an initiator group with initiators
The example initiator group is for Windows. FC Protocol and iSCSI initiators are allowed. Note that the `return_records` query parameter is used to obtain the newly created initiator group in the response.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup()
    resource.svm.name = "svm1"
    resource.name = "igroup2"
    resource.os_type = "windows"
    resource.protocol = "mixed"
    resource.initiators = [
        {"name": "20:01:00:50:56:bb:70:72"},
        {"name": "iqn.1991-05.com.ms:host1"},
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Igroup(
    {
        "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
        "os_type": "windows",
        "initiators": [
            {
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/20:01:00:50:56:bb:70:72"
                    }
                },
                "name": "20:01:00:50:56:bb:70:72",
            },
            {
                "_links": {
                    "self": {
                        "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/iqn.1991-05.com.ms:host1"
                    }
                },
                "name": "iqn.1991-05.com.ms:host1",
            },
        ],
        "_links": {
            "self": {
                "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
            }
        },
        "protocol": "mixed",
        "svm": {
            "name": "svm1",
            "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            "_links": {
                "self": {"href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"}
            },
        },
        "name": "igroup2",
    }
)

```
</div>
</div>

---
### Retrieving all initiator groups
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Igroup.get_collection()))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    Igroup(
        {
            "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "svm": {
                "name": "svm1",
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
            },
            "name": "igroup1",
        }
    ),
    Igroup(
        {
            "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "svm": {
                "name": "svm1",
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
            },
            "name": "igroup2",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all properties of all initiator groups
The `fields` query parameter is used to request all initiator group properties.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Igroup.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    Igroup(
        {
            "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
            "os_type": "linux",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "protocol": "iscsi",
            "svm": {
                "name": "svm1",
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
            },
            "name": "igroup1",
        }
    ),
    Igroup(
        {
            "uuid": "abf9c39d-ab9f-11e8-b8a3-005056bb7072",
            "os_type": "windows",
            "initiators": [
                {
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/20:01:00:50:56:bb:70:72"
                        }
                    },
                    "name": "20:01:00:50:56:bb:70:72",
                },
                {
                    "_links": {
                        "self": {
                            "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072/initiators/iqn.1991-05.com.ms:host1"
                        }
                    },
                    "name": "iqn.1991-05.com.ms:host1",
                },
            ],
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/abf9c39d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "protocol": "mixed",
            "svm": {
                "name": "svm1",
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
            },
            "name": "igroup2",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all initiator groups for Linux
The `os_type` query parameter is used to perform the query.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Igroup.get_collection(os_type="linux")))

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    Igroup(
        {
            "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
            "os_type": "linux",
            "_links": {
                "self": {
                    "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
                }
            },
            "svm": {
                "name": "svm1",
                "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"
                    }
                },
            },
            "name": "igroup1",
        }
    )
]

```
</div>
</div>

---
### Retrieving a specific initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
Igroup(
    {
        "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
        "os_type": "linux",
        "_links": {
            "self": {
                "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
            }
        },
        "protocol": "iscsi",
        "svm": {
            "name": "svm1",
            "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            "_links": {
                "self": {"href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"}
            },
        },
        "name": "igroup1",
    }
)

```
</div>
</div>

---
### Retrieving LUNs mapped to a specific initiator group
The `fields` parameter is used to specify the desired properties.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.get(fields="lun_maps")
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
Igroup(
    {
        "uuid": "8f249e7d-ab9f-11e8-b8a3-005056bb7072",
        "_links": {
            "self": {
                "href": "/api/protocols/san/igroups/8f249e7d-ab9f-11e8-b8a3-005056bb7072"
            }
        },
        "lun_maps": [
            {
                "lun": {
                    "uuid": "4b33ba57-c4e0-4dbb-bc47-214800d18a71",
                    "_links": {
                        "self": {
                            "href": "/api/storage/luns/4b33ba57-c4e0-4dbb-bc47-214800d18a71"
                        }
                    },
                    "node": {
                        "name": "node1",
                        "uuid": "f17182af-223f-4d51-8197-2cb2146d5c4c",
                        "_links": {
                            "self": {
                                "href": "/api/cluster/nodes/f17182af-223f-4d51-8197-2cb2146d5c4c"
                            }
                        },
                    },
                    "name": "/vol/vol1/lun1",
                },
                "logical_unit_number": 0,
            }
        ],
        "svm": {
            "name": "svm1",
            "uuid": "02b0dfff-aa28-11e8-a653-005056bb7072",
            "_links": {
                "self": {"href": "/api/svm/svms/02b0dfff-aa28-11e8-a653-005056bb7072"}
            },
        },
        "name": "igroup1",
    }
)

```
</div>
</div>

---
### Renaming an initiator group
Note that renaming an initiator group must be done in a PATCH request separate from any other modifications.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.name = "igroup1_newName"
    resource.patch()

```

---
### Changing the operating system type of an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.os_type = "aix"
    resource.patch()

```

---
### Adding an initiator to an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupInitiator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupInitiator("8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.name = "iqn.1991-05.com.ms:host2"
    resource.post(hydrate=True)
    print(resource)

```

---
### Adding multiple initiators to an initiator group
Note the use of the `records` property to add multiple initiators to the initiator group in a single API call.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupInitiator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupInitiator("8f249e7d-ab9f-11e8-b8a3-005056bb7072")
    resource.records = [
        {"name": "iqn.1991-05.com.ms:host3"},
        {"name": "iqn.1991-05.com.ms:host4"},
    ]
    resource.post(hydrate=True)
    print(resource)

```

---
### Removing an initiator from an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupInitiator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupInitiator(
        "8f249e7d-ab9f-11e8-b8a3-005056bb7072", name="iqn.1991-05.com.ms:host3"
    )
    resource.delete()

```

---
### Removing an initiator from a mapped initiator group
Normally, removing an initiator from an initiator group that is mapped to a LUN is not allowed. The removal can be forced using the `allow_delete_while_mapped` query parameter.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IgroupInitiator

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IgroupInitiator(
        "8f249e7d-ab9f-11e8-b8a3-005056bb7072", name="iqn.1991-05.com.ms:host4"
    )
    resource.delete(allow_delete_while_mapped=True)

```

---
### Deleting an initiator group
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="abf9c39d-ab9f-11e8-b8a3-005056bb7072")
    resource.delete()

```

---
### Deleting a mapped initiator group
Normally, deleting an initiator group that is mapped to a LUN is not allowed. The deletion can be forced using the `allow_delete_while_mapped` query parameter.
<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Igroup

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Igroup(uuid="abf9c39d-ab9f-11e8-b8a3-005056bb7072")
    resource.delete(allow_delete_while_mapped=True)

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


__all__ = ["Igroup", "IgroupSchema"]
__pdoc__ = {
    "IgroupSchema.resource": False,
    "Igroup.igroup_show": False,
    "Igroup.igroup_create": False,
    "Igroup.igroup_modify": False,
    "Igroup.igroup_delete": False,
}


class IgroupSchema(ResourceSchema):
    """The fields of the Igroup object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the igroup. """

    delete_on_unmap = fields.Boolean(
        data_key="delete_on_unmap",
    )
    r""" An option that causes the initiator group to be deleted when the last LUN map associated with it is deleted. Optional in POST and PATCH. This property defaults to _false_ when the initiator group is created. """

    initiators = fields.List(fields.Nested("netapp_ontap.models.igroup_initiator_no_records.IgroupInitiatorNoRecordsSchema", unknown=EXCLUDE), data_key="initiators")
    r""" The initiators that are members of the group. Optional in POST.<br/>
Zero or more initiators can be supplied when the initiator group is created. After creation, initiators can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/initiators` endpoint. See [`POST /protocols/san/igroups/{igroup.uuid}/initiators`](#/SAN/igroup_initiator_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/initiators/{name}`](#/SAN/igroup_initiator_delete) for more details. """

    lun_maps = fields.List(fields.Nested("netapp_ontap.models.igroup_lun_maps.IgroupLunMapsSchema", unknown=EXCLUDE), data_key="lun_maps")
    r""" All LUN maps with which the initiator is associated.<br/>
If the requested igroup is part of a remote, non-local, MetroCluster SVM, the LUN maps are not retrieved.
There is an added cost to retrieving property values for `lun_maps`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more. """

    name = fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=96),
    )
    r""" The name of the initiator group. Required in POST; optional in PATCH.<br/>
Note that renaming an initiator group must be done in a PATCH request separate from any other modifications.


Example: igroup1 """

    os_type = fields.Str(
        data_key="os_type",
        validate=enum_validation(['aix', 'hpux', 'hyper_v', 'linux', 'netware', 'openvms', 'solaris', 'vmware', 'windows', 'xen']),
    )
    r""" The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system. Required in POST; optional in PATCH.


Valid choices:

* aix
* hpux
* hyper_v
* linux
* netware
* openvms
* solaris
* vmware
* windows
* xen """

    protocol = fields.Str(
        data_key="protocol",
        validate=enum_validation(['fcp', 'iscsi', 'mixed']),
    )
    r""" The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group. Optional in POST; if not supplied, this defaults to _mixed_.<br/>
The protocol of an initiator group cannot be changed after creation of the group.


Valid choices:

* fcp
* iscsi
* mixed """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the igroup. """

    uuid = fields.Str(
        data_key="uuid",
    )
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return Igroup

    gettable_fields = [
        "links",
        "delete_on_unmap",
        "initiators",
        "lun_maps",
        "name",
        "os_type",
        "protocol",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """links,delete_on_unmap,initiators,lun_maps,name,os_type,protocol,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "delete_on_unmap",
        "name",
        "os_type",
        "svm.name",
        "svm.uuid",
    ]
    """delete_on_unmap,name,os_type,svm.name,svm.uuid,"""

    postable_fields = [
        "delete_on_unmap",
        "initiators",
        "name",
        "os_type",
        "protocol",
        "svm.name",
        "svm.uuid",
    ]
    """delete_on_unmap,initiators,name,os_type,protocol,svm.name,svm.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Igroup.get_collection(fields=field)]
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
            raise NetAppRestError("Igroup modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Igroup(Resource):
    r""" An initiator group (igroup) is a collection of Fibre Channel (FC) world wide port names (WWPN), and/or iSCSI Qualified Names (IQNs), and/or iSCSI EUIs (Extended Unique Identifiers) that identify host initiators.<br/>
Initiator groups are used to control which hosts can access specific LUNs. To grant access to a LUN from one or more hosts, create an initiator group containing the hosts' initiator names, then create a LUN map that associates the initiator group with the LUN.<br/>
An initiator can appear in multiple initiator groups. An initiator group can be mapped to multiple LUNs. A specific initiator can be mapped to a specific LUN only once.<br/>
All initiators in an initiator group must be from the same operating system. The initiator group's operating system is specified when the initiator group is created.<br/>
When an initiator group is created, the `protocol` property is used to restrict member initiators to Fibre Channel (_fcp_), iSCSI (_iscsi_), or both (_mixed_).<br/>
Zero or more initiators can be supplied when the initiator group is created. After creation, initiators can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/initiators` endpoint. See [`POST /protocols/san/igroups/{igroup.uuid}/initiators`](#/SAN/igroup_initiator_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/initiators/{name}`](#/SAN/igroup_initiator_delete) for more details.<br/> """

    _schema = IgroupSchema
    _path = "/api/protocols/san/igroups"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves initiator groups.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `lun_maps.*`
### Related ONTAP commands
* `lun igroup show`
* `lun mapping show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="igroup show")
        def igroup_show(
            delete_on_unmap: Choices.define(_get_field_list("delete_on_unmap"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            os_type: Choices.define(_get_field_list("os_type"), cache_choices=True, inexact=True)=None,
            protocol: Choices.define(_get_field_list("protocol"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["delete_on_unmap", "name", "os_type", "protocol", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Igroup resources

            Args:
                delete_on_unmap: An option that causes the initiator group to be deleted when the last LUN map associated with it is deleted. Optional in POST and PATCH. This property defaults to _false_ when the initiator group is created. 
                name: The name of the initiator group. Required in POST; optional in PATCH.<br/> Note that renaming an initiator group must be done in a PATCH request separate from any other modifications. 
                os_type: The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system. Required in POST; optional in PATCH. 
                protocol: The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group. Optional in POST; if not supplied, this defaults to _mixed_.<br/> The protocol of an initiator group cannot be changed after creation of the group. 
                uuid: The unique identifier of the initiator group. 
            """

            kwargs = {}
            if delete_on_unmap is not None:
                kwargs["delete_on_unmap"] = delete_on_unmap
            if name is not None:
                kwargs["name"] = name
            if os_type is not None:
                kwargs["os_type"] = os_type
            if protocol is not None:
                kwargs["protocol"] = protocol
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Igroup.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves initiator groups.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `lun_maps.*`
### Related ONTAP commands
* `lun igroup show`
* `lun mapping show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        r"""Updates an initiator group.
### Related ONTAP commands
* `lun igroup modify`
* `lun igroup rename`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        r"""Deletes an initiator group.
### Related ONTAP commands
* `lun igroup delete`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves initiator groups.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `lun_maps.*`
### Related ONTAP commands
* `lun igroup show`
* `lun mapping show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an initiator group.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `lun_maps.*`
### Related ONTAP commands
* `lun igroup show`
* `lun mapping show`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
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
        r"""Creates an initiator group.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the initiator group.
* `name` - Name of the initiator group.
* `os_type` - Operating system of the initiator group's initiators.
### Recommended optional properties
* `initiators.name` - Name(s) of initiator group's initiators. This property can be used to create the initiator group and populate it with initiators in a single request.
### Default property values
If not specified in POST, the following default property values are assigned.
* `protocol` - _mixed_ - Data protocol of the initiator group's initiators.
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="igroup create")
        async def igroup_create(
            links: dict = None,
            delete_on_unmap: bool = None,
            initiators: dict = None,
            lun_maps: dict = None,
            name: str = None,
            os_type: str = None,
            protocol: str = None,
            svm: dict = None,
            uuid: str = None,
        ) -> ResourceTable:
            """Create an instance of a Igroup resource

            Args:
                links: 
                delete_on_unmap: An option that causes the initiator group to be deleted when the last LUN map associated with it is deleted. Optional in POST and PATCH. This property defaults to _false_ when the initiator group is created. 
                initiators: The initiators that are members of the group. Optional in POST.<br/> Zero or more initiators can be supplied when the initiator group is created. After creation, initiators can be added or removed from the initiator group using the `/protocols/san/igroups/{igroup.uuid}/initiators` endpoint. See [`POST /protocols/san/igroups/{igroup.uuid}/initiators`](#/SAN/igroup_initiator_create) and [`DELETE /protocols/san/igroups/{igroup.uuid}/initiators/{name}`](#/SAN/igroup_initiator_delete) for more details. 
                lun_maps: All LUN maps with which the initiator is associated.<br/> If the requested igroup is part of a remote, non-local, MetroCluster SVM, the LUN maps are not retrieved. There is an added cost to retrieving property values for `lun_maps`. They are not populated for either a collection GET or an instance GET unless explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more. 
                name: The name of the initiator group. Required in POST; optional in PATCH.<br/> Note that renaming an initiator group must be done in a PATCH request separate from any other modifications. 
                os_type: The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system. Required in POST; optional in PATCH. 
                protocol: The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group. Optional in POST; if not supplied, this defaults to _mixed_.<br/> The protocol of an initiator group cannot be changed after creation of the group. 
                svm: 
                uuid: The unique identifier of the initiator group. 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if delete_on_unmap is not None:
                kwargs["delete_on_unmap"] = delete_on_unmap
            if initiators is not None:
                kwargs["initiators"] = initiators
            if lun_maps is not None:
                kwargs["lun_maps"] = lun_maps
            if name is not None:
                kwargs["name"] = name
            if os_type is not None:
                kwargs["os_type"] = os_type
            if protocol is not None:
                kwargs["protocol"] = protocol
            if svm is not None:
                kwargs["svm"] = svm
            if uuid is not None:
                kwargs["uuid"] = uuid

            resource = Igroup(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create Igroup: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an initiator group.
### Related ONTAP commands
* `lun igroup modify`
* `lun igroup rename`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="igroup modify")
        async def igroup_modify(
            delete_on_unmap: bool = None,
            query_delete_on_unmap: bool = None,
            name: str = None,
            query_name: str = None,
            os_type: str = None,
            query_os_type: str = None,
            protocol: str = None,
            query_protocol: str = None,
            uuid: str = None,
            query_uuid: str = None,
        ) -> ResourceTable:
            """Modify an instance of a Igroup resource

            Args:
                delete_on_unmap: An option that causes the initiator group to be deleted when the last LUN map associated with it is deleted. Optional in POST and PATCH. This property defaults to _false_ when the initiator group is created. 
                query_delete_on_unmap: An option that causes the initiator group to be deleted when the last LUN map associated with it is deleted. Optional in POST and PATCH. This property defaults to _false_ when the initiator group is created. 
                name: The name of the initiator group. Required in POST; optional in PATCH.<br/> Note that renaming an initiator group must be done in a PATCH request separate from any other modifications. 
                query_name: The name of the initiator group. Required in POST; optional in PATCH.<br/> Note that renaming an initiator group must be done in a PATCH request separate from any other modifications. 
                os_type: The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system. Required in POST; optional in PATCH. 
                query_os_type: The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system. Required in POST; optional in PATCH. 
                protocol: The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group. Optional in POST; if not supplied, this defaults to _mixed_.<br/> The protocol of an initiator group cannot be changed after creation of the group. 
                query_protocol: The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group. Optional in POST; if not supplied, this defaults to _mixed_.<br/> The protocol of an initiator group cannot be changed after creation of the group. 
                uuid: The unique identifier of the initiator group. 
                query_uuid: The unique identifier of the initiator group. 
            """

            kwargs = {}
            changes = {}
            if query_delete_on_unmap is not None:
                kwargs["delete_on_unmap"] = query_delete_on_unmap
            if query_name is not None:
                kwargs["name"] = query_name
            if query_os_type is not None:
                kwargs["os_type"] = query_os_type
            if query_protocol is not None:
                kwargs["protocol"] = query_protocol
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if delete_on_unmap is not None:
                changes["delete_on_unmap"] = delete_on_unmap
            if name is not None:
                changes["name"] = name
            if os_type is not None:
                changes["os_type"] = os_type
            if protocol is not None:
                changes["protocol"] = protocol
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(Igroup, "find"):
                resource = Igroup.find(
                    **kwargs
                )
            else:
                resource = Igroup()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify Igroup: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an initiator group.
### Related ONTAP commands
* `lun igroup delete`
### Learn more
* [`DOC /protocols/san/igroups`](#docs-SAN-protocols_san_igroups)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="igroup delete")
        async def igroup_delete(
            delete_on_unmap: bool = None,
            name: str = None,
            os_type: str = None,
            protocol: str = None,
            uuid: str = None,
        ) -> None:
            """Delete an instance of a Igroup resource

            Args:
                delete_on_unmap: An option that causes the initiator group to be deleted when the last LUN map associated with it is deleted. Optional in POST and PATCH. This property defaults to _false_ when the initiator group is created. 
                name: The name of the initiator group. Required in POST; optional in PATCH.<br/> Note that renaming an initiator group must be done in a PATCH request separate from any other modifications. 
                os_type: The host operating system of the initiator group. All initiators in the group should be hosts of the same operating system. Required in POST; optional in PATCH. 
                protocol: The protocols supported by the initiator group. This restricts the type of initiators that can be added to the initiator group. Optional in POST; if not supplied, this defaults to _mixed_.<br/> The protocol of an initiator group cannot be changed after creation of the group. 
                uuid: The unique identifier of the initiator group. 
            """

            kwargs = {}
            if delete_on_unmap is not None:
                kwargs["delete_on_unmap"] = delete_on_unmap
            if name is not None:
                kwargs["name"] = name
            if os_type is not None:
                kwargs["os_type"] = os_type
            if protocol is not None:
                kwargs["protocol"] = protocol
            if uuid is not None:
                kwargs["uuid"] = uuid

            if hasattr(Igroup, "find"):
                resource = Igroup.find(
                    **kwargs
                )
            else:
                resource = Igroup()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete Igroup: %s" % err)


