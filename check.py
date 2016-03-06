#!/usr/bin/env python2
# _*_ coding: utf-8 _*_


# import pyotp
from db import DB

def numcheck(name, number):
    anfo = DB(name).search()
    print anfo
