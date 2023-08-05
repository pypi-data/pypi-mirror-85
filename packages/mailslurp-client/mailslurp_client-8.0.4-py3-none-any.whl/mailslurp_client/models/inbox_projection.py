# coding: utf-8

"""
    MailSlurp API

    MailSlurp is an API for sending and receiving emails from dynamically allocated email addresses. It's designed for developers and QA teams to test applications, process inbound emails, send templated notifications, attachments, and more.   ## Resources - [Homepage](https://www.mailslurp.com) - Get an [API KEY](https://app.mailslurp.com/sign-up/) - Generated [SDK Clients](https://www.mailslurp.com/docs/) - [Examples](https://github.com/mailslurp/examples) repository   # noqa: E501

    The version of the OpenAPI document: 6.5.2
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from mailslurp_client.configuration import Configuration


class InboxProjection(object):
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
        'created_at': 'datetime',
        'email_address': 'str',
        'favourite': 'bool',
        'id': 'str',
        'name': 'str',
        'tags': 'list[str]'
    }

    attribute_map = {
        'created_at': 'createdAt',
        'email_address': 'emailAddress',
        'favourite': 'favourite',
        'id': 'id',
        'name': 'name',
        'tags': 'tags'
    }

    def __init__(self, created_at=None, email_address=None, favourite=None, id=None, name=None, tags=None, local_vars_configuration=None):  # noqa: E501
        """InboxProjection - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._created_at = None
        self._email_address = None
        self._favourite = None
        self._id = None
        self._name = None
        self._tags = None
        self.discriminator = None

        self.created_at = created_at
        if email_address is not None:
            self.email_address = email_address
        if favourite is not None:
            self.favourite = favourite
        self.id = id
        if name is not None:
            self.name = name
        if tags is not None:
            self.tags = tags

    @property
    def created_at(self):
        """Gets the created_at of this InboxProjection.  # noqa: E501


        :return: The created_at of this InboxProjection.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InboxProjection.


        :param created_at: The created_at of this InboxProjection.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def email_address(self):
        """Gets the email_address of this InboxProjection.  # noqa: E501


        :return: The email_address of this InboxProjection.  # noqa: E501
        :rtype: str
        """
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        """Sets the email_address of this InboxProjection.


        :param email_address: The email_address of this InboxProjection.  # noqa: E501
        :type: str
        """

        self._email_address = email_address

    @property
    def favourite(self):
        """Gets the favourite of this InboxProjection.  # noqa: E501


        :return: The favourite of this InboxProjection.  # noqa: E501
        :rtype: bool
        """
        return self._favourite

    @favourite.setter
    def favourite(self, favourite):
        """Sets the favourite of this InboxProjection.


        :param favourite: The favourite of this InboxProjection.  # noqa: E501
        :type: bool
        """

        self._favourite = favourite

    @property
    def id(self):
        """Gets the id of this InboxProjection.  # noqa: E501


        :return: The id of this InboxProjection.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InboxProjection.


        :param id: The id of this InboxProjection.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this InboxProjection.  # noqa: E501


        :return: The name of this InboxProjection.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InboxProjection.


        :param name: The name of this InboxProjection.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def tags(self):
        """Gets the tags of this InboxProjection.  # noqa: E501


        :return: The tags of this InboxProjection.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this InboxProjection.


        :param tags: The tags of this InboxProjection.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

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
        if not isinstance(other, InboxProjection):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InboxProjection):
            return True

        return self.to_dict() != other.to_dict()
