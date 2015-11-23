
from . import api
from .. import db
from ..models import Node

@api.route('/', methods=['GET', 'POST'])
def index():
    return api.send_static_file('static/index.html')

@api.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

