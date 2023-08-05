# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_container.configuration import Configuration


class ContainerContainerDistributionResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'content_guard': 'str',
        'pulp_href': 'str',
        'pulp_created': 'datetime',
        'base_path': 'str',
        'name': 'str',
        'repository_version': 'str',
        'repository': 'str',
        'registry_path': 'str',
        'namespace': 'str'
    }

    attribute_map = {
        'content_guard': 'content_guard',
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'base_path': 'base_path',
        'name': 'name',
        'repository_version': 'repository_version',
        'repository': 'repository',
        'registry_path': 'registry_path',
        'namespace': 'namespace'
    }

    def __init__(self, content_guard=None, pulp_href=None, pulp_created=None, base_path=None, name=None, repository_version=None, repository=None, registry_path=None, namespace=None, local_vars_configuration=None):  # noqa: E501
        """ContainerContainerDistributionResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._content_guard = None
        self._pulp_href = None
        self._pulp_created = None
        self._base_path = None
        self._name = None
        self._repository_version = None
        self._repository = None
        self._registry_path = None
        self._namespace = None
        self.discriminator = None

        if content_guard is not None:
            self.content_guard = content_guard
        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        self.base_path = base_path
        self.name = name
        self.repository_version = repository_version
        self.repository = repository
        if registry_path is not None:
            self.registry_path = registry_path
        if namespace is not None:
            self.namespace = namespace

    @property
    def content_guard(self):
        """Gets the content_guard of this ContainerContainerDistributionResponse.  # noqa: E501

        An optional content-guard. If none is specified, a default one will be used.  # noqa: E501

        :return: The content_guard of this ContainerContainerDistributionResponse.  # noqa: E501
        :rtype: str
        """
        return self._content_guard

    @content_guard.setter
    def content_guard(self, content_guard):
        """Sets the content_guard of this ContainerContainerDistributionResponse.

        An optional content-guard. If none is specified, a default one will be used.  # noqa: E501

        :param content_guard: The content_guard of this ContainerContainerDistributionResponse.  # noqa: E501
        :type: str
        """

        self._content_guard = content_guard

    @property
    def pulp_href(self):
        """Gets the pulp_href of this ContainerContainerDistributionResponse.  # noqa: E501


        :return: The pulp_href of this ContainerContainerDistributionResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this ContainerContainerDistributionResponse.


        :param pulp_href: The pulp_href of this ContainerContainerDistributionResponse.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this ContainerContainerDistributionResponse.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this ContainerContainerDistributionResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this ContainerContainerDistributionResponse.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this ContainerContainerDistributionResponse.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def base_path(self):
        """Gets the base_path of this ContainerContainerDistributionResponse.  # noqa: E501

        The base (relative) path component of the published url. Avoid paths that                     overlap with other distribution base paths (e.g. \"foo\" and \"foo/bar\")  # noqa: E501

        :return: The base_path of this ContainerContainerDistributionResponse.  # noqa: E501
        :rtype: str
        """
        return self._base_path

    @base_path.setter
    def base_path(self, base_path):
        """Sets the base_path of this ContainerContainerDistributionResponse.

        The base (relative) path component of the published url. Avoid paths that                     overlap with other distribution base paths (e.g. \"foo\" and \"foo/bar\")  # noqa: E501

        :param base_path: The base_path of this ContainerContainerDistributionResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and base_path is None:  # noqa: E501
            raise ValueError("Invalid value for `base_path`, must not be `None`")  # noqa: E501

        self._base_path = base_path

    @property
    def name(self):
        """Gets the name of this ContainerContainerDistributionResponse.  # noqa: E501

        A unique name. Ex, `rawhide` and `stable`.  # noqa: E501

        :return: The name of this ContainerContainerDistributionResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ContainerContainerDistributionResponse.

        A unique name. Ex, `rawhide` and `stable`.  # noqa: E501

        :param name: The name of this ContainerContainerDistributionResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def repository_version(self):
        """Gets the repository_version of this ContainerContainerDistributionResponse.  # noqa: E501

        RepositoryVersion to be served  # noqa: E501

        :return: The repository_version of this ContainerContainerDistributionResponse.  # noqa: E501
        :rtype: str
        """
        return self._repository_version

    @repository_version.setter
    def repository_version(self, repository_version):
        """Sets the repository_version of this ContainerContainerDistributionResponse.

        RepositoryVersion to be served  # noqa: E501

        :param repository_version: The repository_version of this ContainerContainerDistributionResponse.  # noqa: E501
        :type: str
        """

        self._repository_version = repository_version

    @property
    def repository(self):
        """Gets the repository of this ContainerContainerDistributionResponse.  # noqa: E501

        The latest RepositoryVersion for this Repository will be served.  # noqa: E501

        :return: The repository of this ContainerContainerDistributionResponse.  # noqa: E501
        :rtype: str
        """
        return self._repository

    @repository.setter
    def repository(self, repository):
        """Sets the repository of this ContainerContainerDistributionResponse.

        The latest RepositoryVersion for this Repository will be served.  # noqa: E501

        :param repository: The repository of this ContainerContainerDistributionResponse.  # noqa: E501
        :type: str
        """

        self._repository = repository

    @property
    def registry_path(self):
        """Gets the registry_path of this ContainerContainerDistributionResponse.  # noqa: E501

        The Registry hostame/name/ to use with docker pull command defined by this distribution.  # noqa: E501

        :return: The registry_path of this ContainerContainerDistributionResponse.  # noqa: E501
        :rtype: str
        """
        return self._registry_path

    @registry_path.setter
    def registry_path(self, registry_path):
        """Sets the registry_path of this ContainerContainerDistributionResponse.

        The Registry hostame/name/ to use with docker pull command defined by this distribution.  # noqa: E501

        :param registry_path: The registry_path of this ContainerContainerDistributionResponse.  # noqa: E501
        :type: str
        """

        self._registry_path = registry_path

    @property
    def namespace(self):
        """Gets the namespace of this ContainerContainerDistributionResponse.  # noqa: E501

        Namespace this distribution belongs to.  # noqa: E501

        :return: The namespace of this ContainerContainerDistributionResponse.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this ContainerContainerDistributionResponse.

        Namespace this distribution belongs to.  # noqa: E501

        :param namespace: The namespace of this ContainerContainerDistributionResponse.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ContainerContainerDistributionResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ContainerContainerDistributionResponse):
            return True

        return self.to_dict() != other.to_dict()
