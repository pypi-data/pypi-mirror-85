r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["VolumeEfficiency", "VolumeEfficiencySchema"]
__pdoc__ = {
    "VolumeEfficiencySchema.resource": False,
    "VolumeEfficiency": False,
}


class VolumeEfficiencySchema(ResourceSchema):
    """The fields of the VolumeEfficiency object"""

    application_io_size = fields.Str(data_key="application_io_size")
    r""" Block size to use by compression. Valid for POST.

Valid choices:

* 8k
* auto """

    compaction = fields.Str(data_key="compaction")
    r""" The system can be enabled/disabled compaction.<br>inline &dash; Data will be compacted first and written to the volume.<br>none &dash; None<br>mixed &dash; Read only field for FlexGroups, where some of the constituent volumes are compaction enabled and some are disabled.

Valid choices:

* inline
* none
* mixed """

    compression = fields.Str(data_key="compression")
    r""" The system can be enabled/disabled compression.<br>inline &dash; Data will be compressed first and written to the volume.<br>background &dash; Data will be written to the volume and compressed later.<br>both &dash; Inline compression compresses the data and write to the volume, background compression compresses only the blocks on which inline compression is not run.<br>none &dash; None<br>mixed &dash; Read only field for FlexGroups, where some of the constituent volumes are compression enabled and some are disabled.

Valid choices:

* inline
* background
* both
* none
* mixed """

    cross_volume_dedupe = fields.Str(data_key="cross_volume_dedupe")
    r""" The system can be enabled/disabled cross volume dedupe. it can be enabled only when dedupe is enabled.<br>inline &dash; Data will be cross volume deduped first and written to the volume.<br>background &dash; Data will be written to the volume and cross volume deduped later.<br>both &dash; Inline cross volume dedupe dedupes the data and write to the volume, background cross volume dedupe dedupes only the blocks on which inline dedupe is not run.<br>none &dash; None<br>mixed &dash; Read only field for FlexGroups, where some of the constituent volumes are cross volume dedupe enabled and some are disabled.

Valid choices:

* inline
* background
* both
* none
* mixed """

    dedupe = fields.Str(data_key="dedupe")
    r""" The system can be enabled/disabled dedupe.<br>inline &dash; Data will be deduped first and written to the volume.<br>background &dash; Data will be written to the volume and deduped later.<br>both &dash; Inline dedupe dedupes the data and write to the volume, background dedupe dedupes only the blocks on which inline dedupe is not run.<br>none &dash; None<br>mixed &dash; Read only field for FlexGroups, where some of the constituent volumes are dedupe enabled and some are disabled.

Valid choices:

* inline
* background
* both
* none
* mixed """

    policy = fields.Nested("netapp_ontap.models.volume_efficiency_policy1.VolumeEfficiencyPolicy1Schema", unknown=EXCLUDE, data_key="policy")
    r""" The policy field of the volume_efficiency. """

    schedule = fields.Str(data_key="schedule")
    r""" Schedule associated with volume. """

    @property
    def resource(self):
        return VolumeEfficiency

    gettable_fields = [
        "application_io_size",
        "compaction",
        "compression",
        "cross_volume_dedupe",
        "dedupe",
        "policy",
        "schedule",
    ]
    """application_io_size,compaction,compression,cross_volume_dedupe,dedupe,policy,schedule,"""

    patchable_fields = [
        "application_io_size",
        "compaction",
        "compression",
        "cross_volume_dedupe",
        "dedupe",
        "policy",
    ]
    """application_io_size,compaction,compression,cross_volume_dedupe,dedupe,policy,"""

    postable_fields = [
        "application_io_size",
        "compaction",
        "compression",
        "cross_volume_dedupe",
        "dedupe",
        "policy",
    ]
    """application_io_size,compaction,compression,cross_volume_dedupe,dedupe,policy,"""


class VolumeEfficiency(Resource):

    _schema = VolumeEfficiencySchema
