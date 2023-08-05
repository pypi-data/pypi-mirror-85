r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
Azure Key Vault (AKV) is a cloud key management service (KMS) that provides a secure store for secrets. This feature
allows ONTAP to securely store its encryption keys using AKV.
In order to use AKV with ONTAP, you must first deploy an Azure application with the appropriate access to an AKV and then provide
ONTAP with the necessary details, such as key vault name, application ID so that ONTAP can communicate with the deployed Azure application.
The properties "state", "azure_reachability" and "ekmip_reachability" are considered advanced properties and are populated only when explicitly requested.
## Examples
### Creating an AKV for a cluster
The example AKV is configured at the cluster-scope. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key manager configuration.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault()
    resource.client_id = "client1"
    resource.tenant_id = "tenant1"
    resource.name = "https:://mykeyvault.azure.vault.net/"
    resource.key_id = "https://keyvault-test.vault.azure.net/keys/key1/a8e619fd8f234db3b0b95c59540e2a74"
    resource.client_secret = "myclientPwd"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
AzureKeyVault(
    {
        "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
        "_links": {
            "self": {
                "href": "/api/security/azure-key-vaults/85619643-9a06-11ea-8d52-005056bbeba5"
            }
        },
        "name": "https:://mykeyvault.azure.vault.net/",
        "tenant_id": "tenant1",
        "client_id": "client1",
        "key_id": "https://keyvault-test.vault.azure.net/keys/key1",
    }
)

```
</div>
</div>

---
### Creating an AKV for an SVM
The example AKV is configured for a specific SVM. Note the <i>return_records=true</i> query parameter is used to obtain the newly created key manager configuration.<br/>
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault()
    resource.svm.uuid = "4f7abf4c-9a07-11ea-8d52-005056bbeba5"
    resource.client_id = "client1"
    resource.tenant_id = "tenant1"
    resource.name = "https:://mykeyvault.azure.vault.net/"
    resource.key_id = "https://keyvault-test.vault.azure.net/keys/key1"
    resource.client_secret = "myclientPwd"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
AzureKeyVault(
    {
        "uuid": "024cd3cf-9a08-11ea-8d52-005056bbeba5",
        "_links": {
            "self": {
                "href": "/api/security/azure-key-vaults/024cd3cf-9a08-11ea-8d52-005056bbeba5"
            }
        },
        "svm": {"name": "vs0", "uuid": "4f7abf4c-9a07-11ea-8d52-005056bbeba5"},
        "name": "https:://mykeyvault.azure.vault.net/",
        "tenant_id": "tenant1",
        "client_id": "client1",
        "key_id": "https://keyvault-test.vault.azure.net/keys/key1",
    }
)

```
</div>
</div>

---
### Retrieving the AKVs configured for all clusters and SVMs
The following example shows how to retrieve all configured AKVs along with their configurations.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(AzureKeyVault.get_collection(fields="*")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    AzureKeyVault(
        {
            "uuid": "024cd3cf-9a08-11ea-8d52-005056bbeba5",
            "scope": "svm",
            "_links": {
                "self": {
                    "href": "/api/security/azure-key-vaults/024cd3cf-9a08-11ea-8d52-005056bbeba5"
                }
            },
            "svm": {"name": "vs0", "uuid": "4f7abf4c-9a07-11ea-8d52-005056bbeba5"},
            "name": "https:://mykeyvault.azure.vault.net/",
            "tenant_id": "tenant1",
            "client_id": "client1",
            "key_id": "https://keyvault-test.vault.azure.net/keys/key1",
            "state": {"code": 0, "message": ""},
        }
    ),
    AzureKeyVault(
        {
            "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
            "scope": "cluster",
            "_links": {
                "self": {
                    "href": "/api/security/azure-key-vaults/85619643-9a06-11ea-8d52-005056bbeba5"
                }
            },
            "name": "https:://mykeyvault.azure.vault.net/",
            "tenant_id": "tenant1",
            "client_id": "client1",
            "key_id": "https://keyvault-test.vault.azure.net/keys/key1",
            "state": {"code": 0, "message": ""},
        }
    ),
]

