from . import db


class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    lastUpdate = db.Column(db.DateTime())

    def __repr__(self):
        return '<Node %r>' % self.name


class LogEntry(db.Model):
    """ TODO: Currently incomplete """

    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<LogEntry %r>' % self.name
