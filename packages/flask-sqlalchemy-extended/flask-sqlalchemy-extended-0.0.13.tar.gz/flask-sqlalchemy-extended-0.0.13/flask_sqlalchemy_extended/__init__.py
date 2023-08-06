from typing import Any, Type
from flask_sqlalchemy import SQLAlchemy
from .model import Model


def Column(
    *args,
    primary_key: bool = None,
    nullable: bool = None,
    unique: bool = None,
    default: Any = None
): pass


class SQLAlchemy(SQLAlchemy):
    Model: Type[Model]
    Column: Column