```
</div>
</div>

---
### Retrieving the AKV configured for a specific SVM
The following example retrieves a configured AKV for a specific SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
AzureKeyVault(
    {
        "uuid": "85619643-9a06-11ea-8d52-005056bbeba5",
        "scope": "cluster",
        "_links": {
            "self": {
                "href": "/api/security/azure-key-vaults/85619643-9a06-11ea-8d52-005056bbeba5"
            }
        },
        "name": "https:://mykeyvault.azure.vault.net/",
        "tenant_id": "tenant1",
        "client_id": "client1",
        "key_id": "https://keyvault-test.vault.azure.net/keys/key1",
        "state": {"code": 0, "message": ""},
    }
)

```
</div>
</div>

---
### Retrieving the advanced properties of an AKV configured for a specific SVM
The following example retrieves the advanced properties of a configured AKV for a specific SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.get(fields='state,azure_reachability,ekmip_reachability"')
    print(resource)

```

---
### Updating the client password of a specific SVM
The following example updates the client password of a configured AKV for a specific SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.client_secret = "newSecret"
    resource.patch()

```

---
### Deleting an AKV configuration for a specific SVM
The following example deletes a configured AKV for a specific SVM.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.delete()

```

---
### Restoring the keys for a specific SVM configured with an AKV
The following example restores all the keys of a specific SVM configured with an AKV.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.restore()

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
AzureKeyVault({})

```
</div>
</div>

---
### Rekeying the internal key for a specific SVM configured with an AKV
The following example rekeys the internal key of a specific SVM configured with an AKV.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import AzureKeyVault

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = AzureKeyVault(uuid="85619643-9a06-11ea-8d52-005056bbeba5")
    resource.rekey_internal()

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
AzureKeyVault({})

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


__all__ = ["AzureKeyVault", "AzureKeyVaultSchema"]
__pdoc__ = {
    "AzureKeyVaultSchema.resource": False,
    "AzureKeyVault.azure_key_vault_show": False,
    "AzureKeyVault.azure_key_vault_create": False,
    "AzureKeyVault.azure_key_vault_modify": False,
    "AzureKeyVault.azure_key_vault_delete": False,
}


class AzureKeyVaultSchema(ResourceSchema):
    """The fields of the AzureKeyVault object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the azure_key_vault. """

    azure_reachability = fields.Nested("netapp_ontap.models.azure_key_vault_connectivity.AzureKeyVaultConnectivitySchema", data_key="azure_reachability", unknown=EXCLUDE)
    r""" The azure_reachability field of the azure_key_vault. """

    client_id = fields.Str(
        data_key="client_id",
    )
    r""" Application client ID of the deployed Azure application with appropriate access to an AKV.

Example: aaaaaaaa-bbbb-aaaa-bbbb-aaaaaaaaaaaa """

    client_secret = fields.Str(
        data_key="client_secret",
    )
    r""" Password used by the application to prove its identity to AKV.

Example: abcdef """

    ekmip_reachability = fields.List(fields.Nested("netapp_ontap.models.ekmip_server_connectivity.EkmipServerConnectivitySchema", unknown=EXCLUDE), data_key="ekmip_reachability")
    r""" The ekmip_reachability field of the azure_key_vault. """

    key_id = fields.Str(
        data_key="key_id",
    )
    r""" Key Identifier of AKV key encryption key.

Example: https://keyvault1.vault.azure.net/keys/key1 """

    name = fields.Str(
        data_key="name",
    )
    r""" Name of the deployed AKV that will be used by ONTAP for storing keys.

Example: https://kmip-akv-keyvault.vault.azure.net/ """

    polling_period = Size(
        data_key="polling_period",
    )
    r""" Polling period in minutes.

Example: 55 """

    proxy_host = fields.Str(
        data_key="proxy_host",
    )
    r""" Proxy host.

Example: proxy.eng.com """

    proxy_password = fields.Str(
        data_key="proxy_password",
    )
    r""" Proxy password. Password is not audited.

Example: proxypassword """

    proxy_port = Size(
        data_key="proxy_port",
    )
    r""" Proxy port.

Example: 1234 """

    proxy_type = fields.Str(
        data_key="proxy_type",
        validate=enum_validation(['http', 'https']),
    )
    r""" Type of proxy.

Valid choices:

* http
* https """

    proxy_username = fields.Str(
        data_key="proxy_username",
    )
    r""" Proxy username.

Example: proxyuser """

    scope = fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
    )
    r""" Set to "svm" for interfaces owned by an SVM. Otherwise, set to "cluster".

Valid choices:

* svm
* cluster """

    state = fields.Nested("netapp_ontap.models.azure_key_vault_state.AzureKeyVaultStateSchema", data_key="state", unknown=EXCLUDE)
    r""" The state field of the azure_key_vault. """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the azure_key_vault. """

    tenant_id = fields.Str(
        data_key="tenant_id",
    )
    r""" Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.

