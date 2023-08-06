# Copyright 2020 Okera Inc. All Rights Reserved.
#
# Some integration tests for auth in PyOkera
#
# pylint: disable=global-statement
# pylint: disable=no-self-use
# pylint: disable=no-else-return
# pylint: disable=duplicate-code

import unittest

#from okera import context, _thrift_api
#from datetime import datetime
from okera.tests import pycerebro_test_common as common
from okera._thrift_api import (TAttribute, TAttributeMatchLevel)

class ListDatasetsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Initializes one time state that is shared across test cases. This is used
            to speed up the tests. State that can be shared across (but still stable)
            should be here instead of __cleanup()."""
        super(ListDatasetsTest, cls).setUpClass()

    def _get_t_attribute_obj(self, namespace, key):
        attribute = TAttribute()
        attribute.attribute_namespace = namespace
        attribute.key = key
        return attribute

    def test_list_datasets_tag_filter(self):
        """ Test for multi-tag filter
        """
        db1 = 'attributes_test_db1'
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            # create attributes
            conn.create_attribute('test_namespace', 'test_key1')
            conn.create_attribute('test_namespace', 'test_key2')
            conn.create_attribute('test_namespace', 'test_key3')

            # create databases
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % db1)
            conn.execute_ddl('CREATE DATABASE %s' % db1)

            # create tables
            conn.execute_ddl('CREATE TABLE %s.t1(c1 int, c11 int)' % db1)
            conn.execute_ddl('CREATE TABLE %s.t2(c2 int, c22 int)' % db1)
            conn.execute_ddl('CREATE TABLE %s.t3(c3 int, c33 int)' % db1)

            conn.assign_attribute('test_namespace', 'test_key1', db1)
            conn.assign_attribute('test_namespace', 'test_key2', db1, 't1')
            conn.assign_attribute('test_namespace', 'test_key3', db1, 't2', 'c2')

            # Create TAttribute objects required for testing
            attributes = []
            attr1_db_level = self._get_t_attribute_obj('test_namespace', 'test_key1')
            attr2_tab_level = self._get_t_attribute_obj('test_namespace', 'test_key2')
            attr3_col_level = self._get_t_attribute_obj('test_namespace', 'test_key3')

            # No Table should be returned.
            # Input tag is on DATABASE level and Match_Level = TABLE_ONLY
            attributes.append(attr1_db_level)
            datasets = conn.list_datasets(
                db1, tags=attributes, tag_match_level=TAttributeMatchLevel.TABLE_ONLY)
            self.assertTrue(len(datasets) == 0)

            # should return the table: t1
            # Input tag is on TABLE level and Match_Level = TABLE_ONLY
            attributes.clear()
            attributes.append(attr2_tab_level)
            datasets = conn.list_datasets(
                db1, tags=attributes, tag_match_level=TAttributeMatchLevel.TABLE_ONLY)
            self.assertTrue(len(datasets) == 1)
            for dataset in datasets:
                self.assertTrue(dataset.name == 't1')

            # No Table should be returned.
            # Input tag is on TABLE level and Match_Level = TABLE_ONLY
            attributes.clear()
            attributes.append(attr3_col_level)
            datasets = conn.list_datasets(
                db1, tags=attributes, tag_match_level=TAttributeMatchLevel.TABLE_ONLY)
            self.assertTrue(len(datasets) == 0)

            # should return the table: t1, t2
            # Input tags are on TABLE & COLUMN level and Match_Level = TABLE_PLUS
            attributes.clear()
            attributes.append(attr2_tab_level)
            attributes.append(attr3_col_level)
            datasets = conn.list_datasets(
                db1, tags=attributes, tag_match_level=TAttributeMatchLevel.TABLE_PLUS)
            self.assertTrue(len(datasets) == 2)
            returned_tbls = []
            for dataset in datasets:
                returned_tbls.append(dataset.name)
            self.assertTrue('t1' in returned_tbls)
            self.assertTrue('t2' in returned_tbls)

            # should return the table: t2
            # Input tags are on TABLE & COLUMN level and Match_Level = COLUMN_ONLY
            attributes.clear()
            attributes.append(attr2_tab_level)
            attributes.append(attr3_col_level)
            datasets = conn.list_datasets(
                db1, tags=attributes, tag_match_level=TAttributeMatchLevel.COLUMN_ONLY)
            self.assertTrue(len(datasets) == 1)
            for dataset in datasets:
                self.assertTrue(dataset.name == 't2')

            # No Table should be returned.
            # Input tags are on DB, TABLE & COLUMN level and Match_Level = DATABASE_ONLY
            attributes.clear()
            attributes.append(attr1_db_level)
            attributes.append(attr2_tab_level)
            attributes.append(attr3_col_level)
            datasets = conn.list_datasets(
                db1, tags=attributes, tag_match_level=TAttributeMatchLevel.DATABASE_ONLY)
            self.assertTrue(len(datasets) == 0)

            # should return the table: t1, t2, t3
            # Input tags are on DB, TABLE & COLUMN level and Match_Level = DATABASE_PLUS
            datasets = conn.list_datasets(
                db1, tags=attributes, tag_match_level=TAttributeMatchLevel.DATABASE_PLUS)
            self.assertTrue(len(datasets) == 3)
            returned_tbls.clear()
            for dataset in datasets:
                returned_tbls.append(dataset.name)
            self.assertTrue('t1' in returned_tbls)
            self.assertTrue('t2' in returned_tbls)
            self.assertTrue('t3' in returned_tbls)

            # test to verify that if a tag matches at the DB level, all the tables
            # within that DB (after honoring other filters) should be returned
            # should return the table: t1, t2, t3
            # Input tags are only on DB level and Match_Level = DATABASE_PLUS
            attributes.clear()
            attributes.append(attr1_db_level)
            datasets = conn.list_datasets(
                db1, tags=attributes, tag_match_level=TAttributeMatchLevel.DATABASE_PLUS)
            print(datasets)
            for dataset in datasets:
                print('Table Name: {0}'.format(dataset.name))

            self.assertTrue(len(datasets) == 3)
            returned_tbls = []
            for dataset in datasets:
                returned_tbls.append(dataset.name)
            self.assertTrue('t1' in returned_tbls)
            self.assertTrue('t2' in returned_tbls)
            self.assertTrue('t3' in returned_tbls)

            # drop databases
            conn.execute_ddl('DROP DATABASE IF EXISTS %s CASCADE' % db1)

if __name__ == "__main__":
    unittest.main()
