# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['AlidnsDomainAttachment']


class AlidnsDomainAttachment(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides bind the domain name to the Alidns instance resource.

        > **NOTE:** Available in v1.99.0+.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        dns = alicloud.dns.AlidnsDomainAttachment("dns",
            domain_names=[
                "test111.abc",
                "test222.abc",
            ],
            instance_id="dns-cn-mp91lyq9xxxx")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] domain_names: The domain names bound to the DNS instance.
        :param pulumi.Input[str] instance_id: The id of the DNS instance.
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

            if domain_names is None:
                raise TypeError("Missing required property 'domain_names'")
            __props__['domain_names'] = domain_names
            if instance_id is None:
                raise TypeError("Missing required property 'instance_id'")
            __props__['instance_id'] = instance_id
        super(AlidnsDomainAttachment, __self__).__init__(
            'alicloud:dns/alidnsDomainAttachment:AlidnsDomainAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            domain_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            instance_id: Optional[pulumi.Input[str]] = None) -> 'AlidnsDomainAttachment':
        """
        Get an existing AlidnsDomainAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] domain_names: The domain names bound to the DNS instance.
        :param pulumi.Input[str] instance_id: The id of the DNS instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["domain_names"] = domain_names
        __props__["instance_id"] = instance_id
        return AlidnsDomainAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="domainNames")
    def domain_names(self) -> pulumi.Output[Sequence[str]]:
        """
        The domain names bound to the DNS instance.
        """
        return pulumi.get(self, "domain_names")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The id of the DNS instance.
        """
        return pulumi.get(self, "instance_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

