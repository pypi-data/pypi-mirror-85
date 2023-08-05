r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
This API is used to display connection status information for the external virus-scanning servers or \"Vscan servers\".
## Examples
### Retrieving all fields for the Vscan server status
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Vscan

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Vscan(**{"svm.uuid": "server_status"})
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Vscan(
        {
            "_links": {
                "self": {
                    "href": "/api/protocols/vscan/server_status/86fbc414-f140-11e8-8e22-0050568e0945/Cluster-01/10.141.46.173"
                }
            },
            "svm": {
                "name": "vs1",
                "uuid": "86fbc414-f140-11e8-8e22-0050568e0945",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/86fbc414-f140-11e8-8e22-0050568e0945"
                    }
                },
            },
        }
    ),
    Vscan(
        {
            "_links": {
                "self": {
                    "href": "/api/protocols/vscan/server_status/86fbc414-f140-11e8-8e22-0050568e0945/Cluster-01/fd20%3A8b1e%3Ab255%3A5053%3A%3A46%3A173"
                }
            },
            "svm": {
                "name": "vs1",
                "uuid": "86fbc414-f140-11e8-8e22-0050568e0945",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/86fbc414-f140-11e8-8e22-0050568e0945"
                    }
                },
            },
        }
    ),
]

```
</div>
</div>

---
### Retrieving the server status information for the server with IP address 10.141.46.173
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Vscan

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Vscan(**{"svm.uuid": "server_status"})
    resource.get(ip="10.141.46.173", fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    Vscan(
        {
            "_links": {
                "self": {
                    "href": "/api/protocols/vscan/server_status/86fbc414-f140-11e8-8e22-0050568e0945/Cluster-01/10.141.46.173"
                }
            },
            "svm": {
                "name": "vs1",
                "uuid": "86fbc414-f140-11e8-8e22-0050568e0945",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/86fbc414-f140-11e8-8e22-0050568e0945"
                    }
                },
            },
        }
    )
]

```
</div>
</div>

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


__all__ = ["VscanServerStatus", "VscanServerStatusSchema"]
__pdoc__ = {
    "VscanServerStatusSchema.resource": False,
    "VscanServerStatus.vscan_server_status_show": False,
    "VscanServerStatus.vscan_server_status_create": False,
    "VscanServerStatus.vscan_server_status_modify": False,
    "VscanServerStatus.vscan_server_status_delete": False,
}


class VscanServerStatusSchema(ResourceSchema):
    """The fields of the VscanServerStatus object"""

    disconnected_reason = fields.Str(
        data_key="disconnected_reason",
    )
    r""" Specifies the server disconnected reason.
The following is a list of the possible reasons:

* unknown                   - Disconnected, unknown reason.
* vscan_disabled            - Disconnected, Vscan is disabled on the SVM.
* no_data_lif               - Disconnected, SVM does not have data LIF.
* session_uninitialized     - Disconnected, session is not initialized.
* remote_closed             - Disconnected, server has closed the connection.
* invalid_protocol_msg      - Disconnected, invalid protocol message received.
* invalid_session_id        - Disconnected, invalid session ID received.
* inactive_connection       - Disconnected, no activity on connection.
* invalid_user              - Connection request by an invalid user.
* server_removed            - Disconnected, server has been removed from the active Scanners List.
enum:
  - unknown
  - vscan_disabled
  - no_data_lif
  - session_uninitialized
  - remote_closed
  - invalid_protocol_msg
  - invalid_session_id
  - inactive_connection
  - invalid_user
  - server_removed """

    ip = fields.Str(
        data_key="ip",
    )
    r""" IP address of the Vscan server. """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE)
    r""" The node field of the vscan_server_status. """

    state = fields.Str(
        data_key="state",
    )
    r""" Specifies the server connection state indicating if it is in the connected or disconnected state.
The following is a list of the possible states:

* connected                 - Connected
* disconnected              - Disconnected
enum:
  - connected
  - disconnected """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the vscan_server_status. """

    type = fields.Str(
        data_key="type",
        validate=enum_validation(['primary', 'backup']),
    )
    r""" Server type. The possible values are:

  * primary - Primary server
  * backup  - Backup server


Valid choices:

