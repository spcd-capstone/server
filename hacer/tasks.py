import sys
import importlib

from celery.signals import task_prerun
from flask import g
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import func

from . import create_celery_app
from . import db
from .models import NodeType, ScriptLogEntry

import hasapi


celery = create_celery_app()


@task_prerun.connect
def celery_prerun(*args, **kwargs):
    with celery.app.app_context():
        pass


@celery.task()
def launch_script(name, params):
    thread_id = 0
    max_entry = db.session.query(func.max(ScriptLogEntry.thread_id).label("max")).first().max
    if not max_entry is None:
        thread_id = max_entry + 1

    import hasapi
    hasapi.db_session_maker = scoped_session(sessionmaker(bind=db.engine))
    hasapi.thread_id = thread_id
    hasapi.script_name = name
    hasapi.params = params

    m = "hacer.scripts." + name
    if (m in sys.modules):
        importlib.reload(sys.modules[m])
    else:
        __import__(m)

