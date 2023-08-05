r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
Displays DNS information and controls the DNS subsytem. DNS domain name and DNS servers are required parameters.
## Retrieving DNS information
The DNS GET endpoint retrieves all of the DNS configurations for data SVMs.
DNS configuration for the cluster is retrieved via [`/api/cluster`](#docs-cluster-cluster).
## Examples
### Retrieving all of the fields for all of the DNS configurations
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Dns.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Dns(
        {
            "servers": ["10.10.10.10"],
            "domains": ["domainA.example.com"],
            "_links": {
                "self": {
                    "href": "/api/name-services/dns/179d3c85-7053-11e8-b9b8-005056b41bd1"
                }
            },
            "svm": {
                "name": "vs1",
                "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"
                    }
                },
            },
        }
    ),
    Dns(
        {
            "servers": ["11.11.11.11", "22.22.22.22", "33.33.33.33"],
            "domains": ["sample.example.com"],
            "_links": {
                "self": {
                    "href": "/api/name-services/dns/19076d35-6e27-11e8-b9b8-005056b41bd1"
                }
            },
            "svm": {
                "name": "vs2",
                "uuid": "19076d35-6e27-11e8-b9b8-005056b41bd1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/19076d35-6e27-11e8-b9b8-005056b41bd1"
                    }
                },
            },
        }
    ),
]

```
</div>
</div>

### Retrieving all DNS configurations whose domain name starts with _dom*_.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Dns.get_collection(domains="dom*")))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    Dns(
        {
            "domains": ["domainA.example.com"],
            "_links": {
                "self": {
                    "href": "/api/name-services/dns/179d3c85-7053-11e8-b9b8-005056b41bd1"
                }
            },
            "svm": {
                "name": "vs1",
                "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"
                    }
                },
            },
        }
    )
]

```
</div>
</div>

### Retrieving the DNS configuration for a specific SVM
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Dns(
    {
        "servers": ["10.10.10.10"],
        "domains": ["domainA.example.com"],
        "_links": {
            "self": {
                "href": "/api/name-services/dns/179d3c85-7053-11e8-b9b8-005056b41bd1"
            }
        },
        "svm": {
            "name": "vs1",
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
            "_links": {
                "self": {"href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"}
            },
        },
    }
)

```
</div>
</div>

## Creating a DNS configuration
The DNS POST endpoint creates a DNS configuration for the specified SVM.
## Example
The following example shows a POST operation:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns()
    resource.svm.uuid = "179d3c85-7053-11e8-b9b8-005056b41bd1"
    resource.domains = ["domainA.example.com"]
    resource.servers = ["10.10.10.10"]
    resource.post(hydrate=True)
    print(resource)

```

## Updating a DNS configuration
The DNS PATCH endpoint updates the DNS configuration for the specified SVM.
## Examples
### Updating both the DNS domains and servers
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.domains = ["domainA.example.com", "domainB.example.com"]
    resource.servers = ["10.10.10.10", "10.10.10.11"]
    resource.patch()

```

### Updating the DNS servers only
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.servers = ["10.10.10.10"]
    resource.patch()

```

