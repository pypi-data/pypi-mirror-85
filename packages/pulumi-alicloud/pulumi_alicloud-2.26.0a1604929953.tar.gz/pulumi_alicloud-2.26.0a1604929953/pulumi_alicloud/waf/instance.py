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
                 big_screen: Optional[pulumi.Input[str]] = None,
                 exclusive_ip_package: Optional[pulumi.Input[str]] = None,
                 ext_bandwidth: Optional[pulumi.Input[str]] = None,
                 ext_domain_package: Optional[pulumi.Input[str]] = None,
                 log_storage: Optional[pulumi.Input[str]] = None,
                 log_time: Optional[pulumi.Input[str]] = None,
                 modify_type: Optional[pulumi.Input[str]] = None,
                 package_code: Optional[pulumi.Input[str]] = None,
                 period: Optional[pulumi.Input[int]] = None,
                 prefessional_service: Optional[pulumi.Input[str]] = None,
                 renew_period: Optional[pulumi.Input[int]] = None,
                 renewal_status: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 subscription_type: Optional[pulumi.Input[str]] = None,
                 waf_log: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a WAF Instance resource to create instance in the Web Application Firewall.

        For information about WAF and how to use it, see [What is Alibaba Cloud WAF](https://www.alibabacloud.com/help/doc-detail/28517.htm).

        > **NOTE:** Available in 1.83.0+ .

        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.waf.Instance("default",
            big_screen="0",
            exclusive_ip_package="1",
            ext_bandwidth="50",
            ext_domain_package="1",
            log_storage="3",
            log_time="180",
            package_code="version_3",
            period=1,
            prefessional_service="false",
            resource_group_id="rs-abc12345",
            subscription_type="Subscription",
            waf_log="false")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] big_screen: Specify whether big screen is supported. Valid values: ["0", "1"]. "0" for false and "1" for true.
        :param pulumi.Input[str] exclusive_ip_package: Specify the number of exclusive WAF IP addresses.
        :param pulumi.Input[str] ext_bandwidth: The extra bandwidth. Unit: Mbit/s.
        :param pulumi.Input[str] ext_domain_package: The number of extra domains.
        :param pulumi.Input[str] log_storage: Log storage size. Unit: T. Valid values: [3, 5, 10, 20, 50].
        :param pulumi.Input[str] log_time: Log storage period. Unit: day. Valid values: [180, 360].
        :param pulumi.Input[str] modify_type: Type of configuration change. Valid value: Upgrade.
        :param pulumi.Input[str] package_code: Subscription plan:
               * China site customers can purchase the following versions of China Mainland region, valid values: ["version_3", "version_4", "version_5"].
               * China site customers can purchase the following versions of International region, valid values: ["version_pro_asia", "version_business_asia", "version_enterprise_asia"]
               * International site customers can purchase the following versions of China Mainland region: ["version_pro_china", "version_business_china", "version_enterprise_china"]
               * International site customers can purchase the following versions of International region: ["version_pro", "version_business", "version_enterprise"].
        :param pulumi.Input[int] period: Service time of Web Application Firewall.
        :param pulumi.Input[str] prefessional_service: Specify whether professional service is supported. Valid values: ["true", "false"]
        :param pulumi.Input[int] renew_period: Renewal period of WAF service. Unit: month
        :param pulumi.Input[str] renewal_status: Renewal status of WAF service. Valid values: 
               * AutoRenewal: The service time of WAF is renewed automatically.
               * ManualRenewal (default): The service time of WAF is renewed manually.Specifies whether to configure a Layer-7 proxy, such as Anti-DDoS Pro or CDN, to filter the inbound traffic before it is forwarded to WAF. Valid values: "On" and "Off". Default to "Off".
        :param pulumi.Input[str] resource_group_id: The resource group ID.
        :param pulumi.Input[str] subscription_type: Subscription of WAF service. Valid values: ["Subscription", "PayAsYouGo"].
        :param pulumi.Input[str] waf_log: Specify whether Log service is supported. Valid values: ["true", "false"]
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

            if big_screen is None:
                raise TypeError("Missing required property 'big_screen'")
            __props__['big_screen'] = big_screen
            if exclusive_ip_package is None:
                raise TypeError("Missing required property 'exclusive_ip_package'")
            __props__['exclusive_ip_package'] = exclusive_ip_package
            if ext_bandwidth is None:
                raise TypeError("Missing required property 'ext_bandwidth'")
            __props__['ext_bandwidth'] = ext_bandwidth
            if ext_domain_package is None:
                raise TypeError("Missing required property 'ext_domain_package'")
            __props__['ext_domain_package'] = ext_domain_package
            if log_storage is None:
                raise TypeError("Missing required property 'log_storage'")
            __props__['log_storage'] = log_storage
            if log_time is None:
                raise TypeError("Missing required property 'log_time'")
            __props__['log_time'] = log_time
            __props__['modify_type'] = modify_type
            if package_code is None:
                raise TypeError("Missing required property 'package_code'")
            __props__['package_code'] = package_code
            __props__['period'] = period
            if prefessional_service is None:
                raise TypeError("Missing required property 'prefessional_service'")
            __props__['prefessional_service'] = prefessional_service
            __props__['renew_period'] = renew_period
            __props__['renewal_status'] = renewal_status
            __props__['resource_group_id'] = resource_group_id
            if subscription_type is None:
                raise TypeError("Missing required property 'subscription_type'")
            __props__['subscription_type'] = subscription_type
            if waf_log is None:
                raise TypeError("Missing required property 'waf_log'")
            __props__['waf_log'] = waf_log
            __props__['status'] = None
        super(Instance, __self__).__init__(
            'alicloud:waf/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            big_screen: Optional[pulumi.Input[str]] = None,
            exclusive_ip_package: Optional[pulumi.Input[str]] = None,
            ext_bandwidth: Optional[pulumi.Input[str]] = None,
            ext_domain_package: Optional[pulumi.Input[str]] = None,
            log_storage: Optional[pulumi.Input[str]] = None,
            log_time: Optional[pulumi.Input[str]] = None,
            modify_type: Optional[pulumi.Input[str]] = None,
            package_code: Optional[pulumi.Input[str]] = None,
            period: Optional[pulumi.Input[int]] = None,
            prefessional_service: Optional[pulumi.Input[str]] = None,
            renew_period: Optional[pulumi.Input[int]] = None,
            renewal_status: Optional[pulumi.Input[str]] = None,
            resource_group_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[int]] = None,
            subscription_type: Optional[pulumi.Input[str]] = None,
            waf_log: Optional[pulumi.Input[str]] = None) -> 'Instance':
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] big_screen: Specify whether big screen is supported. Valid values: ["0", "1"]. "0" for false and "1" for true.
        :param pulumi.Input[str] exclusive_ip_package: Specify the number of exclusive WAF IP addresses.
        :param pulumi.Input[str] ext_bandwidth: The extra bandwidth. Unit: Mbit/s.
        :param pulumi.Input[str] ext_domain_package: The number of extra domains.
        :param pulumi.Input[str] log_storage: Log storage size. Unit: T. Valid values: [3, 5, 10, 20, 50].
        :param pulumi.Input[str] log_time: Log storage period. Unit: day. Valid values: [180, 360].
        :param pulumi.Input[str] modify_type: Type of configuration change. Valid value: Upgrade.
        :param pulumi.Input[str] package_code: Subscription plan:
               * China site customers can purchase the following versions of China Mainland region, valid values: ["version_3", "version_4", "version_5"].
               * China site customers can purchase the following versions of International region, valid values: ["version_pro_asia", "version_business_asia", "version_enterprise_asia"]
               * International site customers can purchase the following versions of China Mainland region: ["version_pro_china", "version_business_china", "version_enterprise_china"]
               * International site customers can purchase the following versions of International region: ["version_pro", "version_business", "version_enterprise"].
        :param pulumi.Input[int] period: Service time of Web Application Firewall.
        :param pulumi.Input[str] prefessional_service: Specify whether professional service is supported. Valid values: ["true", "false"]
        :param pulumi.Input[int] renew_period: Renewal period of WAF service. Unit: month
        :param pulumi.Input[str] renewal_status: Renewal status of WAF service. Valid values: 
               * AutoRenewal: The service time of WAF is renewed automatically.
               * ManualRenewal (default): The service time of WAF is renewed manually.Specifies whether to configure a Layer-7 proxy, such as Anti-DDoS Pro or CDN, to filter the inbound traffic before it is forwarded to WAF. Valid values: "On" and "Off". Default to "Off".
        :param pulumi.Input[str] resource_group_id: The resource group ID.
        :param pulumi.Input[int] status: The status of the instance.
        :param pulumi.Input[str] subscription_type: Subscription of WAF service. Valid values: ["Subscription", "PayAsYouGo"].
        :param pulumi.Input[str] waf_log: Specify whether Log service is supported. Valid values: ["true", "false"]
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["big_screen"] = big_screen
        __props__["exclusive_ip_package"] = exclusive_ip_package
        __props__["ext_bandwidth"] = ext_bandwidth
        __props__["ext_domain_package"] = ext_domain_package
        __props__["log_storage"] = log_storage
        __props__["log_time"] = log_time
        __props__["modify_type"] = modify_type
        __props__["package_code"] = package_code
        __props__["period"] = period
        __props__["prefessional_service"] = prefessional_service
        __props__["renew_period"] = renew_period
        __props__["renewal_status"] = renewal_status
        __props__["resource_group_id"] = resource_group_id
        __props__["status"] = status
        __props__["subscription_type"] = subscription_type
        __props__["waf_log"] = waf_log
        return Instance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="bigScreen")
    def big_screen(self) -> pulumi.Output[str]:
        """
        Specify whether big screen is supported. Valid values: ["0", "1"]. "0" for false and "1" for true.
        """
        return pulumi.get(self, "big_screen")

    @property
    @pulumi.getter(name="exclusiveIpPackage")
    def exclusive_ip_package(self) -> pulumi.Output[str]:
        """
        Specify the number of exclusive WAF IP addresses.
        """
        return pulumi.get(self, "exclusive_ip_package")

    @property
    @pulumi.getter(name="extBandwidth")
    def ext_bandwidth(self) -> pulumi.Output[str]:
        """
        The extra bandwidth. Unit: Mbit/s.
        """
        return pulumi.get(self, "ext_bandwidth")

    @property
    @pulumi.getter(name="extDomainPackage")
    def ext_domain_package(self) -> pulumi.Output[str]:
        """
        The number of extra domains.
        """
        return pulumi.get(self, "ext_domain_package")

    @property
    @pulumi.getter(name="logStorage")
    def log_storage(self) -> pulumi.Output[str]:
        """
        Log storage size. Unit: T. Valid values: [3, 5, 10, 20, 50].
        """
        return pulumi.get(self, "log_storage")

    @property
    @pulumi.getter(name="logTime")
    def log_time(self) -> pulumi.Output[str]:
        """
        Log storage period. Unit: day. Valid values: [180, 360].
        """
        return pulumi.get(self, "log_time")

    @property
    @pulumi.getter(name="modifyType")
    def modify_type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of configuration change. Valid value: Upgrade.
        """
        return pulumi.get(self, "modify_type")

    @property
    @pulumi.getter(name="packageCode")
    def package_code(self) -> pulumi.Output[str]:
        """
        Subscription plan:
        * China site customers can purchase the following versions of China Mainland region, valid values: ["version_3", "version_4", "version_5"].
        * China site customers can purchase the following versions of International region, valid values: ["version_pro_asia", "version_business_asia", "version_enterprise_asia"]
        * International site customers can purchase the following versions of China Mainland region: ["version_pro_china", "version_business_china", "version_enterprise_china"]
        * International site customers can purchase the following versions of International region: ["version_pro", "version_business", "version_enterprise"].
        """
        return pulumi.get(self, "package_code")

    @property
    @pulumi.getter
    def period(self) -> pulumi.Output[Optional[int]]:
        """
        Service time of Web Application Firewall.
        """
        return pulumi.get(self, "period")

    @property
    @pulumi.getter(name="prefessionalService")
    def prefessional_service(self) -> pulumi.Output[str]:
        """
        Specify whether professional service is supported. Valid values: ["true", "false"]
        """
        return pulumi.get(self, "prefessional_service")

    @property
    @pulumi.getter(name="renewPeriod")
    def renew_period(self) -> pulumi.Output[Optional[int]]:
        """
        Renewal period of WAF service. Unit: month
        """
        return pulumi.get(self, "renew_period")

    @property
    @pulumi.getter(name="renewalStatus")
    def renewal_status(self) -> pulumi.Output[Optional[str]]:
        """
        Renewal status of WAF service. Valid values: 
        * AutoRenewal: The service time of WAF is renewed automatically.
        * ManualRenewal (default): The service time of WAF is renewed manually.Specifies whether to configure a Layer-7 proxy, such as Anti-DDoS Pro or CDN, to filter the inbound traffic before it is forwarded to WAF. Valid values: "On" and "Off". Default to "Off".
        """
        return pulumi.get(self, "renewal_status")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource group ID.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[int]:
        """
        The status of the instance.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subscriptionType")
    def subscription_type(self) -> pulumi.Output[str]:
        """
        Subscription of WAF service. Valid values: ["Subscription", "PayAsYouGo"].
        """
        return pulumi.get(self, "subscription_type")

    @property
    @pulumi.getter(name="wafLog")
    def waf_log(self) -> pulumi.Output[str]:
        """
        Specify whether Log service is supported. Valid values: ["true", "false"]
        """
        return pulumi.get(self, "waf_log")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

