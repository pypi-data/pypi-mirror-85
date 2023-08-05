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


__all__ = ["FileMove", "FileMoveSchema"]
__pdoc__ = {
    "FileMoveSchema.resource": False,
    "FileMove.file_move_show": False,
    "FileMove.file_move_create": False,
    "FileMove.file_move_modify": False,
    "FileMove.file_move_delete": False,
}


class FileMoveSchema(ResourceSchema):
    """The fields of the FileMove object"""

    cutover_time = Size(
        data_key="cutover_time",
    )
    r""" The maximum amount of time (in seconds) that the source can be quiesced before a destination file must be made available for read-write traffic.

Example: 10 """

    files_to_move = fields.List(fields.Nested("netapp_ontap.models.file_move_files_to_move.FileMoveFilesToMoveSchema", unknown=EXCLUDE), data_key="files_to_move")
    r""" A list of source files along with the destination file they are moved to. If the terminal path component of the destination is a directory, then the source file's basename is replicated in that directory. """

    max_throughput = Size(
        data_key="max_throughput",
    )
    r""" The maximum amount of data (in bytes) that can be transferred per second in support of this operation. """

    reference_cutover_time = Size(
        data_key="reference_cutover_time",
    )
    r""" The maximum amount of time (in seconds) that the source reference file can be quiesced before the corresponding destination file must be made available for read-write traffic.

Example: 10 """

    reference_file = fields.Nested("netapp_ontap.models.file_move_reference_file.FileMoveReferenceFileSchema", data_key="reference_file", unknown=EXCLUDE)
    r""" The reference_file field of the file_move. """

    @property
    def resource(self):
        return FileMove

    gettable_fields = [
        "cutover_time",
        "files_to_move",
        "max_throughput",
        "reference_cutover_time",
        "reference_file",
    ]
    """cutover_time,files_to_move,max_throughput,reference_cutover_time,reference_file,"""

    patchable_fields = [
        "cutover_time",
        "files_to_move",
        "max_throughput",
        "reference_cutover_time",
        "reference_file",
    ]
    """cutover_time,files_to_move,max_throughput,reference_cutover_time,reference_file,"""

    postable_fields = [
        "cutover_time",
        "files_to_move",
        "max_throughput",
        "reference_cutover_time",
        "reference_file",
    ]
    """cutover_time,files_to_move,max_throughput,reference_cutover_time,reference_file,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in FileMove.get_collection(fields=field)]
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
            raise NetAppRestError("FileMove modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class FileMove(Resource):
    r""" File move """

    _schema = FileMoveSchema
    _path = "/api/storage/file/move"







    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Starts a file move operation. Only supported on flexible volumes.
## Required properties
* `files_to_move` - List of files with the destination they are to be moved to.
## Default property values
* `cutover_time` - _10_
* `hold_quiescence` - _false_
* `max_throughput` - _0_
* `reference_cutover_time` - _10_
## Related ONTAP commands
* `volume file move start`
## Examples
### Copying two files
The POST request is used to move file(s).
```
# The API:
/api/storage/file/move
# The call:
curl -X POST  "https://<mgmt-ip>/api/storage/file/move" -H "accept: application/hal+json" -d '{"files_to_move":[{"source":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/src_f1"},"destination":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/dst_f1"}}, {"source":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/src_f2"},"destination":{"volume":{"name":"vol_a"},"svm":{"name":"vs0"},"path":"d1/dst_f2"}}]}'
# The response:
{
  "job": {
    "uuid": "b89bc5dd-94a3-11e8-a7a3-0050568edf84",
    "_links": {
       "self": {
         "href": "/api/cluster/jobs/b89bc5dd-94a3-11e8-a7a3-0050568edf84"
       }
     }
   }
}
```
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="file move create")
        async def file_move_create(
            cutover_time: Size = None,
            files_to_move: dict = None,
            max_throughput: Size = None,
            reference_cutover_time: Size = None,
            reference_file: dict = None,
        ) -> ResourceTable:
            """Create an instance of a FileMove resource

            Args:
                cutover_time: The maximum amount of time (in seconds) that the source can be quiesced before a destination file must be made available for read-write traffic.
                files_to_move: A list of source files along with the destination file they are moved to. If the terminal path component of the destination is a directory, then the source file's basename is replicated in that directory.
                max_throughput: The maximum amount of data (in bytes) that can be transferred per second in support of this operation.
                reference_cutover_time: The maximum amount of time (in seconds) that the source reference file can be quiesced before the corresponding destination file must be made available for read-write traffic.
                reference_file: 
            """

            kwargs = {}
            if cutover_time is not None:
                kwargs["cutover_time"] = cutover_time
            if files_to_move is not None:
                kwargs["files_to_move"] = files_to_move
            if max_throughput is not None:
                kwargs["max_throughput"] = max_throughput
            if reference_cutover_time is not None:
                kwargs["reference_cutover_time"] = reference_cutover_time
            if reference_file is not None:
                kwargs["reference_file"] = reference_file

            resource = FileMove(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create FileMove: %s" % err)
            return [resource]




