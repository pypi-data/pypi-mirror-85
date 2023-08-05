r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
LDAP servers are used to centrally maintain user information. LDAP configurations must be set up
to look up information stored in the LDAP directory on the external LDAP servers. This API is used to retrieve and manage
cluster LDAP server configurations.<br>
## Examples
### Retrieving the cluster LDAP information
The cluster LDAP GET request retrieves the LDAP configuration of the cluster.<br>
The following example shows how a GET request is used to retrieve the cluster LDAP information:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
ClusterLdap(
    {
        "servers": ["10.10.10.10", "domainB.example.com"],
        "_links": {"self": {"href": "/api/security/authentication/cluster/ldap"}},
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

### Creating the cluster LDAP configuration
The cluster LDAP POST operation creates an LDAP configuration for the cluster.<br>
The following example shows how to issue a POST request with all of the fields specified:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
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

The following example shows how to issue a POST request with a number of optional fields not specified:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
    resource.port = 389
    resource.bind_dn = "cn=Administrators,cn=users,dc=domainA,dc=example,dc=com"
    resource.bind_password = "abc"
    resource.base_dn = "dc=domainA,dc=example,dc=com"
    resource.session_security = "none"
    resource.post(hydrate=True)
    print(resource)

```

### Updating the cluster LDAP configuration
The cluster LDAP PATCH request updates the LDAP configuration of the cluster.<br>
The following example shows how a PATCH request is used to update the cluster LDAP configuration:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
    resource.servers = ["55.55.55.55"]
    resource.schema = "ad_idmu"
    resource.port = 636
    resource.use_start_tls = False
    resource.patch()

```

### Deleting the cluster LDAP configuration
The cluster LDAP DELETE request deletes the LDAP configuration of the cluster.<br>
The following example shows how a DELETE request is used to delete the cluster LDAP configuration:
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterLdap

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterLdap()
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


__all__ = ["ClusterLdap", "ClusterLdapSchema"]
__pdoc__ = {
    "ClusterLdapSchema.resource": False,
    "ClusterLdap.cluster_ldap_show": False,
    "ClusterLdap.cluster_ldap_create": False,
    "ClusterLdap.cluster_ldap_modify": False,
    "ClusterLdap.cluster_ldap_delete": False,
}


class ClusterLdapSchema(ResourceSchema):
    """The fields of the ClusterLdap object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the cluster_ldap. """

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
    r""" The servers field of the cluster_ldap. """

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

    use_start_tls = fields.Boolean(
        data_key="use_start_tls",
    )
    r""" Specifies whether or not to use Start TLS over LDAP connections. """

    @property
    def resource(self):
        return ClusterLdap

    gettable_fields = [
        "links",
        "base_dn",
        "base_scope",
        "bind_dn",
        "min_bind_level",
        "port",
        "schema",
        "servers",
        "session_security",
        "use_start_tls",
    ]
    """links,base_dn,base_scope,bind_dn,min_bind_level,port,schema,servers,session_security,use_start_tls,"""

    patchable_fields = [
        "base_dn",
        "base_scope",
        "bind_dn",
        "bind_password",
        "min_bind_level",
        "port",
        "schema",
        "servers",
        "session_security",
        "use_start_tls",
    ]
    """base_dn,base_scope,bind_dn,bind_password,min_bind_level,port,schema,servers,session_security,use_start_tls,"""

    postable_fields = [
        "base_dn",
        "base_scope",
        "bind_dn",
        "bind_password",
        "min_bind_level",
        "port",
        "schema",
        "servers",
        "session_security",
        "use_start_tls",
    ]
    """base_dn,base_scope,bind_dn,bind_password,min_bind_level,port,schema,servers,session_security,use_start_tls,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in ClusterLdap.get_collection(fields=field)]
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
            raise NetAppRestError("ClusterLdap modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class ClusterLdap(Resource):
    """Allows interaction with ClusterLdap objects on the host"""

    _schema = ClusterLdapSchema
    _path = "/api/security/authentication/cluster/ldap"






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the cluster LDAP configuration.

### Learn more
* [`DOC /security/authentication/cluster/ldap`](#docs-security-security_authentication_cluster_ldap)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cluster ldap show")
        def cluster_ldap_show(
            base_dn: Choices.define(_get_field_list("base_dn"), cache_choices=True, inexact=True)=None,
            base_scope: Choices.define(_get_field_list("base_scope"), cache_choices=True, inexact=True)=None,
            bind_dn: Choices.define(_get_field_list("bind_dn"), cache_choices=True, inexact=True)=None,
            bind_password: Choices.define(_get_field_list("bind_password"), cache_choices=True, inexact=True)=None,
            min_bind_level: Choices.define(_get_field_list("min_bind_level"), cache_choices=True, inexact=True)=None,
            port: Choices.define(_get_field_list("port"), cache_choices=True, inexact=True)=None,
            schema: Choices.define(_get_field_list("schema"), cache_choices=True, inexact=True)=None,
            servers: Choices.define(_get_field_list("servers"), cache_choices=True, inexact=True)=None,
            session_security: Choices.define(_get_field_list("session_security"), cache_choices=True, inexact=True)=None,
            use_start_tls: Choices.define(_get_field_list("use_start_tls"), cache_choices=True, inexact=True)=None,
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single ClusterLdap resource

            Args:
                base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                port: The port used to connect to the LDAP Servers.
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
            """

            kwargs = {}
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

            resource = ClusterLdap(
                **kwargs
            )
            resource.get()
            return [resource]

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""A cluster can have only one LDAP configuration. IPv6 must be enabled if IPv6 family addresses are specified.
### Required properties
* `servers` - List of LDAP servers used for this client configuration.
* `bind_dn` - Specifies the user that binds to the LDAP servers.
* `base_dn` - Specifies the default base DN for all searches.
### Recommended optional properties
* `schema` - Schema template name.
* `port` - Port used to connect to the LDAP Servers.
* `min_bind_level` - Minimum bind authentication level.
* `bind_password` - Specifies the bind password for the LDAP servers.
* `base_scope` - Specifies the default search scope for LDAP queries.
* `use_start_tls` - Specifies whether or not to use Start TLS over LDAP connections.
* `session_security` - Specifies the level of security to be used for LDAP communications.
### Default property values
* `schema` - _RFC-2307_
* `port` - _389_
* `min_bind_level` - _simple_
* `base_scope` - _subtree_
* `use_start_tls` - _false_
* `session_security` - _none_
<br/>
Configuring more than one LDAP server is recommended to avoid a single point of failure. Both FQDNs and IP addresses are supported for the `servers` property.
The LDAP servers are validated as part of this operation. LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server is invalid.
3. The server is unreachable.<br/>

### Learn more
* [`DOC /security/authentication/cluster/ldap`](#docs-security-security_authentication_cluster_ldap)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cluster ldap create")
        async def cluster_ldap_create(
            links: dict = None,
            base_dn: str = None,
            base_scope: str = None,
            bind_dn: str = None,
            bind_password: str = None,
            min_bind_level: str = None,
            port: Size = None,
            schema: str = None,
            servers = None,
            session_security: str = None,
            use_start_tls: bool = None,
        ) -> ResourceTable:
            """Create an instance of a ClusterLdap resource

            Args:
                links: 
                base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                port: The port used to connect to the LDAP Servers.
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
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
            if schema is not None:
                kwargs["schema"] = schema
            if servers is not None:
                kwargs["servers"] = servers
            if session_security is not None:
                kwargs["session_security"] = session_security
            if use_start_tls is not None:
                kwargs["use_start_tls"] = use_start_tls

            resource = ClusterLdap(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create ClusterLdap: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Both mandatory and optional parameters of the LDAP configuration can be updated.
IPv6 must be enabled if IPv6 family addresses are specified. Configuring more than one LDAP server is recommended to avoid a single point of failure. Both FQDNs and IP addresses are supported for the `servers` property.
The LDAP servers are validated as part of this operation. LDAP validation fails in the following scenarios:<br/>
1. The server does not have LDAP installed.
2. The server is invalid.
3. The server is unreachable. <br/>

### Learn more
* [`DOC /security/authentication/cluster/ldap`](#docs-security-security_authentication_cluster_ldap)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cluster ldap modify")
        async def cluster_ldap_modify(
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
            schema: str = None,
            query_schema: str = None,
            servers=None,
            query_servers=None,
            session_security: str = None,
            query_session_security: str = None,
            use_start_tls: bool = None,
            query_use_start_tls: bool = None,
        ) -> ResourceTable:
            """Modify an instance of a ClusterLdap resource

            Args:
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
            if query_schema is not None:
                kwargs["schema"] = query_schema
            if query_servers is not None:
                kwargs["servers"] = query_servers
            if query_session_security is not None:
                kwargs["session_security"] = query_session_security
            if query_use_start_tls is not None:
                kwargs["use_start_tls"] = query_use_start_tls

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
            if schema is not None:
                changes["schema"] = schema
            if servers is not None:
                changes["servers"] = servers
            if session_security is not None:
                changes["session_security"] = session_security
            if use_start_tls is not None:
                changes["use_start_tls"] = use_start_tls

            if hasattr(ClusterLdap, "find"):
                resource = ClusterLdap.find(
                    **kwargs
                )
            else:
                resource = ClusterLdap()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify ClusterLdap: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the LDAP configuration of the cluster.

### Learn more
* [`DOC /security/authentication/cluster/ldap`](#docs-security-security_authentication_cluster_ldap)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cluster ldap delete")
        async def cluster_ldap_delete(
            base_dn: str = None,
            base_scope: str = None,
            bind_dn: str = None,
            bind_password: str = None,
            min_bind_level: str = None,
            port: Size = None,
            schema: str = None,
            servers=None,
            session_security: str = None,
            use_start_tls: bool = None,
        ) -> None:
            """Delete an instance of a ClusterLdap resource

            Args:
                base_dn: Specifies the default base DN for all searches.
                base_scope: Specifies the default search scope for LDAP queries: * base - search the named entry only * onelevel - search all entries immediately below the DN * subtree - search the named DN entry and the entire subtree below the DN 
                bind_dn: Specifies the user that binds to the LDAP servers.
                bind_password: Specifies the bind password for the LDAP servers.
                min_bind_level: The minimum bind authentication level. Possible values are: * anonymous - anonymous bind * simple - simple bind * sasl - Simple Authentication and Security Layer (SASL) bind 
                port: The port used to connect to the LDAP Servers.
                schema: The name of the schema template used by the SVM. * AD-IDMU - Active Directory Identity Management for UNIX * AD-SFU - Active Directory Services for UNIX * MS-AD-BIS - Active Directory Identity Management for UNIX * RFC-2307 - Schema based on RFC 2307 * Custom schema 
                servers: 
                session_security: Specifies the level of security to be used for LDAP communications: * none - no signing or sealing * sign - sign LDAP traffic * seal - seal and sign LDAP traffic 
                use_start_tls: Specifies whether or not to use Start TLS over LDAP connections. 
            """

            kwargs = {}
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
            if schema is not None:
                kwargs["schema"] = schema
            if servers is not None:
                kwargs["servers"] = servers
            if session_security is not None:
                kwargs["session_security"] = session_security
            if use_start_tls is not None:
                kwargs["use_start_tls"] = use_start_tls

            if hasattr(ClusterLdap, "find"):
                resource = ClusterLdap.find(
                    **kwargs
                )
            else:
                resource = ClusterLdap()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete ClusterLdap: %s" % err)


