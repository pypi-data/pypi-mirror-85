r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
Before any users or applications can access data on the CIFS server over SMB, a CIFS share must be created with sufficient share permissions. CIFS share is a named access point in a volume which is tied to the CIFS server on the SVM. Before creating a CIFS share make sure that the path is valid within the scope of the SVM and that it is reachable.</br>
Permissions can be assigned to this newly created share by specifying the 'acls' field. When a CIFS share is created, ONTAP creates a default ACL for this share with 'Full-Control' permissions for an 'Everyone' user.
## Examples
### Creating a CIFS share
To create a CIFS share for a CIFS server, use the following API. Note the <i>return_records=true</i> query parameter used to obtain the newly created entry in the response.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShare()
    resource.access_based_enumeration = False
    resource.acls = [
        {"permission": "no_access", "type": "unix_user", "user_or_group": "root"}
    ]
    resource.change_notify = True
    resource.comment = "HR Department Share"
    resource.encryption = False
    resource.home_directory = False
    resource.name = "TEST"
    resource.oplocks = True
    resource.path = "/"
    resource.svm.name = "vs1"
    resource.svm.uuid = "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"
    resource.unix_symlink = "local"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
CifsShare(
    {
        "change_notify": True,
        "access_based_enumeration": False,
        "path": "/",
        "comment": "HR Department Share",
        "svm": {"name": "vs1", "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"},
        "oplocks": True,
        "name": "TEST",
        "acls": [
            {"user_or_group": "root", "type": "unix_user", "permission": "no_access"}
        ],
        "unix_symlink": "local",
        "home_directory": False,
        "encryption": False,
    }
)

```
</div>
</div>

---
### Retrieving CIFS Shares for all SVMs in the cluster
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(CifsShare.get_collection(fields="*", return_timeout=15)))

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
[
    CifsShare(
        {
            "change_notify": False,
            "access_based_enumeration": False,
            "volume": {"name": "vol1", "uuid": "4e06f1bc-1ddc-42e2-abb2-f221c6a2ab2a"},
            "path": "/",
            "_links": {
                "self": {
                    "href": "/api/protocols/cifs/shares/000c5cd2-ebdf-11e8-a96e-0050568ea3cb/admin%24"
                }
            },
            "svm": {
                "name": "vs1",
                "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/000c5cd2-ebdf-11e8-a96e-0050568ea3cb"
                    }
                },
            },
            "oplocks": False,
            "name": "admin$",
            "home_directory": False,
            "encryption": False,
        }
    ),
    CifsShare(
        {
            "change_notify": True,
            "access_based_enumeration": False,
            "volume": {"name": "vol1", "uuid": "4e06f1bc-1ddc-42e2-abb2-f221c6a2ab2a"},
            "path": "/",
            "_links": {
                "self": {
                    "href": "/api/protocols/cifs/shares/000c5cd2-ebdf-11e8-a96e-0050568ea3cb/c%24"
                }
            },
            "svm": {
                "name": "vs1",
                "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/000c5cd2-ebdf-11e8-a96e-0050568ea3cb"
                    }
                },
            },
            "oplocks": True,
            "name": "c$",
            "acls": [
                {
                    "user_or_group": "BUILTIN\\Administrators",
                    "type": "windows",
                    "permission": "full_control",
                }
            ],
            "unix_symlink": "local",
            "home_directory": False,
            "encryption": False,
        }
    ),
    CifsShare(
        {
            "change_notify": False,
            "access_based_enumeration": False,
            "volume": {"name": "vol1", "uuid": "4e06f1bc-1ddc-42e2-abb2-f221c6a2ab2a"},
            "path": "/",
            "_links": {
                "self": {
                    "href": "/api/protocols/cifs/shares/000c5cd2-ebdf-11e8-a96e-0050568ea3cb/ipc%24"
                }
            },
            "svm": {
                "name": "vs1",
                "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/000c5cd2-ebdf-11e8-a96e-0050568ea3cb"
                    }
                },
            },
            "oplocks": False,
            "name": "ipc$",
            "home_directory": False,
            "encryption": False,
        }
    ),
    CifsShare(
        {
            "change_notify": True,
            "access_based_enumeration": False,
            "volume": {"name": "vol1", "uuid": "4e06f1bc-1ddc-42e2-abb2-f221c6a2ab2a"},
            "path": "/",
            "_links": {
                "self": {
                    "href": "/api/protocols/cifs/shares/000c5cd2-ebdf-11e8-a96e-0050568ea3cb/TEST"
                }
            },
            "comment": "HR Department Share",
            "svm": {
                "name": "vs1",
                "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/000c5cd2-ebdf-11e8-a96e-0050568ea3cb"
                    }
                },
            },
            "oplocks": True,
            "name": "TEST",
            "acls": [
                {
                    "user_or_group": "Everyone",
                    "type": "windows",
                    "permission": "full_control",
                },
                {
                    "user_or_group": "root",
                    "type": "unix_user",
                    "permission": "no_access",
                },
            ],
            "unix_symlink": "local",
            "home_directory": False,
            "encryption": False,
        }
    ),
]

```
</div>
</div>

