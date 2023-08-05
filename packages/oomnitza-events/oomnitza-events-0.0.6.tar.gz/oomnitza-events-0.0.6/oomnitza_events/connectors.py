# -*- coding: utf-8 -*-
"""Connectors module

This module defines the connector we use to send data to data warehouse.
"""
import logging
import uuid

from abc import ABC
from abc import abstractmethod
from typing import Dict

import analytics  # segment.io
import arrow
import psycopg2  # postgresql lib to connect / query to redshift db

from oomnitza_events.errors import (
    InvalidCredentialsError, InvalidDatabaseInfoError
)
from oomnitza_events.constants import OOMNITZA_EVENTS_LOG_NAME


LOGGER = logging.getLogger(OOMNITZA_EVENTS_LOG_NAME)


class BaseConnector(ABC):
    """Base connector class."""

    def __init__(self, *args, **kwargs):
        """Initializes connector with calling credentials verify function."""
        self.verify_credentials(*args, **kwargs)

    @abstractmethod
    def verify_credentials(self, *args, **kwargs):
        """Abstract method used to define credentials validation."""
        pass


class Segment(BaseConnector):

    def __init__(self, credentials):
        super().__init__(credentials)
        analytics.write_key = credentials

    def verify_credentials(self, credentials):
        """Verifies coming credentials is in string type.

        Args:
            credentials: A string of segment.io 'write_key'.
        """
        if not credentials:
            err_msg = "The write_key is required for initializing Segment " \
                      "connector."
            raise InvalidCredentialsError(err_msg)

        if not isinstance(credentials, str):
            err_msg = "The write_key has to be a string."
            raise InvalidCredentialsError(err_msg)

    @staticmethod
    def identify(user_id: str,
                 properties: Dict):
        """Binds a user_id to user's profile.

        Args:
            user_id: An user's identification string ties to his or her profile.
            properties: A free-form dictionary of properties of an user,
                        like full_name and role.

        """
        try:
            analytics.identify(user_id,
                               properties)
        except Exception as e:
            LOGGER.error(e)

    @staticmethod
    def track(user_id: str,
              event: str,
              properties: Dict):
        """Records actions users perform, along with properties that describe
        the actions.

        Args:
            user_id: An user's identification string ties to his or her profile.
            event: A name of the action type that a user has performed.
                   For example, "object_action", "login".
            properties: A free-form dictionary of properties of the event.
                For example,
                    {
                        "auth_type": "saml",
                        "client_type": "mobile",
                        "identity_provider": "okta"
                    }
        """
        try:
            analytics.track(user_id,
                            event,
                            properties)
        except Exception as e:
            LOGGER.error(e)


class Redshift(BaseConnector):

    REQUIRED_DB_FIELDS = ('host', 'port', 'user', 'password', 'database')

    def __init__(self, db_schema_name, db_config):
        super().__init__(db_schema_name, db_config)
        self._db_schema_name = db_schema_name
        self._db_config = db_config

    def verify_credentials(self, db_schema_name, db_config):
        """Verifies coming db_schema_name and db_config are valid.

        Args:
            db_schema_name: A string which is a schema name of data warehouse db
            db_config: A dictionary which includes requirements to connect to db

        """
        if not db_schema_name:
            err_msg = "The Redshift schema is not defined."
            raise InvalidDatabaseInfoError(err_msg)

        if not isinstance(db_schema_name, str):
            err_msg = "The Redshift schema has to be a string."
            raise InvalidDatabaseInfoError(err_msg)

        if not db_config:
            err_msg = "The Redshift db info is required for initializing " \
                      "connection."
            raise InvalidDatabaseInfoError(err_msg)

        if not isinstance(db_config, dict):
            err_msg = "The Redshift db info has to be a dictionary."
            raise InvalidDatabaseInfoError(err_msg)

        if not all(field in db_config for field in self.REQUIRED_DB_FIELDS):
            err_msg = "The Redshift db info should include 'host', 'port', " \
                      "'user', 'password', 'database'."
            raise InvalidDatabaseInfoError(err_msg)

    def insert_users_identities(self,
                                subdomain,
                                system_type,
                                oomnitza_events_version,
                                data):
        with psycopg2.connect(**self._db_config) as conn:
            with conn.cursor() as cur:
                try:
                    cur_time = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss')
                    identifies_values = []
                    users_values = []
                    for user_identity in data:
                        identifies_values.append(
                            cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (uuid.uuid4().hex,
                                 cur_time,
                                 cur_time,
                                 cur_time,
                                 cur_time,
                                 user_identity.get('role'),
                                 user_identity.get('user_id'),
                                 user_identity.get('full_name'),
                                 subdomain,
                                 system_type,
                                 oomnitza_events_version,)
                            )
                        )
                        users_values.append(
                            cur.mogrify(
                                "(%s, %s, %s, %s, %s, %s, %s)",
                                (user_identity.get('user_id'),
                                 cur_time,
                                 user_identity.get('full_name'),
                                 user_identity.get('role'),
                                 subdomain,
                                 system_type,
                                 oomnitza_events_version,)
                            )
                        )

                    identifies_sql = """INSERT INTO {}.Identifies (
                        id, 
                        received_at, 
                        original_timestamp, 
                        sent_at, 
                        timestamp, 
                        role, 
                        user_id, 
                        full_name, 
                        server, 
                        system_type,
                        oomnitza_events_version) VALUES {}""".format(
                            self._db_schema_name,
                            b','.join(identifies_values).decode('utf-8'))
                    cur.execute(identifies_sql)

                    users_sql = """INSERT INTO {}.Users (
                        id, 
                        received_at,
                        full_name, 
                        role, 
                        server, 
                        system_type,
                        oomnitza_events_version) VALUES {}""".format(
                            self._db_schema_name,
                            b','.join(users_values).decode('utf-8'))
                    cur.execute(users_sql)
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as ex:
                    LOGGER.error(ex)

        # Unlike other context manager objects, existing the with block does
        # not close the connection but only terminates the transaction
        conn.close()
