#!/usr/bin/env python2
# _*_ coding: utf-8 _*_

import psycopg2
from datetime import datetime


class DB(object):
    def __init__(self, name, otp=None, status=None):
        self.name = name
        self.otp = otp
        self.status = status
        try:
            self.db = psycopg2.connect('dbname=otp_db host=127.0.0.1 user=otp_admin password=Paic#234')
            self.cur = self.db.cursor()
        except Exception:
            return False

    def save(self):
        '''
        Save user information...
        '''
        if self.otp is None:
            return False
        date = datetime.isoformat(datetime.now())[:19].replace('T', ' ')
        self.cur.execute("INSERT INTO otp_info (name, otp_number, create_date) VALUES ('%s', '%s', '%s');" % (self.name, self.otp, date))
        self.db.commit()
        return True

    def search(self):
        '''
        Search information...
        '''
        self.cur.execute("SELECT * FROM otp_info WHERE name='%s';" % (self.name))
        return self.cur.fetchone()

    def change(self):
        '''
        Change information...
        '''
        date = datetime.isoformat(datetime.now())[:19].replace('T', ' ')
        if self.otp is not None:
            self.cur.execute("UPDATE otp_info SET otp_number='%s', modify_date='%s' where name='%s';" % (self.otp, date, self.name))
            self.db.commit()
            return True
        elif self.status is not None:
            self.cur.execute("UPDATE otp_info SET status='%s', modify_date='%s' where name='%s';" % (self.status, date, self.name))
            self.db.commit()
            return True
        else:
            return False
