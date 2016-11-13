#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the file_key_values ORM object."""
from json import dumps
from metadata.orm.test.base import TestBase
from metadata.orm.keywords import Keywords
from metadata.orm.test.test_citations import SAMPLE_CITATION_HASH, TestCitations
from metadata.orm.citations import Citations

SAMPLE_KEYWORD_HASH = {
    '_id': 142,
    'citation_id': SAMPLE_CITATION_HASH['_id'],
    'keyword': 'halitosis',
    'encoding': 'UTF8'
}

SAMPLE_UNICODE_KEYWORD_HASH = {
    '_id': 143,
    'citation_id': SAMPLE_CITATION_HASH['_id'],
    'keyword': u'blargééééé',
    'encoding': 'UTF8'
}


class TestKeywords(TestBase):
    """Test the InstitutionPerson ORM object."""

    obj_cls = Keywords
    obj_id = Keywords.id

    @classmethod
    def dependent_cls(cls):
        """Return dependent classes for the Keywords object."""
        return TestCitations.dependent_cls() + [Keywords]

    @classmethod
    def base_create_dep_objs(cls):
        """Create all objects that FileKeyValue need."""
        cite = Citations()
        TestCitations.base_create_dep_objs()
        cite.from_hash(SAMPLE_CITATION_HASH)
        cite.save(force_insert=True)

    def test_keywords_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_KEYWORD_HASH)

    def test_unicode_keywords_hash(self):
        """Test the hash portion using base object method."""
        self.base_test_hash(SAMPLE_UNICODE_KEYWORD_HASH)

    def test_keywords_json(self):
        """Test the hash portion using base object method."""
        self.base_test_json(dumps(SAMPLE_KEYWORD_HASH))

    def test_keywords_search_expr(self):
        """Test the hash portion using base object method."""
        self.base_where_clause_search_expr(
            SAMPLE_UNICODE_KEYWORD_HASH,
            keyword_operator='ILIKE',
            keyword=u'%é%'
        )

    def test_keywords_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_KEYWORD_HASH)

    def test_unicode_keywords_where(self):
        """Test the hash portion using base object method."""
        self.base_where_clause(SAMPLE_UNICODE_KEYWORD_HASH)