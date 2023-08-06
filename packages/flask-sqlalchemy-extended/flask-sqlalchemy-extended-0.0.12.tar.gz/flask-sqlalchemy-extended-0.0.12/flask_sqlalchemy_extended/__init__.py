from typing import Type
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import TypeEngine
from .model import Model


def Column(
    *args,
    primary_key: bool = None,
    nullable: bool = None,
    unique: bool = None,
): pass


class SQLAlchemy(SQLAlchemy):
    Model: Type[Model]
    Column: Column
