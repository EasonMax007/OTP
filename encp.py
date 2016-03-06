#!/usr/bin/env python2
# _*_ coding: utf-8 _*_


import binascii
from Crypto.Cipher import AES


class crypt(object):
    def __init__(self, solt, otp=None):
        if otp is None:
            return False
        else:
            self.otp = otp
        self.solt = (solt + 'PL7H3GGMEDCBJ2SC')[:16]
        self.key = '4YLTB46MGAWLW5XB'
        self.iv = 'S6BQD7L7Q7YPPGRB'

    def en(self):
        obj = AES.new(self.key, AES.MODE_CBC, self.iv)
        ciphertext = obj.encrypt(self.otp + self.solt)
        return binascii.b2a_hex(ciphertext)

    def de(self):
        ace = binascii.a2b_hex(self.otp)
        obj = AES.new(self.key, AES.MODE_CBC, self.iv)
        return obj.decrypt(ace)[:16]
