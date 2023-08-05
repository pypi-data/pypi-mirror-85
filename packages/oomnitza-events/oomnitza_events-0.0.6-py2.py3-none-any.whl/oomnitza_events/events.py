# -*- coding: utf-8 -*-
"""Oomnitza events client module

This includes the client for sending runtime events like login, workflow run,
asset creation, software edit through third-party service to data
warehouse. Also, this includes the client for uploading data to data warehouse
directly.
"""
import logging
from typing import Any, List, Dict

from oomnitza_events import trackers
from oomnitza_events.constants import OOMNITZA_EVENTS_LOG_NAME
from oomnitza_events.utils import Validator

LOGGER = logging.getLogger(OOMNITZA_EVENTS_LOG_NAME)


class Client:
    """Client class of events tracker which is used for tracking events in
    runtime.
    """
    _TRACKER_TYPES = {
        'user_identity': trackers.UserIdentityTracker,
        'login': trackers.LoginTracker,
        'oomnitza_user_login': trackers.OomnitzaUserLoginTracker,
        'wf_run': trackers.WorkflowRunTracker,
        'object_action': trackers.ObjectActionTracker,
        'daily_data_load': trackers.DailyDataLoadTracker,
    }

    def __init__(self,
                 subdomain: str,
                 credentials: Any,
                 enabled: bool,
                 system_type: str):
        """Initializes the events trackers.

        Args:
            subdomain: A string of subdomain used to tell which server is data
                       coming from e.g. 'airbnb'.
            credentials: The events tracker connector credentials
                         e.g. Segment connector credentials is a string of
                              'write_key'
            enabled: A boolean which is a flag to determine if connector will
                     send over the data to data warehouse.
            system_type: A string used to tell the type of system
                         e.g. 'prod', 'sandbox', 'dev'.

        Raises:
            TypeError: An error occurred if "enabled" is in the wrong type.

        """
        self._trackers = {}
        Validator.verify_enabled(enabled)
        if enabled:
            self._initialize_trackers(subdomain,
                                      credentials,
                                      system_type)

    def _initialize_trackers(self,
                             subdomain: str,
                             credentials: Any,
                             system_type: str):
        for tracker_type, tracker_class in self._TRACKER_TYPES.items():
            self._trackers[tracker_type] = tracker_class(
                subdomain=subdomain,
                credentials=credentials,
                system_type=system_type
            )

    def track(self,
              user_id: str,
              track_type: str,
              properties: Dict):
        """Tracks an event.

        Args:
            user_id: A string of Oomnitza user's id used to identify the event
                     initializer.
            track_type: A string of tracking type e.g. "login", "object_action".
                        This helps assign the right tracker.
            properties: A free-form dictionary of the properties of the event.
                For example, following is properties of "login" event
                    {
                        "auth_type": "saml",
                        "client_type": "mobile",
                        "identity_provider": "okta"
                    }

        """
        if track_type not in self._TRACKER_TYPES:
            err_msg = f"The track type '{track_type}' is not supported."
            LOGGER.error(err_msg)
            return

        if track_type not in self._trackers:
            err_msg = f"The tracker of '{track_type}' was not initialized " \
                      f"because events tracker is disabled."
            LOGGER.info(err_msg)
            return

        tracker = self._trackers[track_type]
        tracker.track(user_id=user_id,
                      properties=properties)


class UploadClient:
    """Client class for uploading data to data warehouse directly instead of
    through third-party service. It can reduce the data usage quota of
    third-party service. This is useful for something like backfilling existing
    records.
    """
    _UPLOADER_TYPES = {
        'user_identity': trackers.UserIdentityUploader,
    }

    def __init__(self,
                 subdomain: str,
                 system_type: str,
                 db_schema_name: str,
                 db_config: Dict):
        """Initializes the uploaders.

            Args:
                subdomain: A string of subdomain used to tell which server is
                           data coming from e.g. 'airbnb'.
                system_type: A string used to tell the type of system e.g.
                             'prod', 'sandbox'.
                db_schema_name: This is schema name of data warehouse db.
                                e.g. Redshift db schema 'webui', 'dev'
                db_config: This is config for connecting to data warehouse db.
                           e.g. 'host', 'user', 'password', 'port', 'database'

            """
        self._uploaders = {}
        self._initialize_uploaders(subdomain,
                                   system_type,
                                   db_schema_name,
                                   db_config)

    def _initialize_uploaders(self,
                              subdomain: str,
                              system_type: str,
                              db_schema_name: str,
                              db_config: Dict):
        for uploader_type, uploader_class in self._UPLOADER_TYPES.items():
            self._uploaders[uploader_type] = uploader_class(
                subdomain=subdomain,
                system_type=system_type,
                db_schema_name=db_schema_name,
                db_config=db_config
            )

    def upload(self, upload_type: str, data: List[Dict]):
        """Uploads list of records. It's usually used for one-time task.

            Args:
                upload_type: A string which helps assign the right uploader
                             e.g. "user_identity"
                data: The data is in a list of dict.
                    For example, following is list of users identities
                        [{
                            "user_id": "XXX",
                            "full_name": "foo bar",
                            "role": "Employee"
                        }, ...]

            """
        if upload_type not in self._UPLOADER_TYPES:
            err_msg = f"The upload type '{upload_type}' is not supported."
            LOGGER.error(err_msg)
            return

        if upload_type not in self._uploaders:
            err_msg = f"The uploader of '{upload_type}' was not initialized."
            LOGGER.info(err_msg)
            return

        uploader = self._uploaders[upload_type]
        uploader.upload(data)