## Deleting a DNS configuration
The DNS DELETE endpoint deletes the DNS configuration for the specified SVM.
## Example
The following example shows a DELETE operation.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Dns

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Dns(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.delete()

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


__all__ = ["Dns", "DnsSchema"]
__pdoc__ = {
    "DnsSchema.resource": False,
    "Dns.dns_show": False,
    "Dns.dns_create": False,
    "Dns.dns_modify": False,
    "Dns.dns_delete": False,
}


class DnsSchema(ResourceSchema):
    """The fields of the Dns object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the dns. """

    domains = fields.List(fields.Str, data_key="domains")
    r""" The domains field of the dns. """

    servers = fields.List(fields.Str, data_key="servers")
    r""" The servers field of the dns. """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the dns. """

    @property
    def resource(self):
        return Dns

    gettable_fields = [
        "links",
        "domains",
        "servers",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,domains,servers,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "domains",
        "servers",
        "svm.name",
        "svm.uuid",
    ]
    """domains,servers,svm.name,svm.uuid,"""

    postable_fields = [
        "domains",
        "servers",
        "svm.name",
        "svm.uuid",
    ]
    """domains,servers,svm.name,svm.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Dns.get_collection(fields=field)]
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
            raise NetAppRestError("Dns modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Dns(Resource):
    """Allows interaction with Dns objects on the host"""

    _schema = DnsSchema
    _path = "/api/name-services/dns"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the DNS configurations of all data SVMs.
DNS configuration for the cluster is retrieved and managed via [`/api/cluster`](#docs-cluster-cluster).
### Related ONTAP commands
* `vserver services name-service dns show`
* `vserver services name-service dns check`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="dns show")
        def dns_show(
            domains: Choices.define(_get_field_list("domains"), cache_choices=True, inexact=True)=None,
            servers: Choices.define(_get_field_list("servers"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["domains", "servers", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Dns resources

            Args:
                domains: 
                servers: 
            """

            kwargs = {}
            if domains is not None:
                kwargs["domains"] = domains
            if servers is not None:
                kwargs["servers"] = servers
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Dns.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves the DNS configurations of all data SVMs.
DNS configuration for the cluster is retrieved and managed via [`/api/cluster`](#docs-cluster-cluster).
### Related ONTAP commands
* `vserver services name-service dns show`
* `vserver services name-service dns check`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
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
        r"""Updates DNS domain and server configurations of an SVM.
### Important notes
- Both DNS domains and servers can be modified.
- The domains and servers fields cannot be empty.
- IPv6 must be enabled if IPv6 family addresses are specified for the `servers` field.
- The DNS server specified using the `servers` field is validated during this operation.<br/>
The validation fails in the following scenarios:<br/>
1. The server is not a DNS server.
2. The server does not exist.
3. The server is unreachable.<br/>

### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)"""
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
        r"""Deletes DNS domain configuration of the specified SVM.
### Related ONTAP commands
* `vserver services name-service dns delete`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the DNS configurations of all data SVMs.
DNS configuration for the cluster is retrieved and managed via [`/api/cluster`](#docs-cluster-cluster).
### Related ONTAP commands
* `vserver services name-service dns show`
* `vserver services name-service dns check`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves DNS domain and server configuration of an SVM. By default, both DNS domains and servers are displayed.
DNS configuration for the cluster is retrieved and managed via [`/api/cluster`](#docs-cluster-cluster).
### Related ONTAP commands
* `vserver services name-service dns show`
* `vserver services name-service dns check`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
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
        r"""Creates DNS domain and server configurations for an SVM.<br/>
### Important notes
- Each SVM can have only one DNS configuration.
- The domain name and the servers fields cannot be empty.
- IPv6 must be enabled if IPv6 family addresses are specified in the `servers` field.
- Configuring more than one DNS server is recommended to avoid a single point of failure.
- The DNS server specified using the `servers` field is validated during this operation.<br/>
</br> The validation fails in the following scenarios:<br/>
1. The server is not a DNS server.
2. The server does not exist.
3. The server is unreachable.<br/>

### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="dns create")
        async def dns_create(
            links: dict = None,
            domains: str = None,
            servers: str = None,
            svm: dict = None,
        ) -> ResourceTable:
            """Create an instance of a Dns resource

            Args:
                links: 
                domains: 
                servers: 
                svm: 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if domains is not None:
                kwargs["domains"] = domains
            if servers is not None:
                kwargs["servers"] = servers
            if svm is not None:
                kwargs["svm"] = svm

            resource = Dns(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create Dns: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates DNS domain and server configurations of an SVM.
### Important notes
- Both DNS domains and servers can be modified.
- The domains and servers fields cannot be empty.
- IPv6 must be enabled if IPv6 family addresses are specified for the `servers` field.
- The DNS server specified using the `servers` field is validated during this operation.<br/>
The validation fails in the following scenarios:<br/>
1. The server is not a DNS server.
2. The server does not exist.
3. The server is unreachable.<br/>

### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="dns modify")
        async def dns_modify(
            domains: str = None,
            query_domains: str = None,
            servers: str = None,
            query_servers: str = None,
        ) -> ResourceTable:
            """Modify an instance of a Dns resource

            Args:
                domains: 
                query_domains: 
                servers: 
                query_servers: 
            """

            kwargs = {}
            changes = {}
            if query_domains is not None:
                kwargs["domains"] = query_domains
            if query_servers is not None:
                kwargs["servers"] = query_servers

            if domains is not None:
                changes["domains"] = domains
            if servers is not None:
                changes["servers"] = servers

            if hasattr(Dns, "find"):
                resource = Dns.find(
                    **kwargs
                )
            else:
                resource = Dns()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify Dns: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes DNS domain configuration of the specified SVM.
### Related ONTAP commands
* `vserver services name-service dns delete`
### Learn more
* [`DOC /name-services/dns`](#docs-name-services-name-services_dns)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="dns delete")
        async def dns_delete(
            domains: str = None,
            servers: str = None,
        ) -> None:
            """Delete an instance of a Dns resource

            Args:
                domains: 
                servers: 
            """

            kwargs = {}
            if domains is not None:
                kwargs["domains"] = domains
            if servers is not None:
                kwargs["servers"] = servers

            if hasattr(Dns, "find"):
                resource = Dns.find(
                    **kwargs
                )
            else:
                resource = Dns()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete Dns: %s" % err)


