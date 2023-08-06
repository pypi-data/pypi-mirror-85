from typing import Type
from flask_sqlalchemy import SQLAlchemy
from .model import Model


def Column(primary_key: bool):
    pass


class SQLAlchemy(SQLAlchemy):
    Model: Type[Model]
    Column: Column
