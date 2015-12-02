from flask import redirect, url_for

from . import api
from .. import db
from ..models import Node

@api.route('/', methods=['GET', 'POST'])
def index():
    return "hello from blueprint"


