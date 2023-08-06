# This file is part of Flask-Multipass-LDAP-CERN.
# Copyright (C) 2017-2020 CERN
#
# Flask-Multipass-LDAP-CERN is free software; you can redistribute it
# and/or modify it under the terms of the Revised BSD License.

from __future__ import unicode_literals

import re

from flask_multipass.providers.ldap import LDAPIdentityProvider, LDAPGroup, LDAPAuthProvider


def _fix_affiliation(affiliation, _re=re.compile(r'^eduGAIN - ', re.IGNORECASE)):
    if not affiliation or affiliation.startswith('urn:'):
        # Ignore urn:Facebook and similar pseudo affiliations
        return ''
    else:
        # Remove the edugain prefix if we have one.
        return _re.sub('', affiliation)


def fix_data(identity_info):
    # Names containing OpenID URLs
    first_name = identity_info.data.get('first_name') or ''
    if 'https://me.yahoo.com' in first_name:
        identity_info.data['first_name'] = None
    # Affiliations containing unrelated information
    affiliations = identity_info.data.getlist('affiliation')
    if affiliations:
        identity_info.data.setlist('affiliation', map(_fix_affiliation, affiliations))


class CERNLDAPGroup(LDAPGroup):
    def get_members(self):
        for identity_info in super(CERNLDAPGroup, self).get_members():
            fix_data(identity_info)
            yield identity_info


class CERNLDAPSettingsMixin(object):
    def set_defaults(self):
        self.ldap_settings.setdefault('uid', 'cn')
        self.ldap_settings.setdefault('user_base', 'DC=cern,DC=ch')
        self.ldap_settings.setdefault('user_filter', '(objectCategory=user)')
        self.ldap_settings.setdefault('gid', 'cn')
        self.ldap_settings.setdefault('group_base', 'OU=Workgroups,DC=cern,DC=ch')
        self.ldap_settings.setdefault('group_filter', '(objectCategory=group)')
        self.ldap_settings.setdefault('member_of_attr', 'memberOf')
        self.ldap_settings.setdefault('ad_group_style', True)
        super(CERNLDAPSettingsMixin, self).set_defaults()


class CERNLDAPAuthProvider(CERNLDAPSettingsMixin, LDAPAuthProvider):
    pass


class CERNLDAPIdentityProvider(CERNLDAPSettingsMixin, LDAPIdentityProvider):
    group_class = CERNLDAPGroup

    def _get_identity(self, identifier):
        identity_info = super(CERNLDAPIdentityProvider, self)._get_identity(identifier)
        if identity_info:
            fix_data(identity_info)
        return identity_info

    def search_identities(self, criteria, exact=False):
        for identity_info in super(CERNLDAPIdentityProvider, self).search_identities(criteria, exact=exact):
            fix_data(identity_info)
            yield identity_info
