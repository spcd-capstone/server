import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + (os.environ.get("HADB_PATH") or "tmp.db")

    @staticmethod
    def init_app(app):
        pass


config = {
    'default': Config
}

