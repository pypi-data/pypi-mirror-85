# coding: utf-8

"""
    Stencila Hub API

    ## Authentication  Many endpoints in the Stencila Hub API require an authentication token. These tokens carry many privileges, so be sure to keep them secure. Do not place your tokens in publicly accessible areas such as client-side code. The API is only served over HTTPS to avoid exposing tokens and other data on the network.  To obtain a token, [`POST /api/tokens`](#operations-tokens-tokens_create) with either a `username` and `password` pair, or an [OpenID Connect](https://openid.net/connect/) token. Then use the token in the `Authorization` header of subsequent requests with the prefix `Token` e.g.      curl -H \"Authorization: Token 48866b1e38a2e9db0baada2140b2327937f4a3636dd5f2dfd8c212341c88d34\" https://hub.stenci.la/api/projects/  Alternatively, you can use `Basic` authentication with the token used as the username and no password. This can be more convenient when using command line tools such as [cURL](https://curl.haxx.se/) e.g.      curl -u 48866b1e38a2e9db0baada2140b2327937f4a3636dd5f2dfd8c212341c88d34: https://hub.stenci.la/api/projects/  Or, the less ubiquitous, but more accessible [httpie](https://httpie.org/):      http --auth 48866b1e38a2e9db0baada2140b2327937f4a3636dd5f2dfd8c212341c88d34: https://hub.stenci.la/api/projects/  In both examples above, the trailing colon is not required but avoids being asked for a password.  ## Versioning  The Stencila Hub is released using semantic versioning. The current version is available from the [`GET /api/status`](/api/status) endpoint. Please see the [Github release page](https://github.com/stencila/hub/releases) and the [changelog](https://github.com/stencila/hub/blob/master/CHANGELOG.md) for details on each release. We currently do not provide versioning of the API but plan to do so soon (probably by using a `Accept: application/vnd.stencila.hub+json;version=1.0` request header). If you are using, or interested in using, the API please contact us and we may be able to expedite this.   # noqa: E501

    The version of the OpenAPI document: v1
    Contact: hello@stenci.la
    Generated by: https://openapi-generator.tech
"""


import inspect
import pprint
import re  # noqa: F401
import six

from stencila.hub.configuration import Configuration


class InlineObject7(object):
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
        'project': 'int',
        'app': 'str',
        'host': 'str',
        'node': 'object'
    }

    attribute_map = {
        'project': 'project',
        'app': 'app',
        'host': 'host',
        'node': 'node'
    }

    def __init__(self, project=None, app=None, host=None, node=None, local_vars_configuration=None):  # noqa: E501
        """InlineObject7 - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._project = None
        self._app = None
        self._host = None
        self._node = None
        self.discriminator = None

        self.project = project
        self.app = app
        self.host = host
        self.node = node

    @property
    def project(self):
        """Gets the project of this InlineObject7.  # noqa: E501

        The project this node is associated with.  # noqa: E501

        :return: The project of this InlineObject7.  # noqa: E501
        :rtype: int
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this InlineObject7.

        The project this node is associated with.  # noqa: E501

        :param project: The project of this InlineObject7.  # noqa: E501
        :type project: int
        """

        self._project = project

    @property
    def app(self):
        """Gets the app of this InlineObject7.  # noqa: E501

        An identifier for the app that created the node.  # noqa: E501

        :return: The app of this InlineObject7.  # noqa: E501
        :rtype: str
        """
        return self._app

    @app.setter
    def app(self, app):
        """Sets the app of this InlineObject7.

        An identifier for the app that created the node.  # noqa: E501

        :param app: The app of this InlineObject7.  # noqa: E501
        :type app: str
        """

        self._app = app

    @property
    def host(self):
        """Gets the host of this InlineObject7.  # noqa: E501

        URL of the host document within which the node was created.  # noqa: E501

        :return: The host of this InlineObject7.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this InlineObject7.

        URL of the host document within which the node was created.  # noqa: E501

        :param host: The host of this InlineObject7.  # noqa: E501
        :type host: str
        """
        if (self.local_vars_configuration.client_side_validation and
                host is not None and len(host) > 200):
            raise ValueError("Invalid value for `host`, length must be less than or equal to `200`")  # noqa: E501

        self._host = host

    @property
    def node(self):
        """Gets the node of this InlineObject7.  # noqa: E501

        The node itself.  # noqa: E501

        :return: The node of this InlineObject7.  # noqa: E501
        :rtype: object
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this InlineObject7.

        The node itself.  # noqa: E501

        :param node: The node of this InlineObject7.  # noqa: E501
        :type node: object
        """
        if self.local_vars_configuration.client_side_validation and node is None:  # noqa: E501
            raise ValueError("Invalid value for `node`, must not be `None`")  # noqa: E501

        self._node = node

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = inspect.getargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, InlineObject7):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineObject7):
            return True

        return self.to_dict() != other.to_dict()
