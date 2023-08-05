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
    'GetConfigurationRecordersRecorderResult',
    'GetDeliveryChannelsChannelResult',
    'GetRulesRuleResult',
    'GetRulesRuleSourceDetailResult',
]

@pulumi.output_type
class GetConfigurationRecordersRecorderResult(dict):
    def __init__(__self__, *,
                 account_id: str,
                 id: str,
                 organization_enable_status: str,
                 organization_master_id: int,
                 resource_types: Sequence[str],
                 status: str):
        """
        :param str id: The ID of the Config Configuration Recorder. Value as the `account_id`.
               * `account_id`- The ID of the Alicloud account.
        :param str organization_enable_status: Status of resource monitoring.
        :param int organization_master_id: The ID of the Enterprise management account.
        :param Sequence[str] resource_types: A list of resource types to be monitored.
        :param str status: Enterprise version configuration audit enabled status.
        """
        pulumi.set(__self__, "account_id", account_id)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "organization_enable_status", organization_enable_status)
        pulumi.set(__self__, "organization_master_id", organization_master_id)
        pulumi.set(__self__, "resource_types", resource_types)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> str:
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the Config Configuration Recorder. Value as the `account_id`.
        * `account_id`- The ID of the Alicloud account.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="organizationEnableStatus")
    def organization_enable_status(self) -> str:
        """
        Status of resource monitoring.
        """
        return pulumi.get(self, "organization_enable_status")

    @property
    @pulumi.getter(name="organizationMasterId")
    def organization_master_id(self) -> int:
        """
        The ID of the Enterprise management account.
        """
        return pulumi.get(self, "organization_master_id")

    @property
    @pulumi.getter(name="resourceTypes")
    def resource_types(self) -> Sequence[str]:
        """
        A list of resource types to be monitored.
        """
        return pulumi.get(self, "resource_types")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Enterprise version configuration audit enabled status.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class GetDeliveryChannelsChannelResult(dict):
    def __init__(__self__, *,
                 delivery_channel_assume_role_arn: str,
                 delivery_channel_condition: str,
                 delivery_channel_id: str,
                 delivery_channel_name: str,
                 delivery_channel_target_arn: str,
                 delivery_channel_type: str,
                 description: str,
                 id: str,
                 status: int):
        """
        :param str delivery_channel_assume_role_arn: The Alibaba Cloud Resource Name (ARN) of the role assumed by delivery method.
        :param str delivery_channel_condition: The rule attached to the delivery method. This parameter is applicable only to delivery methods of the Message Service (MNS) type.
        :param str delivery_channel_id: The ID of the delivery channel.
        :param str delivery_channel_name: The name of the delivery channel.
        :param str delivery_channel_target_arn: The ARN of the delivery destination.
        :param str delivery_channel_type: The type of the delivery method.
        :param str description: The description of the delivery method.
        :param str id: The ID of the Config Delivery Channel.
        :param int status: The status of the config delivery channel. Valid values `0`: Disable delivery channel, `1`: Enable delivery channel.
        """
        pulumi.set(__self__, "delivery_channel_assume_role_arn", delivery_channel_assume_role_arn)
        pulumi.set(__self__, "delivery_channel_condition", delivery_channel_condition)
        pulumi.set(__self__, "delivery_channel_id", delivery_channel_id)
        pulumi.set(__self__, "delivery_channel_name", delivery_channel_name)
        pulumi.set(__self__, "delivery_channel_target_arn", delivery_channel_target_arn)
        pulumi.set(__self__, "delivery_channel_type", delivery_channel_type)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="deliveryChannelAssumeRoleArn")
    def delivery_channel_assume_role_arn(self) -> str:
        """
        The Alibaba Cloud Resource Name (ARN) of the role assumed by delivery method.
        """
        return pulumi.get(self, "delivery_channel_assume_role_arn")

    @property
    @pulumi.getter(name="deliveryChannelCondition")
    def delivery_channel_condition(self) -> str:
        """
        The rule attached to the delivery method. This parameter is applicable only to delivery methods of the Message Service (MNS) type.
        """
        return pulumi.get(self, "delivery_channel_condition")

    @property
    @pulumi.getter(name="deliveryChannelId")
    def delivery_channel_id(self) -> str:
        """
        The ID of the delivery channel.
        """
        return pulumi.get(self, "delivery_channel_id")

    @property
    @pulumi.getter(name="deliveryChannelName")
    def delivery_channel_name(self) -> str:
        """
        The name of the delivery channel.
        """
        return pulumi.get(self, "delivery_channel_name")

    @property
    @pulumi.getter(name="deliveryChannelTargetArn")
    def delivery_channel_target_arn(self) -> str:
        """
        The ARN of the delivery destination.
        """
        return pulumi.get(self, "delivery_channel_target_arn")

    @property
    @pulumi.getter(name="deliveryChannelType")
    def delivery_channel_type(self) -> str:
        """
        The type of the delivery method.
        """
        return pulumi.get(self, "delivery_channel_type")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the delivery method.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the Config Delivery Channel.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def status(self) -> int:
        """
        The status of the config delivery channel. Valid values `0`: Disable delivery channel, `1`: Enable delivery channel.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class GetRulesRuleResult(dict):
    def __init__(__self__, *,
                 account_id: int,
                 config_rule_arn: str,
                 config_rule_id: str,
                 config_rule_state: str,
                 create_timestamp: int,
                 description: str,
                 id: str,
                 input_parameters: Mapping[str, Any],
                 modified_timestamp: int,
                 risk_level: int,
                 rule_name: str,
                 source_details: Sequence['outputs.GetRulesRuleSourceDetailResult'],
                 source_identifier: str,
                 source_owner: str):
        """
        :param str config_rule_state: The state of the config rule, valid values: `ACTIVE`, `DELETING`, `DELETING_RESULTS`, `EVALUATING` and `INACTIVE`.
        :param str id: The ID of the Config Rule.
               * `account_id`- The ID of the Alicloud account.
               * `config_rule_arn`- The ARN of the Config Rule.
               * `config_rule_id`- The ID of the Config Rule.
               * `config_rule_state`- The state of the Config Rule.
               * `create_timestamp`- The timestamp of the Config Rule created.
               * `description`- The description of the Config Rule.
               * `input_parameters`- The input paramrters of the Config Rule.
               * `modified_timestamp`- the timestamp of the Config Rule modified.
               * `risk_level`- The risk level of the Config Rule.
               * `rule_name`- The name of the Config Rule.
               * `source_details`- The source details of the Config Rule.
        :param int risk_level: The risk level of Config Rule. Valid values: `1`: Critical ,`2`: Warning , `3`: Info.
        """
        pulumi.set(__self__, "account_id", account_id)
        pulumi.set(__self__, "config_rule_arn", config_rule_arn)
        pulumi.set(__self__, "config_rule_id", config_rule_id)
        pulumi.set(__self__, "config_rule_state", config_rule_state)
        pulumi.set(__self__, "create_timestamp", create_timestamp)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "input_parameters", input_parameters)
        pulumi.set(__self__, "modified_timestamp", modified_timestamp)
        pulumi.set(__self__, "risk_level", risk_level)
        pulumi.set(__self__, "rule_name", rule_name)
        pulumi.set(__self__, "source_details", source_details)
        pulumi.set(__self__, "source_identifier", source_identifier)
        pulumi.set(__self__, "source_owner", source_owner)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> int:
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter(name="configRuleArn")
    def config_rule_arn(self) -> str:
        return pulumi.get(self, "config_rule_arn")

    @property
    @pulumi.getter(name="configRuleId")
    def config_rule_id(self) -> str:
        return pulumi.get(self, "config_rule_id")

    @property
    @pulumi.getter(name="configRuleState")
    def config_rule_state(self) -> str:
        """
        The state of the config rule, valid values: `ACTIVE`, `DELETING`, `DELETING_RESULTS`, `EVALUATING` and `INACTIVE`.
        """
        return pulumi.get(self, "config_rule_state")

    @property
    @pulumi.getter(name="createTimestamp")
    def create_timestamp(self) -> int:
        return pulumi.get(self, "create_timestamp")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the Config Rule.
        * `account_id`- The ID of the Alicloud account.
        * `config_rule_arn`- The ARN of the Config Rule.
        * `config_rule_id`- The ID of the Config Rule.
        * `config_rule_state`- The state of the Config Rule.
        * `create_timestamp`- The timestamp of the Config Rule created.
        * `description`- The description of the Config Rule.
        * `input_parameters`- The input paramrters of the Config Rule.
        * `modified_timestamp`- the timestamp of the Config Rule modified.
        * `risk_level`- The risk level of the Config Rule.
        * `rule_name`- The name of the Config Rule.
        * `source_details`- The source details of the Config Rule.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="inputParameters")
    def input_parameters(self) -> Mapping[str, Any]:
        return pulumi.get(self, "input_parameters")

    @property
    @pulumi.getter(name="modifiedTimestamp")
    def modified_timestamp(self) -> int:
        return pulumi.get(self, "modified_timestamp")

    @property
    @pulumi.getter(name="riskLevel")
    def risk_level(self) -> int:
        """
        The risk level of Config Rule. Valid values: `1`: Critical ,`2`: Warning , `3`: Info.
        """
        return pulumi.get(self, "risk_level")

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> str:
        return pulumi.get(self, "rule_name")

    @property
    @pulumi.getter(name="sourceDetails")
    def source_details(self) -> Sequence['outputs.GetRulesRuleSourceDetailResult']:
        return pulumi.get(self, "source_details")

    @property
    @pulumi.getter(name="sourceIdentifier")
    def source_identifier(self) -> str:
        return pulumi.get(self, "source_identifier")

    @property
    @pulumi.getter(name="sourceOwner")
    def source_owner(self) -> str:
        return pulumi.get(self, "source_owner")


@pulumi.output_type
class GetRulesRuleSourceDetailResult(dict):
    def __init__(__self__, *,
                 event_source: str,
                 maximum_execution_frequency: str,
                 message_type: str):
        """
        :param str event_source: Event source of the Config Rule.
        :param str maximum_execution_frequency: Rule execution cycle.
        :param str message_type: Rule trigger mechanism.
               * `source_identifier`- The name of the custom rule or managed rule.
               * `source_owner`- The source owner of the Config Rule.
        """
        pulumi.set(__self__, "event_source", event_source)
        pulumi.set(__self__, "maximum_execution_frequency", maximum_execution_frequency)
        pulumi.set(__self__, "message_type", message_type)

    @property
    @pulumi.getter(name="eventSource")
    def event_source(self) -> str:
        """
        Event source of the Config Rule.
        """
        return pulumi.get(self, "event_source")

    @property
    @pulumi.getter(name="maximumExecutionFrequency")
    def maximum_execution_frequency(self) -> str:
        """
        Rule execution cycle.
        """
        return pulumi.get(self, "maximum_execution_frequency")

    @property
    @pulumi.getter(name="messageType")
    def message_type(self) -> str:
        """
        Rule trigger mechanism.
        * `source_identifier`- The name of the custom rule or managed rule.
        * `source_owner`- The source owner of the Config Rule.
        """
        return pulumi.get(self, "message_type")


