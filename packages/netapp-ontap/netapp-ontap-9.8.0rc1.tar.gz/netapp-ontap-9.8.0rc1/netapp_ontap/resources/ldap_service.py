r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
LDAP servers are used to centrally maintain user information. LDAP configurations must be set up
to lookup information stored in the LDAP directory on the external LDAP servers. This API is used to retrieve and manage
LDAP server configurations.
## Retrieving LDAP information
The LDAP GET endpoint retrieves all of the LDAP configurations in the cluster.
## Examples
### Retrieving all of the fields for all LDAP configurations
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LdapService.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    LdapService(
        {
            "servers": ["10.10.10.10", "domainB.example.com"],
            "_links": {
                "self": {
                    "href": "/api/name-services/ldap/179d3c85-7053-11e8-b9b8-005056b41bd1"
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
            "session_security": "none",
            "base_scope": "subtree",
            "schema": "ad_idmu",
            "min_bind_level": "anonymous",
            "bind_dn": "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com",
            "port": 389,
            "use_start_tls": True,
            "base_dn": "dc=domainA,dc=example,dc=com",
        }
    ),
    LdapService(
        {
            "servers": ["11.11.11.11"],
            "_links": {
                "self": {
                    "href": "/api/name-services/ldap/6a52023b-7066-11e8-b9b8-005056b41bd1"
                }
            },
            "svm": {
                "name": "vs2",
                "uuid": "6a52023b-7066-11e8-b9b8-005056b41bd1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/6a52023b-7066-11e8-b9b8-005056b41bd1"
                    }
                },
            },
            "session_security": "sign",
            "base_scope": "subtree",
            "schema": "rfc_2307",
            "min_bind_level": "simple",
            "bind_dn": "cn=Administrators,cn=users,dc=domainB,dc=example,dc=com",
            "port": 389,
            "use_start_tls": True,
            "base_dn": "dc=domainB,dc=example,dc=com",
        }
    ),
]

```
</div>
</div>

---
### Retrieving all of the LDAP configurations that have the *use_start_tls* set to *true*
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(LdapService.get_collection(use_start_tls=True)))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    LdapService(
        {
            "_links": {
                "self": {
                    "href": "/api/name-services/ldap/6a52023b-7066-11e8-b9b8-005056b41bd1"
                }
            },
            "svm": {
                "name": "vs2",
                "uuid": "6a52023b-7066-11e8-b9b8-005056b41bd1",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/6a52023b-7066-11e8-b9b8-005056b41bd1"
                    }
                },
            },
            "use_start_tls": True,
        }
    )
]

```
</div>
</div>

---
### Retrieving the LDAP configuration of a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
LdapService(
    {
        "servers": ["10.10.10.10", "domainB.example.com"],
        "_links": {
            "self": {
                "href": "/api/name-services/ldap/179d3c85-7053-11e8-b9b8-005056b41bd1"
            }
        },
        "svm": {
            "name": "vs1",
            "uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1",
            "_links": {
                "self": {"href": "/api/svm/svms/179d3c85-7053-11e8-b9b8-005056b41bd1"}
            },
        },
        "session_security": "none",
        "base_scope": "subtree",
        "schema": "ad_idmu",
        "min_bind_level": "anonymous",
        "bind_dn": "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com",
        "port": 389,
        "use_start_tls": True,
        "base_dn": "dc=domainA,dc=example,dc=com",
    }
)

```
</div>
</div>

---
## Creating an LDAP configuration
The LDAP POST endpoint creates an LDAP configuration for the specified SVM.
## Examples
### Creating an LDAP configuration with all the fields specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService()
    resource.svm.uuid = "179d3c85-7053-11e8-b9b8-005056b41bd1"
    resource.servers = ["10.10.10.10", "domainB.example.com"]
    resource.schema = "ad_idmu"
    resource.port = 389
    resource.min_bind_level = "anonymous"
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.base_scope = "subtree"
    resource.use_start_tls = False
    resource.session_security = "none"
    resource.post(hydrate=True)
    print(resource)

```

