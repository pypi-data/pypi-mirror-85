# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['Instance']


class Instance(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 deploy_type: Optional[pulumi.Input[int]] = None,
                 disk_size: Optional[pulumi.Input[int]] = None,
                 disk_type: Optional[pulumi.Input[int]] = None,
                 eip_max: Optional[pulumi.Input[int]] = None,
                 io_max: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 paid_type: Optional[pulumi.Input[str]] = None,
                 security_group: Optional[pulumi.Input[str]] = None,
                 spec_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 topic_quota: Optional[pulumi.Input[int]] = None,
                 vswitch_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an ALIKAFKA instance resource.

        > **NOTE:** Available in 1.59.0+

        > **NOTE:** Creation or modification may took about 10-40 minutes.

        > **NOTE:** Only the following regions support create alikafka pre paid instance.
        [`cn-hangzhou`,`cn-beijing`,`cn-shenzhen`,`cn-shanghai`,`cn-qingdao`,`cn-hongkong`,`cn-huhehaote`,`cn-zhangjiakou`,`cn-chengdu`,`cn-heyuan`,`ap-southeast-1`,`ap-southeast-3`,`ap-southeast-5`,`ap-south-1`,`ap-northeast-1`,`eu-central-1`,`eu-west-1`,`us-west-1`,`us-east-1`]

        > **NOTE:** Only the following regions support create alikafka post paid instance(International account is not support to buy post paid instance currently).
        [`cn-hangzhou`,`cn-beijing`,`cn-shenzhen`,`cn-shanghai`,`cn-qingdao`,`cn-hongkong`,`cn-huhehaote`,`cn-zhangjiakou`,`cn-chengdu`,`cn-heyuan`,`ap-southeast-1`,`ap-southeast-3`,`ap-northeast-1`,`eu-central-1`,`eu-west-1`,`us-west-1`,`us-east-1`]
        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        instance_name = config.get("instanceName")
        if instance_name is None:
            instance_name = "alikafkaInstanceName"
        default_zones = alicloud.get_zones(available_resource_creation="VSwitch")
        default_network = alicloud.vpc.Network("defaultNetwork", cidr_block="172.16.0.0/12")
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=default_network.id,
            cidr_block="172.16.0.0/24",
            availability_zone=default_zones.zones[0].id)
        default_instance = alicloud.alikafka.Instance("defaultInstance",
            topic_quota=50,
            disk_type=1,
            disk_size=500,
            deploy_type=4,
            io_max=20,
            vswitch_id=default_switch.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] deploy_type: The deploy type of the instance. Currently only support two deploy type, 4: eip/vpc instance, 5: vpc instance.
        :param pulumi.Input[int] disk_size: The disk size of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[int] disk_type: The disk type of the instance. 0: efficient cloud disk , 1: SSD.
        :param pulumi.Input[int] eip_max: The max bandwidth of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[int] io_max: The max value of io of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[str] name: Name of your Kafka instance. The length should between 3 and 64 characters. If not set, will use instance id as instance name.
        :param pulumi.Input[str] paid_type: The paid type of the instance. Support two type, "PrePaid": pre paid type instance, "PostPaid": post paid type instance. Default is PostPaid. When modify this value, it only support adjust from post pay to pre pay.
        :param pulumi.Input[str] security_group: （Optional, ForceNew, Available in v1.93.0+） The ID of security group for this instance. If the security group is empty, system will create a default one.
        :param pulumi.Input[str] spec_type: The spec type of the instance. Support two type, "normal": normal version instance, "professional": professional version instance. Default is normal. When modify this value, it only support adjust from normal to professional. Note only pre paid type instance support professional specific type.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[int] topic_quota: The max num of topic can be create of the instance. When modify this value, it only adjust to a greater value.
        :param pulumi.Input[str] vswitch_id: The ID of attaching vswitch to instance.
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

            if deploy_type is None:
                raise TypeError("Missing required property 'deploy_type'")
            __props__['deploy_type'] = deploy_type
            if disk_size is None:
                raise TypeError("Missing required property 'disk_size'")
            __props__['disk_size'] = disk_size
            if disk_type is None:
                raise TypeError("Missing required property 'disk_type'")
            __props__['disk_type'] = disk_type
            __props__['eip_max'] = eip_max
            if io_max is None:
                raise TypeError("Missing required property 'io_max'")
            __props__['io_max'] = io_max
            __props__['name'] = name
            __props__['paid_type'] = paid_type
            __props__['security_group'] = security_group
            __props__['spec_type'] = spec_type
            __props__['tags'] = tags
            if topic_quota is None:
                raise TypeError("Missing required property 'topic_quota'")
            __props__['topic_quota'] = topic_quota
            if vswitch_id is None:
                raise TypeError("Missing required property 'vswitch_id'")
            __props__['vswitch_id'] = vswitch_id
            __props__['end_point'] = None
            __props__['vpc_id'] = None
            __props__['zone_id'] = None
        super(Instance, __self__).__init__(
            'alicloud:alikafka/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            deploy_type: Optional[pulumi.Input[int]] = None,
            disk_size: Optional[pulumi.Input[int]] = None,
            disk_type: Optional[pulumi.Input[int]] = None,
            eip_max: Optional[pulumi.Input[int]] = None,
            end_point: Optional[pulumi.Input[str]] = None,
            io_max: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            paid_type: Optional[pulumi.Input[str]] = None,
            security_group: Optional[pulumi.Input[str]] = None,
            spec_type: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            topic_quota: Optional[pulumi.Input[int]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None,
            vswitch_id: Optional[pulumi.Input[str]] = None,
            zone_id: Optional[pulumi.Input[str]] = None) -> 'Instance':
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] deploy_type: The deploy type of the instance. Currently only support two deploy type, 4: eip/vpc instance, 5: vpc instance.
        :param pulumi.Input[int] disk_size: The disk size of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[int] disk_type: The disk type of the instance. 0: efficient cloud disk , 1: SSD.
        :param pulumi.Input[int] eip_max: The max bandwidth of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[str] end_point: The EndPoint to access the kafka instance.
        :param pulumi.Input[int] io_max: The max value of io of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[str] name: Name of your Kafka instance. The length should between 3 and 64 characters. If not set, will use instance id as instance name.
        :param pulumi.Input[str] paid_type: The paid type of the instance. Support two type, "PrePaid": pre paid type instance, "PostPaid": post paid type instance. Default is PostPaid. When modify this value, it only support adjust from post pay to pre pay.
        :param pulumi.Input[str] security_group: （Optional, ForceNew, Available in v1.93.0+） The ID of security group for this instance. If the security group is empty, system will create a default one.
        :param pulumi.Input[str] spec_type: The spec type of the instance. Support two type, "normal": normal version instance, "professional": professional version instance. Default is normal. When modify this value, it only support adjust from normal to professional. Note only pre paid type instance support professional specific type.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[int] topic_quota: The max num of topic can be create of the instance. When modify this value, it only adjust to a greater value.
        :param pulumi.Input[str] vpc_id: The ID of attaching VPC to instance.
        :param pulumi.Input[str] vswitch_id: The ID of attaching vswitch to instance.
        :param pulumi.Input[str] zone_id: The Zone to launch the kafka instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["deploy_type"] = deploy_type
        __props__["disk_size"] = disk_size
        __props__["disk_type"] = disk_type
        __props__["eip_max"] = eip_max
        __props__["end_point"] = end_point
        __props__["io_max"] = io_max
        __props__["name"] = name
        __props__["paid_type"] = paid_type
        __props__["security_group"] = security_group
        __props__["spec_type"] = spec_type
        __props__["tags"] = tags
        __props__["topic_quota"] = topic_quota
        __props__["vpc_id"] = vpc_id
        __props__["vswitch_id"] = vswitch_id
        __props__["zone_id"] = zone_id
        return Instance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deployType")
    def deploy_type(self) -> pulumi.Output[int]:
        """
        The deploy type of the instance. Currently only support two deploy type, 4: eip/vpc instance, 5: vpc instance.
        """
        return pulumi.get(self, "deploy_type")

    @property
    @pulumi.getter(name="diskSize")
    def disk_size(self) -> pulumi.Output[int]:
        """
        The disk size of the instance. When modify this value, it only support adjust to a greater value.
        """
        return pulumi.get(self, "disk_size")

    @property
    @pulumi.getter(name="diskType")
    def disk_type(self) -> pulumi.Output[int]:
        """
        The disk type of the instance. 0: efficient cloud disk , 1: SSD.
        """
        return pulumi.get(self, "disk_type")

    @property
    @pulumi.getter(name="eipMax")
    def eip_max(self) -> pulumi.Output[Optional[int]]:
        """
        The max bandwidth of the instance. When modify this value, it only support adjust to a greater value.
        """
        return pulumi.get(self, "eip_max")

    @property
    @pulumi.getter(name="endPoint")
    def end_point(self) -> pulumi.Output[str]:
        """
        The EndPoint to access the kafka instance.
        """
        return pulumi.get(self, "end_point")

    @property
    @pulumi.getter(name="ioMax")
    def io_max(self) -> pulumi.Output[int]:
        """
        The max value of io of the instance. When modify this value, it only support adjust to a greater value.
        """
        return pulumi.get(self, "io_max")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of your Kafka instance. The length should between 3 and 64 characters. If not set, will use instance id as instance name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="paidType")
    def paid_type(self) -> pulumi.Output[Optional[str]]:
        """
        The paid type of the instance. Support two type, "PrePaid": pre paid type instance, "PostPaid": post paid type instance. Default is PostPaid. When modify this value, it only support adjust from post pay to pre pay.
        """
        return pulumi.get(self, "paid_type")

    @property
    @pulumi.getter(name="securityGroup")
    def security_group(self) -> pulumi.Output[Optional[str]]:
        """
        （Optional, ForceNew, Available in v1.93.0+） The ID of security group for this instance. If the security group is empty, system will create a default one.
        """
        return pulumi.get(self, "security_group")

    @property
    @pulumi.getter(name="specType")
    def spec_type(self) -> pulumi.Output[Optional[str]]:
        """
        The spec type of the instance. Support two type, "normal": normal version instance, "professional": professional version instance. Default is normal. When modify this value, it only support adjust from normal to professional. Note only pre paid type instance support professional specific type.
        """
        return pulumi.get(self, "spec_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="topicQuota")
    def topic_quota(self) -> pulumi.Output[int]:
        """
        The max num of topic can be create of the instance. When modify this value, it only adjust to a greater value.
        """
        return pulumi.get(self, "topic_quota")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The ID of attaching VPC to instance.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> pulumi.Output[str]:
        """
        The ID of attaching vswitch to instance.
        """
        return pulumi.get(self, "vswitch_id")

    @property
    @pulumi.getter(name="zoneId")
    def zone_id(self) -> pulumi.Output[str]:
        """
        The Zone to launch the kafka instance.
        """
        return pulumi.get(self, "zone_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

