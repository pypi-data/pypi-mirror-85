# -*- coding: utf-8 -*-
"""Schemas module

This module defines data schemas for validating properties coming through
the trackers.
"""
CLIENT_TYPES = ('mobile', 'web')
AUTH_TYPES = ('basic', 'saml')
ACTION_TYPES = ('view', 'create', 'edit', 'delete', 'restore')
WF_ACTION_TYPES = ('any', 'create', 'edit', 'delete', 'scheduled',
                   'parent_associated', 'parent_dissociated',
                   'child_associated', 'child_dissociated')
WF_STATUS = ('start', 'done')
WF_OBJECT_TYPES = ('accessories', 'assets', 'audits', 'contracts', 'locations',
                   'users', 'saas', 'saas_users', 'software', 'stockrooms')
AGENT_TYPES = ('api', 'connector', 'import', 'ticket_plugin', 'webui', 'wf',
               'jit', 'saas')
OBJECT_TYPES = ('accessories', 'assets', 'audits', 'contracts', 'locations',
                'users', 'saas', 'software', 'stockrooms')
SYSTEM_TYPES = ('demo', 'dev', 'poc', 'prod', 'sandbox', 'preprod')
MODULE_ENABLED_VALUES = ('enabled', 'disabled')


USER_SCHEMA = {
    'full_name': {
        'type': 'string',
        'required': True,
        'nullable': True  # 'empty' default is True
    },
    'role': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    },
    'oomnitza_events_version': {
        'type': 'string',
        'required': True,
        'empty': False
    },
}


UPLOAD_SCHEMA = {
    'server': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    },
    'oomnitza_events_version': {
        'type': 'string',
        'required': True,
        'empty': False
    },
}


USER_UPLOAD_SCHEMA = {
    'user_id': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'full_name': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'role': {
        'type': 'string',
        'required': True,
        'nullable': True
    }
}


LOGIN_SCHEMA = {
    'client_type': {
        'type': 'string',
        'allowed': CLIENT_TYPES,
        'required': True
    },
    'auth_type': {
        'type': 'string',
        'allowed': AUTH_TYPES,
        'required': True
    },
    'identity_provider': {
        'type': 'string',
        'required': True,
        'nullable': True  # 'empty' default is True
    },
    'user_agent': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False  # 'nullable' default is False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    },
    'oomnitza_events_version': {
        'type': 'string',
        'required': True,
        'empty': False
    },
}


OOMNITZA_USER_LOGIN_SCHEMA = {
    'email': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'ip_address': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'role': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'access_date': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'reason': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'description': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False  # 'nullable' default is False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    },
    'oomnitza_events_version': {
        'type': 'string',
        'required': True,
        'empty': False
    },
}

WORKFLOW_RUN_SCHEMA = {
    'run_id': {
        'type': 'integer',
        'required': True
    },
    'wf_id': {
        'type': 'integer',
        'required': True
    },
    'wf_name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'action_type': {
        'type': 'string',
        'required': True,
        'allowed': WF_ACTION_TYPES
    },
    'object_type': {
        'type': 'string',
        'required': True,
        'allowed': WF_OBJECT_TYPES
    },
    'status': {
        'type': 'string',
        'required': True,
        'allowed': WF_STATUS
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    },
    'oomnitza_events_version': {
        'type': 'string',
        'required': True,
        'empty': False
    },
}

OBJECT_ACTION_SCHEMA = {
    'action_type': {
        'type': 'string',
        'required': True,
        'allowed': ACTION_TYPES
    },
    'agent_type': {
        'type': 'string',
        'required': True,
        'allowed': AGENT_TYPES
    },
    'agent_name': {
        'type': 'string',
        'required': True,
        'nullable': True  # 'empty' default is True
    },
    'object_type': {
        'type': 'string',
        'required': True,
        'allowed': OBJECT_TYPES
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    },
    'oomnitza_events_version': {
        'type': 'string',
        'required': True,
        'empty': False
    },
}

DAILY_DATA_LOAD_SCHEMA = {
    'accessories_enabled': {
        'type': 'string',
        'required': True,
        'allowed': MODULE_ENABLED_VALUES
    },
    'accessories_total_active': {
        'type': 'integer',
        'required': True
    },
    'accessories_total_archived': {
        'type': 'integer',
        'required': True
    },
    'accessories_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'assets_enabled': {
        'type': 'string',
        'required': True,
        'allowed': MODULE_ENABLED_VALUES
    },
    'assets_total_active': {
        'type': 'integer',
        'required': True
    },
    'assets_total_archived': {
        'type': 'integer',
        'required': True
    },
    'assets_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'contracts_enabled': {
        'type': 'string',
        'required': True,
        'allowed': MODULE_ENABLED_VALUES
    },
    'contracts_total_active': {
        'type': 'integer',
        'required': True
    },
    'contracts_total_archived': {
        'type': 'integer',
        'required': True
    },
    'contracts_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'locations_total_active': {
        'type': 'integer',
        'required': True
    },
    'locations_total_archived': {
        'type': 'integer',
        'required': True
    },
    'locations_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'users_enabled': {
        'type': 'string',
        'required': True,
        'allowed': MODULE_ENABLED_VALUES
    },
    'users_total_active': {
        'type': 'integer',
        'required': True
    },
    'users_total_archived': {
        'type': 'integer',
        'required': True
    },
    'users_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'saas_enabled': {
        'type': 'string',
        'required': True,
        'allowed': MODULE_ENABLED_VALUES
    },
    'saas_total_active': {
        'type': 'integer',
        'required': True},
    'saas_total_archived': {
        'type': 'integer',
        'required': True
    },
    'saas_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'saas_users_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'software_enabled': {
        'type': 'string',
        'required': True,
        'allowed': MODULE_ENABLED_VALUES
    },
    'software_total_active': {
        'type': 'integer',
        'required': True
    },
    'software_total_archived': {
        'type': 'integer',
        'required': True
    },
    'software_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'stockrooms_total_active': {
        'type': 'integer',
        'required': True
    },
    'stockrooms_total_archived': {
        'type': 'integer',
        'required': True
    },
    'stockrooms_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'audits_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'transactions_wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'wf_total_active': {
        'type': 'integer',
        'required': True
    },
    'roles_total_active': {
        'type': 'integer',
        'required': True
    },
    'last_login_date': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'total_logins_past_7_days': {
        'type': 'integer',
        'required': True
    },
    'total_logins_past_4_weeks': {
        'type': 'integer',
        'required': True
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'release_version': {
        'type': 'string',
        'required': True
    },
    'system_type': {
        'type': 'string',
        'required': True,
        'allowed': SYSTEM_TYPES
    },
    'oomnitza_events_version': {
        'type': 'string',
        'required': True,
        'empty': False
    },
}