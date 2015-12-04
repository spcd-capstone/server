from flask import jsonify, request

import json

from . import api
from .. import db
from ..models import Node

@api.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = Node.query.all()
    return jsonify({ 'node_list': [node.to_json() for node in nodes]})

@api.route('/nodes/id/<int:id>', methods=['GET'])
def get_node(id):
    node = Node.query.get_or_404(id)
    return jsonify(node.to_json())

@api.route('/nodes/id/<int:id>', methods=['POST'])
def post_node(id):
    node = Node.query.get_or_404(id)

    req = request.get_json(force=True)
    node.name = req['name']
    db.session.commit()
    return json.dumps({'success': True}), 200, {'Content-Type': 'application/json'}

