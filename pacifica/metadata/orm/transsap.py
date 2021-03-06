#!/usr/bin/python
# -*- coding: utf-8 -*-
"""TransSAP model."""
from peewee import ForeignKeyField, Expression, OP
from pacifica.metadata.rest.orm import CherryPyAPI
from pacifica.metadata.orm.transactions import Transactions
from pacifica.metadata.orm.users import Users
from pacifica.metadata.orm.proposals import Proposals
from pacifica.metadata.orm.analytical_tools import AnalyticalTools
from pacifica.metadata.orm.utils import unicode_type


class TransSAP(CherryPyAPI):
    """
    TransSAP model class.

    Attributes:
        +-------------------+-------------------------------------------+
        | Name              | Description                               |
        +===================+===========================================+
        | submitter         | User who submitted the transaction        |
        +-------------------+-------------------------------------------+
        | analytical_tool   | Analytical tool the transaction came from |
        +-------------------+-------------------------------------------+
        | proposal          | Proposal the transaction is for           |
        +-------------------+-------------------------------------------+
        | suspense_date     | date the transaction is available         |
        +-------------------+-------------------------------------------+
    """

    id = ForeignKeyField(
        Transactions, index=True, primary_key=True,
        unique=True, backref='transsap'
    )
    submitter = ForeignKeyField(Users, backref='transsap')
    analytical_tool = ForeignKeyField(AnalyticalTools, backref='transsap')
    proposal = ForeignKeyField(Proposals, backref='transsap')

    def to_hash(self, **flags):
        """Convert the object to a hash."""
        obj = super(TransSAP, self).to_hash(**flags)
        obj['_id'] = int(self.__data__['id'])
        obj['submitter'] = int(self.__data__['submitter'])
        obj['analytical_tool'] = int(self.__data__['analytical_tool'])
        obj['proposal'] = unicode_type(self.__data__['proposal'])
        return obj

    def from_hash(self, obj):
        """Convert the hash into the object."""
        super(TransSAP, self).from_hash(obj)
        self._set_only_if('_id', obj, 'id', lambda: int(obj['_id']))
        attr_cls_map = [
            ('submitter', Users),
            ('proposal', Proposals),
            ('analytical_tool', AnalyticalTools)
        ]
        for key, obj_cls in attr_cls_map:
            self._set_only_if(
                key, obj, key,
                lambda o=obj_cls, k=key: o.get(o.id == obj[k])
            )

    @classmethod
    def where_clause(cls, kwargs):
        """Where clause for the various elements."""
        where_clause = super(TransSAP, cls).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(TransSAP.id, OP.EQ, kwargs['_id'])
        return cls._where_attr_clause(
            where_clause,
            kwargs,
            [
                'analytical_tool',
                'submitter',
                'proposal'
            ]
        )
