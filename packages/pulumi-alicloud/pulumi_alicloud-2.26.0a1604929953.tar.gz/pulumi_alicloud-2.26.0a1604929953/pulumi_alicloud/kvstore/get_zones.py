# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'GetZonesResult',
    'AwaitableGetZonesResult',
    'get_zones',
]

@pulumi.output_type
class GetZonesResult:
    """
    A collection of values returned by getZones.
    """
    def __init__(__self__, id=None, ids=None, instance_charge_type=None, multi=None, output_file=None, zones=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if instance_charge_type and not isinstance(instance_charge_type, str):
            raise TypeError("Expected argument 'instance_charge_type' to be a str")
        pulumi.set(__self__, "instance_charge_type", instance_charge_type)
        if multi and not isinstance(multi, bool):
            raise TypeError("Expected argument 'multi' to be a bool")
        pulumi.set(__self__, "multi", multi)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        A list of zone IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="instanceChargeType")
    def instance_charge_type(self) -> Optional[str]:
        return pulumi.get(self, "instance_charge_type")

    @property
    @pulumi.getter
    def multi(self) -> Optional[bool]:
        return pulumi.get(self, "multi")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def zones(self) -> Sequence['outputs.GetZonesZoneResult']:
        """
        A list of availability zones. Each element contains the following attributes:
        """
        return pulumi.get(self, "zones")


class AwaitableGetZonesResult(GetZonesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetZonesResult(
            id=self.id,
            ids=self.ids,
            instance_charge_type=self.instance_charge_type,
            multi=self.multi,
            output_file=self.output_file,
            zones=self.zones)


def get_zones(instance_charge_type: Optional[str] = None,
              multi: Optional[bool] = None,
              output_file: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetZonesResult:
    """
    This data source provides availability zones for KVStore that can be accessed by an Alibaba Cloud account within the region configured in the provider.

    > **NOTE:** Available in v1.73.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    zones_ids = alicloud.kvstore.get_zones()
    # Create an KVStore instance with the first matched zone
    kvstore = alicloud.kvstore.Instance("kvstore", availability_zone=zones_ids.zones[0].id)
    # Other properties...
    ```


    :param str instance_charge_type: Filter the results by a specific instance charge type. Valid values: `PrePaid` and `PostPaid`. Default to `PostPaid`.
    :param bool multi: Indicate whether the zones can be used in a multi AZ configuration. Default to `false`. Multi AZ is usually used to launch KVStore instances.
    """
    __args__ = dict()
    __args__['instanceChargeType'] = instance_charge_type
    __args__['multi'] = multi
    __args__['outputFile'] = output_file
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:kvstore/getZones:getZones', __args__, opts=opts, typ=GetZonesResult).value

    return AwaitableGetZonesResult(
        id=__ret__.id,
        ids=__ret__.ids,
        instance_charge_type=__ret__.instance_charge_type,
        multi=__ret__.multi,
        output_file=__ret__.output_file,
        zones=__ret__.zones)
