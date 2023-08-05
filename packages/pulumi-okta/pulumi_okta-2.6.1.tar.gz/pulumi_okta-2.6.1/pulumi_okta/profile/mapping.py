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

__all__ = ['Mapping']


class Mapping(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delete_when_absent: Optional[pulumi.Input[bool]] = None,
                 mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MappingMappingArgs']]]]] = None,
                 source_id: Optional[pulumi.Input[str]] = None,
                 target_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a profile mapping.

        This resource allows you to manage a profile mapping by source id.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        user = okta.user.get_user_profile_mapping_source()
        example = okta.profile.Mapping("example",
            delete_when_absent=True,
            mappings=[
                okta.profile.MappingMappingArgs(
                    expression="appuser.firstName",
                    id="firstName",
                ),
                okta.profile.MappingMappingArgs(
                    expression="appuser.lastName",
                    id="lastName",
                ),
                okta.profile.MappingMappingArgs(
                    expression="appuser.email",
                    id="email",
                ),
                okta.profile.MappingMappingArgs(
                    expression="appuser.email",
                    id="login",
                ),
            ],
            source_id="<source id>",
            target_id=user.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] delete_when_absent: Tells the provider whether to attempt to delete missing mappings under profile mapping.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MappingMappingArgs']]]] mappings: Priority of the policy.
        :param pulumi.Input[str] source_id: Source id of the profile mapping.
        :param pulumi.Input[str] target_id: ID of the mapping target.
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

            __props__['delete_when_absent'] = delete_when_absent
            __props__['mappings'] = mappings
            if source_id is None:
                raise TypeError("Missing required property 'source_id'")
            __props__['source_id'] = source_id
            if target_id is None:
                raise TypeError("Missing required property 'target_id'")
            __props__['target_id'] = target_id
            __props__['source_name'] = None
            __props__['source_type'] = None
            __props__['target_name'] = None
            __props__['target_type'] = None
        super(Mapping, __self__).__init__(
            'okta:profile/mapping:Mapping',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            delete_when_absent: Optional[pulumi.Input[bool]] = None,
            mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MappingMappingArgs']]]]] = None,
            source_id: Optional[pulumi.Input[str]] = None,
            source_name: Optional[pulumi.Input[str]] = None,
            source_type: Optional[pulumi.Input[str]] = None,
            target_id: Optional[pulumi.Input[str]] = None,
            target_name: Optional[pulumi.Input[str]] = None,
            target_type: Optional[pulumi.Input[str]] = None) -> 'Mapping':
        """
        Get an existing Mapping resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] delete_when_absent: Tells the provider whether to attempt to delete missing mappings under profile mapping.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MappingMappingArgs']]]] mappings: Priority of the policy.
        :param pulumi.Input[str] source_id: Source id of the profile mapping.
        :param pulumi.Input[str] source_name: Name of the mapping source.
        :param pulumi.Input[str] source_type: ID of the mapping source.
        :param pulumi.Input[str] target_id: ID of the mapping target.
        :param pulumi.Input[str] target_name: Name of the mapping target.
        :param pulumi.Input[str] target_type: ID of the mapping target.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["delete_when_absent"] = delete_when_absent
        __props__["mappings"] = mappings
        __props__["source_id"] = source_id
        __props__["source_name"] = source_name
        __props__["source_type"] = source_type
        __props__["target_id"] = target_id
        __props__["target_name"] = target_name
        __props__["target_type"] = target_type
        return Mapping(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deleteWhenAbsent")
    def delete_when_absent(self) -> pulumi.Output[Optional[bool]]:
        """
        Tells the provider whether to attempt to delete missing mappings under profile mapping.
        """
        return pulumi.get(self, "delete_when_absent")

    @property
    @pulumi.getter
    def mappings(self) -> pulumi.Output[Optional[Sequence['outputs.MappingMapping']]]:
        """
        Priority of the policy.
        """
        return pulumi.get(self, "mappings")

    @property
    @pulumi.getter(name="sourceId")
    def source_id(self) -> pulumi.Output[str]:
        """
        Source id of the profile mapping.
        """
        return pulumi.get(self, "source_id")

    @property
    @pulumi.getter(name="sourceName")
    def source_name(self) -> pulumi.Output[str]:
        """
        Name of the mapping source.
        """
        return pulumi.get(self, "source_name")

    @property
    @pulumi.getter(name="sourceType")
    def source_type(self) -> pulumi.Output[str]:
        """
        ID of the mapping source.
        """
        return pulumi.get(self, "source_type")

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> pulumi.Output[str]:
        """
        ID of the mapping target.
        """
        return pulumi.get(self, "target_id")

    @property
    @pulumi.getter(name="targetName")
    def target_name(self) -> pulumi.Output[str]:
        """
        Name of the mapping target.
        """
        return pulumi.get(self, "target_name")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Output[str]:
        """
        ID of the mapping target.
        """
        return pulumi.get(self, "target_type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

