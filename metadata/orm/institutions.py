#!/usr/bin/python
"""
Describes an institution and its attributes.
"""
from peewee import BooleanField, TextField, CharField, Expression, OP
from metadata.rest.orm import CherryPyAPI

class Institutions(CherryPyAPI):
    """
    Institution model scribes an institute.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | institution_name  | Name of the institution             |
        +-------------------+-------------------------------------+
        | association_cd    | Type of institution (TBD)           |
        +-------------------+-------------------------------------+
        | is_foreign        | Is the institution foreign or not   |
        +-------------------+-------------------------------------+
        | encoding          | Any encoding for the name           |
        +-------------------+-------------------------------------+
    """
    institution_name = TextField(default="")
    association_cd = CharField(default="UNK")
    is_foreign = BooleanField(default=False)
    encoding = CharField(default="UTF8")

    @staticmethod
    def elastic_mapping_builder(obj):
        """
        Build the elasticsearch mapping bits
        """
        super(Institutions, Institutions).elastic_mapping_builder(obj)
        obj['institution_name'] = obj['association_cd'] = \
        obj['encoding'] = {'type': 'string'}
        obj['is_foreign'] = {'type': 'boolean'}

    def to_hash(self):
        """
        Converts the object to a hash
        """
        obj = super(Institutions, self).to_hash()
        obj['_id'] = int(self.id)
        obj['institution_name'] = unicode(self.institution_name)
        obj['association_cd'] = str(self.association_cd)
        obj['is_foreign'] = bool(self.is_foreign)
        obj['encoding'] = str(self.encoding)
        return obj

    def from_hash(self, obj):
        """
        Convert the hash into the object.
        """
        super(Institutions, self).from_hash(obj)
        # pylint: disable=invalid-name
        if '_id' in obj:
            self.id = int(obj['_id'])
        # pylint: enable=invalid-name
        if 'institution_name' in obj:
            self.institution_name = unicode(obj['institution_name'])
        if 'association_cd' in obj:
            self.association_cd = str(obj['association_cd'])
        if 'is_foreign' in obj:
            self.is_foreign = bool(obj['is_foreign'])
        if 'encoding' in obj:
            self.encoding = str(obj['encoding'])

    def where_clause(self, kwargs):
        """
        PeeWee specific where clause used for search.
        """
        where_clause = super(Institutions, self).where_clause(kwargs)
        if '_id' in kwargs:
            where_clause &= Expression(Institutions.id, OP.EQ, kwargs['_id'])
        for key in ['institution_name', 'is_foreign', 'association_cd', 'encoding']:
            if key in kwargs:
                where_clause &= Expression(getattr(Institutions, key), OP.EQ, kwargs[key])
        return where_clause
