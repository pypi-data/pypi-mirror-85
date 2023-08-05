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

__all__ = ['SiteMonitor']


class SiteMonitor(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 alert_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 interval: Optional[pulumi.Input[int]] = None,
                 isp_cities: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SiteMonitorIspCityArgs']]]]] = None,
                 options_json: Optional[pulumi.Input[str]] = None,
                 task_name: Optional[pulumi.Input[str]] = None,
                 task_type: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        This resource provides a site monitor resource and it can be used to monitor public endpoints and websites.
        Details at https://www.alibabacloud.com/help/doc-detail/67907.htm

        Available in 1.72.0+

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        basic = alicloud.cms.SiteMonitor("basic",
            address="http://www.alibabacloud.com",
            interval=5,
            isp_cities=[alicloud.cms.SiteMonitorIspCityArgs(
                city="546",
                isp="465",
            )],
            task_name="tf-testAccCmsSiteMonitor_basic",
            task_type="HTTP")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The URL or IP address monitored by the site monitoring task.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] alert_ids: The IDs of existing alert rules to be associated with the site monitoring task.
        :param pulumi.Input[int] interval: The monitoring interval of the site monitoring task. Unit: minutes. Valid values: 1, 5, and 15. Default value: 1.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SiteMonitorIspCityArgs']]]] isp_cities: The detection points in a JSON array. For example, `[{"city":"546","isp":"465"},{"city":"572","isp":"465"},{"city":"738","isp":"465"}]` indicates the detection points in Beijing, Hangzhou, and Qingdao respectively. You can call the [DescribeSiteMonitorISPCityList](https://www.alibabacloud.com/help/en/doc-detail/115045.htm) operation to query detection point information. If this parameter is not specified, three detection points will be chosen randomly for monitoring.
        :param pulumi.Input[str] options_json: The extended options of the protocol of the site monitoring task. The options vary according to the protocol.
        :param pulumi.Input[str] task_name: The name of the site monitoring task. The name must be 4 to 100 characters in length. The name can contain the following types of characters: letters, digits, and underscores.
        :param pulumi.Input[str] task_type: The protocol of the site monitoring task. Currently, site monitoring supports the following protocols: HTTP, Ping, TCP, UDP, DNS, SMTP, POP3, and FTP.
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

            if address is None:
                raise TypeError("Missing required property 'address'")
            __props__['address'] = address
            __props__['alert_ids'] = alert_ids
            __props__['interval'] = interval
            __props__['isp_cities'] = isp_cities
            __props__['options_json'] = options_json
            if task_name is None:
                raise TypeError("Missing required property 'task_name'")
            __props__['task_name'] = task_name
            if task_type is None:
                raise TypeError("Missing required property 'task_type'")
            __props__['task_type'] = task_type
            __props__['create_time'] = None
            __props__['task_state'] = None
            __props__['update_time'] = None
        super(SiteMonitor, __self__).__init__(
            'alicloud:cms/siteMonitor:SiteMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            address: Optional[pulumi.Input[str]] = None,
            alert_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            create_time: Optional[pulumi.Input[str]] = None,
            interval: Optional[pulumi.Input[int]] = None,
            isp_cities: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SiteMonitorIspCityArgs']]]]] = None,
            options_json: Optional[pulumi.Input[str]] = None,
            task_name: Optional[pulumi.Input[str]] = None,
            task_state: Optional[pulumi.Input[str]] = None,
            task_type: Optional[pulumi.Input[str]] = None,
            update_time: Optional[pulumi.Input[str]] = None) -> 'SiteMonitor':
        """
        Get an existing SiteMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The URL or IP address monitored by the site monitoring task.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] alert_ids: The IDs of existing alert rules to be associated with the site monitoring task.
        :param pulumi.Input[int] interval: The monitoring interval of the site monitoring task. Unit: minutes. Valid values: 1, 5, and 15. Default value: 1.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SiteMonitorIspCityArgs']]]] isp_cities: The detection points in a JSON array. For example, `[{"city":"546","isp":"465"},{"city":"572","isp":"465"},{"city":"738","isp":"465"}]` indicates the detection points in Beijing, Hangzhou, and Qingdao respectively. You can call the [DescribeSiteMonitorISPCityList](https://www.alibabacloud.com/help/en/doc-detail/115045.htm) operation to query detection point information. If this parameter is not specified, three detection points will be chosen randomly for monitoring.
        :param pulumi.Input[str] options_json: The extended options of the protocol of the site monitoring task. The options vary according to the protocol.
        :param pulumi.Input[str] task_name: The name of the site monitoring task. The name must be 4 to 100 characters in length. The name can contain the following types of characters: letters, digits, and underscores.
        :param pulumi.Input[str] task_type: The protocol of the site monitoring task. Currently, site monitoring supports the following protocols: HTTP, Ping, TCP, UDP, DNS, SMTP, POP3, and FTP.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["address"] = address
        __props__["alert_ids"] = alert_ids
        __props__["create_time"] = create_time
        __props__["interval"] = interval
        __props__["isp_cities"] = isp_cities
        __props__["options_json"] = options_json
        __props__["task_name"] = task_name
        __props__["task_state"] = task_state
        __props__["task_type"] = task_type
        __props__["update_time"] = update_time
        return SiteMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Output[str]:
        """
        The URL or IP address monitored by the site monitoring task.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="alertIds")
    def alert_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The IDs of existing alert rules to be associated with the site monitoring task.
        """
        return pulumi.get(self, "alert_ids")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def interval(self) -> pulumi.Output[Optional[int]]:
        """
        The monitoring interval of the site monitoring task. Unit: minutes. Valid values: 1, 5, and 15. Default value: 1.
        """
        return pulumi.get(self, "interval")

    @property
    @pulumi.getter(name="ispCities")
    def isp_cities(self) -> pulumi.Output[Optional[Sequence['outputs.SiteMonitorIspCity']]]:
        """
        The detection points in a JSON array. For example, `[{"city":"546","isp":"465"},{"city":"572","isp":"465"},{"city":"738","isp":"465"}]` indicates the detection points in Beijing, Hangzhou, and Qingdao respectively. You can call the [DescribeSiteMonitorISPCityList](https://www.alibabacloud.com/help/en/doc-detail/115045.htm) operation to query detection point information. If this parameter is not specified, three detection points will be chosen randomly for monitoring.
        """
        return pulumi.get(self, "isp_cities")

    @property
    @pulumi.getter(name="optionsJson")
    def options_json(self) -> pulumi.Output[Optional[str]]:
        """
        The extended options of the protocol of the site monitoring task. The options vary according to the protocol.
        """
        return pulumi.get(self, "options_json")

    @property
    @pulumi.getter(name="taskName")
    def task_name(self) -> pulumi.Output[str]:
        """
        The name of the site monitoring task. The name must be 4 to 100 characters in length. The name can contain the following types of characters: letters, digits, and underscores.
        """
        return pulumi.get(self, "task_name")

    @property
    @pulumi.getter(name="taskState")
    def task_state(self) -> pulumi.Output[str]:
        return pulumi.get(self, "task_state")

    @property
    @pulumi.getter(name="taskType")
    def task_type(self) -> pulumi.Output[str]:
        """
        The protocol of the site monitoring task. Currently, site monitoring supports the following protocols: HTTP, Ping, TCP, UDP, DNS, SMTP, POP3, and FTP.
        """
        return pulumi.get(self, "task_type")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        return pulumi.get(self, "update_time")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

