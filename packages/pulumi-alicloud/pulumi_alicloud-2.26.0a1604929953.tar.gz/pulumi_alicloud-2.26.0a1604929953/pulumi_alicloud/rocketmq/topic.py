# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['Topic']


class Topic(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 message_type: Optional[pulumi.Input[int]] = None,
                 perm: Optional[pulumi.Input[int]] = None,
                 remark: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 topic: Optional[pulumi.Input[str]] = None,
                 topic_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an ONS topic resource.

        For more information about how to use it, see [RocketMQ Topic Management API](https://www.alibabacloud.com/help/doc-detail/29591.html).

        > **NOTE:** Available in 1.53.0+

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "onsInstanceName"
        topic = config.get("topic")
        if topic is None:
            topic = "onsTopicName"
        default_instance = alicloud.rocketmq.Instance("defaultInstance", remark="default_ons_instance_remark")
        default_topic = alicloud.rocketmq.Topic("defaultTopic",
            topic_name=topic,
            instance_id=default_instance.id,
            message_type=0,
            remark="dafault_ons_topic_remark")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: ID of the ONS Instance that owns the topics.
        :param pulumi.Input[int] message_type: The type of the message. Read [Ons Topic Create](https://www.alibabacloud.com/help/doc-detail/29591.html) for further details.
        :param pulumi.Input[int] perm: This attribute is used to set the read-write mode for the topic. Read [Request parameters](https://www.alibabacloud.com/help/doc-detail/56880.html) for further details.
        :param pulumi.Input[str] remark: This attribute is a concise description of topic. The length cannot exceed 128.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
               - Key: It can be up to 64 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It cannot be a null string.
               - Value: It can be up to 128 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It can be a null string.
        :param pulumi.Input[str] topic: Replaced by `topic_name` after version 1.97.0.
        :param pulumi.Input[str] topic_name: Name of the topic. Two topics on a single instance cannot have the same name and the name cannot start with 'GID' or 'CID'. The length cannot exceed 64 characters.
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

            if instance_id is None:
                raise TypeError("Missing required property 'instance_id'")
            __props__['instance_id'] = instance_id
            if message_type is None:
                raise TypeError("Missing required property 'message_type'")
            __props__['message_type'] = message_type
            __props__['perm'] = perm
            __props__['remark'] = remark
            __props__['tags'] = tags
            if topic is not None:
                warnings.warn("Field 'topic' has been deprecated from version 1.97.0. Use 'topic_name' instead.", DeprecationWarning)
                pulumi.log.warn("topic is deprecated: Field 'topic' has been deprecated from version 1.97.0. Use 'topic_name' instead.")
            __props__['topic'] = topic
            __props__['topic_name'] = topic_name
        super(Topic, __self__).__init__(
            'alicloud:rocketmq/topic:Topic',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            message_type: Optional[pulumi.Input[int]] = None,
            perm: Optional[pulumi.Input[int]] = None,
            remark: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            topic: Optional[pulumi.Input[str]] = None,
            topic_name: Optional[pulumi.Input[str]] = None) -> 'Topic':
        """
        Get an existing Topic resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: ID of the ONS Instance that owns the topics.
        :param pulumi.Input[int] message_type: The type of the message. Read [Ons Topic Create](https://www.alibabacloud.com/help/doc-detail/29591.html) for further details.
        :param pulumi.Input[int] perm: This attribute is used to set the read-write mode for the topic. Read [Request parameters](https://www.alibabacloud.com/help/doc-detail/56880.html) for further details.
        :param pulumi.Input[str] remark: This attribute is a concise description of topic. The length cannot exceed 128.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
               - Key: It can be up to 64 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It cannot be a null string.
               - Value: It can be up to 128 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It can be a null string.
        :param pulumi.Input[str] topic: Replaced by `topic_name` after version 1.97.0.
        :param pulumi.Input[str] topic_name: Name of the topic. Two topics on a single instance cannot have the same name and the name cannot start with 'GID' or 'CID'. The length cannot exceed 64 characters.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["instance_id"] = instance_id
        __props__["message_type"] = message_type
        __props__["perm"] = perm
        __props__["remark"] = remark
        __props__["tags"] = tags
        __props__["topic"] = topic
        __props__["topic_name"] = topic_name
        return Topic(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        ID of the ONS Instance that owns the topics.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="messageType")
    def message_type(self) -> pulumi.Output[int]:
        """
        The type of the message. Read [Ons Topic Create](https://www.alibabacloud.com/help/doc-detail/29591.html) for further details.
        """
        return pulumi.get(self, "message_type")

    @property
    @pulumi.getter
    def perm(self) -> pulumi.Output[Optional[int]]:
        """
        This attribute is used to set the read-write mode for the topic. Read [Request parameters](https://www.alibabacloud.com/help/doc-detail/56880.html) for further details.
        """
        return pulumi.get(self, "perm")

    @property
    @pulumi.getter
    def remark(self) -> pulumi.Output[Optional[str]]:
        """
        This attribute is a concise description of topic. The length cannot exceed 128.
        """
        return pulumi.get(self, "remark")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        - Key: It can be up to 64 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It cannot be a null string.
        - Value: It can be up to 128 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It can be a null string.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def topic(self) -> pulumi.Output[str]:
        """
        Replaced by `topic_name` after version 1.97.0.
        """
        return pulumi.get(self, "topic")

    @property
    @pulumi.getter(name="topicName")
    def topic_name(self) -> pulumi.Output[str]:
        """
        Name of the topic. Two topics on a single instance cannot have the same name and the name cannot start with 'GID' or 'CID'. The length cannot exceed 64 characters.
        """
        return pulumi.get(self, "topic_name")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

