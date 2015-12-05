from threading import Thread

from flask import Flask,g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from celery import Celery

from config import config


db = SQLAlchemy()


def create_before_request(app):
    def before_request():
        g.db = db
    return before_request


def create_app(config_name = 'default'):
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(config[config_name])
    app.debug = True
    config[config_name].init_app(app)

    db.init_app(app)

    # attach routes and custom error pages here
    from hacer.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # start discovery server
    with app.app_context():
        from discovery import run_discovery_server
        app.discovery_thread = Thread(target=run_discovery_server, kwargs={ "Session": scoped_session(sessionmaker(bind=db.engine)) })
        app.discovery_thread.daemon = True
        app.discovery_thread.start()

    app.before_request(create_before_request(app))
    return app


def create_celery_app(app=None):
    app = app or create_app()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.app = app
    return celery

