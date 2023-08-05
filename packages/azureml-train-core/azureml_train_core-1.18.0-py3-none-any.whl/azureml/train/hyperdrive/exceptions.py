# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Exceptions thrown by HyperDrive."""

from azureml._common.exceptions import AzureMLException
from azureml._common._error_response._error_response_constants import ErrorCodes


class HyperDriveUserException(AzureMLException):
    """
    Exceptions related to user error.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.USER_ERROR

    def __init__(self, exception_message, **kwargs):
        """
        Initialize a new instance of HyperDriveUserException.

        :param exception_message: A message describing the error.
        :type exception_message: str
        """
        super(HyperDriveUserException, self).__init__(exception_message, **kwargs)


class HyperDriveSystemException(AzureMLException):
    """
    Exception related to system errors.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.SYSTEM_ERROR

    def __init__(self, exception_message, **kwargs):
        """
        Initialize a new instance of HyperDriveSystemException.

        :param exception_message: A message describing the error.
        :type exception_message: str
        """
        super(HyperDriveSystemException, self).__init__(exception_message, **kwargs)


class HyperDriveServiceException(HyperDriveSystemException):
    """
    Exceptions related to service error.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.SERVICE_ERROR

    def __init__(self, exception_message, **kwargs):
        """
        Initialize a new instance of HyperDriveServiceException.

        :param exception_message: A message describing the error.
        :type exception_message: str
        """
        super(HyperDriveServiceException, self).__init__(exception_message, **kwargs)


class HyperDriveConfigException(HyperDriveUserException):
    """
    Exception thrown due to validation errors while creating HyperDrive run.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.VALIDATION_ERROR

    def __init__(self, exception_message, **kwargs):
        """
        Initialize a new instance of HyperDriveConfigException.

        :param exception_message: A message describing the error.
        :type exception_message: str
        """
        super(HyperDriveConfigException, self).__init__(exception_message, **kwargs)


class HyperDriveScenarioNotSupportedException(HyperDriveConfigException):
    """
    Exception thrown when config values point to a scenario not supported while creating a HyperDrive Run.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.SCENARIONOTSUPORTED_ERROR


class HyperDriveNotImplementedException(HyperDriveScenarioNotSupportedException):
    """
    Exception related to capabilities not implemented for HyperDrive Run.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.NOTIMPLEMENTED_ERROR


class HyperDriveRehydrateException(HyperDriveSystemException):
    """Exception thrown when creating re hydrating a HyperDrive Run."""
