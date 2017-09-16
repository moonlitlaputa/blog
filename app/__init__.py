# coding: utf-8
import logging

from celery import Celery
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_cache import Cache
from raven.contrib.flask import Sentry

from config import config
from app.utils import assets

# app = None

toolbar = DebugToolbarExtension()
mail = Mail()
moment = Moment()
pagedown = PageDown()
db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})
sentry = Sentry()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

celery = Celery(__name__, broker='redis://localhost:6379')

photos = UploadSet('photos', IMAGES)


def create_app(config_name):
    # global app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    _config = config[config_name]
    _config.init_app(app)

    configure_uploads(app, (photos, ))
    # toolbar.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    assets.init_app(app)
    cache.init_app(app)
    if config_name == "production":
        sentry.init_app(
            app, dsn=_config.SENTRY_DSN, logging=True, level=logging.ERROR)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_v1.post import api_post
    app.register_blueprint(api_post)

    from .api_v1.auth import api_auth
    app.register_blueprint(api_auth)

    from .api_v1.user import api_user
    app.register_blueprint(api_user)

    from .api_v1.comment import api_comment
    app.register_blueprint(api_comment)

    return app


def make_celery(app, _celery):
    _celery.conf.update(app.config)
    TaskBase = _celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    _celery.Task = ContextTask
    return _celery
