# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['MountTarget']


class MountTarget(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_group_name: Optional[pulumi.Input[str]] = None,
                 file_system_id: Optional[pulumi.Input[str]] = None,
                 security_group_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 vswitch_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a NAS Mount Target resource.
        For information about NAS Mount Target and how to use it, see [Manage NAS Mount Targets](https://www.alibabacloud.com/help/en/doc-detail/27531.htm).

        > NOTE: Available in v1.34.0+.

        > NOTE: Currently this resource support create a mount point in a classic network only when current region is China mainland regions.

        > NOTE: You must grant NAS with specific RAM permissions when creating a classic mount targets,
        and it only can be achieved by creating a classic mount target mannually.
        See [Add a mount point](https://www.alibabacloud.com/help/doc-detail/60431.htm) and [Why do I need RAM permissions to create a mount point in a classic network](https://www.alibabacloud.com/help/faq-detail/42176.htm).

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example_file_system = alicloud.nas.FileSystem("exampleFileSystem",
            protocol_type="NFS",
            storage_type="Performance",
            description="test file system")
        example_access_group = alicloud.nas.AccessGroup("exampleAccessGroup",
            access_group_name="test_name",
            access_group_type="Classic",
            description="test access group")
        example_mount_target = alicloud.nas.MountTarget("exampleMountTarget",
            file_system_id=example_file_system.id,
            access_group_name=example_access_group.access_group_name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_group_name: The name of the permission group that applies to the mount target.
        :param pulumi.Input[str] file_system_id: The ID of the file system.
        :param pulumi.Input[str] security_group_id: The ID of security group.
        :param pulumi.Input[str] status: Whether the MountTarget is active. The status of the mount target. Valid values: `Active` and `Inactive`, Default value is `Active`. Before you mount a file system, make sure that the mount target is in the Active state.
        :param pulumi.Input[str] vswitch_id: The ID of the VSwitch in the VPC where the mount target resides.
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

            if access_group_name is None:
                raise TypeError("Missing required property 'access_group_name'")
            __props__['access_group_name'] = access_group_name
            if file_system_id is None:
                raise TypeError("Missing required property 'file_system_id'")
            __props__['file_system_id'] = file_system_id
            __props__['security_group_id'] = security_group_id
            __props__['status'] = status
            __props__['vswitch_id'] = vswitch_id
        super(MountTarget, __self__).__init__(
            'alicloud:nas/mountTarget:MountTarget',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_group_name: Optional[pulumi.Input[str]] = None,
            file_system_id: Optional[pulumi.Input[str]] = None,
            security_group_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            vswitch_id: Optional[pulumi.Input[str]] = None) -> 'MountTarget':
        """
        Get an existing MountTarget resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_group_name: The name of the permission group that applies to the mount target.
        :param pulumi.Input[str] file_system_id: The ID of the file system.
        :param pulumi.Input[str] security_group_id: The ID of security group.
        :param pulumi.Input[str] status: Whether the MountTarget is active. The status of the mount target. Valid values: `Active` and `Inactive`, Default value is `Active`. Before you mount a file system, make sure that the mount target is in the Active state.
        :param pulumi.Input[str] vswitch_id: The ID of the VSwitch in the VPC where the mount target resides.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["access_group_name"] = access_group_name
        __props__["file_system_id"] = file_system_id
        __props__["security_group_id"] = security_group_id
        __props__["status"] = status
        __props__["vswitch_id"] = vswitch_id
        return MountTarget(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessGroupName")
    def access_group_name(self) -> pulumi.Output[str]:
        """
        The name of the permission group that applies to the mount target.
        """
        return pulumi.get(self, "access_group_name")

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> pulumi.Output[str]:
        """
        The ID of the file system.
        """
        return pulumi.get(self, "file_system_id")

    @property
    @pulumi.getter(name="securityGroupId")
    def security_group_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of security group.
        """
        return pulumi.get(self, "security_group_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Whether the MountTarget is active. The status of the mount target. Valid values: `Active` and `Inactive`, Default value is `Active`. Before you mount a file system, make sure that the mount target is in the Active state.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the VSwitch in the VPC where the mount target resides.
        """
        return pulumi.get(self, "vswitch_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

