import hashlib
import pkgutil
import sys

from flask import abort, jsonify, request

from . import api
from .. import db
from .. import tasks

import hacer.scripts


@api.route('/scripts/list', methods=['GET'])
def script_list():
    return jsonify({"script_list": get_script_list()})


@api.route('/scripts/exec/id/<int:script_id>', methods=['GET','POST'])
def script_exec_by_id(script_id):
    scripts = get_script_list()
    script = list(filter(lambda s: s.get('id') == script_id, scripts))
    if not script:
        abort(404)
    script = script[0]

    req = request.get_json(force=True)
    params = []
    if not req.get('params') is None:
        params = req['params']

    tasks.launch_script.delay(script['name'], params)
    return "", 200, {'Content-Type': 'application/json'}


@api.route('/scripts/exec/name/<string:script_name>', methods=['POST'])
def script_exec_by_name(script_name):
    scripts = get_script_list()
    script = list(filter(lambda s: s.get('name') == script_name, scripts))
    if not script:
        abort(404)
    script = script[0]

    req = request.get_json(force=True)
    params = []
    if not req.get('params') is None:
        params = req['params']

    tasks.launch_script.delay(script['name'], params)
    return "", 200, {'Content-Type': 'application/json'}


def get_script_list():
    l = [name for _, name, _ in pkgutil.iter_modules(hacer.scripts.__path__)]
    return [name_to_record(n) for n in l]


def name_to_record(name):
    script_id = hash_name(name)
    return { 'id': script_id, 'name': name }


def hash_name(name):
    h = hashlib.md5(name.encode()).hexdigest()
    return int(h[:8], 16)