---
### Creating an LDAP configuration with Active Directory domain and preferred Active Directory servers specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService()
    resource.svm.name = "vs2"
    resource.ad_domain = "domainA.example.com"
    resource.preferred_ad_servers = ["11.11.11.11"]
    resource.port = 389
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.session_security = "none"
    resource.post(hydrate=True)
    print(resource)

```

---
### Creating an LDAP configuration with a number of optional fields not specified
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService()
    resource.svm.name = "vs2"
    resource.servers = ["11.11.11.11"]
    resource.port = 389
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.session_security = "none"
    resource.post(hydrate=True)
    print(resource)

```

---
## Updating an LDAP configuration
The LDAP PATCH endpoint updates the LDAP configuration for the specified SVM. The following example shows a PATCH operation:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.servers = ["55.55.55.55"]
    resource.schema = "ad_idmu"
    resource.port = 636
    resource.use_start_tls = False
    resource.patch()

```

---
## Deleting an LDAP configuration
The LDAP DELETE endpoint deletes the LDAP configuration for the specified SVM. The following example shows a DELETE operation:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import LdapService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = LdapService(**{"svm.uuid": "179d3c85-7053-11e8-b9b8-005056b41bd1"})
    resource.delete()

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


__all__ = ["LdapService", "LdapServiceSchema"]
__pdoc__ = {
    "LdapServiceSchema.resource": False,
    "LdapService.ldap_service_show": False,
    "LdapService.ldap_service_create": False,
    "LdapService.ldap_service_modify": False,
    "LdapService.ldap_service_delete": False,
}


class LdapServiceSchema(ResourceSchema):
    """The fields of the LdapService object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the ldap_service. """

    ad_domain = fields.Str(
        data_key="ad_domain",
    )
    r""" This parameter specifies the name of the Active Directory domain
used to discover LDAP servers for use by this client.
This is mutually exclusive with `servers` during POST and PATCH. """

    base_dn = fields.Str(
        data_key="base_dn",
    )
    r""" Specifies the default base DN for all searches. """

    base_scope = fields.Str(
        data_key="base_scope",
        validate=enum_validation(['base', 'onelevel', 'subtree']),
    )
    r""" Specifies the default search scope for LDAP queries:

* base - search the named entry only
* onelevel - search all entries immediately below the DN
* subtree - search the named DN entry and the entire subtree below the DN


Valid choices:

* base
* onelevel
* subtree """

    bind_dn = fields.Str(
        data_key="bind_dn",
    )
    r""" Specifies the user that binds to the LDAP servers. """

    bind_password = fields.Str(
        data_key="bind_password",
    )
    r""" Specifies the bind password for the LDAP servers. """

    min_bind_level = fields.Str(
        data_key="min_bind_level",
        validate=enum_validation(['anonymous', 'simple', 'sasl']),
    )
    r""" The minimum bind authentication level. Possible values are:

* anonymous - anonymous bind
* simple - simple bind
* sasl - Simple Authentication and Security Layer (SASL) bind


Valid choices:

* anonymous
* simple
* sasl """

    port = Size(
        data_key="port",
        validate=integer_validation(minimum=1, maximum=65535),
    )
    r""" The port used to connect to the LDAP Servers.

Example: 389 """

    preferred_ad_servers = fields.List(fields.Str, data_key="preferred_ad_servers")
    r""" The preferred_ad_servers field of the ldap_service. """

    schema = fields.Str(
        data_key="schema",
    )
    r""" The name of the schema template used by the SVM.

* AD-IDMU - Active Directory Identity Management for UNIX
* AD-SFU - Active Directory Services for UNIX
* MS-AD-BIS - Active Directory Identity Management for UNIX
* RFC-2307 - Schema based on RFC 2307
* Custom schema """

    servers = fields.List(fields.Str, data_key="servers")
    r""" The servers field of the ldap_service. """

    session_security = fields.Str(
        data_key="session_security",
        validate=enum_validation(['none', 'sign', 'seal']),
    )
    r""" Specifies the level of security to be used for LDAP communications:

* none - no signing or sealing
* sign - sign LDAP traffic
* seal - seal and sign LDAP traffic


Valid choices:

* none
* sign
* seal """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the ldap_service. """

    use_start_tls = fields.Boolean(
        data_key="use_start_tls",
    )
    r""" Specifies whether or not to use Start TLS over LDAP connections. """

    @property
    def resource(self):
        return LdapService

    gettable_fields = [
        "links",
        "ad_domain",
        "base_dn",
        "base_scope",
        "bind_dn",
        "min_bind_level",
        "port",
        "preferred_ad_servers",
        "schema",
        "servers",
        "session_security",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "use_start_tls",
    ]
    """links,ad_domain,base_dn,base_scope,bind_dn,min_bind_level,port,preferred_ad_servers,schema,servers,session_security,svm.links,svm.name,svm.uuid,use_start_tls,"""

    patchable_fields = [
        "ad_domain",
        "base_dn",
        "base_scope",
        "bind_dn",
        "bind_password",
        "min_bind_level",
        "port",
        "preferred_ad_servers",
        "schema",
        "servers",
        "session_security",
        "svm.name",
        "svm.uuid",
        "use_start_tls",
    ]
    """ad_domain,base_dn,base_scope,bind_dn,bind_password,min_bind_level,port,preferred_ad_servers,schema,servers,session_security,svm.name,svm.uuid,use_start_tls,"""

    postable_fields = [
        "ad_domain",
        "base_dn",
        "base_scope",
        "bind_dn",
        "bind_password",
        "min_bind_level",
        "port",
        "preferred_ad_servers",
        "schema",
        "servers",
        "session_security",
        "svm.name",
        "svm.uuid",
        "use_start_tls",
    ]
    """ad_domain,base_dn,base_scope,bind_dn,bind_password,min_bind_level,port,preferred_ad_servers,schema,servers,session_security,svm.name,svm.uuid,use_start_tls,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in LdapService.get_collection(fields=field)]
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
            raise NetAppRestError("LdapService modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class LdapService(Resource):
    """Allows interaction with LdapService objects on the host"""

    _schema = LdapServiceSchema
    _path = "/api/name-services/ldap"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the LDAP configurations for all SVMs.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ldap service show")
        def ldap_service_show(
            ad_domain: Choices.define(_get_field_list("ad_domain"), cache_choices=True, inexact=True)=None,
            base_dn: Choices.define(_get_field_list("base_dn"), cache_choices=True, inexact=True)=None,
            base_scope: Choices.define(_get_field_list("base_scope"), cache_choices=True, inexact=True)=None,
            bind_dn: Choices.define(_get_field_list("bind_dn"), cache_choices=True, inexact=True)=None,
            bind_password: Choices.define(_get_field_list("bind_password"), cache_choices=True, inexact=True)=None,
            min_bind_level: Choices.define(_get_field_list("min_bind_level"), cache_choices=True, inexact=True)=None,
            port: Choices.define(_get_field_list("port"), cache_choices=True, inexact=True)=None,
            preferred_ad_servers: Choices.define(_get_field_list("preferred_ad_servers"), cache_choices=True, inexact=True)=None,
            schema: Choices.define(_get_field_list("schema"), cache_choices=True, inexact=True)=None,
            servers: Choices.define(_get_field_list("servers"), cache_choices=True, inexact=True)=None,
            session_security: Choices.define(_get_field_list("session_security"), cache_choices=True, inexact=True)=None,
            use_start_tls: Choices.define(_get_field_list("use_start_tls"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["ad_domain", "base_dn", "base_scope", "bind_dn", "bind_password", "min_bind_level", "port", "preferred_ad_servers", "schema", "servers", "session_security", "use_start_tls", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of LdapService resources

            Args:
                ad_domain: This parameter specifies the name of the Active Directory domain used to discover LDAP servers for use by this client. This is mutually exclusive with `servers` during POST and PATCH. 
                base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                port: The port used to connect to the LDAP Servers.
                preferred_ad_servers: 
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
            """

            kwargs = {}
            if ad_domain is not None:
                kwargs["ad_domain"] = ad_domain
            if base_dn is not None:
                kwargs["base_dn"] = base_dn
            if base_scope is not None:
                kwargs["base_scope"] = base_scope
            if bind_dn is not None:
                kwargs["bind_dn"] = bind_dn
            if bind_password is not None:
                kwargs["bind_password"] = bind_password
            if min_bind_level is not None:
                kwargs["min_bind_level"] = min_bind_level
            if port is not None:
                kwargs["port"] = port
            if preferred_ad_servers is not None:
                kwargs["preferred_ad_servers"] = preferred_ad_servers
            if schema is not None:
                kwargs["schema"] = schema
            if servers is not None:
                kwargs["servers"] = servers
            if session_security is not None:
                kwargs["session_security"] = session_security
            if use_start_tls is not None:
                kwargs["use_start_tls"] = use_start_tls
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return LdapService.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves the LDAP configurations for all SVMs.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
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
        r"""Updates an LDAP configuration of an SVM.
### Important notes
* Both mandatory and optional parameters of the LDAP configuration can be updated.
* The LDAP servers and Active Directory domain are mutually exclusive fields. These fields cannot be empty. At any point in time, either the LDAP servers or Active Directory domain must be populated.
* IPv6 must be enabled if IPv6 family addresses are specified.<br/>
</br>Configuring more than one LDAP server is recommended to avoid a sinlge point of failure.
Both FQDNs and IP addresses are supported for the "servers" field.
The Active Directory domain or LDAP servers are validated as part of this operation.<br/>
LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server or Active Directory domain is invalid.
3. The server or Active Directory domain is unreachable<br/>

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
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
        r"""Deletes the LDAP configuration of the specified SVM. LDAP can be removed as a source from the ns-switch if LDAP is not used as a source for lookups.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the LDAP configurations for all SVMs.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves LDAP configuration for an SVM. All parameters for the LDAP configuration are displayed by default.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
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
        r"""Creates an LDAP configuration for an SVM.
### Important notes
* Each SVM can have one LDAP configuration.
* The LDAP servers and Active Directory domain are mutually exclusive fields. These fields cannot be empty. At any point in time, either the LDAP servers or Active Directory domain must be populated.
* LDAP configuration with Active Directory domain cannot be created on an admin SVM.
* IPv6 must be enabled if IPv6 family addresses are specified.</br>
#### The following parameters are optional:
- preferred AD servers
- schema
- port
- min_bind_level
- bind_password
- base_scope
- use_start_tls
- session_security</br>
Configuring more than one LDAP server is recommended to avoid a single point of failure.
Both FQDNs and IP addresses are supported for the "servers" field.
The Acitve Directory domain or LDAP servers are validated as part of this operation.</br>
LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server or Active Directory domain is invalid.
3. The server or Active Directory domain is unreachable.<br/>

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ldap service create")
        async def ldap_service_create(
            links: dict = None,
            ad_domain: str = None,
            base_dn: str = None,
            base_scope: str = None,
            bind_dn: str = None,
            bind_password: str = None,
            min_bind_level: str = None,
            port: Size = None,
            preferred_ad_servers = None,
            schema: str = None,
            servers = None,
            session_security: str = None,
            svm: dict = None,
            use_start_tls: bool = None,
        ) -> ResourceTable:
            """Create an instance of a LdapService resource

            Args:
                links: 
                ad_domain: This parameter specifies the name of the Active Directory domain used to discover LDAP servers for use by this client. This is mutually exclusive with `servers` during POST and PATCH. 
                base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                port: The port used to connect to the LDAP Servers.
                preferred_ad_servers: 
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                svm: 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if ad_domain is not None:
                kwargs["ad_domain"] = ad_domain
            if base_dn is not None:
                kwargs["base_dn"] = base_dn
            if base_scope is not None:
                kwargs["base_scope"] = base_scope
            if bind_dn is not None:
                kwargs["bind_dn"] = bind_dn
            if bind_password is not None:
                kwargs["bind_password"] = bind_password
            if min_bind_level is not None:
                kwargs["min_bind_level"] = min_bind_level
            if port is not None:
                kwargs["port"] = port
            if preferred_ad_servers is not None:
                kwargs["preferred_ad_servers"] = preferred_ad_servers
            if schema is not None:
                kwargs["schema"] = schema
            if servers is not None:
                kwargs["servers"] = servers
            if session_security is not None:
                kwargs["session_security"] = session_security
            if svm is not None:
                kwargs["svm"] = svm
            if use_start_tls is not None:
                kwargs["use_start_tls"] = use_start_tls

            resource = LdapService(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create LdapService: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an LDAP configuration of an SVM.
### Important notes
* Both mandatory and optional parameters of the LDAP configuration can be updated.
* The LDAP servers and Active Directory domain are mutually exclusive fields. These fields cannot be empty. At any point in time, either the LDAP servers or Active Directory domain must be populated.
* IPv6 must be enabled if IPv6 family addresses are specified.<br/>
</br>Configuring more than one LDAP server is recommended to avoid a sinlge point of failure.
Both FQDNs and IP addresses are supported for the "servers" field.
The Active Directory domain or LDAP servers are validated as part of this operation.<br/>
LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server or Active Directory domain is invalid.
3. The server or Active Directory domain is unreachable<br/>

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ldap service modify")
        async def ldap_service_modify(
            ad_domain: str = None,
            query_ad_domain: str = None,
            base_dn: str = None,
            query_base_dn: str = None,
            base_scope: str = None,
            query_base_scope: str = None,
            bind_dn: str = None,
            query_bind_dn: str = None,
            bind_password: str = None,
            query_bind_password: str = None,
            min_bind_level: str = None,
            query_min_bind_level: str = None,
            port: Size = None,
            query_port: Size = None,
            preferred_ad_servers=None,
            query_preferred_ad_servers=None,
            schema: str = None,
            query_schema: str = None,
            servers=None,
            query_servers=None,
            session_security: str = None,
            query_session_security: str = None,
            use_start_tls: bool = None,
            query_use_start_tls: bool = None,
        ) -> ResourceTable:
            """Modify an instance of a LdapService resource

            Args:
                ad_domain: This parameter specifies the name of the Active Directory domain used to discover LDAP servers for use by this client. This is mutually exclusive with `servers` during POST and PATCH. 
                query_ad_domain: This parameter specifies the name of the Active Directory domain used to discover LDAP servers for use by this client. This is mutually exclusive with `servers` during POST and PATCH. 
                base_dn: Specifies the default base DN for all searches.
                query_base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                query_base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_dn: Specifies the user that binds to the LDAP servers.
                query_bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                query_bind_password: Specifies the bind password for the LDAP servers.
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                query_min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                port: The port used to connect to the LDAP Servers.
                query_port: The port used to connect to the LDAP Servers.
                preferred_ad_servers: 
                query_preferred_ad_servers: 
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                query_schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                query_servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                query_session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
                query_use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
            """

            kwargs = {}
            changes = {}
            if query_ad_domain is not None:
                kwargs["ad_domain"] = query_ad_domain
            if query_base_dn is not None:
                kwargs["base_dn"] = query_base_dn
            if query_base_scope is not None:
                kwargs["base_scope"] = query_base_scope
            if query_bind_dn is not None:
                kwargs["bind_dn"] = query_bind_dn
            if query_bind_password is not None:
                kwargs["bind_password"] = query_bind_password
            if query_min_bind_level is not None:
                kwargs["min_bind_level"] = query_min_bind_level
            if query_port is not None:
                kwargs["port"] = query_port
            if query_preferred_ad_servers is not None:
                kwargs["preferred_ad_servers"] = query_preferred_ad_servers
            if query_schema is not None:
                kwargs["schema"] = query_schema
            if query_servers is not None:
                kwargs["servers"] = query_servers
            if query_session_security is not None:
                kwargs["session_security"] = query_session_security
            if query_use_start_tls is not None:
                kwargs["use_start_tls"] = query_use_start_tls

            if ad_domain is not None:
                changes["ad_domain"] = ad_domain
            if base_dn is not None:
                changes["base_dn"] = base_dn
            if base_scope is not None:
                changes["base_scope"] = base_scope
            if bind_dn is not None:
                changes["bind_dn"] = bind_dn
            if bind_password is not None:
                changes["bind_password"] = bind_password
            if min_bind_level is not None:
                changes["min_bind_level"] = min_bind_level
            if port is not None:
                changes["port"] = port
            if preferred_ad_servers is not None:
                changes["preferred_ad_servers"] = preferred_ad_servers
            if schema is not None:
                changes["schema"] = schema
            if servers is not None:
                changes["servers"] = servers
            if session_security is not None:
                changes["session_security"] = session_security
            if use_start_tls is not None:
                changes["use_start_tls"] = use_start_tls

            if hasattr(LdapService, "find"):
                resource = LdapService.find(
                    **kwargs
                )
            else:
                resource = LdapService()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify LdapService: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the LDAP configuration of the specified SVM. LDAP can be removed as a source from the ns-switch if LDAP is not used as a source for lookups.

### Learn more
* [`DOC /name-services/ldap`](#docs-name-services-name-services_ldap)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ldap service delete")
        async def ldap_service_delete(
            ad_domain: str = None,
            base_dn: str = None,
            base_scope: str = None,
            bind_dn: str = None,
            bind_password: str = None,
            min_bind_level: str = None,
            port: Size = None,
            preferred_ad_servers=None,
            schema: str = None,
            servers=None,
            session_security: str = None,
            use_start_tls: bool = None,
        ) -> None:
            """Delete an instance of a LdapService resource

            Args:
                ad_domain: This parameter specifies the name of the Active Directory domain used to discover LDAP servers for use by this client. This is mutually exclusive with `servers` during POST and PATCH. 
                base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                port: The port used to connect to the LDAP Servers.
                preferred_ad_servers: 
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
            """

            kwargs = {}
            if ad_domain is not None:
                kwargs["ad_domain"] = ad_domain
            if base_dn is not None:
                kwargs["base_dn"] = base_dn
            if base_scope is not None:
                kwargs["base_scope"] = base_scope
            if bind_dn is not None:
                kwargs["bind_dn"] = bind_dn
            if bind_password is not None:
                kwargs["bind_password"] = bind_password
            if min_bind_level is not None:
                kwargs["min_bind_level"] = min_bind_level
            if port is not None:
                kwargs["port"] = port
            if preferred_ad_servers is not None:
                kwargs["preferred_ad_servers"] = preferred_ad_servers
            if schema is not None:
                kwargs["schema"] = schema
            if servers is not None:
                kwargs["servers"] = servers
            if session_security is not None:
                kwargs["session_security"] = session_security
            if use_start_tls is not None:
                kwargs["use_start_tls"] = use_start_tls

            if hasattr(LdapService, "find"):
                resource = LdapService.find(
                    **kwargs
                )
            else:
                resource = LdapService()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete LdapService: %s" % err)


