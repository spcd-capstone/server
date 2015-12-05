from flask import Blueprint

api = Blueprint('api', __name__, static_folder='static')

from . import views, nodes, logs, scripts


