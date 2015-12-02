import datetime
import json
import socket

from hacer.models import Node, NodeType


def run_discovery_server(Session):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 7775))

    while 1:
        raw_data, addr = sock.recvfrom(1024)
        session = Session()

        # parse JSON
        data = json.loads(raw_data.decode())

        # current date/time
        date_time = datetime.datetime.now()

        # ip address into string
        ipstr = str(addr[0])

        # get node type associated with the given name
        node_type = session.query(NodeType).filter_by(name=data['type']).first()
        if node_type is None:
            node_type = session.query(NodeType).filter_by(name='other').one()

        # create new Node
        n = session.query(Node).filter_by(id=data['id']).first()
        if n is None:
            n = Node(id=data['id'])
        n.ip = ipstr
        n.type_id = node_type.id
        n.last_update = date_time

        # insert/update database
        session.add(n)
        session.commit()
        Session.remove()

