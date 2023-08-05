r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["QosPolicyAdaptive", "QosPolicyAdaptiveSchema"]
__pdoc__ = {
    "QosPolicyAdaptiveSchema.resource": False,
    "QosPolicyAdaptive": False,
}


class QosPolicyAdaptiveSchema(ResourceSchema):
    """The fields of the QosPolicyAdaptive object"""

    absolute_min_iops = Size(data_key="absolute_min_iops")
    r""" Specifies the absolute minimum IOPS that is used as an override when the expected_iops is less than this value. These floors are not guaranteed on non-AFF platforms or when FabricPool tiering policies are set. """

    expected_iops = Size(data_key="expected_iops")
    r""" Expected IOPS. Specifies the minimum expected IOPS per TB allocated based on the storage object allocated size. These floors are not guaranteed on non-AFF platforms or when FabricPool tiering policies are set. """

    peak_iops = Size(data_key="peak_iops")
    r""" Peak IOPS. Specifies the maximum possible IOPS per TB allocated based on the storage object allocated size or the storage object used size. """

    @property
    def resource(self):
        return QosPolicyAdaptive

    gettable_fields = [
        "absolute_min_iops",
        "expected_iops",
        "peak_iops",
    ]
    """absolute_min_iops,expected_iops,peak_iops,"""

    patchable_fields = [
        "absolute_min_iops",
        "expected_iops",
        "peak_iops",
    ]
    """absolute_min_iops,expected_iops,peak_iops,"""

    postable_fields = [
        "absolute_min_iops",
        "expected_iops",
        "peak_iops",
    ]
    """absolute_min_iops,expected_iops,peak_iops,"""


class QosPolicyAdaptive(Resource):

    _schema = QosPolicyAdaptiveSchema