* primary
* backup """

    update_time = ImpreciseDateTime(
        data_key="update_time",
    )
    r""" Specifies the time the server is in the connected or disconnected state. """

    vendor = fields.Str(
        data_key="vendor",
    )
    r""" Name of the connected virus-scanner vendor. """

    version = fields.Str(
        data_key="version",
    )
    r""" Version of the connected virus-scanner. """

    @property
    def resource(self):
        return VscanServerStatus

    gettable_fields = [
        "disconnected_reason",
        "ip",
        "node.links",
        "node.name",
        "node.uuid",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "type",
        "update_time",
        "vendor",
        "version",
    ]
    """disconnected_reason,ip,node.links,node.name,node.uuid,state,svm.links,svm.name,svm.uuid,type,update_time,vendor,version,"""

    patchable_fields = [
        "disconnected_reason",
        "ip",
        "node.name",
        "node.uuid",
        "state",
        "svm.name",
        "svm.uuid",
        "type",
        "update_time",
        "vendor",
        "version",
    ]
    """disconnected_reason,ip,node.name,node.uuid,state,svm.name,svm.uuid,type,update_time,vendor,version,"""

    postable_fields = [
        "disconnected_reason",
        "ip",
        "node.name",
        "node.uuid",
        "state",
        "svm.name",
        "svm.uuid",
        "type",
        "update_time",
        "vendor",
        "version",
    ]
    """disconnected_reason,ip,node.name,node.uuid,state,svm.name,svm.uuid,type,update_time,vendor,version,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in VscanServerStatus.get_collection(fields=field)]
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
            raise NetAppRestError("VscanServerStatus modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class VscanServerStatus(Resource):
    r""" Displays the connection status information of the external virus-scanning servers. """

    _schema = VscanServerStatusSchema
    _path = "/api/protocols/vscan/server-status"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a Vscan server status.
### Related ONTAP commands
* `vserver vscan connection-status show-all`
### Learn more
* [`DOC /protocols/vscan/server-status`](#docs-NAS-protocols_vscan_server-status)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="vscan server status show")
        def vscan_server_status_show(
            disconnected_reason: Choices.define(_get_field_list("disconnected_reason"), cache_choices=True, inexact=True)=None,
            ip: Choices.define(_get_field_list("ip"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            type: Choices.define(_get_field_list("type"), cache_choices=True, inexact=True)=None,
            update_time: Choices.define(_get_field_list("update_time"), cache_choices=True, inexact=True)=None,
            vendor: Choices.define(_get_field_list("vendor"), cache_choices=True, inexact=True)=None,
            version: Choices.define(_get_field_list("version"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["disconnected_reason", "ip", "state", "type", "update_time", "vendor", "version", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of VscanServerStatus resources

            Args:
                disconnected_reason: Specifies the server disconnected reason. The following is a list of the possible reasons: * unknown                   - Disconnected, unknown reason. * vscan_disabled            - Disconnected, Vscan is disabled on the SVM. * no_data_lif               - Disconnected, SVM does not have data LIF. * session_uninitialized     - Disconnected, session is not initialized. * remote_closed             - Disconnected, server has closed the connection. * invalid_protocol_msg      - Disconnected, invalid protocol message received. * invalid_session_id        - Disconnected, invalid session ID received. * inactive_connection       - Disconnected, no activity on connection. * invalid_user              - Connection request by an invalid user. * server_removed            - Disconnected, server has been removed from the active Scanners List. enum:   - unknown   - vscan_disabled   - no_data_lif   - session_uninitialized   - remote_closed   - invalid_protocol_msg   - invalid_session_id   - inactive_connection   - invalid_user   - server_removed 
                ip: IP address of the Vscan server.
                state: Specifies the server connection state indicating if it is in the connected or disconnected state. The following is a list of the possible states: * connected                 - Connected * disconnected              - Disconnected enum:   - connected   - disconnected 
                type: Server type. The possible values are:   * primary - Primary server   * backup  - Backup server 
                update_time: Specifies the time the server is in the connected or disconnected state.
                vendor: Name of the connected virus-scanner vendor.
                version: Version of the connected virus-scanner.
            """

            kwargs = {}
            if disconnected_reason is not None:
                kwargs["disconnected_reason"] = disconnected_reason
            if ip is not None:
                kwargs["ip"] = ip
            if state is not None:
                kwargs["state"] = state
            if type is not None:
                kwargs["type"] = type
            if update_time is not None:
                kwargs["update_time"] = update_time
            if vendor is not None:
                kwargs["vendor"] = vendor
            if version is not None:
                kwargs["version"] = version
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return VscanServerStatus.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves a Vscan server status.
### Related ONTAP commands
* `vserver vscan connection-status show-all`
### Learn more
* [`DOC /protocols/vscan/server-status`](#docs-NAS-protocols_vscan_server-status)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a Vscan server status.
### Related ONTAP commands
* `vserver vscan connection-status show-all`
### Learn more
* [`DOC /protocols/vscan/server-status`](#docs-NAS-protocols_vscan_server-status)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






