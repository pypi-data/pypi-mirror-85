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


def relationship(
    argument,
    secondary=None,
    primaryjoin=None,
    secondaryjoin=None,
    foreign_keys=None,
    uselist=None,
    order_by: bool = False,
    backref=None,
    back_populates=None,
    post_update: bool = False,
    cascade: bool = False,
    extension=None,
    viewonly: bool = False,
    lazy='select',
    collection_class=None,
    passive_deletes: bool = False,
    passive_updates: bool = True,
    remote_side=None,
    enable_typechecks: bool = True,
    join_depth=None,
    comparator_factory=None,
    single_parent: bool = False,
    innerjoin: bool = False,
    distinct_target_key=None,
    doc=None,
    active_history: bool = False,
    cascade_backrefs: bool = True,
    load_on_pending: bool = False,
    bake_queries: bool = True,
    _local_remote_pairs=None,
    query_class=None,
    info=None,
    omit_join=None,
    sync_backref=None
): pass


class SQLAlchemy(SQLAlchemy):
    Model: Type[Model]
    Column: Column
    relationship: relationship
