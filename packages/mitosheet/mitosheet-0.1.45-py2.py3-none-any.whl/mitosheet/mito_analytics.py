#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains analytics objects; exported here to avoid
circular references!
"""
import analytics
import getpass

# Write key taken from segement.com
analytics.write_key = '6I7ptc5wcIGC4WZ0N1t0NXvvAbjRGUgX' 
# For now, we identify users with their logged in user name
# which is fine, because we manage user accounts on trymito.io
static_user_id = getpass.getuser()
analytics.identify(static_user_id, {
    'location': __file__
}) #TODO: get information to store as traits?
