#!/usr/bin/env python

import os
from hacer import create_app, db
from hacer.models import NodeType, Node, ScriptLogEntryType, ScriptLogEntry
from flask.ext.script import Manager, Shell

# from flask.ext.migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
# migrate = Migrate(app, db)


def make_shell_context():
    return dict(manager=manager, app=app, db=db,
            Node=Node,
            NodeType=NodeType,
            ScriptLogEntryType=ScriptLogEntryType,
            ScriptLogEntry=ScriptLogEntry)

manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()

