r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
A CIFS server is necessary to provide SMB clients with access to the Storage Virtual Machine (SVM). Before you begin, the following prerequisites must be in place:</br>

 * At least one SVM LIF must exist on the SVM.
 * The LIFs must be able to connect to the DNS servers configured on the SVM and to an Active Directory domain controller of the domain to which you want to join the CIFS server.
 * The DNS servers must contain the service location records that are needed to locate the Active Directory domain services.
 * The cluster time must be synchronized to within five minutes of the Active Directory domain controller.
## Performance monitoring
Performance of the SVM can be monitored by the `metric.*` and `statistics.*` properties. These show the performance of the SVM in terms of IOPS, latency and throughput. The `metric.*` properties denote an average whereas `statistics.*` properties denote a real-time monotonically increasing value aggregated across all nodes.
### Information on the CIFS server
 You must keep the following in mind when creating the CIFS server:

 * The CIFS server name might or might not be the same as the SVM name.
 * The CIFS server name can be up to 15 characters in length.
 * The following characters are not allowed: @ # * ( ) = + [ ] | ; : " , < > \ / ?
 * You must use the FQDN when specifying the domain.
 * The default is to add the CIFS server machine account to the Active Directory "CN=Computer" object.
 * You can choose to add the CIFS server to a different organizational unit (OU) by specifying the "organizational_unit" parameter. When specifying the OU, do not specify the domain portion of the distinguished name; only specify the OU or CN portion of the distinguished name. ONTAP appends the value provided for the required "-domain" parameter onto the value provided for the "-ou" parameter to create the Active Directory distinguished name, which is used when joining the Active Directory domain.
 * You can optionally choose to add a text comment of up to 48 characters about the CIFS server. If there is a space in the comment text, you must enclose the entire string in quotation marks.
 * You can optionally choose to add a comma-delimited list of one or more NetBIOS aliases for the CIFS server.
 * The initial administrative status of the CIFS server is "up".
 * The <i> large-mtu</i> and <i>multichannel</i> features are enabled for the new CIFS server.
 * If LDAP is configured with the <i>use_start_tls</i> and <i>session_security</i> features, the new CIFS server will also have this property set.
## Examples
### Creating a CIFS server
To create a CIFS server, use the following API. Note the <i>return_records=true</i> query parameter used to obtain the newly created entry in the response.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService()
    resource.ad_domain.fqdn = "CIFS-2008R2-AD.GDL.ENGLAB.NETAPP.COM"
    resource.ad_domain.organizational_unit = "CN=Computers"
    resource.ad_domain.password = "cifs*123"
    resource.ad_domain.user = "administrator"
    resource.comment = "This CIFS Server Belongs to CS Department"
    resource.default_unix_user = "string"
    resource.enabled = True
    resource.name = "CIFS-DOC"
    resource.netbios.aliases = ["ALIAS_1", "ALIAS_2", "ALIAS_3"]
    resource.netbios.enabled = False
    resource.netbios.wins_servers = ["10.224.65.20", "10.224.65.21"]
    resource.security.kdc_encryption = False
    resource.security.encrypt_dc_connection = False
    resource.security.restrict_anonymous = "no_enumeration"
    resource.security.smb_encryption = False
    resource.security.smb_signing = False
    resource.svm.name = "vs1"
    resource.svm.uuid = "ef087155-f9e2-11e8-ac52-0050568ea248"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
CifsService(
    {
        "netbios": {
            "aliases": ["ALIAS_1", "ALIAS_2", "ALIAS_3"],
            "wins_servers": ["10.224.65.20", "10.224.65.21"],
            "enabled": False,
        },
        "enabled": True,
        "default_unix_user": "string",
        "ad_domain": {
            "fqdn": "CIFS-2008R2-AD.GDL.ENGLAB.NETAPP.COM",
            "user": "administrator",
            "password": "cifs*123",
            "organizational_unit": "CN=Computers",
        },
        "comment": "This CIFS Server Belongs to CS Department",
        "svm": {"name": "vs1", "uuid": "9f5ab4cb-f703-11e8-91cc-0050568eca13"},
        "name": "CIFS-DOC",
        "security": {
            "kdc_encryption": False,
            "restrict_anonymous": "no_enumeration",
            "smb_encryption": False,
            "encrypt_dc_connection": False,
            "smb_signing": False,
        },
    }
)

