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

__all__ = ['AuthBackend']


class AuthBackend(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_url: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 max_ttl: Optional[pulumi.Input[str]] = None,
                 organization: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 token_bound_cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 token_explicit_max_ttl: Optional[pulumi.Input[int]] = None,
                 token_max_ttl: Optional[pulumi.Input[int]] = None,
                 token_no_default_policy: Optional[pulumi.Input[bool]] = None,
                 token_num_uses: Optional[pulumi.Input[int]] = None,
                 token_period: Optional[pulumi.Input[int]] = None,
                 token_policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 token_ttl: Optional[pulumi.Input[int]] = None,
                 token_type: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None,
                 tune: Optional[pulumi.Input[pulumi.InputType['AuthBackendTuneArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a Github Auth mount in a Vault server. See the [Vault
        documentation](https://www.vaultproject.io/docs/auth/github/) for more
        information.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_vault as vault

        example = vault.github.AuthBackend("example", organization="myorg")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] base_url: The API endpoint to use. Useful if you
               are running GitHub Enterprise or an API-compatible authentication server.
        :param pulumi.Input[str] description: Specifies the description of the mount.
               This overrides the current stored value, if any.
        :param pulumi.Input[str] max_ttl: (Optional; Deprecated, use `token_max_ttl` instead if you are running Vault >= 1.2) The maximum allowed lifetime of tokens
               issued using this role. This must be a valid [duration string](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[str] organization: The organization configured users must be part of.
        :param pulumi.Input[str] path: Path where the auth backend is mounted. Defaults to `auth/github`
               if not specified.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] token_bound_cidrs: (Optional) List of CIDR blocks; if set, specifies blocks of IP
               addresses which can authenticate successfully, and ties the resulting token to these blocks
               as well.
        :param pulumi.Input[int] token_explicit_max_ttl: (Optional) If set, will encode an
               [explicit max TTL](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls)
               onto the token in number of seconds. This is a hard cap even if `token_ttl` and
               `token_max_ttl` would otherwise allow a renewal.
        :param pulumi.Input[int] token_max_ttl: (Optional) The maximum lifetime for generated tokens in number of seconds.
               Its current value will be referenced at renewal time.
        :param pulumi.Input[bool] token_no_default_policy: (Optional) If set, the default policy will not be set on
               generated tokens; otherwise it will be added to the policies set in token_policies.
        :param pulumi.Input[int] token_num_uses: (Optional) The
               [period](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls),
               if any, in number of seconds to set on the token.
        :param pulumi.Input[int] token_period: (Optional) If set, indicates that the
               token generated using this role should never expire. The token should be renewed within the
               duration specified by this value. At each renewal, the token's TTL will be set to the
               value of this field. Specified in seconds.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] token_policies: (Optional) List of policies to encode onto generated tokens. Depending
               on the auth method, this list may be supplemented by user/group/other values.
        :param pulumi.Input[int] token_ttl: (Optional) The incremental lifetime for generated tokens in number of seconds.
               Its current value will be referenced at renewal time.
        :param pulumi.Input[str] token_type: Specifies the type of tokens that should be returned by
               the mount. Valid values are "default-service", "default-batch", "service", "batch".
        :param pulumi.Input[str] ttl: (Optional; Deprecated, use `token_ttl` instead if you are running Vault >= 1.2) The TTL period of tokens issued
               using this role. This must be a valid [duration string](https://golang.org/pkg/time/#ParseDuration).
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

            __props__['base_url'] = base_url
            __props__['description'] = description
            if max_ttl is not None:
                warnings.warn("use `token_max_ttl` instead if you are running Vault >= 1.2", DeprecationWarning)
                pulumi.log.warn("max_ttl is deprecated: use `token_max_ttl` instead if you are running Vault >= 1.2")
            __props__['max_ttl'] = max_ttl
            if organization is None:
                raise TypeError("Missing required property 'organization'")
            __props__['organization'] = organization
            __props__['path'] = path
            __props__['token_bound_cidrs'] = token_bound_cidrs
            __props__['token_explicit_max_ttl'] = token_explicit_max_ttl
            __props__['token_max_ttl'] = token_max_ttl
            __props__['token_no_default_policy'] = token_no_default_policy
            __props__['token_num_uses'] = token_num_uses
            __props__['token_period'] = token_period
            __props__['token_policies'] = token_policies
            __props__['token_ttl'] = token_ttl
            __props__['token_type'] = token_type
            if ttl is not None:
                warnings.warn("use `token_ttl` instead if you are running Vault >= 1.2", DeprecationWarning)
                pulumi.log.warn("ttl is deprecated: use `token_ttl` instead if you are running Vault >= 1.2")
            __props__['ttl'] = ttl
            __props__['tune'] = tune
            __props__['accessor'] = None
        super(AuthBackend, __self__).__init__(
            'vault:github/authBackend:AuthBackend',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            accessor: Optional[pulumi.Input[str]] = None,
            base_url: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            max_ttl: Optional[pulumi.Input[str]] = None,
            organization: Optional[pulumi.Input[str]] = None,
            path: Optional[pulumi.Input[str]] = None,
            token_bound_cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            token_explicit_max_ttl: Optional[pulumi.Input[int]] = None,
            token_max_ttl: Optional[pulumi.Input[int]] = None,
            token_no_default_policy: Optional[pulumi.Input[bool]] = None,
            token_num_uses: Optional[pulumi.Input[int]] = None,
            token_period: Optional[pulumi.Input[int]] = None,
            token_policies: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            token_ttl: Optional[pulumi.Input[int]] = None,
            token_type: Optional[pulumi.Input[str]] = None,
            ttl: Optional[pulumi.Input[str]] = None,
            tune: Optional[pulumi.Input[pulumi.InputType['AuthBackendTuneArgs']]] = None) -> 'AuthBackend':
        """
        Get an existing AuthBackend resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] accessor: The mount accessor related to the auth mount. It is useful for integration with [Identity Secrets Engine](https://www.vaultproject.io/docs/secrets/identity/index.html).
        :param pulumi.Input[str] base_url: The API endpoint to use. Useful if you
               are running GitHub Enterprise or an API-compatible authentication server.
        :param pulumi.Input[str] description: Specifies the description of the mount.
               This overrides the current stored value, if any.
        :param pulumi.Input[str] max_ttl: (Optional; Deprecated, use `token_max_ttl` instead if you are running Vault >= 1.2) The maximum allowed lifetime of tokens
               issued using this role. This must be a valid [duration string](https://golang.org/pkg/time/#ParseDuration).
        :param pulumi.Input[str] organization: The organization configured users must be part of.
        :param pulumi.Input[str] path: Path where the auth backend is mounted. Defaults to `auth/github`
               if not specified.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] token_bound_cidrs: (Optional) List of CIDR blocks; if set, specifies blocks of IP
               addresses which can authenticate successfully, and ties the resulting token to these blocks
               as well.
        :param pulumi.Input[int] token_explicit_max_ttl: (Optional) If set, will encode an
               [explicit max TTL](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls)
               onto the token in number of seconds. This is a hard cap even if `token_ttl` and
               `token_max_ttl` would otherwise allow a renewal.
        :param pulumi.Input[int] token_max_ttl: (Optional) The maximum lifetime for generated tokens in number of seconds.
               Its current value will be referenced at renewal time.
        :param pulumi.Input[bool] token_no_default_policy: (Optional) If set, the default policy will not be set on
               generated tokens; otherwise it will be added to the policies set in token_policies.
        :param pulumi.Input[int] token_num_uses: (Optional) The
               [period](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls),
               if any, in number of seconds to set on the token.
        :param pulumi.Input[int] token_period: (Optional) If set, indicates that the
               token generated using this role should never expire. The token should be renewed within the
               duration specified by this value. At each renewal, the token's TTL will be set to the
               value of this field. Specified in seconds.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] token_policies: (Optional) List of policies to encode onto generated tokens. Depending
               on the auth method, this list may be supplemented by user/group/other values.
        :param pulumi.Input[int] token_ttl: (Optional) The incremental lifetime for generated tokens in number of seconds.
               Its current value will be referenced at renewal time.
        :param pulumi.Input[str] token_type: Specifies the type of tokens that should be returned by
               the mount. Valid values are "default-service", "default-batch", "service", "batch".
        :param pulumi.Input[str] ttl: (Optional; Deprecated, use `token_ttl` instead if you are running Vault >= 1.2) The TTL period of tokens issued
               using this role. This must be a valid [duration string](https://golang.org/pkg/time/#ParseDuration).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["accessor"] = accessor
        __props__["base_url"] = base_url
        __props__["description"] = description
        __props__["max_ttl"] = max_ttl
        __props__["organization"] = organization
        __props__["path"] = path
        __props__["token_bound_cidrs"] = token_bound_cidrs
        __props__["token_explicit_max_ttl"] = token_explicit_max_ttl
        __props__["token_max_ttl"] = token_max_ttl
        __props__["token_no_default_policy"] = token_no_default_policy
        __props__["token_num_uses"] = token_num_uses
        __props__["token_period"] = token_period
        __props__["token_policies"] = token_policies
        __props__["token_ttl"] = token_ttl
        __props__["token_type"] = token_type
        __props__["ttl"] = ttl
        __props__["tune"] = tune
        return AuthBackend(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def accessor(self) -> pulumi.Output[str]:
        """
        The mount accessor related to the auth mount. It is useful for integration with [Identity Secrets Engine](https://www.vaultproject.io/docs/secrets/identity/index.html).
        """
        return pulumi.get(self, "accessor")

    @property
    @pulumi.getter(name="baseUrl")
    def base_url(self) -> pulumi.Output[Optional[str]]:
        """
        The API endpoint to use. Useful if you
        are running GitHub Enterprise or an API-compatible authentication server.
        """
        return pulumi.get(self, "base_url")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the description of the mount.
        This overrides the current stored value, if any.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="maxTtl")
    def max_ttl(self) -> pulumi.Output[Optional[str]]:
        """
        (Optional; Deprecated, use `token_max_ttl` instead if you are running Vault >= 1.2) The maximum allowed lifetime of tokens
        issued using this role. This must be a valid [duration string](https://golang.org/pkg/time/#ParseDuration).
        """
        return pulumi.get(self, "max_ttl")

    @property
    @pulumi.getter
    def organization(self) -> pulumi.Output[str]:
        """
        The organization configured users must be part of.
        """
        return pulumi.get(self, "organization")

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[Optional[str]]:
        """
        Path where the auth backend is mounted. Defaults to `auth/github`
        if not specified.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="tokenBoundCidrs")
    def token_bound_cidrs(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        (Optional) List of CIDR blocks; if set, specifies blocks of IP
        addresses which can authenticate successfully, and ties the resulting token to these blocks
        as well.
        """
        return pulumi.get(self, "token_bound_cidrs")

    @property
    @pulumi.getter(name="tokenExplicitMaxTtl")
    def token_explicit_max_ttl(self) -> pulumi.Output[Optional[int]]:
        """
        (Optional) If set, will encode an
        [explicit max TTL](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls)
        onto the token in number of seconds. This is a hard cap even if `token_ttl` and
        `token_max_ttl` would otherwise allow a renewal.
        """
        return pulumi.get(self, "token_explicit_max_ttl")

    @property
    @pulumi.getter(name="tokenMaxTtl")
    def token_max_ttl(self) -> pulumi.Output[Optional[int]]:
        """
        (Optional) The maximum lifetime for generated tokens in number of seconds.
        Its current value will be referenced at renewal time.
        """
        return pulumi.get(self, "token_max_ttl")

    @property
    @pulumi.getter(name="tokenNoDefaultPolicy")
    def token_no_default_policy(self) -> pulumi.Output[Optional[bool]]:
        """
        (Optional) If set, the default policy will not be set on
        generated tokens; otherwise it will be added to the policies set in token_policies.
        """
        return pulumi.get(self, "token_no_default_policy")

    @property
    @pulumi.getter(name="tokenNumUses")
    def token_num_uses(self) -> pulumi.Output[Optional[int]]:
        """
        (Optional) The
        [period](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls),
        if any, in number of seconds to set on the token.
        """
        return pulumi.get(self, "token_num_uses")

    @property
    @pulumi.getter(name="tokenPeriod")
    def token_period(self) -> pulumi.Output[Optional[int]]:
        """
        (Optional) If set, indicates that the
        token generated using this role should never expire. The token should be renewed within the
        duration specified by this value. At each renewal, the token's TTL will be set to the
        value of this field. Specified in seconds.
        """
        return pulumi.get(self, "token_period")

    @property
    @pulumi.getter(name="tokenPolicies")
    def token_policies(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        (Optional) List of policies to encode onto generated tokens. Depending
        on the auth method, this list may be supplemented by user/group/other values.
        """
        return pulumi.get(self, "token_policies")

    @property
    @pulumi.getter(name="tokenTtl")
    def token_ttl(self) -> pulumi.Output[Optional[int]]:
        """
        (Optional) The incremental lifetime for generated tokens in number of seconds.
        Its current value will be referenced at renewal time.
        """
        return pulumi.get(self, "token_ttl")

    @property
    @pulumi.getter(name="tokenType")
    def token_type(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the type of tokens that should be returned by
        the mount. Valid values are "default-service", "default-batch", "service", "batch".
        """
        return pulumi.get(self, "token_type")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[Optional[str]]:
        """
        (Optional; Deprecated, use `token_ttl` instead if you are running Vault >= 1.2) The TTL period of tokens issued
        using this role. This must be a valid [duration string](https://golang.org/pkg/time/#ParseDuration).
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def tune(self) -> pulumi.Output['outputs.AuthBackendTune']:
        return pulumi.get(self, "tune")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

