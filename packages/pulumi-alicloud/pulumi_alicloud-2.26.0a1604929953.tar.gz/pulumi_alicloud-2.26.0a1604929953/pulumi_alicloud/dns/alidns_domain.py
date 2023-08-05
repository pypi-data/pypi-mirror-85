# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['AlidnsDomain']


class AlidnsDomain(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 lang: Optional[pulumi.Input[str]] = None,
                 remark: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a Alidns domain resource.

        > **NOTE:** The domain name which you want to add must be already registered and had not added by another account. Every domain name can only exist in a unique group.

        > **NOTE:** Available in v1.95.0+.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Add a new Domain.
        dns = alicloud.dns.AlidnsDomain("dns",
            domain_name="starmove.com",
            group_id="85ab8713-4a30-4de4-9d20-155ff830****",
            tags={
                "Created": "Terraform",
                "Environment": "test",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain_name: Name of the domain. This name without suffix can have a string of 1 to 63 characters(domain name subject, excluding suffix), must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        :param pulumi.Input[str] group_id: Id of the group in which the domain will add. If not supplied, then use default group.
        :param pulumi.Input[str] lang: User language.
        :param pulumi.Input[str] remark: Remarks information for your domain name.
        :param pulumi.Input[str] resource_group_id: The Id of resource group which the dns domain belongs.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
               - Key: It can be up to 64 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It cannot be a null string.
               - Value: It can be up to 128 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It can be a null string.
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

            if domain_name is None:
                raise TypeError("Missing required property 'domain_name'")
            __props__['domain_name'] = domain_name
            __props__['group_id'] = group_id
            __props__['lang'] = lang
            __props__['remark'] = remark
            __props__['resource_group_id'] = resource_group_id
            __props__['tags'] = tags
            __props__['dns_servers'] = None
            __props__['domain_id'] = None
            __props__['group_name'] = None
            __props__['puny_code'] = None
        super(AlidnsDomain, __self__).__init__(
            'alicloud:dns/alidnsDomain:AlidnsDomain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            dns_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            domain_id: Optional[pulumi.Input[str]] = None,
            domain_name: Optional[pulumi.Input[str]] = None,
            group_id: Optional[pulumi.Input[str]] = None,
            group_name: Optional[pulumi.Input[str]] = None,
            lang: Optional[pulumi.Input[str]] = None,
            puny_code: Optional[pulumi.Input[str]] = None,
            remark: Optional[pulumi.Input[str]] = None,
            resource_group_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None) -> 'AlidnsDomain':
        """
        Get an existing AlidnsDomain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain_id: The domain ID.
        :param pulumi.Input[str] domain_name: Name of the domain. This name without suffix can have a string of 1 to 63 characters(domain name subject, excluding suffix), must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        :param pulumi.Input[str] group_id: Id of the group in which the domain will add. If not supplied, then use default group.
        :param pulumi.Input[str] group_name: Domain name group name.
        :param pulumi.Input[str] lang: User language.
        :param pulumi.Input[str] puny_code: Only return punycode codes for Chinese domain names.
        :param pulumi.Input[str] remark: Remarks information for your domain name.
        :param pulumi.Input[str] resource_group_id: The Id of resource group which the dns domain belongs.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
               - Key: It can be up to 64 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It cannot be a null string.
               - Value: It can be up to 128 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It can be a null string.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["dns_servers"] = dns_servers
        __props__["domain_id"] = domain_id
        __props__["domain_name"] = domain_name
        __props__["group_id"] = group_id
        __props__["group_name"] = group_name
        __props__["lang"] = lang
        __props__["puny_code"] = puny_code
        __props__["remark"] = remark
        __props__["resource_group_id"] = resource_group_id
        __props__["tags"] = tags
        return AlidnsDomain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> pulumi.Output[Sequence[str]]:
        return pulumi.get(self, "dns_servers")

    @property
    @pulumi.getter(name="domainId")
    def domain_id(self) -> pulumi.Output[str]:
        """
        The domain ID.
        """
        return pulumi.get(self, "domain_id")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        Name of the domain. This name without suffix can have a string of 1 to 63 characters(domain name subject, excluding suffix), must contain only alphanumeric characters or "-", and must not begin or end with "-", and "-" must not in the 3th and 4th character positions at the same time. Suffix `.sh` and `.tel` are not supported.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[Optional[str]]:
        """
        Id of the group in which the domain will add. If not supplied, then use default group.
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> pulumi.Output[str]:
        """
        Domain name group name.
        """
        return pulumi.get(self, "group_name")

    @property
    @pulumi.getter
    def lang(self) -> pulumi.Output[Optional[str]]:
        """
        User language.
        """
        return pulumi.get(self, "lang")

    @property
    @pulumi.getter(name="punyCode")
    def puny_code(self) -> pulumi.Output[str]:
        """
        Only return punycode codes for Chinese domain names.
        """
        return pulumi.get(self, "puny_code")

    @property
    @pulumi.getter
    def remark(self) -> pulumi.Output[Optional[str]]:
        """
        Remarks information for your domain name.
        """
        return pulumi.get(self, "remark")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Output[str]:
        """
        The Id of resource group which the dns domain belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        - Key: It can be up to 64 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It cannot be a null string.
        - Value: It can be up to 128 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It can be a null string.
        """
        return pulumi.get(self, "tags")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

