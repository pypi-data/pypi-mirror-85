r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


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


__all__ = ["FileClone", "FileCloneSchema"]
__pdoc__ = {
    "FileCloneSchema.resource": False,
    "FileClone.file_clone_show": False,
    "FileClone.file_clone_create": False,
    "FileClone.file_clone_modify": False,
    "FileClone.file_clone_delete": False,
}


class FileCloneSchema(ResourceSchema):
    """The fields of the FileClone object"""

    autodelete = fields.Boolean(
        data_key="autodelete",
    )
    r""" Mark clone file for auto deletion. """

    destination_path = fields.Str(
        data_key="destination_path",
    )
    r""" Relative path of the clone/destination file in the volume.

Example: dest_file1, dir1/dest_file2 """

    is_backup = fields.Boolean(
        data_key="is_backup",
    )
    r""" Mark clone file for backup. """

    overwrite_destination = fields.Boolean(
        data_key="overwrite_destination",
    )
    r""" Destination file gets overwritten. """

    range = fields.List(fields.Str, data_key="range")
    r""" List of block ranges for sub-file cloning in the format "source-file-block-number:destination-file-block-number:block-count"

Example: [36605,73210] """

    source_path = fields.Str(
        data_key="source_path",
    )
    r""" Relative path of the source file in the volume.

Example: src_file1, dir1/src_file2, ./.snapshot/snap1/src_file3 """

    volume = fields.Nested("netapp_ontap.resources.volume.VolumeSchema", data_key="volume", unknown=EXCLUDE)
    r""" The volume field of the file_clone. """

    @property
    def resource(self):
        return FileClone

    gettable_fields = [
        "autodelete",
        "destination_path",
        "is_backup",
        "overwrite_destination",
        "range",
        "source_path",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """autodelete,destination_path,is_backup,overwrite_destination,range,source_path,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "autodelete",
        "destination_path",
        "is_backup",
        "overwrite_destination",
        "range",
        "source_path",
        "volume.name",
        "volume.uuid",
    ]
    """autodelete,destination_path,is_backup,overwrite_destination,range,source_path,volume.name,volume.uuid,"""

    postable_fields = [
        "autodelete",
        "destination_path",
        "is_backup",
        "overwrite_destination",
        "range",
        "source_path",
        "volume.name",
        "volume.uuid",
    ]
    """autodelete,destination_path,is_backup,overwrite_destination,range,source_path,volume.name,volume.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in FileClone.get_collection(fields=field)]
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
            raise NetAppRestError("FileClone modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class FileClone(Resource):
    r""" File clone """

    _schema = FileCloneSchema
    _path = "/api/storage/file/clone"







    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a clone of the file."""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="file clone create")
        async def file_clone_create(
            autodelete: bool = None,
            destination_path: str = None,
            is_backup: bool = None,
            overwrite_destination: bool = None,
            range = None,
            source_path: str = None,
            volume: dict = None,
        ) -> ResourceTable:
            """Create an instance of a FileClone resource

            Args:
                autodelete: Mark clone file for auto deletion.
                destination_path: Relative path of the clone/destination file in the volume.
                is_backup: Mark clone file for backup.
                overwrite_destination: Destination file gets overwritten.
                range: List of block ranges for sub-file cloning in the format \"source-file-block-number:destination-file-block-number:block-count\"
                source_path: Relative path of the source file in the volume.
                volume: 
            """

            kwargs = {}
            if autodelete is not None:
                kwargs["autodelete"] = autodelete
            if destination_path is not None:
                kwargs["destination_path"] = destination_path
            if is_backup is not None:
                kwargs["is_backup"] = is_backup
            if overwrite_destination is not None:
                kwargs["overwrite_destination"] = overwrite_destination
            if range is not None:
                kwargs["range"] = range
            if source_path is not None:
                kwargs["source_path"] = source_path
            if volume is not None:
                kwargs["volume"] = volume

            resource = FileClone(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create FileClone: %s" % err)
            return [resource]




