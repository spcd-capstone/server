from flask import redirect, url_for, jsonify, request

import json

from . import api
from .. import db
from ..models import ScriptLogEntry

@api.route('/logs/script', methods=['GET'])
def get_script_logs_all():
    entries = ScriptLogEntry.query.all()
    return jsonify({ 'entry_list': [entry.to_json() for entry in entries]})

@api.route('/logs/script/thread_id/<int:tid>', methods=['GET'])
def get_script_logs_thread(tid):
    entries = ScriptLogEntry.query.filter_by(thread_id=tid).all()
    return jsonify({ 'entry_list': [entry.to_json() for entry in entries]})

