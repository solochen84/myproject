# coding=utf-8

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.mail import Mail
from flask.ext.pagedown import PageDown


login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'
login_manager.login_message = u'请先登录'
db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()

moment = Moment()

if __name__ == '__main__':
    bootstrap = Bootstrap()


    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hard to guess string'
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'mysql://root:mopon@172.16.34.7:3306/test'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    app.config['MAIL_SERVER'] = 'smtp.qiye.163.com'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = 'chenxiaolu.sz@mopon.cn'
    app.config['MAIL_PASSWORD'] = 'cxl@taijiu2015'
    app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
    app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <chenxiaolu.sz@mopon.cn>'
    app.config['FLASKY_ADMIN'] = 'chenxiaolu.sz@mopon.cn'
    app.config['FLASKY_POSTS_PER_PAGE'] = 2
    app.config['FLASKY_FOLLOWERS_PER_PAGE'] = 2
    app.config['FLASKY_COMMENTS_PER_PAGE'] = 2

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)

    from model import User, AnonymousUser
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.anonymous_user = AnonymousUser

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    app.run(debug=True)


