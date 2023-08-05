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


class Snapshot(object):
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
        'id': 'str',
        'number': 'int',
        'created': 'datetime',
        'path': 'str',
        'zip_name': 'str',
        'container_image': 'str',
        'creator': 'int',
        'job': 'int'
    }

    attribute_map = {
        'id': 'id',
        'number': 'number',
        'created': 'created',
        'path': 'path',
        'zip_name': 'zipName',
        'container_image': 'containerImage',
        'creator': 'creator',
        'job': 'job'
    }

    def __init__(self, id=None, number=None, created=None, path=None, zip_name=None, container_image=None, creator=None, job=None, local_vars_configuration=None):  # noqa: E501
        """Snapshot - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._number = None
        self._created = None
        self._path = None
        self._zip_name = None
        self._container_image = None
        self._creator = None
        self._job = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if number is not None:
            self.number = number
        if created is not None:
            self.created = created
        self.path = path
        self.zip_name = zip_name
        if container_image is not None:
            self.container_image = container_image
        if creator is not None:
            self.creator = creator
        if job is not None:
            self.job = job

    @property
    def id(self):
        """Gets the id of this Snapshot.  # noqa: E501

        The unique id of the snapshot.  # noqa: E501

        :return: The id of this Snapshot.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Snapshot.

        The unique id of the snapshot.  # noqa: E501

        :param id: The id of this Snapshot.  # noqa: E501
        :type id: str
        """
        if (self.local_vars_configuration.client_side_validation and
                id is not None and len(id) < 1):
            raise ValueError("Invalid value for `id`, length must be greater than or equal to `1`")  # noqa: E501

        self._id = id

    @property
    def number(self):
        """Gets the number of this Snapshot.  # noqa: E501

        The number of the snapshot within the project.  # noqa: E501

        :return: The number of this Snapshot.  # noqa: E501
        :rtype: int
        """
        return self._number

    @number.setter
    def number(self, number):
        """Sets the number of this Snapshot.

        The number of the snapshot within the project.  # noqa: E501

        :param number: The number of this Snapshot.  # noqa: E501
        :type number: int
        """

        self._number = number

    @property
    def created(self):
        """Gets the created of this Snapshot.  # noqa: E501

        The time the snapshot was created.  # noqa: E501

        :return: The created of this Snapshot.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Snapshot.

        The time the snapshot was created.  # noqa: E501

        :param created: The created of this Snapshot.  # noqa: E501
        :type created: datetime
        """

        self._created = created

    @property
    def path(self):
        """Gets the path of this Snapshot.  # noqa: E501

        The path of the snapshot's directory within the snapshot storage volume.  # noqa: E501

        :return: The path of this Snapshot.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this Snapshot.

        The path of the snapshot's directory within the snapshot storage volume.  # noqa: E501

        :param path: The path of this Snapshot.  # noqa: E501
        :type path: str
        """
        if (self.local_vars_configuration.client_side_validation and
                path is not None and len(path) > 1024):
            raise ValueError("Invalid value for `path`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                path is not None and len(path) < 1):
            raise ValueError("Invalid value for `path`, length must be greater than or equal to `1`")  # noqa: E501

        self._path = path

    @property
    def zip_name(self):
        """Gets the zip_name of this Snapshot.  # noqa: E501

        The name of snapshot's Zip file (within the snapshot directory).  # noqa: E501

        :return: The zip_name of this Snapshot.  # noqa: E501
        :rtype: str
        """
        return self._zip_name

    @zip_name.setter
    def zip_name(self, zip_name):
        """Sets the zip_name of this Snapshot.

        The name of snapshot's Zip file (within the snapshot directory).  # noqa: E501

        :param zip_name: The zip_name of this Snapshot.  # noqa: E501
        :type zip_name: str
        """
        if (self.local_vars_configuration.client_side_validation and
                zip_name is not None and len(zip_name) > 1024):
            raise ValueError("Invalid value for `zip_name`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                zip_name is not None and len(zip_name) < 1):
            raise ValueError("Invalid value for `zip_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._zip_name = zip_name

    @property
    def container_image(self):
        """Gets the container_image of this Snapshot.  # noqa: E501

        The container image to use as the execution environment for this snapshot.  # noqa: E501

        :return: The container_image of this Snapshot.  # noqa: E501
        :rtype: str
        """
        return self._container_image

    @container_image.setter
    def container_image(self, container_image):
        """Sets the container_image of this Snapshot.

        The container image to use as the execution environment for this snapshot.  # noqa: E501

        :param container_image: The container_image of this Snapshot.  # noqa: E501
        :type container_image: str
        """
        if (self.local_vars_configuration.client_side_validation and
                container_image is not None and len(container_image) < 1):
            raise ValueError("Invalid value for `container_image`, length must be greater than or equal to `1`")  # noqa: E501

        self._container_image = container_image

    @property
    def creator(self):
        """Gets the creator of this Snapshot.  # noqa: E501

        The user who created the snapshot.  # noqa: E501

        :return: The creator of this Snapshot.  # noqa: E501
        :rtype: int
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this Snapshot.

        The user who created the snapshot.  # noqa: E501

        :param creator: The creator of this Snapshot.  # noqa: E501
        :type creator: int
        """

        self._creator = creator

    @property
    def job(self):
        """Gets the job of this Snapshot.  # noqa: E501

        The job that created the snapshot  # noqa: E501

        :return: The job of this Snapshot.  # noqa: E501
        :rtype: int
        """
        return self._job

    @job.setter
    def job(self, job):
        """Sets the job of this Snapshot.

        The job that created the snapshot  # noqa: E501

        :param job: The job of this Snapshot.  # noqa: E501
        :type job: int
        """

        self._job = job

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
        if not isinstance(other, Snapshot):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Snapshot):
            return True

        return self.to_dict() != other.to_dict()
