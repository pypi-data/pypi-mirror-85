# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'ScalingConfigurationDataDiskArgs',
    'ScalingGroupVServerGroupsVserverGroupArgs',
    'ScalingGroupVServerGroupsVserverGroupVserverAttributeArgs',
    'ScalingRuleStepAdjustmentArgs',
]

@pulumi.input_type
class ScalingConfigurationDataDiskArgs:
    def __init__(__self__, *,
                 auto_snapshot_policy_id: Optional[pulumi.Input[str]] = None,
                 category: Optional[pulumi.Input[str]] = None,
                 delete_with_instance: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 device: Optional[pulumi.Input[str]] = None,
                 encrypted: Optional[pulumi.Input[bool]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[int]] = None,
                 snapshot_id: Optional[pulumi.Input[str]] = None):
        if auto_snapshot_policy_id is not None:
            pulumi.set(__self__, "auto_snapshot_policy_id", auto_snapshot_policy_id)
        if category is not None:
            pulumi.set(__self__, "category", category)
        if delete_with_instance is not None:
            pulumi.set(__self__, "delete_with_instance", delete_with_instance)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if device is not None:
            warnings.warn("Attribute device has been deprecated on disk attachment resource. Suggest to remove it from your template.", DeprecationWarning)
            pulumi.log.warn("device is deprecated: Attribute device has been deprecated on disk attachment resource. Suggest to remove it from your template.")
        if device is not None:
            pulumi.set(__self__, "device", device)
        if encrypted is not None:
            pulumi.set(__self__, "encrypted", encrypted)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if snapshot_id is not None:
            pulumi.set(__self__, "snapshot_id", snapshot_id)

    @property
    @pulumi.getter(name="autoSnapshotPolicyId")
    def auto_snapshot_policy_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "auto_snapshot_policy_id")

    @auto_snapshot_policy_id.setter
    def auto_snapshot_policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auto_snapshot_policy_id", value)

    @property
    @pulumi.getter
    def category(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "category")

    @category.setter
    def category(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "category", value)

    @property
    @pulumi.getter(name="deleteWithInstance")
    def delete_with_instance(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "delete_with_instance")

    @delete_with_instance.setter
    def delete_with_instance(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "delete_with_instance", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def device(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "device")

    @device.setter
    def device(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "device", value)

    @property
    @pulumi.getter
    def encrypted(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encrypted", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "snapshot_id")

    @snapshot_id.setter
    def snapshot_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "snapshot_id", value)


@pulumi.input_type
class ScalingGroupVServerGroupsVserverGroupArgs:
    def __init__(__self__, *,
                 loadbalancer_id: pulumi.Input[str],
                 vserver_attributes: pulumi.Input[Sequence[pulumi.Input['ScalingGroupVServerGroupsVserverGroupVserverAttributeArgs']]]):
        pulumi.set(__self__, "loadbalancer_id", loadbalancer_id)
        pulumi.set(__self__, "vserver_attributes", vserver_attributes)

    @property
    @pulumi.getter(name="loadbalancerId")
    def loadbalancer_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "loadbalancer_id")

    @loadbalancer_id.setter
    def loadbalancer_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "loadbalancer_id", value)

    @property
    @pulumi.getter(name="vserverAttributes")
    def vserver_attributes(self) -> pulumi.Input[Sequence[pulumi.Input['ScalingGroupVServerGroupsVserverGroupVserverAttributeArgs']]]:
        return pulumi.get(self, "vserver_attributes")

    @vserver_attributes.setter
    def vserver_attributes(self, value: pulumi.Input[Sequence[pulumi.Input['ScalingGroupVServerGroupsVserverGroupVserverAttributeArgs']]]):
        pulumi.set(self, "vserver_attributes", value)


@pulumi.input_type
class ScalingGroupVServerGroupsVserverGroupVserverAttributeArgs:
    def __init__(__self__, *,
                 port: pulumi.Input[int],
                 vserver_group_id: pulumi.Input[str],
                 weight: pulumi.Input[int]):
        pulumi.set(__self__, "port", port)
        pulumi.set(__self__, "vserver_group_id", vserver_group_id)
        pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter
    def port(self) -> pulumi.Input[int]:
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: pulumi.Input[int]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="vserverGroupId")
    def vserver_group_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "vserver_group_id")

    @vserver_group_id.setter
    def vserver_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vserver_group_id", value)

    @property
    @pulumi.getter
    def weight(self) -> pulumi.Input[int]:
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: pulumi.Input[int]):
        pulumi.set(self, "weight", value)


@pulumi.input_type
class ScalingRuleStepAdjustmentArgs:
    def __init__(__self__, *,
                 metric_interval_lower_bound: Optional[pulumi.Input[str]] = None,
                 metric_interval_upper_bound: Optional[pulumi.Input[str]] = None,
                 scaling_adjustment: Optional[pulumi.Input[int]] = None):
        if metric_interval_lower_bound is not None:
            pulumi.set(__self__, "metric_interval_lower_bound", metric_interval_lower_bound)
        if metric_interval_upper_bound is not None:
            pulumi.set(__self__, "metric_interval_upper_bound", metric_interval_upper_bound)
        if scaling_adjustment is not None:
            pulumi.set(__self__, "scaling_adjustment", scaling_adjustment)

    @property
    @pulumi.getter(name="metricIntervalLowerBound")
    def metric_interval_lower_bound(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "metric_interval_lower_bound")

    @metric_interval_lower_bound.setter
    def metric_interval_lower_bound(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_interval_lower_bound", value)

    @property
    @pulumi.getter(name="metricIntervalUpperBound")
    def metric_interval_upper_bound(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "metric_interval_upper_bound")

    @metric_interval_upper_bound.setter
    def metric_interval_upper_bound(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_interval_upper_bound", value)

    @property
    @pulumi.getter(name="scalingAdjustment")
    def scaling_adjustment(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "scaling_adjustment")

    @scaling_adjustment.setter
    def scaling_adjustment(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "scaling_adjustment", value)


