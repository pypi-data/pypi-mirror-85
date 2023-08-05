# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['SecretBackend']


class SecretBackend(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_uri: Optional[pulumi.Input[str]] = None,
                 default_lease_ttl_seconds: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 max_lease_ttl_seconds: Optional[pulumi.Input[int]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 verify_connection: Optional[pulumi.Input[bool]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Create a SecretBackend resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_uri: Specifies the RabbitMQ connection URI.
        :param pulumi.Input[int] default_lease_ttl_seconds: The default TTL for credentials
               issued by this backend.
        :param pulumi.Input[str] description: A human-friendly description for this backend.
        :param pulumi.Input[int] max_lease_ttl_seconds: The maximum TTL that can be requested
               for credentials issued by this backend.
        :param pulumi.Input[str] password: Specifies the RabbitMQ management administrator password.
        :param pulumi.Input[str] path: The unique path this backend should be mounted at. Must
               not begin or end with a `/`. Defaults to `aws`.
        :param pulumi.Input[str] username: Specifies the RabbitMQ management administrator username.
        :param pulumi.Input[bool] verify_connection: Specifies whether to verify connection URI, username, and password.
               Defaults to `true`.
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

            if connection_uri is None:
                raise TypeError("Missing required property 'connection_uri'")
            __props__['connection_uri'] = connection_uri
            __props__['default_lease_ttl_seconds'] = default_lease_ttl_seconds
            __props__['description'] = description
            __props__['max_lease_ttl_seconds'] = max_lease_ttl_seconds
            if password is None:
                raise TypeError("Missing required property 'password'")
            __props__['password'] = password
            __props__['path'] = path
            if username is None:
                raise TypeError("Missing required property 'username'")
            __props__['username'] = username
            __props__['verify_connection'] = verify_connection
        super(SecretBackend, __self__).__init__(
            'vault:rabbitMq/secretBackend:SecretBackend',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            connection_uri: Optional[pulumi.Input[str]] = None,
            default_lease_ttl_seconds: Optional[pulumi.Input[int]] = None,
            description: Optional[pulumi.Input[str]] = None,
            max_lease_ttl_seconds: Optional[pulumi.Input[int]] = None,
            password: Optional[pulumi.Input[str]] = None,
            path: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None,
            verify_connection: Optional[pulumi.Input[bool]] = None) -> 'SecretBackend':
        """
        Get an existing SecretBackend resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_uri: Specifies the RabbitMQ connection URI.
        :param pulumi.Input[int] default_lease_ttl_seconds: The default TTL for credentials
               issued by this backend.
        :param pulumi.Input[str] description: A human-friendly description for this backend.
        :param pulumi.Input[int] max_lease_ttl_seconds: The maximum TTL that can be requested
               for credentials issued by this backend.
        :param pulumi.Input[str] password: Specifies the RabbitMQ management administrator password.
        :param pulumi.Input[str] path: The unique path this backend should be mounted at. Must
               not begin or end with a `/`. Defaults to `aws`.
        :param pulumi.Input[str] username: Specifies the RabbitMQ management administrator username.
        :param pulumi.Input[bool] verify_connection: Specifies whether to verify connection URI, username, and password.
               Defaults to `true`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["connection_uri"] = connection_uri
        __props__["default_lease_ttl_seconds"] = default_lease_ttl_seconds
        __props__["description"] = description
        __props__["max_lease_ttl_seconds"] = max_lease_ttl_seconds
        __props__["password"] = password
        __props__["path"] = path
        __props__["username"] = username
        __props__["verify_connection"] = verify_connection
        return SecretBackend(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionUri")
    def connection_uri(self) -> pulumi.Output[str]:
        """
        Specifies the RabbitMQ connection URI.
        """
        return pulumi.get(self, "connection_uri")

    @property
    @pulumi.getter(name="defaultLeaseTtlSeconds")
    def default_lease_ttl_seconds(self) -> pulumi.Output[int]:
        """
        The default TTL for credentials
        issued by this backend.
        """
        return pulumi.get(self, "default_lease_ttl_seconds")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A human-friendly description for this backend.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="maxLeaseTtlSeconds")
    def max_lease_ttl_seconds(self) -> pulumi.Output[int]:
        """
        The maximum TTL that can be requested
        for credentials issued by this backend.
        """
        return pulumi.get(self, "max_lease_ttl_seconds")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        """
        Specifies the RabbitMQ management administrator password.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[Optional[str]]:
        """
        The unique path this backend should be mounted at. Must
        not begin or end with a `/`. Defaults to `aws`.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        """
        Specifies the RabbitMQ management administrator username.
        """
        return pulumi.get(self, "username")

    @property
    @pulumi.getter(name="verifyConnection")
    def verify_connection(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to verify connection URI, username, and password.
        Defaults to `true`.
        """
        return pulumi.get(self, "verify_connection")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

