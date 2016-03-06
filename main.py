#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import re
import qrcode
from db import DB
from otp import User
from encp import crypt
from auth import authenticate
from StringIO import StringIO
from datetime import timedelta
from flask import Flask, redirect, url_for, request, render_template, session, flash, send_file

app = Flask(__name__)


@app.route('/')
def index():
    if session.get('loggin_in') is not True:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('userinfo'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    policy = re.compile('^\D{4,}\d{3}$')
    if request.method == 'POST':
        user = request.form['username'].lower()
        pwd = request.form['password']
        if policy.match(user) is None:
            return render_template('login.html', error=u'用户名格式错误')
        if not pwd:
            return render_template('login.html', error=u'密码不能为空')
        au_status = authenticate(user, pwd)
        if au_status == 'super':
            return redirect(url_for('backdoor'))
        elif au_status:
            ainfo = DB(user).search()
            if ainfo is None:
                session['otp_info'] = u'未绑定'
            else:
                if ainfo[4] is 1:
                    session['otp_info'] = u'已绑定'
                else:
                    session['otp_info'] = u'已禁用'
            session['user'] = user
            session['pwd'] = pwd
            session['logged_in'] = True
            return redirect(url_for('userinfo'))
        else:
            return render_template('login.html', error=u'用户名或密码错误')
    else:
        return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('pwd', None)
    session.pop('logged_in', None)
    session.pop('otp_info', None)
    flash('You were logged out')
    return render_template('login.html', error=u'用户已注销')


@app.route('/backdoor')
def backdoor():
    error = None
    return render_template('backdoor.html', error=None)


@app.route('/user/info.html')
def userinfo():
    error = None
    if session.get('logged_in'):
        return render_template('userinfo.html', error=error)
    else:
        return render_template('login.html', error=u'会话已过期，请重新登录')


@app.route('/user/bound.html', methods=['GET', 'POST'])
def bound():
    error = None
    if session.get('logged_in'):
        if request.method == 'POST':
            otp_info = User(session['user'])
            real_key = otp_info.otpkey()
            otp_key = crypt(real_key).en()
            if DB(session['user']).search() is None:
                DB(session['user'], otp=otp_key).save()
                session['otp_info'] = u'已绑定'
            else:
                DB(session['user'], otp=otp_key).change()
                session['otp_info'] = u'已重置'
            return render_template('qrcode.html', error=None, key=real_key, url=otp_key)
        else:
            return render_template('bound.html', error=None)
    else:
        return render_template('login.html', error=u'会话已过期，请重新登录')


@app.route('/qr/<url>')
def qr(url):
    otp_key = DB(session['user']).search()[1]
    otp_key = crypt(otp_key).de()
    otp_url = User(session['user']).otpurl(otp_key)
    qr = qrcode.make(otp_url)
    img = StringIO()
    qr.save(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route('/user/check.html', methods=['GET', 'POST'])
def check():
    error = None
    if session.get('logged_in'):
        if request.method == 'POST':
        return render_template('check.html', error=error)
    else:
        return render_template('login.html', error=u'会话已过期，请重新登录')


@app.route('/software/info.html')
def software():
    error = None
    if session.get('logged_in'):
        return render_template('software.html', error=error)
    else:
        return render_template('login.html', error=u'会话已过期，请重新登录')


@app.route('/software/ios.html')
def ios():
    error = None
    if session.get('logged_in'):
        return render_template('ios.html', error=error)
    else:
        return render_template('login.html', error=u'会话已过期，请重新登录')


@app.route('/software/android.html')
def android():
    error = None
    if session.get('logged_in'):
        return render_template('android.html', error=error)
    else:
        return render_template('login.html', error=u'会话已过期，请重新登录')


if __name__ == '__main__':
    app.secret_key = ';o,Z>&Jg3e#fjx2d'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.permanent_session_lifetime = timedelta(minutes=5)
    app.debug = True
    app.run()
