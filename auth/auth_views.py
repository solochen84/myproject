# coding=utf-8

from . import auth
from flask import render_template, abort, session, flash, redirect, url_for, get_flashed_messages, request, current_app
from .auth_froms import LoginForm, RegisterForm, ChangePwdForm, ForgetPwdForm, ResetPwdForm
from model import User, Role
from flask.ext.login import login_user, login_required, logout_user, current_user
from start import db
from common.email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        # print(login_form.password.data)
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码错误')
    return render_template('auth/login.html', form=login_form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User(email=register_form.email.data, username=register_form.username.data, password=register_form.password.data, confirmed=True)
        user.gravatar()
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, u'激活账号', 'auth/email/confirm', user=user, token=token)
        flash(u'注册成功，一封邮件已经发到您邮箱，请前往邮箱激活')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=register_form)


@auth.route('/changepwd', methods=['GET', 'POST'])
@login_required
def change_pwd():
    change_pwd_form = ChangePwdForm()
    if change_pwd_form.validate_on_submit():
        if not current_user.verify_password(change_pwd_form.old_password.data):
            flash(u'密码输入错误')
        else:
            current_user.password = change_pwd_form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'密码修改成功')
    return render_template('auth/changepwd.html', form=change_pwd_form)


@auth.route('/forgetpwd', methods=['GET', 'POST'])
def forget_pwd():
    forget_pwd_form = ForgetPwdForm()
    if forget_pwd_form.validate_on_submit():
        user = User.query.filter_by(email=forget_pwd_form.email.data).first()
        token = user.generate_confirmation_token()
        send_email(user.email, u'重设密码', 'auth/email/forgetpwd', user=user, token=token)
        flash(u'一封邮件已经发到您邮箱，请前往邮箱修改密码')
        return redirect(url_for('main.index'))
    return render_template('auth/forgetpwd.html', form=forget_pwd_form)


@auth.route('/resetpwd/<token>', methods=['GET', 'POST'])
def reset_pwd(token):
    user = User.get_user_by_token(token)
    if not user:
        abort(404)
    reset_pwd_form = ResetPwdForm()
    if reset_pwd_form.validate_on_submit():
        user.password = reset_pwd_form.password.data
        db.session.add(user)
        db.session.commit()
        flash(u'密码重设成功')
    return render_template('auth/resetpwd.html', form=reset_pwd_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经登出.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm_user(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash(u'您已经确认了您的账号，谢谢！')
    else:
        flash(u'激活链接不对或已过期，请确认')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed_user():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/resendconfirmation')
@login_required
def resend_confirmation():
    if not current_user.confirmed:
        token = current_user.generate_confirmation_token()
        send_email(current_user.email, u'激活账号', 'auth/email/confirm', user=current_user, token=token)
        flash(u'注册成功，一封邮件已经发到您邮箱，请前往邮箱激活')


@auth.before_app_request
def before_request():
    # db.drop_all()
    # db.create_all()
    # db.session.commit()
    # Role.insert_roles()
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

