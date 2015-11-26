from . import db


class NodeType(db.Model):
    __tablename__ = 'nodetypes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    nodes = db.relationship('Node', backref='type')

    def insert_types():
        types = [ "toggle", "light_rgb", "sensor_temp", "thermostat", "other" ]

        for t in types:
            nt = NodeType.query.filter_by(name=t).first()
            if nt is None:
                nt = NodeType(name=t)
            db.session.add(nt)

        db.session.commit()


class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    type_id = db.Column(db.Integer, db.ForeignKey('nodetypes.id'))
    ip = db.Column(db.String(16))
    lastUpdate = db.Column(db.DateTime())

    def __repr__(self):
        return '<Node %r>' % self.name


class ScriptLogEntryType(db.Model):
    __tablename__ = "scriptlogentrytypes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    nodes = db.relationship('ScriptLogEntry', backref='entry_type')

    def __repr__(self):
        return '<Node %r>' % self.name

    def insert_types():
        types = [ "launch", "output", "sent_set", "sent_get", "result",
                "exception", "exit_status" ]

        for t in types:
            nt = ScriptLogEntryType.query.filter_by(name=t).first()
            if nt is None:
                nt = ScriptLogEntryType(name=t)
            db.session.add(nt)

        db.session.commit()


class ScriptLogEntry(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    typestamp = db.Column(db.DateTime())
    thread_id = db.Column(db.Integer)
    script_name = db.Column(db.String())
    entry_type_id = db.Column(db.Integer, db.ForeignKey('scriptlogentrytypes.id'))
    data = db.Column(db.Text)

    def __repr__(self):
        return '<ScriptLogEntry %r>' % self.name

