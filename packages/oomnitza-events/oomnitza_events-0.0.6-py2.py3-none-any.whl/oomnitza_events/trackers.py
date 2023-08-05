# -*- coding: utf-8 -*-
"""Trackers module

This module defines various trackers and uploader like login, workflow run, etc.
Also, it defines the validation for coming data according to type of tracker or
uploader.
"""
import cerberus
import logging

from typing import Dict, List, Any

from oomnitza_events.connectors import Segment, Redshift
from oomnitza_events.constants import LOGIN_EVENT_NAME
from oomnitza_events.constants import OOMNITZA_USER_LOGIN_EVENT_NAME
from oomnitza_events.constants import WORKFLOW_RUN_EVENT_NAME
from oomnitza_events.constants import OBJECT_ACTION_EVENT_NAME
from oomnitza_events.constants import DAILY_DATA_LOAD_EVENT_NAME
from oomnitza_events.constants import OOMNITZA_EVENTS_LOG_NAME
from oomnitza_events.schemas import USER_SCHEMA
from oomnitza_events.schemas import UPLOAD_SCHEMA
from oomnitza_events.schemas import USER_UPLOAD_SCHEMA
from oomnitza_events.schemas import LOGIN_SCHEMA
from oomnitza_events.schemas import OOMNITZA_USER_LOGIN_SCHEMA
from oomnitza_events.schemas import WORKFLOW_RUN_SCHEMA
from oomnitza_events.schemas import OBJECT_ACTION_SCHEMA
from oomnitza_events.schemas import DAILY_DATA_LOAD_SCHEMA
from oomnitza_events.utils import Validator
from oomnitza_events.version import __version__


LOGGER = logging.getLogger(OOMNITZA_EVENTS_LOG_NAME)