Example: zzzzzzzz-yyyy-zzzz-yyyy-zzzzzzzzzzzz """

    uuid = fields.Str(
        data_key="uuid",
    )
    r""" A unique identifier for the Azure Key Vault (AKV).

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return AzureKeyVault

    gettable_fields = [
        "links",
        "azure_reachability",
        "client_id",
        "ekmip_reachability",
        "key_id",
        "name",
        "polling_period",
        "proxy_host",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "scope",
        "state",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tenant_id",
        "uuid",
    ]
    """links,azure_reachability,client_id,ekmip_reachability,key_id,name,polling_period,proxy_host,proxy_port,proxy_type,proxy_username,scope,state,svm.links,svm.name,svm.uuid,tenant_id,uuid,"""

    patchable_fields = [
        "client_secret",
        "ekmip_reachability",
        "key_id",
        "polling_period",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "svm.name",
        "svm.uuid",
    ]
    """client_secret,ekmip_reachability,key_id,polling_period,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,svm.name,svm.uuid,"""

    postable_fields = [
        "client_id",
        "client_secret",
        "ekmip_reachability",
        "key_id",
        "name",
        "polling_period",
        "proxy_host",
        "proxy_password",
        "proxy_port",
        "proxy_type",
        "proxy_username",
        "svm.name",
        "svm.uuid",
        "tenant_id",
    ]
    """client_id,client_secret,ekmip_reachability,key_id,name,polling_period,proxy_host,proxy_password,proxy_port,proxy_type,proxy_username,svm.name,svm.uuid,tenant_id,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in AzureKeyVault.get_collection(fields=field)]
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
            raise NetAppRestError("AzureKeyVault modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class AzureKeyVault(Resource):
    """Allows interaction with AzureKeyVault objects on the host"""

    _schema = AzureKeyVaultSchema
    _path = "/api/security/azure-key-vaults"
    _keys = ["uuid"]
    _action_form_data_parameters = { 'file':'file', }

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves AKVs configured for all clusters and SVMs.
### Related ONTAP commands
* `security key-manager external azure show`
* `security key-manager external azure check`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="azure key vault show")
        def azure_key_vault_show(
            client_id: Choices.define(_get_field_list("client_id"), cache_choices=True, inexact=True)=None,
            client_secret: Choices.define(_get_field_list("client_secret"), cache_choices=True, inexact=True)=None,
            key_id: Choices.define(_get_field_list("key_id"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            polling_period: Choices.define(_get_field_list("polling_period"), cache_choices=True, inexact=True)=None,
            proxy_host: Choices.define(_get_field_list("proxy_host"), cache_choices=True, inexact=True)=None,
            proxy_password: Choices.define(_get_field_list("proxy_password"), cache_choices=True, inexact=True)=None,
            proxy_port: Choices.define(_get_field_list("proxy_port"), cache_choices=True, inexact=True)=None,
            proxy_type: Choices.define(_get_field_list("proxy_type"), cache_choices=True, inexact=True)=None,
            proxy_username: Choices.define(_get_field_list("proxy_username"), cache_choices=True, inexact=True)=None,
            scope: Choices.define(_get_field_list("scope"), cache_choices=True, inexact=True)=None,
            tenant_id: Choices.define(_get_field_list("tenant_id"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["client_id", "client_secret", "key_id", "name", "polling_period", "proxy_host", "proxy_password", "proxy_port", "proxy_type", "proxy_username", "scope", "tenant_id", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of AzureKeyVault resources

            Args:
                client_id: Application client ID of the deployed Azure application with appropriate access to an AKV.
                client_secret: Password used by the application to prove its identity to AKV.
                key_id: Key Identifier of AKV key encryption key.
                name: Name of the deployed AKV that will be used by ONTAP for storing keys.
                polling_period: Polling period in minutes.
                proxy_host: Proxy host.
                proxy_password: Proxy password. Password is not audited.
                proxy_port: Proxy port.
                proxy_type: Type of proxy.
                proxy_username: Proxy username.
                scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                tenant_id: Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
                uuid: A unique identifier for the Azure Key Vault (AKV).
            """

            kwargs = {}
            if client_id is not None:
                kwargs["client_id"] = client_id
            if client_secret is not None:
                kwargs["client_secret"] = client_secret
            if key_id is not None:
                kwargs["key_id"] = key_id
            if name is not None:
                kwargs["name"] = name
            if polling_period is not None:
                kwargs["polling_period"] = polling_period
            if proxy_host is not None:
                kwargs["proxy_host"] = proxy_host
            if proxy_password is not None:
                kwargs["proxy_password"] = proxy_password
            if proxy_port is not None:
                kwargs["proxy_port"] = proxy_port
            if proxy_type is not None:
                kwargs["proxy_type"] = proxy_type
            if proxy_username is not None:
                kwargs["proxy_username"] = proxy_username
            if scope is not None:
                kwargs["scope"] = scope
            if tenant_id is not None:
                kwargs["tenant_id"] = tenant_id
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return AzureKeyVault.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves AKVs configured for all clusters and SVMs.
### Related ONTAP commands
* `security key-manager external azure show`
* `security key-manager external azure check`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
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
        r"""Updates the AKV configuration.
### Optional properties
* `client_secret` - New password used to prove the application's identity to the AKV.
* `key_id`- Key Identifier of the new AKV key encryption key.
* `proxy_type`` - Type of proxy (http, https etc.) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `polling_period` - Polling period in minutes.
### Related ONTAP commands
* `security key-manager external azure update-client-secret`
* `security key-manager external azure rekey-external`
* `security key-manager external azure update-config`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
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
        r"""Deletes an AKV configuration.
