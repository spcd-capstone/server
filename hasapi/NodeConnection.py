import contextlib
from datetime import datetime
import socket

import hasapi
from . import serialization
from hacer.models import Node, ScriptLogEntry, ScriptLogEntryType

class NodeNotConnected(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidCommand(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidResponse(Exception):
    pass


class NodeConnection:

    def __init__(self):
        self.node_port = 7777
        self.sock = socket.socket()
        self.is_connected = False
        self.db_session_maker = None
        self.script_name = None
        self.thread_id = None
        self.node_name = None
        self.params = []


    def __enter__(self):
        try:
            self.db_session_maker = haapi.db_session_maker
            self.thread_id = haapi.thread_id
            self.script_name = haapi.script_name
            self.node_name = haapi.node_name
            self.params = haapi.params
        except AttrributeError as ex:
            self.__log("exception", repr(ex))

        try:
            session = self.db_session_maker()
            node = session.query(Node).filter_by(name=self.node_name).one()
            self.sock.connect((node.ip, self.node_port))
            self.is_connected = True
        except Exception as ex:
            # Log error here
            #print("Could not connect. Exception type is {}".format(type(e).__name__))
            self.__log("exception", repr(ex))

        return self


    def __exit__(self, ex_type, ex_value, traceback):
        try:
            self.sock.close()

            if not ex_type is None:
                msg = "{}: {}".format(ex_type, ex_value)
                self.__log("exception", msg);
                self.__log("exit_status", "failed")

            else:
                self.__log("exit_status", "success")

        except Exception:
            pass

        return True


    def __del__(self):
        self.sock.close()

    def setVal(self, key, value):
        if not self.isConnected:
            msg = "No node name provided"
            if self.node_name:
                msg = "Not connected to node {}".format(self.node_name)

            raise NodeNotConnected(msg)

        k = serialization.serialize(key)
        v = serialization.serialize(value)

        self.sock.send(bytes("s" + k + v, 'UTF-8'))
        self.__log("sent_set", "\"{}\": \"{}\"".format(key, value))

        v = self.sock.recv(1024).decode()
        if not v:
            raise TimeoutError("no response recieved")

        self.__log("result", v)

        if v[0] != '+':
            raise InvalidResponse("recieved invalid response: {}".format(v))


    def getVal(self, key):
        if not self.isConnected:
            msg = "No node name provided"
            if self.node_name:
                msg = "Not connected to node {}".format(self.node_name)

            raise NodeNotConnected(msg)

        k = serialization.serialize(key)

        self.sock.send(bytes("g" + k, 'UTF-8'))
        self.__log("sent_get", "\"{}\"".format(key))

        v = self.sock.recv(1024).decode()
        self.__log("result", v)

        if not v:
            raise TimeoutError("no response recieved")
        if not v[0] == '+':
            raise InvalidResponse("response was: {}".format(v))
        return serialization.deserialize(v)


    def log(self, msg):
        self.__log("output", msg)


    def __log(self, entry_type, msg):
        try:
            session = self.db_session_maker()
            etype = session.query(ScriptLogEntryType).filter_by(name=entry_type).one()
            entry = ScriptLogEntry(
                timestamp = datetime.now(),
                thread_id = self.thread_id,
                script_name = self.script_name,
                params = " ".join(self.params),
                entry_type_id = etype.id,
                data = msg)
            session.add(entry)
            session.commit()

        except Exception as ex:
            pass


