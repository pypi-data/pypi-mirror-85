# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Alarm']


class Alarm(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 contact_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 dimensions: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 effective_interval: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 end_time: Optional[pulumi.Input[int]] = None,
                 escalations_critical: Optional[pulumi.Input[pulumi.InputType['AlarmEscalationsCriticalArgs']]] = None,
                 escalations_info: Optional[pulumi.Input[pulumi.InputType['AlarmEscalationsInfoArgs']]] = None,
                 escalations_warn: Optional[pulumi.Input[pulumi.InputType['AlarmEscalationsWarnArgs']]] = None,
                 metric: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 operator: Optional[pulumi.Input[str]] = None,
                 period: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 silence_time: Optional[pulumi.Input[int]] = None,
                 start_time: Optional[pulumi.Input[int]] = None,
                 statistics: Optional[pulumi.Input[str]] = None,
                 threshold: Optional[pulumi.Input[str]] = None,
                 triggered_count: Optional[pulumi.Input[int]] = None,
                 webhook: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        This resource provides a alarm rule resource and it can be used to monitor several cloud services according different metrics.
        Details for [alarm rule](https://www.alibabacloud.com/help/doc-detail/28608.htm).

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        basic = alicloud.cms.Alarm("basic",
            contact_groups=["test-group"],
            dimensions={
                "device": "/dev/vda1,/dev/vdb1",
                "instance_id": "i-bp1247,i-bp11gd",
            },
            effective_interval="0:00-2:00",
            escalations_critical=alicloud.cms.AlarmEscalationsCriticalArgs(
                comparison_operator="<=",
                statistics="Average",
                threshold="35",
                times=2,
            ),
            metric="disk_writebytes",
            period=900,
            project="acs_ecs_dashboard",
            webhook=f"https://{data['alicloud_account']['current']['id']}.eu-central-1.fc.aliyuncs.com/2016-08-15/proxy/Terraform/AlarmEndpointMock/")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] contact_groups: List contact groups of the alarm rule, which must have been created on the console.
        :param pulumi.Input[Mapping[str, Any]] dimensions: Map of the resources associated with the alarm rule, such as "instanceId", "device" and "port". Each key's value is a string and it uses comma to split multiple items. For more information, see [Metrics Reference](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        :param pulumi.Input[str] effective_interval: The interval of effecting alarm rule. It foramt as "hh:mm-hh:mm", like "0:00-4:00". Default to "00:00-23:59".
        :param pulumi.Input[bool] enabled: Whether to enable alarm rule. Default to true.
        :param pulumi.Input[int] end_time: It has been deprecated from provider version 1.50.0 and 'effective_interval' instead.
        :param pulumi.Input[pulumi.InputType['AlarmEscalationsCriticalArgs']] escalations_critical: A configuration of critical alarm (documented below).
        :param pulumi.Input[pulumi.InputType['AlarmEscalationsInfoArgs']] escalations_info: A configuration of critical info (documented below).
        :param pulumi.Input[pulumi.InputType['AlarmEscalationsWarnArgs']] escalations_warn: A configuration of critical warn (documented below).
        :param pulumi.Input[str] metric: Name of the monitoring metrics corresponding to a project, such as "CPUUtilization" and "networkin_rate". For more information, see [Metrics Reference](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        :param pulumi.Input[str] name: The alarm rule name.
        :param pulumi.Input[str] operator: It has been deprecated from provider version 1.94.0 and 'escalations_critical.comparison_operator' instead.
        :param pulumi.Input[int] period: Index query cycle, which must be consistent with that defined for metrics. Default to 300, in seconds.
        :param pulumi.Input[str] project: Monitor project name, such as "acs_ecs_dashboard" and "acs_rds_dashboard". For more information, see [Metrics Reference](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        :param pulumi.Input[int] silence_time: Notification silence period in the alarm state, in seconds. Valid value range: [300, 86400]. Default to 86400
        :param pulumi.Input[int] start_time: It has been deprecated from provider version 1.50.0 and 'effective_interval' instead.
        :param pulumi.Input[str] statistics: Critical level alarm statistics method.. It must be consistent with that defined for metrics. Valid values: ["Average", "Minimum", "Maximum"]. Default to "Average".
        :param pulumi.Input[str] threshold: Critical level alarm threshold value, which must be a numeric value currently.
        :param pulumi.Input[int] triggered_count: It has been deprecated from provider version 1.94.0 and 'escalations_critical.times' instead.
        :param pulumi.Input[str] webhook: The webhook that should be called when the alarm is triggered. Currently, only http protocol is supported. Default is empty string.
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

            if contact_groups is None:
                raise TypeError("Missing required property 'contact_groups'")
            __props__['contact_groups'] = contact_groups
            if dimensions is None:
                raise TypeError("Missing required property 'dimensions'")
            __props__['dimensions'] = dimensions
            __props__['effective_interval'] = effective_interval
            __props__['enabled'] = enabled
            if end_time is not None:
                warnings.warn("Field 'end_time' has been deprecated from provider version 1.50.0. New field 'effective_interval' instead.", DeprecationWarning)
                pulumi.log.warn("end_time is deprecated: Field 'end_time' has been deprecated from provider version 1.50.0. New field 'effective_interval' instead.")
            __props__['end_time'] = end_time
            __props__['escalations_critical'] = escalations_critical
            __props__['escalations_info'] = escalations_info
            __props__['escalations_warn'] = escalations_warn
            if metric is None:
                raise TypeError("Missing required property 'metric'")
            __props__['metric'] = metric
            __props__['name'] = name
            if operator is not None:
                warnings.warn("Field 'operator' has been deprecated from provider version 1.94.0. New field 'escalations_critical.comparison_operator' instead.", DeprecationWarning)
                pulumi.log.warn("operator is deprecated: Field 'operator' has been deprecated from provider version 1.94.0. New field 'escalations_critical.comparison_operator' instead.")
            __props__['operator'] = operator
            __props__['period'] = period
            if project is None:
                raise TypeError("Missing required property 'project'")
            __props__['project'] = project
            __props__['silence_time'] = silence_time
            if start_time is not None:
                warnings.warn("Field 'start_time' has been deprecated from provider version 1.50.0. New field 'effective_interval' instead.", DeprecationWarning)
                pulumi.log.warn("start_time is deprecated: Field 'start_time' has been deprecated from provider version 1.50.0. New field 'effective_interval' instead.")
            __props__['start_time'] = start_time
            if statistics is not None:
                warnings.warn("Field 'statistics' has been deprecated from provider version 1.94.0. New field 'escalations_critical.statistics' instead.", DeprecationWarning)
                pulumi.log.warn("statistics is deprecated: Field 'statistics' has been deprecated from provider version 1.94.0. New field 'escalations_critical.statistics' instead.")
            __props__['statistics'] = statistics
            if threshold is not None:
                warnings.warn("Field 'threshold' has been deprecated from provider version 1.94.0. New field 'escalations_critical.threshold' instead.", DeprecationWarning)
                pulumi.log.warn("threshold is deprecated: Field 'threshold' has been deprecated from provider version 1.94.0. New field 'escalations_critical.threshold' instead.")
            __props__['threshold'] = threshold
            if triggered_count is not None:
                warnings.warn("Field 'triggered_count' has been deprecated from provider version 1.94.0. New field 'escalations_critical.times' instead.", DeprecationWarning)
                pulumi.log.warn("triggered_count is deprecated: Field 'triggered_count' has been deprecated from provider version 1.94.0. New field 'escalations_critical.times' instead.")
            __props__['triggered_count'] = triggered_count
            __props__['webhook'] = webhook
            __props__['status'] = None
        super(Alarm, __self__).__init__(
            'alicloud:cms/alarm:Alarm',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            contact_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            dimensions: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            effective_interval: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            end_time: Optional[pulumi.Input[int]] = None,
            escalations_critical: Optional[pulumi.Input[pulumi.InputType['AlarmEscalationsCriticalArgs']]] = None,
            escalations_info: Optional[pulumi.Input[pulumi.InputType['AlarmEscalationsInfoArgs']]] = None,
            escalations_warn: Optional[pulumi.Input[pulumi.InputType['AlarmEscalationsWarnArgs']]] = None,
            metric: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            operator: Optional[pulumi.Input[str]] = None,
            period: Optional[pulumi.Input[int]] = None,
            project: Optional[pulumi.Input[str]] = None,
            silence_time: Optional[pulumi.Input[int]] = None,
            start_time: Optional[pulumi.Input[int]] = None,
            statistics: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            threshold: Optional[pulumi.Input[str]] = None,
            triggered_count: Optional[pulumi.Input[int]] = None,
            webhook: Optional[pulumi.Input[str]] = None) -> 'Alarm':
        """
        Get an existing Alarm resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] contact_groups: List contact groups of the alarm rule, which must have been created on the console.
        :param pulumi.Input[Mapping[str, Any]] dimensions: Map of the resources associated with the alarm rule, such as "instanceId", "device" and "port". Each key's value is a string and it uses comma to split multiple items. For more information, see [Metrics Reference](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        :param pulumi.Input[str] effective_interval: The interval of effecting alarm rule. It foramt as "hh:mm-hh:mm", like "0:00-4:00". Default to "00:00-23:59".
        :param pulumi.Input[bool] enabled: Whether to enable alarm rule. Default to true.
        :param pulumi.Input[int] end_time: It has been deprecated from provider version 1.50.0 and 'effective_interval' instead.
        :param pulumi.Input[pulumi.InputType['AlarmEscalationsCriticalArgs']] escalations_critical: A configuration of critical alarm (documented below).
        :param pulumi.Input[pulumi.InputType['AlarmEscalationsInfoArgs']] escalations_info: A configuration of critical info (documented below).
        :param pulumi.Input[pulumi.InputType['AlarmEscalationsWarnArgs']] escalations_warn: A configuration of critical warn (documented below).
        :param pulumi.Input[str] metric: Name of the monitoring metrics corresponding to a project, such as "CPUUtilization" and "networkin_rate". For more information, see [Metrics Reference](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        :param pulumi.Input[str] name: The alarm rule name.
        :param pulumi.Input[str] operator: It has been deprecated from provider version 1.94.0 and 'escalations_critical.comparison_operator' instead.
        :param pulumi.Input[int] period: Index query cycle, which must be consistent with that defined for metrics. Default to 300, in seconds.
        :param pulumi.Input[str] project: Monitor project name, such as "acs_ecs_dashboard" and "acs_rds_dashboard". For more information, see [Metrics Reference](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        :param pulumi.Input[int] silence_time: Notification silence period in the alarm state, in seconds. Valid value range: [300, 86400]. Default to 86400
        :param pulumi.Input[int] start_time: It has been deprecated from provider version 1.50.0 and 'effective_interval' instead.
        :param pulumi.Input[str] statistics: Critical level alarm statistics method.. It must be consistent with that defined for metrics. Valid values: ["Average", "Minimum", "Maximum"]. Default to "Average".
        :param pulumi.Input[str] status: The current alarm rule status.
        :param pulumi.Input[str] threshold: Critical level alarm threshold value, which must be a numeric value currently.
        :param pulumi.Input[int] triggered_count: It has been deprecated from provider version 1.94.0 and 'escalations_critical.times' instead.
        :param pulumi.Input[str] webhook: The webhook that should be called when the alarm is triggered. Currently, only http protocol is supported. Default is empty string.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["contact_groups"] = contact_groups
        __props__["dimensions"] = dimensions
        __props__["effective_interval"] = effective_interval
        __props__["enabled"] = enabled
        __props__["end_time"] = end_time
        __props__["escalations_critical"] = escalations_critical
        __props__["escalations_info"] = escalations_info
        __props__["escalations_warn"] = escalations_warn
        __props__["metric"] = metric
        __props__["name"] = name
        __props__["operator"] = operator
        __props__["period"] = period
        __props__["project"] = project
        __props__["silence_time"] = silence_time
        __props__["start_time"] = start_time
        __props__["statistics"] = statistics
        __props__["status"] = status
        __props__["threshold"] = threshold
        __props__["triggered_count"] = triggered_count
        __props__["webhook"] = webhook
        return Alarm(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="contactGroups")
    def contact_groups(self) -> pulumi.Output[Sequence[str]]:
        """
        List contact groups of the alarm rule, which must have been created on the console.
        """
        return pulumi.get(self, "contact_groups")

    @property
    @pulumi.getter
    def dimensions(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        Map of the resources associated with the alarm rule, such as "instanceId", "device" and "port". Each key's value is a string and it uses comma to split multiple items. For more information, see [Metrics Reference](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        """
        return pulumi.get(self, "dimensions")

    @property
    @pulumi.getter(name="effectiveInterval")
    def effective_interval(self) -> pulumi.Output[Optional[str]]:
        """
        The interval of effecting alarm rule. It foramt as "hh:mm-hh:mm", like "0:00-4:00". Default to "00:00-23:59".
        """
        return pulumi.get(self, "effective_interval")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to enable alarm rule. Default to true.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[Optional[int]]:
        """
        It has been deprecated from provider version 1.50.0 and 'effective_interval' instead.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="escalationsCritical")
    def escalations_critical(self) -> pulumi.Output[Optional['outputs.AlarmEscalationsCritical']]:
        """
        A configuration of critical alarm (documented below).
        """
        return pulumi.get(self, "escalations_critical")

    @property
    @pulumi.getter(name="escalationsInfo")
    def escalations_info(self) -> pulumi.Output[Optional['outputs.AlarmEscalationsInfo']]:
        """
        A configuration of critical info (documented below).
        """
        return pulumi.get(self, "escalations_info")

    @property
    @pulumi.getter(name="escalationsWarn")
    def escalations_warn(self) -> pulumi.Output[Optional['outputs.AlarmEscalationsWarn']]:
        """
        A configuration of critical warn (documented below).
        """
        return pulumi.get(self, "escalations_warn")

    @property
    @pulumi.getter
    def metric(self) -> pulumi.Output[str]:
        """
        Name of the monitoring metrics corresponding to a project, such as "CPUUtilization" and "networkin_rate". For more information, see [Metrics Reference](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        """
        return pulumi.get(self, "metric")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The alarm rule name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def operator(self) -> pulumi.Output[str]:
        """
        It has been deprecated from provider version 1.94.0 and 'escalations_critical.comparison_operator' instead.
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def period(self) -> pulumi.Output[Optional[int]]:
        """
        Index query cycle, which must be consistent with that defined for metrics. Default to 300, in seconds.
        """
        return pulumi.get(self, "period")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        Monitor project name, such as "acs_ecs_dashboard" and "acs_rds_dashboard". For more information, see [Metrics Reference](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="silenceTime")
    def silence_time(self) -> pulumi.Output[Optional[int]]:
        """
        Notification silence period in the alarm state, in seconds. Valid value range: [300, 86400]. Default to 86400
        """
        return pulumi.get(self, "silence_time")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[Optional[int]]:
        """
        It has been deprecated from provider version 1.50.0 and 'effective_interval' instead.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def statistics(self) -> pulumi.Output[str]:
        """
        Critical level alarm statistics method.. It must be consistent with that defined for metrics. Valid values: ["Average", "Minimum", "Maximum"]. Default to "Average".
        """
        return pulumi.get(self, "statistics")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The current alarm rule status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def threshold(self) -> pulumi.Output[str]:
        """
        Critical level alarm threshold value, which must be a numeric value currently.
        """
        return pulumi.get(self, "threshold")

    @property
    @pulumi.getter(name="triggeredCount")
    def triggered_count(self) -> pulumi.Output[int]:
        """
        It has been deprecated from provider version 1.94.0 and 'escalations_critical.times' instead.
        """
        return pulumi.get(self, "triggered_count")

    @property
    @pulumi.getter
    def webhook(self) -> pulumi.Output[Optional[str]]:
        """
        The webhook that should be called when the alarm is triggered. Currently, only http protocol is supported. Default is empty string.
        """
        return pulumi.get(self, "webhook")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