### Related ONTAP commands
* `security key-manager external azure disable`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves AKVs configured for all clusters and SVMs.
### Related ONTAP commands
* `security key-manager external azure show`
* `security key-manager external azure check`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the AKV configuration for the SVM specified by the UUID.
### Related ONTAP commands
* `security key-manager external azure show`
* `security key-manager external azure check`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
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
        r"""Configures the AKV configuration for all clusters and SVMs.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create a AKV.
* `client_id` - Application (client) ID of the deployed Azure application with appropriate access to an AKV.
* `tenant_id` - Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
* `client_secret` - Password used by the application to prove its identity to AKV.
* `key_id`- Key Identifier of AKV encryption key.
* `name` - Name of the deployed AKV used by ONTAP for storing keys.
### Optional properties
* `proxy_type`` - Type of proxy (http, https etc.) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
### Related ONTAP commands
* `security key-manager external azure enable`
* `security key-manager external azure update-config`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="azure key vault create")
        async def azure_key_vault_create(
            links: dict = None,
            azure_reachability: dict = None,
            client_id: str = None,
            client_secret: str = None,
            ekmip_reachability: dict = None,
            key_id: str = None,
            name: str = None,
            polling_period: Size = None,
            proxy_host: str = None,
            proxy_password: str = None,
            proxy_port: Size = None,
            proxy_type: str = None,
            proxy_username: str = None,
            scope: str = None,
            state: dict = None,
            svm: dict = None,
            tenant_id: str = None,
            uuid: str = None,
        ) -> ResourceTable:
            """Create an instance of a AzureKeyVault resource

            Args:
                links: 
                azure_reachability: 
                client_id: Application client ID of the deployed Azure application with appropriate access to an AKV.
                client_secret: Password used by the application to prove its identity to AKV.
                ekmip_reachability: 
                key_id: Key Identifier of AKV key encryption key.
                name: Name of the deployed AKV that will be used by ONTAP for storing keys.
                polling_period: Polling period in minutes.
                proxy_host: Proxy host.
                proxy_password: Proxy password. Password is not audited.
                proxy_port: Proxy port.
                proxy_type: Type of proxy.
                proxy_username: Proxy username.
                scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                state: 
                svm: 
                tenant_id: Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
                uuid: A unique identifier for the Azure Key Vault (AKV).
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if azure_reachability is not None:
                kwargs["azure_reachability"] = azure_reachability
            if client_id is not None:
                kwargs["client_id"] = client_id
            if client_secret is not None:
                kwargs["client_secret"] = client_secret
            if ekmip_reachability is not None:
                kwargs["ekmip_reachability"] = ekmip_reachability
            if key_id is not None:
                kwargs["key_id"] = key_id
            if name is not None:
                kwargs["name"] = name
            if polling_period is not None:
                kwargs["polling_period"] = polling_period
            if proxy_host is not None:
                kwargs["proxy_host"] = proxy_host
            if proxy_password is not None:
                kwargs["proxy_password"] = proxy_password
            if proxy_port is not None:
                kwargs["proxy_port"] = proxy_port
            if proxy_type is not None:
                kwargs["proxy_type"] = proxy_type
            if proxy_username is not None:
                kwargs["proxy_username"] = proxy_username
            if scope is not None:
                kwargs["scope"] = scope
            if state is not None:
                kwargs["state"] = state
            if svm is not None:
                kwargs["svm"] = svm
            if tenant_id is not None:
                kwargs["tenant_id"] = tenant_id
            if uuid is not None:
                kwargs["uuid"] = uuid

            resource = AzureKeyVault(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create AzureKeyVault: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the AKV configuration.
### Optional properties
* `client_secret` - New password used to prove the application's identity to the AKV.
* `key_id`- Key Identifier of the new AKV key encryption key.
* `proxy_type`` - Type of proxy (http, https etc.) if proxy configuration is used.
* `proxy_host` - Proxy hostname if proxy configuration is used.
* `proxy_port` - Proxy port number if proxy configuration is used.
* `proxy_username` - Proxy username if proxy configuration is used.
* `proxy_password` - Proxy password if proxy configuration is used.
* `polling_period` - Polling period in minutes.
### Related ONTAP commands
* `security key-manager external azure update-client-secret`
* `security key-manager external azure rekey-external`
* `security key-manager external azure update-config`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="azure key vault modify")
        async def azure_key_vault_modify(
            client_id: str = None,
            query_client_id: str = None,
            client_secret: str = None,
            query_client_secret: str = None,
            key_id: str = None,
            query_key_id: str = None,
            name: str = None,
            query_name: str = None,
            polling_period: Size = None,
            query_polling_period: Size = None,
            proxy_host: str = None,
            query_proxy_host: str = None,
            proxy_password: str = None,
            query_proxy_password: str = None,
            proxy_port: Size = None,
            query_proxy_port: Size = None,
            proxy_type: str = None,
            query_proxy_type: str = None,
            proxy_username: str = None,
            query_proxy_username: str = None,
            scope: str = None,
            query_scope: str = None,
            tenant_id: str = None,
            query_tenant_id: str = None,
            uuid: str = None,
            query_uuid: str = None,
        ) -> ResourceTable:
            """Modify an instance of a AzureKeyVault resource

            Args:
                client_id: Application client ID of the deployed Azure application with appropriate access to an AKV.
                query_client_id: Application client ID of the deployed Azure application with appropriate access to an AKV.
                client_secret: Password used by the application to prove its identity to AKV.
                query_client_secret: Password used by the application to prove its identity to AKV.
                key_id: Key Identifier of AKV key encryption key.
                query_key_id: Key Identifier of AKV key encryption key.
                name: Name of the deployed AKV that will be used by ONTAP for storing keys.
                query_name: Name of the deployed AKV that will be used by ONTAP for storing keys.
                polling_period: Polling period in minutes.
                query_polling_period: Polling period in minutes.
                proxy_host: Proxy host.
                query_proxy_host: Proxy host.
                proxy_password: Proxy password. Password is not audited.
                query_proxy_password: Proxy password. Password is not audited.
                proxy_port: Proxy port.
                query_proxy_port: Proxy port.
                proxy_type: Type of proxy.
                query_proxy_type: Type of proxy.
                proxy_username: Proxy username.
                query_proxy_username: Proxy username.
                scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                query_scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                tenant_id: Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
                query_tenant_id: Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
                uuid: A unique identifier for the Azure Key Vault (AKV).
                query_uuid: A unique identifier for the Azure Key Vault (AKV).
            """

            kwargs = {}
            changes = {}
            if query_client_id is not None:
                kwargs["client_id"] = query_client_id
            if query_client_secret is not None:
                kwargs["client_secret"] = query_client_secret
            if query_key_id is not None:
                kwargs["key_id"] = query_key_id
            if query_name is not None:
                kwargs["name"] = query_name
            if query_polling_period is not None:
                kwargs["polling_period"] = query_polling_period
            if query_proxy_host is not None:
                kwargs["proxy_host"] = query_proxy_host
            if query_proxy_password is not None:
                kwargs["proxy_password"] = query_proxy_password
            if query_proxy_port is not None:
                kwargs["proxy_port"] = query_proxy_port
            if query_proxy_type is not None:
                kwargs["proxy_type"] = query_proxy_type
            if query_proxy_username is not None:
                kwargs["proxy_username"] = query_proxy_username
            if query_scope is not None:
                kwargs["scope"] = query_scope
            if query_tenant_id is not None:
                kwargs["tenant_id"] = query_tenant_id
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if client_id is not None:
                changes["client_id"] = client_id
            if client_secret is not None:
                changes["client_secret"] = client_secret
            if key_id is not None:
                changes["key_id"] = key_id
            if name is not None:
                changes["name"] = name
            if polling_period is not None:
                changes["polling_period"] = polling_period
            if proxy_host is not None:
                changes["proxy_host"] = proxy_host
            if proxy_password is not None:
                changes["proxy_password"] = proxy_password
            if proxy_port is not None:
                changes["proxy_port"] = proxy_port
            if proxy_type is not None:
                changes["proxy_type"] = proxy_type
            if proxy_username is not None:
                changes["proxy_username"] = proxy_username
            if scope is not None:
                changes["scope"] = scope
            if tenant_id is not None:
                changes["tenant_id"] = tenant_id
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(AzureKeyVault, "find"):
                resource = AzureKeyVault.find(
                    **kwargs
                )
            else:
                resource = AzureKeyVault()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify AzureKeyVault: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an AKV configuration.
### Related ONTAP commands
* `security key-manager external azure disable`

### Learn more
* [`DOC /security/azure-key-vaults`](#docs-security-security_azure-key-vaults)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="azure key vault delete")
        async def azure_key_vault_delete(
            client_id: str = None,
            client_secret: str = None,
            key_id: str = None,
            name: str = None,
            polling_period: Size = None,
            proxy_host: str = None,
            proxy_password: str = None,
            proxy_port: Size = None,
            proxy_type: str = None,
            proxy_username: str = None,
            scope: str = None,
            tenant_id: str = None,
            uuid: str = None,
        ) -> None:
            """Delete an instance of a AzureKeyVault resource

            Args:
                client_id: Application client ID of the deployed Azure application with appropriate access to an AKV.
                client_secret: Password used by the application to prove its identity to AKV.
                key_id: Key Identifier of AKV key encryption key.
                name: Name of the deployed AKV that will be used by ONTAP for storing keys.
                polling_period: Polling period in minutes.
                proxy_host: Proxy host.
                proxy_password: Proxy password. Password is not audited.
                proxy_port: Proxy port.
                proxy_type: Type of proxy.
                proxy_username: Proxy username.
                scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                tenant_id: Directory (tenant) ID of the deployed Azure application with appropriate access to an AKV.
                uuid: A unique identifier for the Azure Key Vault (AKV).
            """

            kwargs = {}
            if client_id is not None:
                kwargs["client_id"] = client_id
            if client_secret is not None:
                kwargs["client_secret"] = client_secret
            if key_id is not None:
                kwargs["key_id"] = key_id
            if name is not None:
                kwargs["name"] = name
            if polling_period is not None:
                kwargs["polling_period"] = polling_period
            if proxy_host is not None:
                kwargs["proxy_host"] = proxy_host
            if proxy_password is not None:
                kwargs["proxy_password"] = proxy_password
            if proxy_port is not None:
                kwargs["proxy_port"] = proxy_port
            if proxy_type is not None:
                kwargs["proxy_type"] = proxy_type
            if proxy_username is not None:
                kwargs["proxy_username"] = proxy_username
            if scope is not None:
                kwargs["scope"] = scope
            if tenant_id is not None:
                kwargs["tenant_id"] = tenant_id
            if uuid is not None:
                kwargs["uuid"] = uuid

            if hasattr(AzureKeyVault, "find"):
                resource = AzureKeyVault.find(
                    **kwargs
                )
            else:
                resource = AzureKeyVault()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete AzureKeyVault: %s" % err)

    def rekey_internal(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Rekeys the internal key in the key hierarchy for an SVM with an AKV configuration.
### Related ONTAP commands
* `security key-manager external azure rekey-internal`
"""
        return super()._action(
            "rekey_internal", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    rekey_internal.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)
    def restore(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Restore the keys for an SVM from a configured AKV.
### Related ONTAP commands
* `security key-manager external azure restore`
"""
        return super()._action(
            "restore", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    restore.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