class Singleton(type):
    """Metaclass of tracker class to prevent duplicates of each type of trackers
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseTracker(metaclass=Singleton):
    """Base class of tracker."""

    CONNECTOR = None
    SCHEMA = None

    def __init__(self,
                 subdomain: str,
                 system_type: str):
        Validator.verify_subdomain(subdomain)
        Validator.verify_system_type(system_type)

        self._subdomain = subdomain
        self._system_type = system_type
        self._oomnitza_events_version = __version__
        self._validator = cerberus.Validator()

    def _get_base_properties(self):
        return {
            'server': self._subdomain,
            'system_type': self._system_type,
            'oomnitza_events_version': self._oomnitza_events_version
        }


class BaseEventTracker(BaseTracker):
    """Base class of event tracker."""

    CONNECTOR = Segment
    SCHEMA = None

    def __init__(self,
                 subdomain: str,
                 credentials: Any,
                 system_type: str):
        """Initializes connector and validator which are used for sending data
        to data warehouse and validating the data before sending to data
        warehouse.

        Args:
            subdomain: A string used to tell where is data coming from e.g. 'airbnb'.
            credentials: A connector credentials e.g. A string of Segment
                'write_key'.
            system_type: A string used to tell the type of system e.g. 'prod', 'sandbox'.

        """
        super(BaseEventTracker, self).__init__(subdomain, system_type)
        self._connector = self.CONNECTOR(credentials)

    def track(self,
              user_id: str,
              properties: Dict):
        """Tracks an event if enabled is True.

        Args:
            user_id: A string of user's id used to identify the event
                initializer.
            properties: A free-form dictionary of the properties of the event.
                For example,
                    {
                        "auth_type": "saml",
                        "client_type": "mobile",
                        "identity_provider": "okta"
                    }

        """
        try:
            self._prepare_properties(properties)
            valid_properties = self._validator.validate(properties,
                                                        self.SCHEMA)
            if not valid_properties:
                # TODO: Separate validation of type error and allowed scope to
                #  have more accurate logging level
                LOGGER.info(self._validator.errors)
                return

            self._perform_sync(user_id, properties)
        except Exception as e:
            LOGGER.error(e)

    def _perform_sync(self,
                      user_id: str,
                      properties: Dict):
        """Sends data to data warehouse through the connector."""
        pass

    def _prepare_properties(self,
                            properties: Dict):
        """Prepares the event properties before sending it to data warehouse."""
        base_properties = self._get_base_properties()
        properties.update(base_properties)


class UserIdentityTracker(BaseEventTracker):
    """The class of user identity tracker which includes schema for validating
    the coming properties have the required fields and valid format.
    """
    SCHEMA = USER_SCHEMA

    def _perform_sync(self,
                      user_id: str,
                      properties: Dict):
        """Identify the user identity."""
        self._connector.identify(user_id, properties)


class EventTracker(BaseEventTracker):
    """The class of event tracker which includes event name e.g. 'login',
    'object_action'and schema for validating the coming properties have the
    required fields and valid format.
    """
    EVENT_NAME = None
    SCHEMA = None

    def _perform_sync(self,
                      user_id: str,
                      properties: Dict):
        """Tracks an event with event type name."""
        self._connector.track(user_id, self.EVENT_NAME, properties)


class LoginTracker(EventTracker):
    """The class of login tracker."""
    EVENT_NAME = LOGIN_EVENT_NAME
    SCHEMA = LOGIN_SCHEMA


class OomnitzaUserLoginTracker(EventTracker):
    """The class of login tracker."""
    EVENT_NAME = OOMNITZA_USER_LOGIN_EVENT_NAME
    SCHEMA = OOMNITZA_USER_LOGIN_SCHEMA


class WorkflowRunTracker(EventTracker):
    """The class of login tracker."""
    EVENT_NAME = WORKFLOW_RUN_EVENT_NAME
    SCHEMA = WORKFLOW_RUN_SCHEMA


class ObjectActionTracker(EventTracker):
    """The class of login tracker."""
    EVENT_NAME = OBJECT_ACTION_EVENT_NAME
    SCHEMA = OBJECT_ACTION_SCHEMA


class DailyDataLoadTracker(EventTracker):
    """The class of tracker of daily data load like total count of assets,
    total count of archived assets, etc.
    """
    EVENT_NAME = DAILY_DATA_LOAD_EVENT_NAME
    SCHEMA = DAILY_DATA_LOAD_SCHEMA


class BaseUploader(BaseTracker):
    """Base class of uploader."""

    CONNECTOR = Redshift
    SCHEMA = None

    def __init__(self,
                 subdomain: str,
                 system_type: str,
                 db_schema_name: str,
                 db_config: Dict):

        super(BaseUploader, self).__init__(subdomain, system_type)
        self._connector = self.CONNECTOR(db_schema_name, db_config)

    def upload(self, data: List[Dict]):
        valid = self._validate(data)
        if not valid:
            # TODO: Separate validation of type error and allowed scope to
            #  have more accurate logging level
            LOGGER.info(self._validator.errors)
            return

        self._perform_sync(self._subdomain,
                           self._system_type,
                           self._oomnitza_events_version,
                           data)

    def _base_validate(self):
        base_properties = self._get_base_properties()
        return self._validator.validate(base_properties, UPLOAD_SCHEMA)

    def _validate(self, data):
        valid = self._base_validate()
        for d in data:
            valid = valid and self._validator.validate(d, self.SCHEMA)
            if not valid:
                return valid
        return valid

    def _perform_sync(self,
                      subdomain: str,
                      system_type: str,
                      oomnitza_events_version: str,
                      data: List[Dict]):
        pass


class UserIdentityUploader(BaseUploader):
    """The class of user identity uploader which includes schema for validating
    the coming data have the required fields and valid format.
    """

    SCHEMA = USER_UPLOAD_SCHEMA

    def _perform_sync(self,
                      subdomain: str,
                      system_type: str,
                      oomnitza_events_version: str,
                      data: List[Dict]):
        """Upload the users identities to data warehouse directly."""
        self._connector.insert_users_identities(subdomain,
                                                system_type,
                                                oomnitza_events_version,
                                                data)



