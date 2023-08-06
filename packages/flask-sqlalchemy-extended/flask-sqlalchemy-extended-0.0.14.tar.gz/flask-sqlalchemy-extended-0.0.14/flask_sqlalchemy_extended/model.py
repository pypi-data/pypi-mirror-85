from flask_sqlalchemy.model import Model


def query():
    pass


class Model(Model):
    __tablename__: str
    query: query
