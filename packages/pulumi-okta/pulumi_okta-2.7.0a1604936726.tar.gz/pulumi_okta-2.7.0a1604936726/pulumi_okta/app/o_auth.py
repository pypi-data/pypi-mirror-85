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

__all__ = ['OAuth']


class OAuth(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_key_rotation: Optional[pulumi.Input[bool]] = None,
                 auto_submit_toolbar: Optional[pulumi.Input[bool]] = None,
                 client_basic_secret: Optional[pulumi.Input[str]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_uri: Optional[pulumi.Input[str]] = None,
                 consent_method: Optional[pulumi.Input[str]] = None,
                 custom_client_id: Optional[pulumi.Input[str]] = None,
                 grant_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 hide_ios: Optional[pulumi.Input[bool]] = None,
                 hide_web: Optional[pulumi.Input[bool]] = None,
                 issuer_mode: Optional[pulumi.Input[str]] = None,
                 jwks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OAuthJwkArgs']]]]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 login_uri: Optional[pulumi.Input[str]] = None,
                 logo_uri: Optional[pulumi.Input[str]] = None,
                 omit_secret: Optional[pulumi.Input[bool]] = None,
                 policy_uri: Optional[pulumi.Input[str]] = None,
                 post_logout_redirect_uris: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 profile: Optional[pulumi.Input[str]] = None,
                 redirect_uris: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 response_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 token_endpoint_auth_method: Optional[pulumi.Input[str]] = None,
                 tos_uri: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OAuthUserArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Creates an OIDC Application.

        This resource allows you to create and configure an OIDC Application.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.app.OAuth("example",
            grant_types=["authorization_code"],
            label="example",
            redirect_uris=["https://example.com/"],
            response_types=["code"],
            type="web")
        ```

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.app.OAuth("example",
            grant_types=["client_credentials"],
            jwks=[okta.app.OAuthJwkArgs(
                e="AQAB",
                kid="SIGNING_KEY",
                kty="RSA",
                n="xyz",
            )],
            label="example",
            response_types=["token"],
            token_endpoint_auth_method="private_key_jwt",
            type="service")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_key_rotation: Requested key rotation mode.
        :param pulumi.Input[bool] auto_submit_toolbar: Display auto submit toolbar.
        :param pulumi.Input[str] client_basic_secret: OAuth client secret key, this can be set when token_endpoint_auth_method is client_secret_basic.
        :param pulumi.Input[str] client_id: OAuth client ID. If set during creation, app is created with this id.
        :param pulumi.Input[str] client_uri: URI to a web page providing information about the client.
        :param pulumi.Input[str] consent_method: Indicates whether user consent is required or implicit. Valid values: REQUIRED, TRUSTED. Default value is TRUSTED.
        :param pulumi.Input[str] custom_client_id: **Deprecated** This property allows you to set your client_id during creation. NOTE: updating after creation will be a
               no-op, use client_id for that behavior instead.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] grant_types: List of OAuth 2.0 grant types. Conditional validation params found here https://developer.okta.com/docs/api/resources/apps#credentials-settings-details. Defaults to minimum requirements per app type.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: The groups assigned to the application. It is recommended not to use this and instead use `app.GroupAssignment`.
        :param pulumi.Input[bool] hide_ios: Do not display application icon on mobile app.
        :param pulumi.Input[bool] hide_web: Do not display application icon to users.
        :param pulumi.Input[str] issuer_mode: Indicates whether the Okta Authorization Server uses the original Okta org domain URL or a custom domain URL as the issuer of ID token for this client.
        :param pulumi.Input[str] label: The Application's display name.
        :param pulumi.Input[str] login_uri: URI that initiates login.
        :param pulumi.Input[str] logo_uri: URI that references a logo for the client.
        :param pulumi.Input[bool] omit_secret: This tells the provider not to persist the application's secret to state. If this is ever changes from true => false your app will be recreated.
        :param pulumi.Input[str] policy_uri: URI to web page providing client policy document.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] post_logout_redirect_uris: List of URIs for redirection after logout.
        :param pulumi.Input[str] profile: Custom JSON that represents an OAuth application's profile.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] redirect_uris: List of URIs for use in the redirect-based flow. This is required for all application types except service.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] response_types: List of OAuth 2.0 response type strings.
        :param pulumi.Input[str] status: The status of the application, by default it is `"ACTIVE"`.
        :param pulumi.Input[str] token_endpoint_auth_method: Requested authentication method for the token endpoint. It can be set to `"none"`, `"client_secret_post"`, `"client_secret_basic"`, `"client_secret_jwt"`, `"private_key_jwt"`.
        :param pulumi.Input[str] tos_uri: URI to web page providing client tos (terms of service).
        :param pulumi.Input[str] type: The type of OAuth application.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OAuthUserArgs']]]] users: The users assigned to the application. It is recommended not to use this and instead use `app.User`.
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

            __props__['auto_key_rotation'] = auto_key_rotation
            __props__['auto_submit_toolbar'] = auto_submit_toolbar
            __props__['client_basic_secret'] = client_basic_secret
            __props__['client_id'] = client_id
            __props__['client_uri'] = client_uri
            __props__['consent_method'] = consent_method
            if custom_client_id is not None:
                warnings.warn("This field is being replaced by client_id. Please set that field instead.", DeprecationWarning)
                pulumi.log.warn("custom_client_id is deprecated: This field is being replaced by client_id. Please set that field instead.")
            __props__['custom_client_id'] = custom_client_id
            __props__['grant_types'] = grant_types
            __props__['groups'] = groups
            __props__['hide_ios'] = hide_ios
            __props__['hide_web'] = hide_web
            __props__['issuer_mode'] = issuer_mode
            __props__['jwks'] = jwks
            if label is None:
                raise TypeError("Missing required property 'label'")
            __props__['label'] = label
            __props__['login_uri'] = login_uri
            __props__['logo_uri'] = logo_uri
            __props__['omit_secret'] = omit_secret
            __props__['policy_uri'] = policy_uri
            __props__['post_logout_redirect_uris'] = post_logout_redirect_uris
            __props__['profile'] = profile
            __props__['redirect_uris'] = redirect_uris
            __props__['response_types'] = response_types
            __props__['status'] = status
            __props__['token_endpoint_auth_method'] = token_endpoint_auth_method
            __props__['tos_uri'] = tos_uri
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
            __props__['users'] = users
            __props__['client_secret'] = None
            __props__['name'] = None
            __props__['sign_on_mode'] = None
        super(OAuth, __self__).__init__(
            'okta:app/oAuth:OAuth',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            auto_key_rotation: Optional[pulumi.Input[bool]] = None,
            auto_submit_toolbar: Optional[pulumi.Input[bool]] = None,
            client_basic_secret: Optional[pulumi.Input[str]] = None,
            client_id: Optional[pulumi.Input[str]] = None,
            client_secret: Optional[pulumi.Input[str]] = None,
            client_uri: Optional[pulumi.Input[str]] = None,
            consent_method: Optional[pulumi.Input[str]] = None,
            custom_client_id: Optional[pulumi.Input[str]] = None,
            grant_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            hide_ios: Optional[pulumi.Input[bool]] = None,
            hide_web: Optional[pulumi.Input[bool]] = None,
            issuer_mode: Optional[pulumi.Input[str]] = None,
            jwks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OAuthJwkArgs']]]]] = None,
            label: Optional[pulumi.Input[str]] = None,
            login_uri: Optional[pulumi.Input[str]] = None,
            logo_uri: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            omit_secret: Optional[pulumi.Input[bool]] = None,
            policy_uri: Optional[pulumi.Input[str]] = None,
            post_logout_redirect_uris: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            profile: Optional[pulumi.Input[str]] = None,
            redirect_uris: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            response_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            sign_on_mode: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            token_endpoint_auth_method: Optional[pulumi.Input[str]] = None,
            tos_uri: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            users: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OAuthUserArgs']]]]] = None) -> 'OAuth':
        """
        Get an existing OAuth resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_key_rotation: Requested key rotation mode.
        :param pulumi.Input[bool] auto_submit_toolbar: Display auto submit toolbar.
        :param pulumi.Input[str] client_basic_secret: OAuth client secret key, this can be set when token_endpoint_auth_method is client_secret_basic.
        :param pulumi.Input[str] client_id: OAuth client ID. If set during creation, app is created with this id.
        :param pulumi.Input[str] client_secret: The client secret of the application.
        :param pulumi.Input[str] client_uri: URI to a web page providing information about the client.
        :param pulumi.Input[str] consent_method: Indicates whether user consent is required or implicit. Valid values: REQUIRED, TRUSTED. Default value is TRUSTED.
        :param pulumi.Input[str] custom_client_id: **Deprecated** This property allows you to set your client_id during creation. NOTE: updating after creation will be a
               no-op, use client_id for that behavior instead.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] grant_types: List of OAuth 2.0 grant types. Conditional validation params found here https://developer.okta.com/docs/api/resources/apps#credentials-settings-details. Defaults to minimum requirements per app type.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: The groups assigned to the application. It is recommended not to use this and instead use `app.GroupAssignment`.
        :param pulumi.Input[bool] hide_ios: Do not display application icon on mobile app.
        :param pulumi.Input[bool] hide_web: Do not display application icon to users.
        :param pulumi.Input[str] issuer_mode: Indicates whether the Okta Authorization Server uses the original Okta org domain URL or a custom domain URL as the issuer of ID token for this client.
        :param pulumi.Input[str] label: The Application's display name.
        :param pulumi.Input[str] login_uri: URI that initiates login.
        :param pulumi.Input[str] logo_uri: URI that references a logo for the client.
        :param pulumi.Input[str] name: Name assigned to the application by Okta.
        :param pulumi.Input[bool] omit_secret: This tells the provider not to persist the application's secret to state. If this is ever changes from true => false your app will be recreated.
        :param pulumi.Input[str] policy_uri: URI to web page providing client policy document.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] post_logout_redirect_uris: List of URIs for redirection after logout.
        :param pulumi.Input[str] profile: Custom JSON that represents an OAuth application's profile.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] redirect_uris: List of URIs for use in the redirect-based flow. This is required for all application types except service.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] response_types: List of OAuth 2.0 response type strings.
        :param pulumi.Input[str] sign_on_mode: Sign on mode of application.
        :param pulumi.Input[str] status: The status of the application, by default it is `"ACTIVE"`.
        :param pulumi.Input[str] token_endpoint_auth_method: Requested authentication method for the token endpoint. It can be set to `"none"`, `"client_secret_post"`, `"client_secret_basic"`, `"client_secret_jwt"`, `"private_key_jwt"`.
        :param pulumi.Input[str] tos_uri: URI to web page providing client tos (terms of service).
        :param pulumi.Input[str] type: The type of OAuth application.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OAuthUserArgs']]]] users: The users assigned to the application. It is recommended not to use this and instead use `app.User`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["auto_key_rotation"] = auto_key_rotation
        __props__["auto_submit_toolbar"] = auto_submit_toolbar
        __props__["client_basic_secret"] = client_basic_secret
        __props__["client_id"] = client_id
        __props__["client_secret"] = client_secret
        __props__["client_uri"] = client_uri
        __props__["consent_method"] = consent_method
        __props__["custom_client_id"] = custom_client_id
        __props__["grant_types"] = grant_types
        __props__["groups"] = groups
        __props__["hide_ios"] = hide_ios
        __props__["hide_web"] = hide_web
        __props__["issuer_mode"] = issuer_mode
        __props__["jwks"] = jwks
        __props__["label"] = label
        __props__["login_uri"] = login_uri
        __props__["logo_uri"] = logo_uri
        __props__["name"] = name
        __props__["omit_secret"] = omit_secret
        __props__["policy_uri"] = policy_uri
        __props__["post_logout_redirect_uris"] = post_logout_redirect_uris
        __props__["profile"] = profile
        __props__["redirect_uris"] = redirect_uris
        __props__["response_types"] = response_types
        __props__["sign_on_mode"] = sign_on_mode
        __props__["status"] = status
        __props__["token_endpoint_auth_method"] = token_endpoint_auth_method
        __props__["tos_uri"] = tos_uri
        __props__["type"] = type
        __props__["users"] = users
        return OAuth(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoKeyRotation")
    def auto_key_rotation(self) -> pulumi.Output[Optional[bool]]:
        """
        Requested key rotation mode.
        """
        return pulumi.get(self, "auto_key_rotation")

    @property
    @pulumi.getter(name="autoSubmitToolbar")
    def auto_submit_toolbar(self) -> pulumi.Output[Optional[bool]]:
        """
        Display auto submit toolbar.
        """
        return pulumi.get(self, "auto_submit_toolbar")

    @property
    @pulumi.getter(name="clientBasicSecret")
    def client_basic_secret(self) -> pulumi.Output[Optional[str]]:
        """
        OAuth client secret key, this can be set when token_endpoint_auth_method is client_secret_basic.
        """
        return pulumi.get(self, "client_basic_secret")

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Output[str]:
        """
        OAuth client ID. If set during creation, app is created with this id.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> pulumi.Output[str]:
        """
        The client secret of the application.
        """
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="clientUri")
    def client_uri(self) -> pulumi.Output[Optional[str]]:
        """
        URI to a web page providing information about the client.
        """
        return pulumi.get(self, "client_uri")

    @property
    @pulumi.getter(name="consentMethod")
    def consent_method(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates whether user consent is required or implicit. Valid values: REQUIRED, TRUSTED. Default value is TRUSTED.
        """
        return pulumi.get(self, "consent_method")

    @property
    @pulumi.getter(name="customClientId")
    def custom_client_id(self) -> pulumi.Output[Optional[str]]:
        """
        **Deprecated** This property allows you to set your client_id during creation. NOTE: updating after creation will be a
        no-op, use client_id for that behavior instead.
        """
        return pulumi.get(self, "custom_client_id")

    @property
    @pulumi.getter(name="grantTypes")
    def grant_types(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of OAuth 2.0 grant types. Conditional validation params found here https://developer.okta.com/docs/api/resources/apps#credentials-settings-details. Defaults to minimum requirements per app type.
        """
        return pulumi.get(self, "grant_types")

    @property
    @pulumi.getter
    def groups(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The groups assigned to the application. It is recommended not to use this and instead use `app.GroupAssignment`.
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter(name="hideIos")
    def hide_ios(self) -> pulumi.Output[Optional[bool]]:
        """
        Do not display application icon on mobile app.
        """
        return pulumi.get(self, "hide_ios")

    @property
    @pulumi.getter(name="hideWeb")
    def hide_web(self) -> pulumi.Output[Optional[bool]]:
        """
        Do not display application icon to users.
        """
        return pulumi.get(self, "hide_web")

    @property
    @pulumi.getter(name="issuerMode")
    def issuer_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates whether the Okta Authorization Server uses the original Okta org domain URL or a custom domain URL as the issuer of ID token for this client.
        """
        return pulumi.get(self, "issuer_mode")

    @property
    @pulumi.getter
    def jwks(self) -> pulumi.Output[Optional[Sequence['outputs.OAuthJwk']]]:
        return pulumi.get(self, "jwks")

    @property
    @pulumi.getter
    def label(self) -> pulumi.Output[str]:
        """
        The Application's display name.
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter(name="loginUri")
    def login_uri(self) -> pulumi.Output[Optional[str]]:
        """
        URI that initiates login.
        """
        return pulumi.get(self, "login_uri")

    @property
    @pulumi.getter(name="logoUri")
    def logo_uri(self) -> pulumi.Output[Optional[str]]:
        """
        URI that references a logo for the client.
        """
        return pulumi.get(self, "logo_uri")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name assigned to the application by Okta.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="omitSecret")
    def omit_secret(self) -> pulumi.Output[Optional[bool]]:
        """
        This tells the provider not to persist the application's secret to state. If this is ever changes from true => false your app will be recreated.
        """
        return pulumi.get(self, "omit_secret")

    @property
    @pulumi.getter(name="policyUri")
    def policy_uri(self) -> pulumi.Output[Optional[str]]:
        """
        URI to web page providing client policy document.
        """
        return pulumi.get(self, "policy_uri")

    @property
    @pulumi.getter(name="postLogoutRedirectUris")
    def post_logout_redirect_uris(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of URIs for redirection after logout.
        """
        return pulumi.get(self, "post_logout_redirect_uris")

    @property
    @pulumi.getter
    def profile(self) -> pulumi.Output[Optional[str]]:
        """
        Custom JSON that represents an OAuth application's profile.
        """
        return pulumi.get(self, "profile")

    @property
    @pulumi.getter(name="redirectUris")
    def redirect_uris(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of URIs for use in the redirect-based flow. This is required for all application types except service.
        """
        return pulumi.get(self, "redirect_uris")

    @property
    @pulumi.getter(name="responseTypes")
    def response_types(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of OAuth 2.0 response type strings.
        """
        return pulumi.get(self, "response_types")

    @property
    @pulumi.getter(name="signOnMode")
    def sign_on_mode(self) -> pulumi.Output[str]:
        """
        Sign on mode of application.
        """
        return pulumi.get(self, "sign_on_mode")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        The status of the application, by default it is `"ACTIVE"`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="tokenEndpointAuthMethod")
    def token_endpoint_auth_method(self) -> pulumi.Output[Optional[str]]:
        """
        Requested authentication method for the token endpoint. It can be set to `"none"`, `"client_secret_post"`, `"client_secret_basic"`, `"client_secret_jwt"`, `"private_key_jwt"`.
        """
        return pulumi.get(self, "token_endpoint_auth_method")

    @property
    @pulumi.getter(name="tosUri")
    def tos_uri(self) -> pulumi.Output[Optional[str]]:
        """
        URI to web page providing client tos (terms of service).
        """
        return pulumi.get(self, "tos_uri")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of OAuth application.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def users(self) -> pulumi.Output[Optional[Sequence['outputs.OAuthUser']]]:
        """
        The users assigned to the application. It is recommended not to use this and instead use `app.User`.
        """
        return pulumi.get(self, "users")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

