# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['VbrHealthCheck']


class VbrHealthCheck(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cen_id: Optional[pulumi.Input[str]] = None,
                 health_check_interval: Optional[pulumi.Input[int]] = None,
                 health_check_source_ip: Optional[pulumi.Input[str]] = None,
                 health_check_target_ip: Optional[pulumi.Input[str]] = None,
                 healthy_threshold: Optional[pulumi.Input[int]] = None,
                 vbr_instance_id: Optional[pulumi.Input[str]] = None,
                 vbr_instance_owner_id: Optional[pulumi.Input[int]] = None,
                 vbr_instance_region_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        This topic describes how to configure the health check feature for a Cloud Enterprise Network (CEN) instance.
        After you attach a Virtual Border Router (VBR) to the CEN instance and configure the health check feature, you can monitor the network conditions of the on-premises data center connected to the VBR.

        For information about CEN VBR HealthCheck and how to use it, see [Manage CEN VBR HealthCheck](https://www.alibabacloud.com/help/en/doc-detail/71141.htm).

        > **NOTE:** Available in 1.88.0+

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Create a cen vbr HealrhCheck resource and use it.
        default_instance = alicloud.cen.Instance("defaultInstance", cen_instance_name="test_name")
        default_instance_attachment = alicloud.cen.InstanceAttachment("defaultInstanceAttachment",
            instance_id=default_instance.id,
            child_instance_id="vbr-xxxxx",
            child_instance_type="VBR",
            child_instance_region_id="cn-hangzhou")
        default_vbr_health_check = alicloud.cen.VbrHealthCheck("defaultVbrHealthCheck",
            cen_id=default_instance.id,
            health_check_source_ip="192.168.1.2",
            health_check_target_ip="10.0.0.2",
            vbr_instance_id="vbr-xxxxx",
            vbr_instance_region_id="cn-hangzhou",
            health_check_interval=2,
            healthy_threshold=8,
            opts=ResourceOptions(depends_on=[default_instance_attachment]))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cen_id: The ID of the CEN instance.
        :param pulumi.Input[int] health_check_interval: Specifies the interval at which the health check sends continuous detection packets. Default value: 2. Value range: 2 to 3.
        :param pulumi.Input[str] health_check_source_ip: The source IP address of health checks.
        :param pulumi.Input[str] health_check_target_ip: The destination IP address of health checks.
        :param pulumi.Input[int] healthy_threshold: Specifies the number of probe messages sent by the health check. Default value: 8. Value range: 3 to 8.
        :param pulumi.Input[str] vbr_instance_id: The ID of the VBR.
        :param pulumi.Input[int] vbr_instance_owner_id: The ID of the account to which the VBR belongs.
        :param pulumi.Input[str] vbr_instance_region_id: The ID of the region to which the VBR belongs.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if cen_id is None:
                raise TypeError("Missing required property 'cen_id'")
            __props__['cen_id'] = cen_id
            __props__['health_check_interval'] = health_check_interval
            __props__['health_check_source_ip'] = health_check_source_ip
            if health_check_target_ip is None:
                raise TypeError("Missing required property 'health_check_target_ip'")
            __props__['health_check_target_ip'] = health_check_target_ip
            __props__['healthy_threshold'] = healthy_threshold
            if vbr_instance_id is None:
                raise TypeError("Missing required property 'vbr_instance_id'")
            __props__['vbr_instance_id'] = vbr_instance_id
            __props__['vbr_instance_owner_id'] = vbr_instance_owner_id
            if vbr_instance_region_id is None:
                raise TypeError("Missing required property 'vbr_instance_region_id'")
            __props__['vbr_instance_region_id'] = vbr_instance_region_id
        super(VbrHealthCheck, __self__).__init__(
            'alicloud:cen/vbrHealthCheck:VbrHealthCheck',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cen_id: Optional[pulumi.Input[str]] = None,
            health_check_interval: Optional[pulumi.Input[int]] = None,
            health_check_source_ip: Optional[pulumi.Input[str]] = None,
            health_check_target_ip: Optional[pulumi.Input[str]] = None,
            healthy_threshold: Optional[pulumi.Input[int]] = None,
            vbr_instance_id: Optional[pulumi.Input[str]] = None,
            vbr_instance_owner_id: Optional[pulumi.Input[int]] = None,
            vbr_instance_region_id: Optional[pulumi.Input[str]] = None) -> 'VbrHealthCheck':
        """
        Get an existing VbrHealthCheck resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cen_id: The ID of the CEN instance.
        :param pulumi.Input[int] health_check_interval: Specifies the interval at which the health check sends continuous detection packets. Default value: 2. Value range: 2 to 3.
        :param pulumi.Input[str] health_check_source_ip: The source IP address of health checks.
        :param pulumi.Input[str] health_check_target_ip: The destination IP address of health checks.
        :param pulumi.Input[int] healthy_threshold: Specifies the number of probe messages sent by the health check. Default value: 8. Value range: 3 to 8.
        :param pulumi.Input[str] vbr_instance_id: The ID of the VBR.
        :param pulumi.Input[int] vbr_instance_owner_id: The ID of the account to which the VBR belongs.
        :param pulumi.Input[str] vbr_instance_region_id: The ID of the region to which the VBR belongs.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["cen_id"] = cen_id
        __props__["health_check_interval"] = health_check_interval
        __props__["health_check_source_ip"] = health_check_source_ip
        __props__["health_check_target_ip"] = health_check_target_ip
        __props__["healthy_threshold"] = healthy_threshold
        __props__["vbr_instance_id"] = vbr_instance_id
        __props__["vbr_instance_owner_id"] = vbr_instance_owner_id
        __props__["vbr_instance_region_id"] = vbr_instance_region_id
        return VbrHealthCheck(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cenId")
    def cen_id(self) -> pulumi.Output[str]:
        """
        The ID of the CEN instance.
        """
        return pulumi.get(self, "cen_id")

    @property
    @pulumi.getter(name="healthCheckInterval")
    def health_check_interval(self) -> pulumi.Output[Optional[int]]:
        """
        Specifies the interval at which the health check sends continuous detection packets. Default value: 2. Value range: 2 to 3.
        """
        return pulumi.get(self, "health_check_interval")

    @property
    @pulumi.getter(name="healthCheckSourceIp")
    def health_check_source_ip(self) -> pulumi.Output[Optional[str]]:
        """
        The source IP address of health checks.
        """
        return pulumi.get(self, "health_check_source_ip")

    @property
    @pulumi.getter(name="healthCheckTargetIp")
    def health_check_target_ip(self) -> pulumi.Output[str]:
        """
        The destination IP address of health checks.
        """
        return pulumi.get(self, "health_check_target_ip")

    @property
    @pulumi.getter(name="healthyThreshold")
    def healthy_threshold(self) -> pulumi.Output[Optional[int]]:
        """
        Specifies the number of probe messages sent by the health check. Default value: 8. Value range: 3 to 8.
        """
        return pulumi.get(self, "healthy_threshold")

    @property
    @pulumi.getter(name="vbrInstanceId")
    def vbr_instance_id(self) -> pulumi.Output[str]:
        """
        The ID of the VBR.
        """
        return pulumi.get(self, "vbr_instance_id")

    @property
    @pulumi.getter(name="vbrInstanceOwnerId")
    def vbr_instance_owner_id(self) -> pulumi.Output[Optional[int]]:
        """
        The ID of the account to which the VBR belongs.
        """
        return pulumi.get(self, "vbr_instance_owner_id")

    @property
    @pulumi.getter(name="vbrInstanceRegionId")
    def vbr_instance_region_id(self) -> pulumi.Output[str]:
        """
        The ID of the region to which the VBR belongs.
        """
        return pulumi.get(self, "vbr_instance_region_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

