# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from . import _utilities, _tables

__all__ = [
    'EventHookAuth',
    'EventHookChannel',
    'EventHookHeader',
    'TemplateSmsTranslation',
]

@pulumi.output_type
class EventHookAuth(dict):
    def __init__(__self__, *,
                 key: str,
                 type: str,
                 value: str):
        """
        :param str key: Key to use for authentication, usually the header name, for example `"Authorization"`.
        :param str type: The type of hook to trigger. Currently only `"HTTP"` is supported.
        :param str value: Authentication secret.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Key to use for authentication, usually the header name, for example `"Authorization"`.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of hook to trigger. Currently only `"HTTP"` is supported.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Authentication secret.
        """
        return pulumi.get(self, "value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class EventHookChannel(dict):
    def __init__(__self__, *,
                 type: str,
                 uri: str,
                 version: str):
        """
        :param str type: The type of hook to trigger. Currently only `"HTTP"` is supported.
        :param str uri: The URI the hook will hit.
        :param str version: The version of the channel. Currently only `"1.0.0"` is supported.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "uri", uri)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of hook to trigger. Currently only `"HTTP"` is supported.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        The URI the hook will hit.
        """
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The version of the channel. Currently only `"1.0.0"` is supported.
        """
        return pulumi.get(self, "version")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class EventHookHeader(dict):
    def __init__(__self__, *,
                 key: Optional[str] = None,
                 value: Optional[str] = None):
        """
        :param str key: Key to use for authentication, usually the header name, for example `"Authorization"`.
        :param str value: Authentication secret.
        """
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        Key to use for authentication, usually the header name, for example `"Authorization"`.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        Authentication secret.
        """
        return pulumi.get(self, "value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class TemplateSmsTranslation(dict):
    def __init__(__self__, *,
                 language: str,
                 template: str):
        """
        :param str language: The language to map the template to.
        :param str template: The SMS message.
        """
        pulumi.set(__self__, "language", language)
        pulumi.set(__self__, "template", template)

    @property
    @pulumi.getter
    def language(self) -> str:
        """
        The language to map the template to.
        """
        return pulumi.get(self, "language")

    @property
    @pulumi.getter
    def template(self) -> str:
        """
        The SMS message.
        """
        return pulumi.get(self, "template")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