```
</div>
</div>

---
### Retrieving the full CIFS server configuration for all SVMs in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(CifsService.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    CifsService(
        {
            "netbios": {
                "aliases": ["ALIAS_1", "ALIAS_2", "ALIAS_3"],
                "wins_servers": ["10.224.65.20", "10.224.65.21"],
                "enabled": False,
            },
            "enabled": True,
            "default_unix_user": "string",
            "ad_domain": {
                "fqdn": "CIFS-2008R2-AD.GDL.ENGLAB.NETAPP.COM",
                "organizational_unit": "CN=Computers",
            },
            "comment": "This CIFS Server Belongs to CS Department",
            "svm": {"name": "vs1", "uuid": "9f5ab4cb-f703-11e8-91cc-0050568eca13"},
            "name": "CIFS-DOC",
            "security": {
                "kdc_encryption": False,
                "lm_compatibility_level": "lm_ntlm_ntlmv2_krb",
                "restrict_anonymous": "no_enumeration",
                "smb_encryption": False,
                "encrypt_dc_connection": False,
                "smb_signing": False,
            },
        }
    )
]

```
</div>
</div>

---
### Retrieving CIFS server configuration details for a specific SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService(**{"svm.uuid": "9f5ab4cb-f703-11e8-91cc-0050568eca13"})
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
CifsService(
    {
        "netbios": {
            "aliases": ["ALIAS_1", "ALIAS_2", "ALIAS_3"],
            "wins_servers": ["10.224.65.20", "10.224.65.21"],
            "enabled": False,
        },
        "enabled": True,
        "default_unix_user": "string",
        "ad_domain": {
            "fqdn": "CIFS-2008R2-AD.GDL.ENGLAB.NETAPP.COM",
            "organizational_unit": "CN=Computers",
        },
        "comment": "This CIFS Server Belongs to CS Department",
        "svm": {"name": "vs1", "uuid": "9f5ab4cb-f703-11e8-91cc-0050568eca13"},
        "name": "CIFS-DOC",
        "security": {
            "kdc_encryption": False,
            "lm_compatibility_level": "lm_ntlm_ntlmv2_krb",
            "restrict_anonymous": "no_enumeration",
            "smb_encryption": False,
            "encrypt_dc_connection": False,
            "smb_signing": False,
        },
    }
)

```
</div>
</div>

---
### Updating CIFS server properties for the specified SVM
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService(**{"svm.uuid": "9f5ab4cb-f703-11e8-91cc-0050568eca13"})
    resource.comment = "CIFS SERVER MODIFICATION"
    resource.patch()

```

---
### Removing a CIFS server for a specific SVM
To delete a CIFS server, use the following API. This will delete the CIFS server along with other CIFS configurations such as CIFS share, share ACLs, homedir search-path, and so on.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsService

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsService(**{"svm.uuid": "9f5ab4cb-f703-11e8-91cc-0050568eca13"})
    resource.delete(
        body={"ad_domain": {"password": "cifs*123", "user": "administrator"}}
    )

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


__all__ = ["CifsService", "CifsServiceSchema"]
__pdoc__ = {
    "CifsServiceSchema.resource": False,
    "CifsService.cifs_service_show": False,
    "CifsService.cifs_service_create": False,
    "CifsService.cifs_service_modify": False,
    "CifsService.cifs_service_delete": False,
}


