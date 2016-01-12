# coding=utf-8

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import Required, length, email, equal_to, ValidationError
from model import User


class LoginForm(Form):
    username = StringField(u'用户名', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class RegisterForm(Form):
    username = StringField(u'用户名', validators=[Required()])
    email = StringField(u'邮件', validators=[Required(), length(1,64), email()])
    StringField(u'用户名', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    confirmed_password = PasswordField(u'密码', validators=[Required(), equal_to('password',message=u'密码不匹配')])

    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被注册')


class ChangePwdForm(Form):
    old_password = PasswordField(u'旧密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[Required()])
    confirmed_password = PasswordField(u'新确认密码', validators=[Required(), equal_to('password', message=u'密码不匹配')])
    submit = SubmitField(u'提交')


class ForgetPwdForm(Form):
    email = StringField(u'邮件', validators=[Required(), length(1,64), email()])
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError(u'未找到该邮箱对应的用户')


class ResetPwdForm(Form):
    password = PasswordField(u'新密码', validators=[Required()])
    confirmed_password = PasswordField(u'新确认密码', validators=[Required(), equal_to('password', message=u'密码不匹配')])
    submit = SubmitField(u'提交')