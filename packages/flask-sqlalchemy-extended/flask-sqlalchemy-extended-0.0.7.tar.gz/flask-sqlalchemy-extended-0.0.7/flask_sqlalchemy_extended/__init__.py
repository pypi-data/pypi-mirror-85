from typing import Type
from flask_sqlalchemy import SQLAlchemy
from .model import Model


def Column(primary_key: bool):
    pass


def create_all(bind='__all__', app=None):
    pass


class SQLAlchemy(SQLAlchemy):
    Model: Type[Model]
    Column: Column
    create_all: create_all