class CifsServiceSchema(ResourceSchema):
    """The fields of the CifsService object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the cifs_service. """

    ad_domain = fields.Nested("netapp_ontap.models.ad_domain.AdDomainSchema", data_key="ad_domain", unknown=EXCLUDE)
    r""" The ad_domain field of the cifs_service. """

    comment = fields.Str(
        data_key="comment",
        validate=len_validation(minimum=0, maximum=48),
    )
    r""" A descriptive text comment for the CIFS server. SMB clients can see the CIFS server comment when browsing servers on the network. If there is a space in the comment, you must enclose the entire string in quotation marks.

Example: This CIFS Server Belongs to CS Department """

    default_unix_user = fields.Str(
        data_key="default_unix_user",
    )
    r""" Specifies the UNIX user to which any authenticated CIFS user is mapped to, if the normal user mapping rules fails. """

    enabled = fields.Boolean(
        data_key="enabled",
    )
    r""" Specifies if the CIFS service is administratively enabled. """

    metric = fields.Nested("netapp_ontap.models.performance_metric_svm.PerformanceMetricSvmSchema", data_key="metric", unknown=EXCLUDE)
    r""" The metric field of the cifs_service. """

    name = fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=15),
    )
    r""" The name of the CIFS server.

Example: CIFS1 """

    netbios = fields.Nested("netapp_ontap.models.cifs_netbios.CifsNetbiosSchema", data_key="netbios", unknown=EXCLUDE)
    r""" The netbios field of the cifs_service. """

    security = fields.Nested("netapp_ontap.models.cifs_service_security.CifsServiceSecuritySchema", data_key="security", unknown=EXCLUDE)
    r""" The security field of the cifs_service. """

    statistics = fields.Nested("netapp_ontap.models.performance_metric_raw_svm.PerformanceMetricRawSvmSchema", data_key="statistics", unknown=EXCLUDE)
    r""" The statistics field of the cifs_service. """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the cifs_service. """

    @property
    def resource(self):
        return CifsService

    gettable_fields = [
        "links",
        "ad_domain",
        "comment",
        "default_unix_user",
        "enabled",
        "metric.links",
        "metric.duration",
        "metric.iops",
        "metric.latency",
        "metric.status",
        "metric.throughput",
        "metric.timestamp",
        "name",
        "netbios",
        "security",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.status",
        "statistics.throughput_raw",
        "statistics.timestamp",
        "svm.links",
        "svm.name",
        "svm.uuid",
    ]
    """links,ad_domain,comment,default_unix_user,enabled,metric.links,metric.duration,metric.iops,metric.latency,metric.status,metric.throughput,metric.timestamp,name,netbios,security,statistics.iops_raw,statistics.latency_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,svm.links,svm.name,svm.uuid,"""

    patchable_fields = [
        "ad_domain",
        "comment",
        "default_unix_user",
        "enabled",
        "metric.iops",
        "metric.latency",
        "metric.throughput",
        "name",
        "netbios",
        "security",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.throughput_raw",
        "svm.name",
        "svm.uuid",
    ]
    """ad_domain,comment,default_unix_user,enabled,metric.iops,metric.latency,metric.throughput,name,netbios,security,statistics.iops_raw,statistics.latency_raw,statistics.throughput_raw,svm.name,svm.uuid,"""

    postable_fields = [
        "ad_domain",
        "comment",
        "default_unix_user",
        "enabled",
        "metric.iops",
        "metric.latency",
        "metric.throughput",
        "name",
        "netbios",
        "security",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.throughput_raw",
        "svm.name",
        "svm.uuid",
    ]
    """ad_domain,comment,default_unix_user,enabled,metric.iops,metric.latency,metric.throughput,name,netbios,security,statistics.iops_raw,statistics.latency_raw,statistics.throughput_raw,svm.name,svm.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in CifsService.get_collection(fields=field)]
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
            raise NetAppRestError("CifsService modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class CifsService(Resource):
    """Allows interaction with CifsService objects on the host"""

    _schema = CifsServiceSchema
    _path = "/api/protocols/cifs/services"
    _keys = ["svm.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves CIFS servers.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver cifs server show`
* `vserver cifs server options show`
* `vserver cifs server security show`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cifs service show")
        def cifs_service_show(
            comment: Choices.define(_get_field_list("comment"), cache_choices=True, inexact=True)=None,
            default_unix_user: Choices.define(_get_field_list("default_unix_user"), cache_choices=True, inexact=True)=None,
            enabled: Choices.define(_get_field_list("enabled"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["comment", "default_unix_user", "enabled", "name", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of CifsService resources

            Args:
                comment: A descriptive text comment for the CIFS server. SMB clients can see the CIFS server comment when browsing servers on the network. If there is a space in the comment, you must enclose the entire string in quotation marks.
                default_unix_user: Specifies the UNIX user to which any authenticated CIFS user is mapped to, if the normal user mapping rules fails.
                enabled: Specifies if the CIFS service is administratively enabled. 
                name: The name of the CIFS server.
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if default_unix_user is not None:
                kwargs["default_unix_user"] = default_unix_user
            if enabled is not None:
                kwargs["enabled"] = enabled
            if name is not None:
                kwargs["name"] = name
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return CifsService.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves CIFS servers.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver cifs server show`
* `vserver cifs server options show`
* `vserver cifs server security show`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
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
        r"""Updates both the mandatory and optional parameters of the CIFS configuration. Ensure the CIFS server is administratively disabled when renaming the CIFS server or modifying the <i>ad_domain</i> properties.
### Related ONTAP commands
* `vserver cifs server modify`
* `vserver cifs server options modify`
* `vserver cifs security modify`
* `vserver cifs server add-netbios-aliases`
* `vserver cifs server remove-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
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
        r"""Deletes a CIFS server and related CIFS configurations.
### Related ONTAP commands
* `vserver cifs server delete`
* `vserver cifs remove-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves CIFS servers.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `statistics.*`
* `metric.*`
### Related ONTAP commands
* `vserver cifs server show`
* `vserver cifs server options show`
* `vserver cifs server security show`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a CIFS server.
### Related ONTAP commands
* `vserver cifs server show`
* `vserver cifs server options show`
* `vserver cifs server security show`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
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
        r"""Creates a CIFS server. Each SVM can have one CIFS server.</br>
### Important notes
- The CIFS server name might or might not be the same as the SVM name.
- The CIFS server name can contain up to 15 characters.
- The CIFS server name does not support the following characters: @ # * ( ) = + [ ] | ; : " , < >  / ?
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS server.
* `name` -  Name of the CIFS server.
* `ad_domain.fqdn` - Fully qualified domain name of the Windows Active Directory to which this CIFS server belongs.
* `ad_domain.user` - User account with the access to add the CIFS server to the Active Directory.
* `ad_domain.password` - Account password used to add this CIFS server to the Active Directory.
### Recommended optional properties
* `comment` - Add a text comment of up to 48 characters about the CIFS server.
* `netbios.aliases` - Add a comma-delimited list of one or more NetBIOS aliases for the CIFS server.
* `netbios.wins_servers` - Add a list of Windows Internet Name Server (WINS) addresses that manage and map the NetBIOS name of the CIFS server to their network IP addresses. The IP addresses must be IPv4 addresses.
### Default property values
If not specified in POST, the following default property values are assigned:
* `ad_domain.organizational_unit` - _CN=Computers_
* `enabled` - _true_
* `restrict_anonymous` - _no_enumeration_
* `smb_signing` - _false_
* `smb_encryption` - _false_
* `encrypt_dc_connection` - _false_
* `kdc_encryption` - _false_
* `default_unix_user` - _pcuser_
* `netbios_enabled` - _false_ However, if either "netbios.wins-server" or "netbios.aliases" is set during POST and if `netbios_enabled` is not specified then `netbios_enabled` is set to true.
### Related ONTAP commands
* `vserver cifs server create`
* `vserver cifs server options modify`
* `vserver cifs security modify`
* `vserver cifs server add-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cifs service create")
        async def cifs_service_create(
            links: dict = None,
            ad_domain: dict = None,
            comment: str = None,
            default_unix_user: str = None,
            enabled: bool = None,
            metric: dict = None,
            name: str = None,
            netbios: dict = None,
            security: dict = None,
            statistics: dict = None,
            svm: dict = None,
        ) -> ResourceTable:
            """Create an instance of a CifsService resource

            Args:
                links: 
                ad_domain: 
                comment: A descriptive text comment for the CIFS server. SMB clients can see the CIFS server comment when browsing servers on the network. If there is a space in the comment, you must enclose the entire string in quotation marks.
                default_unix_user: Specifies the UNIX user to which any authenticated CIFS user is mapped to, if the normal user mapping rules fails.
                enabled: Specifies if the CIFS service is administratively enabled. 
                metric: 
                name: The name of the CIFS server.
                netbios: 
                security: 
                statistics: 
                svm: 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if ad_domain is not None:
                kwargs["ad_domain"] = ad_domain
            if comment is not None:
                kwargs["comment"] = comment
            if default_unix_user is not None:
                kwargs["default_unix_user"] = default_unix_user
            if enabled is not None:
                kwargs["enabled"] = enabled
            if metric is not None:
                kwargs["metric"] = metric
            if name is not None:
                kwargs["name"] = name
            if netbios is not None:
                kwargs["netbios"] = netbios
            if security is not None:
                kwargs["security"] = security
            if statistics is not None:
                kwargs["statistics"] = statistics
            if svm is not None:
                kwargs["svm"] = svm

            resource = CifsService(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create CifsService: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates both the mandatory and optional parameters of the CIFS configuration. Ensure the CIFS server is administratively disabled when renaming the CIFS server or modifying the <i>ad_domain</i> properties.
### Related ONTAP commands
* `vserver cifs server modify`
* `vserver cifs server options modify`
* `vserver cifs security modify`
* `vserver cifs server add-netbios-aliases`
* `vserver cifs server remove-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cifs service modify")
        async def cifs_service_modify(
            comment: str = None,
            query_comment: str = None,
            default_unix_user: str = None,
            query_default_unix_user: str = None,
            enabled: bool = None,
            query_enabled: bool = None,
            name: str = None,
            query_name: str = None,
        ) -> ResourceTable:
            """Modify an instance of a CifsService resource

            Args:
                comment: A descriptive text comment for the CIFS server. SMB clients can see the CIFS server comment when browsing servers on the network. If there is a space in the comment, you must enclose the entire string in quotation marks.
                query_comment: A descriptive text comment for the CIFS server. SMB clients can see the CIFS server comment when browsing servers on the network. If there is a space in the comment, you must enclose the entire string in quotation marks.
                default_unix_user: Specifies the UNIX user to which any authenticated CIFS user is mapped to, if the normal user mapping rules fails.
                query_default_unix_user: Specifies the UNIX user to which any authenticated CIFS user is mapped to, if the normal user mapping rules fails.
                enabled: Specifies if the CIFS service is administratively enabled. 
                query_enabled: Specifies if the CIFS service is administratively enabled. 
                name: The name of the CIFS server.
                query_name: The name of the CIFS server.
            """

            kwargs = {}
            changes = {}
            if query_comment is not None:
                kwargs["comment"] = query_comment
            if query_default_unix_user is not None:
                kwargs["default_unix_user"] = query_default_unix_user
            if query_enabled is not None:
                kwargs["enabled"] = query_enabled
            if query_name is not None:
                kwargs["name"] = query_name

            if comment is not None:
                changes["comment"] = comment
            if default_unix_user is not None:
                changes["default_unix_user"] = default_unix_user
            if enabled is not None:
                changes["enabled"] = enabled
            if name is not None:
                changes["name"] = name

            if hasattr(CifsService, "find"):
                resource = CifsService.find(
                    **kwargs
                )
            else:
                resource = CifsService()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify CifsService: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a CIFS server and related CIFS configurations.
### Related ONTAP commands
* `vserver cifs server delete`
* `vserver cifs remove-netbios-aliases`
### Learn more
* [`DOC /protocols/cifs/services`](#docs-NAS-protocols_cifs_services)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cifs service delete")
        async def cifs_service_delete(
            comment: str = None,
            default_unix_user: str = None,
            enabled: bool = None,
            name: str = None,
        ) -> None:
            """Delete an instance of a CifsService resource

            Args:
                comment: A descriptive text comment for the CIFS server. SMB clients can see the CIFS server comment when browsing servers on the network. If there is a space in the comment, you must enclose the entire string in quotation marks.
                default_unix_user: Specifies the UNIX user to which any authenticated CIFS user is mapped to, if the normal user mapping rules fails.
                enabled: Specifies if the CIFS service is administratively enabled. 
                name: The name of the CIFS server.
            """

            kwargs = {}
            if comment is not None:
                kwargs["comment"] = comment
            if default_unix_user is not None:
                kwargs["default_unix_user"] = default_unix_user
            if enabled is not None:
                kwargs["enabled"] = enabled
            if name is not None:
                kwargs["name"] = name

            if hasattr(CifsService, "find"):
                resource = CifsService.find(
                    **kwargs
                )
            else:
                resource = CifsService()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete CifsService: %s" % err)


