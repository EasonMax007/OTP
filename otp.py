#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyotp


class User(object):
    def __init__(self, name):
        self.name = name

    def otpkey(self):
        key = pyotp.random_base32()
        return key

    def authenticate(self, key, num):
        totp = pyotp.TOTP(key)
        if totp.verify(num):
            return True
        else:
            return False

    def otpurl(self, key):
        totp = pyotp.TOTP(key)
        return totp.provisioning_uri(self.name)