---
### Retrieving all CIFS Shares for all SVMs in the cluster for which the acls are configured for a "root" user
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            CifsShare.get_collection(
                fields="*", return_timeout=15, **{"acls.user_or_group": "root"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    CifsShare(
        {
            "change_notify": True,
            "access_based_enumeration": False,
            "volume": {"name": "vol1", "uuid": "4e06f1bc-1ddc-42e2-abb2-f221c6a2ab2a"},
            "path": "/",
            "comment": "HR Department Share",
            "svm": {"name": "vs1", "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"},
            "oplocks": True,
            "name": "TEST",
            "acls": [
                {
                    "user_or_group": "Everyone",
                    "type": "windows",
                    "permission": "full_control",
                },
                {
                    "user_or_group": "root",
                    "type": "unix_user",
                    "permission": "no_access",
                },
            ],
            "unix_symlink": "local",
            "home_directory": False,
            "encryption": False,
        }
    )
]

```
</div>
</div>

### Retrieving a specific CIFS share configuration for an SVM
The configuration being returned is identified by the UUID of its SVM and the name of the share.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShare(
        name="TEST", **{"svm.uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
CifsShare(
    {
        "change_notify": True,
        "access_based_enumeration": False,
        "volume": {"name": "vol1", "uuid": "4e06f1bc-1ddc-42e2-abb2-f221c6a2ab2a"},
        "path": "/",
        "comment": "HR Department Share",
        "svm": {"name": "vs1", "uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"},
        "oplocks": True,
        "name": "TEST",
        "acls": [
            {
                "user_or_group": "Everyone",
                "type": "windows",
                "permission": "full_control",
            },
            {"user_or_group": "root", "type": "unix_user", "permission": "no_access"},
        ],
        "unix_symlink": "local",
        "home_directory": False,
        "encryption": False,
    }
)

```
</div>
</div>

### Updating a specific CIFS share for an SVM
The CIFS share being modified is identified by the UUID of its SVM and the CIFS share name. The CIFS share ACLs cannot be modified with this API.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShare(
        name="TEST", **{"svm.uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"}
    )
    resource.access_based_enumeration = True
    resource.change_notify = True
    resource.comment = "HR Department Share"
    resource.encryption = False
    resource.oplocks = True
    resource.path = "/"
    resource.unix_symlink = "widelink"
    resource.patch()

```

### Removing a specific CIFS share for an SVM
The CIFS share being removed is identified by the UUID of its SVM and the CIFS share name.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsShare

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = CifsShare(
        name="test", **{"svm.uuid": "000c5cd2-ebdf-11e8-a96e-0050568ea3cb"}
    )
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


__all__ = ["CifsShare", "CifsShareSchema"]
__pdoc__ = {
    "CifsShareSchema.resource": False,
    "CifsShare.cifs_share_show": False,
    "CifsShare.cifs_share_create": False,
    "CifsShare.cifs_share_modify": False,
    "CifsShare.cifs_share_delete": False,
}


class CifsShareSchema(ResourceSchema):
    """The fields of the CifsShare object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the cifs_share. """

    access_based_enumeration = fields.Boolean(
        data_key="access_based_enumeration",
    )
    r""" If enabled, all folders inside this share are visible to a user based on that individual user access right; prevents
the display of folders or other shared resources that the user does not have access to. """

    acls = fields.List(fields.Nested("netapp_ontap.resources.cifs_share_acl.CifsShareAclSchema", unknown=EXCLUDE), data_key="acls")
    r""" The acls field of the cifs_share. """

    change_notify = fields.Boolean(
        data_key="change_notify",
    )
    r""" Specifies whether CIFS clients can request for change notifications for directories on this share. """

    comment = fields.Str(
        data_key="comment",
        validate=len_validation(minimum=1, maximum=256),
    )
    r""" Specify the CIFS share descriptions.

Example: HR Department Share """

    encryption = fields.Boolean(
        data_key="encryption",
    )
    r""" Specifies that SMB encryption must be used when accessing this share. Clients that do not support encryption are not
able to access this share. """

    home_directory = fields.Boolean(
        data_key="home_directory",
    )
    r""" Specifies whether or not the share is a home directory share, where the share and path names are dynamic.
ONTAP home directory functionality automatically offer each user a dynamic share to their home directory without creating an
individual SMB share for each user.
The ONTAP CIFS home directory feature enable us to configure a share that maps to
different directories based on the user that connects to it. Instead of creating a separate shares for each user,
a single share with a home directory parameters can be created.
In a home directory share, ONTAP dynamically generates the share-name and share-path by substituting
%w, %u, and %d variables with the corresponding Windows user name, UNIX user name, and domain name, respectively. """

    name = fields.Str(
        data_key="name",
        validate=len_validation(minimum=1, maximum=80),
    )
    r""" Specifies the name of the CIFS share that you want to create. If this
is a home directory share then the share name includes the pattern as
%w (Windows user name), %u (UNIX user name) and %d (Windows domain name)
variables in any combination with this parameter to generate shares dynamically.


Example: HR_SHARE """

    oplocks = fields.Boolean(
        data_key="oplocks",
    )
    r""" Specify whether opportunistic locks are enabled on this share. "Oplocks" allow clients to lock files and cache content locally,
which can increase performance for file operations. """

    path = fields.Str(
        data_key="path",
        validate=len_validation(minimum=1, maximum=256),
    )
    r""" The fully-qualified pathname in the owning SVM namespace that is shared through this share.
If this is a home directory share then the path should be dynamic by specifying the pattern
%w (Windows user name), %u (UNIX user name), or %d (domain name) variables in any combination.
ONTAP generates the path dynamically for the connected user and this path is appended to each
search path to find the full Home Directory path.


Example: /volume_1/eng_vol/ """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the cifs_share. """

    unix_symlink = fields.Str(
        data_key="unix_symlink",
        validate=enum_validation(['local', 'widelink', 'disable']),
    )
    r""" Controls the access of UNIX symbolic links to CIFS clients.
The supported values are:

    * local - Enables only local symbolic links which is within the same CIFS share.
    * widelink - Enables both local symlinks and widelinks.
    * disable - Disables local symlinks and widelinks.


Valid choices:

* local
* widelink
* disable """

    volume = fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE)
    r""" The volume field of the cifs_share. """

    @property
    def resource(self):
        return CifsShare

    gettable_fields = [
        "links",
        "access_based_enumeration",
        "acls",
        "change_notify",
        "comment",
        "encryption",
        "home_directory",
        "name",
        "oplocks",
        "path",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "unix_symlink",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,access_based_enumeration,acls,change_notify,comment,encryption,home_directory,name,oplocks,path,svm.links,svm.name,svm.uuid,unix_symlink,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "access_based_enumeration",
        "change_notify",
        "comment",
        "encryption",
        "oplocks",
        "path",
        "svm.name",
        "svm.uuid",
        "unix_symlink",
        "volume.name",
        "volume.uuid",
    ]
    """access_based_enumeration,change_notify,comment,encryption,oplocks,path,svm.name,svm.uuid,unix_symlink,volume.name,volume.uuid,"""

    postable_fields = [
        "access_based_enumeration",
        "acls",
        "change_notify",
        "comment",
        "encryption",
        "home_directory",
        "name",
        "oplocks",
        "path",
        "svm.name",
        "svm.uuid",
        "unix_symlink",
        "volume.name",
        "volume.uuid",
    ]
    """access_based_enumeration,acls,change_notify,comment,encryption,home_directory,name,oplocks,path,svm.name,svm.uuid,unix_symlink,volume.name,volume.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in CifsShare.get_collection(fields=field)]
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
            raise NetAppRestError("CifsShare modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class CifsShare(Resource):
    r""" CIFS share is a named access point in a volume. Before users and applications can access data on the CIFS server over SMB,
a CIFS share must be created with sufficient share permission. CIFS shares are tied to the CIFS server on the SVM.
When a CIFS share is created, ONTAP creates a default ACL for the share with Full Control permissions for Everyone. """

    _schema = CifsShareSchema
    _path = "/api/protocols/cifs/shares"
    _keys = ["svm.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves CIFS shares.
### Related ONTAP commands
* `vserver cifs share show`
* `vserver cifs share properties show`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cifs share show")
        def cifs_share_show(
            access_based_enumeration: Choices.define(_get_field_list("access_based_enumeration"), cache_choices=True, inexact=True)=None,
            change_notify: Choices.define(_get_field_list("change_notify"), cache_choices=True, inexact=True)=None,
            comment: Choices.define(_get_field_list("comment"), cache_choices=True, inexact=True)=None,
            encryption: Choices.define(_get_field_list("encryption"), cache_choices=True, inexact=True)=None,
            home_directory: Choices.define(_get_field_list("home_directory"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            oplocks: Choices.define(_get_field_list("oplocks"), cache_choices=True, inexact=True)=None,
            path: Choices.define(_get_field_list("path"), cache_choices=True, inexact=True)=None,
            unix_symlink: Choices.define(_get_field_list("unix_symlink"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["access_based_enumeration", "change_notify", "comment", "encryption", "home_directory", "name", "oplocks", "path", "unix_symlink", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of CifsShare resources

            Args:
                access_based_enumeration: If enabled, all folders inside this share are visible to a user based on that individual user access right; prevents the display of folders or other shared resources that the user does not have access to. 
                change_notify: Specifies whether CIFS clients can request for change notifications for directories on this share.
                comment: Specify the CIFS share descriptions.
                encryption: Specifies that SMB encryption must be used when accessing this share. Clients that do not support encryption are not able to access this share. 
                home_directory: Specifies whether or not the share is a home directory share, where the share and path names are dynamic. ONTAP home directory functionality automatically offer each user a dynamic share to their home directory without creating an individual SMB share for each user. The ONTAP CIFS home directory feature enable us to configure a share that maps to different directories based on the user that connects to it. Instead of creating a separate shares for each user, a single share with a home directory parameters can be created. In a home directory share, ONTAP dynamically generates the share-name and share-path by substituting %w, %u, and %d variables with the corresponding Windows user name, UNIX user name, and domain name, respectively. 
                name: Specifies the name of the CIFS share that you want to create. If this is a home directory share then the share name includes the pattern as %w (Windows user name), %u (UNIX user name) and %d (Windows domain name) variables in any combination with this parameter to generate shares dynamically. 
                oplocks: Specify whether opportunistic locks are enabled on this share. \"Oplocks\" allow clients to lock files and cache content locally, which can increase performance for file operations. 
                path: The fully-qualified pathname in the owning SVM namespace that is shared through this share. If this is a home directory share then the path should be dynamic by specifying the pattern %w (Windows user name), %u (UNIX user name), or %d (domain name) variables in any combination. ONTAP generates the path dynamically for the connected user and this path is appended to each search path to find the full Home Directory path. 
                unix_symlink: Controls the access of UNIX symbolic links to CIFS clients. The supported values are:     * local - Enables only local symbolic links which is within the same CIFS share.     * widelink - Enables both local symlinks and widelinks.     * disable - Disables local symlinks and widelinks. 
            """

            kwargs = {}
            if access_based_enumeration is not None:
                kwargs["access_based_enumeration"] = access_based_enumeration
            if change_notify is not None:
                kwargs["change_notify"] = change_notify
            if comment is not None:
                kwargs["comment"] = comment
            if encryption is not None:
                kwargs["encryption"] = encryption
            if home_directory is not None:
                kwargs["home_directory"] = home_directory
            if name is not None:
                kwargs["name"] = name
            if oplocks is not None:
                kwargs["oplocks"] = oplocks
            if path is not None:
                kwargs["path"] = path
            if unix_symlink is not None:
                kwargs["unix_symlink"] = unix_symlink
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return CifsShare.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves CIFS shares.
### Related ONTAP commands
* `vserver cifs share show`
* `vserver cifs share properties show`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
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
        r"""Updates a CIFS share.
### Related ONTAP commands
* `vserver cifs share modify`
* `vserver cifs share properties add`
* `vserver cifs share properties remove`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
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
        r"""Deletes a CIFS share.
### Related ONTAP commands
* `vserver cifs share delete`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves CIFS shares.
### Related ONTAP commands
* `vserver cifs share show`
* `vserver cifs share properties show`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a CIFS share.
### Related ONTAP commands
* `vserver cifs share show`
* `vserver cifs share properties show`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
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
        r"""Creates a CIFS share.
### Required properties
* `svm.uuid` or `svm.name` - Existing SVM in which to create the CIFS share.
* `name` - Name of the CIFS share.
* `path` - Path in the owning SVM namespace that is shared through this share.
### Recommended optional properties
* `comment` - Optionally choose to add a text comment of up to 256 characters about the CIFS share.
* `acls` - Optionally choose to add share permissions that users and groups have on the CIFS share.
### Default property values
If not specified in POST, the following default property values are assigned:
* `home_directory` - _false_
* `oplocks` - _true_
* `access_based_enumeration` - _false_
* `change_notify` - _true_
* `encryption` - _false_
* `unix_symlink` - _local_
### Related ONTAP commands
* `vserver cifs share create`
* `vserver cifs share properties add`
* `vserver cifs share access-control create`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cifs share create")
        async def cifs_share_create(
            links: dict = None,
            access_based_enumeration: bool = None,
            acls: dict = None,
            change_notify: bool = None,
            comment: str = None,
            encryption: bool = None,
            home_directory: bool = None,
            name: str = None,
            oplocks: bool = None,
            path: str = None,
            svm: dict = None,
            unix_symlink: str = None,
            volume: dict = None,
        ) -> ResourceTable:
            """Create an instance of a CifsShare resource

            Args:
                links: 
                access_based_enumeration: If enabled, all folders inside this share are visible to a user based on that individual user access right; prevents the display of folders or other shared resources that the user does not have access to. 
                acls: 
                change_notify: Specifies whether CIFS clients can request for change notifications for directories on this share.
                comment: Specify the CIFS share descriptions.
                encryption: Specifies that SMB encryption must be used when accessing this share. Clients that do not support encryption are not able to access this share. 
                home_directory: Specifies whether or not the share is a home directory share, where the share and path names are dynamic. ONTAP home directory functionality automatically offer each user a dynamic share to their home directory without creating an individual SMB share for each user. The ONTAP CIFS home directory feature enable us to configure a share that maps to different directories based on the user that connects to it. Instead of creating a separate shares for each user, a single share with a home directory parameters can be created. In a home directory share, ONTAP dynamically generates the share-name and share-path by substituting %w, %u, and %d variables with the corresponding Windows user name, UNIX user name, and domain name, respectively. 
                name: Specifies the name of the CIFS share that you want to create. If this is a home directory share then the share name includes the pattern as %w (Windows user name), %u (UNIX user name) and %d (Windows domain name) variables in any combination with this parameter to generate shares dynamically. 
                oplocks: Specify whether opportunistic locks are enabled on this share. \"Oplocks\" allow clients to lock files and cache content locally, which can increase performance for file operations. 
                path: The fully-qualified pathname in the owning SVM namespace that is shared through this share. If this is a home directory share then the path should be dynamic by specifying the pattern %w (Windows user name), %u (UNIX user name), or %d (domain name) variables in any combination. ONTAP generates the path dynamically for the connected user and this path is appended to each search path to find the full Home Directory path. 
                svm: 
                unix_symlink: Controls the access of UNIX symbolic links to CIFS clients. The supported values are:     * local - Enables only local symbolic links which is within the same CIFS share.     * widelink - Enables both local symlinks and widelinks.     * disable - Disables local symlinks and widelinks. 
                volume: 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if access_based_enumeration is not None:
                kwargs["access_based_enumeration"] = access_based_enumeration
            if acls is not None:
                kwargs["acls"] = acls
            if change_notify is not None:
                kwargs["change_notify"] = change_notify
            if comment is not None:
                kwargs["comment"] = comment
            if encryption is not None:
                kwargs["encryption"] = encryption
            if home_directory is not None:
                kwargs["home_directory"] = home_directory
            if name is not None:
                kwargs["name"] = name
            if oplocks is not None:
                kwargs["oplocks"] = oplocks
            if path is not None:
                kwargs["path"] = path
            if svm is not None:
                kwargs["svm"] = svm
            if unix_symlink is not None:
                kwargs["unix_symlink"] = unix_symlink
            if volume is not None:
                kwargs["volume"] = volume

            resource = CifsShare(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create CifsShare: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a CIFS share.
### Related ONTAP commands
* `vserver cifs share modify`
* `vserver cifs share properties add`
* `vserver cifs share properties remove`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cifs share modify")
        async def cifs_share_modify(
            access_based_enumeration: bool = None,
            query_access_based_enumeration: bool = None,
            change_notify: bool = None,
            query_change_notify: bool = None,
            comment: str = None,
            query_comment: str = None,
            encryption: bool = None,
            query_encryption: bool = None,
            home_directory: bool = None,
            query_home_directory: bool = None,
            name: str = None,
            query_name: str = None,
            oplocks: bool = None,
            query_oplocks: bool = None,
            path: str = None,
            query_path: str = None,
            unix_symlink: str = None,
            query_unix_symlink: str = None,
        ) -> ResourceTable:
            """Modify an instance of a CifsShare resource

            Args:
                access_based_enumeration: If enabled, all folders inside this share are visible to a user based on that individual user access right; prevents the display of folders or other shared resources that the user does not have access to. 
                query_access_based_enumeration: If enabled, all folders inside this share are visible to a user based on that individual user access right; prevents the display of folders or other shared resources that the user does not have access to. 
                change_notify: Specifies whether CIFS clients can request for change notifications for directories on this share.
                query_change_notify: Specifies whether CIFS clients can request for change notifications for directories on this share.
                comment: Specify the CIFS share descriptions.
                query_comment: Specify the CIFS share descriptions.
                encryption: Specifies that SMB encryption must be used when accessing this share. Clients that do not support encryption are not able to access this share. 
                query_encryption: Specifies that SMB encryption must be used when accessing this share. Clients that do not support encryption are not able to access this share. 
                home_directory: Specifies whether or not the share is a home directory share, where the share and path names are dynamic. ONTAP home directory functionality automatically offer each user a dynamic share to their home directory without creating an individual SMB share for each user. The ONTAP CIFS home directory feature enable us to configure a share that maps to different directories based on the user that connects to it. Instead of creating a separate shares for each user, a single share with a home directory parameters can be created. In a home directory share, ONTAP dynamically generates the share-name and share-path by substituting %w, %u, and %d variables with the corresponding Windows user name, UNIX user name, and domain name, respectively. 
                query_home_directory: Specifies whether or not the share is a home directory share, where the share and path names are dynamic. ONTAP home directory functionality automatically offer each user a dynamic share to their home directory without creating an individual SMB share for each user. The ONTAP CIFS home directory feature enable us to configure a share that maps to different directories based on the user that connects to it. Instead of creating a separate shares for each user, a single share with a home directory parameters can be created. In a home directory share, ONTAP dynamically generates the share-name and share-path by substituting %w, %u, and %d variables with the corresponding Windows user name, UNIX user name, and domain name, respectively. 
                name: Specifies the name of the CIFS share that you want to create. If this is a home directory share then the share name includes the pattern as %w (Windows user name), %u (UNIX user name) and %d (Windows domain name) variables in any combination with this parameter to generate shares dynamically. 
                query_name: Specifies the name of the CIFS share that you want to create. If this is a home directory share then the share name includes the pattern as %w (Windows user name), %u (UNIX user name) and %d (Windows domain name) variables in any combination with this parameter to generate shares dynamically. 
                oplocks: Specify whether opportunistic locks are enabled on this share. \"Oplocks\" allow clients to lock files and cache content locally, which can increase performance for file operations. 
                query_oplocks: Specify whether opportunistic locks are enabled on this share. \"Oplocks\" allow clients to lock files and cache content locally, which can increase performance for file operations. 
                path: The fully-qualified pathname in the owning SVM namespace that is shared through this share. If this is a home directory share then the path should be dynamic by specifying the pattern %w (Windows user name), %u (UNIX user name), or %d (domain name) variables in any combination. ONTAP generates the path dynamically for the connected user and this path is appended to each search path to find the full Home Directory path. 
                query_path: The fully-qualified pathname in the owning SVM namespace that is shared through this share. If this is a home directory share then the path should be dynamic by specifying the pattern %w (Windows user name), %u (UNIX user name), or %d (domain name) variables in any combination. ONTAP generates the path dynamically for the connected user and this path is appended to each search path to find the full Home Directory path. 
                unix_symlink: Controls the access of UNIX symbolic links to CIFS clients. The supported values are:     * local - Enables only local symbolic links which is within the same CIFS share.     * widelink - Enables both local symlinks and widelinks.     * disable - Disables local symlinks and widelinks. 
                query_unix_symlink: Controls the access of UNIX symbolic links to CIFS clients. The supported values are:     * local - Enables only local symbolic links which is within the same CIFS share.     * widelink - Enables both local symlinks and widelinks.     * disable - Disables local symlinks and widelinks. 
            """

            kwargs = {}
            changes = {}
            if query_access_based_enumeration is not None:
                kwargs["access_based_enumeration"] = query_access_based_enumeration
            if query_change_notify is not None:
                kwargs["change_notify"] = query_change_notify
            if query_comment is not None:
                kwargs["comment"] = query_comment
            if query_encryption is not None:
                kwargs["encryption"] = query_encryption
            if query_home_directory is not None:
                kwargs["home_directory"] = query_home_directory
            if query_name is not None:
                kwargs["name"] = query_name
            if query_oplocks is not None:
                kwargs["oplocks"] = query_oplocks
            if query_path is not None:
                kwargs["path"] = query_path
            if query_unix_symlink is not None:
                kwargs["unix_symlink"] = query_unix_symlink

            if access_based_enumeration is not None:
                changes["access_based_enumeration"] = access_based_enumeration
            if change_notify is not None:
                changes["change_notify"] = change_notify
            if comment is not None:
                changes["comment"] = comment
            if encryption is not None:
                changes["encryption"] = encryption
            if home_directory is not None:
                changes["home_directory"] = home_directory
            if name is not None:
                changes["name"] = name
            if oplocks is not None:
                changes["oplocks"] = oplocks
            if path is not None:
                changes["path"] = path
            if unix_symlink is not None:
                changes["unix_symlink"] = unix_symlink

            if hasattr(CifsShare, "find"):
                resource = CifsShare.find(
                    **kwargs
                )
            else:
                resource = CifsShare()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify CifsShare: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a CIFS share.
### Related ONTAP commands
* `vserver cifs share delete`
### Learn more
* [`DOC /protocols/cifs/shares`](#docs-NAS-protocols_cifs_shares)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cifs share delete")
        async def cifs_share_delete(
            access_based_enumeration: bool = None,
            change_notify: bool = None,
            comment: str = None,
            encryption: bool = None,
            home_directory: bool = None,
            name: str = None,
            oplocks: bool = None,
            path: str = None,
            unix_symlink: str = None,
        ) -> None:
            """Delete an instance of a CifsShare resource

            Args:
                access_based_enumeration: If enabled, all folders inside this share are visible to a user based on that individual user access right; prevents the display of folders or other shared resources that the user does not have access to. 
                change_notify: Specifies whether CIFS clients can request for change notifications for directories on this share.
                comment: Specify the CIFS share descriptions.
                encryption: Specifies that SMB encryption must be used when accessing this share. Clients that do not support encryption are not able to access this share. 
                home_directory: Specifies whether or not the share is a home directory share, where the share and path names are dynamic. ONTAP home directory functionality automatically offer each user a dynamic share to their home directory without creating an individual SMB share for each user. The ONTAP CIFS home directory feature enable us to configure a share that maps to different directories based on the user that connects to it. Instead of creating a separate shares for each user, a single share with a home directory parameters can be created. In a home directory share, ONTAP dynamically generates the share-name and share-path by substituting %w, %u, and %d variables with the corresponding Windows user name, UNIX user name, and domain name, respectively. 
                name: Specifies the name of the CIFS share that you want to create. If this is a home directory share then the share name includes the pattern as %w (Windows user name), %u (UNIX user name) and %d (Windows domain name) variables in any combination with this parameter to generate shares dynamically. 
                oplocks: Specify whether opportunistic locks are enabled on this share. \"Oplocks\" allow clients to lock files and cache content locally, which can increase performance for file operations. 
                path: The fully-qualified pathname in the owning SVM namespace that is shared through this share. If this is a home directory share then the path should be dynamic by specifying the pattern %w (Windows user name), %u (UNIX user name), or %d (domain name) variables in any combination. ONTAP generates the path dynamically for the connected user and this path is appended to each search path to find the full Home Directory path. 
                unix_symlink: Controls the access of UNIX symbolic links to CIFS clients. The supported values are:     * local - Enables only local symbolic links which is within the same CIFS share.     * widelink - Enables both local symlinks and widelinks.     * disable - Disables local symlinks and widelinks. 
            """

            kwargs = {}
            if access_based_enumeration is not None:
                kwargs["access_based_enumeration"] = access_based_enumeration
            if change_notify is not None:
                kwargs["change_notify"] = change_notify
            if comment is not None:
                kwargs["comment"] = comment
            if encryption is not None:
                kwargs["encryption"] = encryption
            if home_directory is not None:
                kwargs["home_directory"] = home_directory
            if name is not None:
                kwargs["name"] = name
            if oplocks is not None:
                kwargs["oplocks"] = oplocks
            if path is not None:
                kwargs["path"] = path
            if unix_symlink is not None:
                kwargs["unix_symlink"] = unix_symlink

            if hasattr(CifsShare, "find"):
                resource = CifsShare.find(
                    **kwargs
                )
            else:
                resource = CifsShare()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete CifsShare: %s" % err)


