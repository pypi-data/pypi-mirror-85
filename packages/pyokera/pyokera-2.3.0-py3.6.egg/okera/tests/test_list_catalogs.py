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
from okera._thrift_api import (TAccessPermissionLevel)

class ListCatalogsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Initializes one time state that is shared across test cases. This is used
            to speed up the tests. State that can be shared across (but still stable)
            should be here instead of __cleanup()."""
        super(ListCatalogsTest, cls).setUpClass()

    def test_list_catalogs(self):
        TEST_USER1 = 'list_catalogs_test_user1'
        TEST_USER2 = 'list_catalogs_test_user2'
        TEST_ROLE1 = 'list_catalogs_test_role1'
        TEST_ROLE2 = 'list_catalogs_test_role2'
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl('DROP ROLE IF EXISTS %s'% TEST_ROLE1)
            conn.execute_ddl('CREATE ROLE %s' % TEST_ROLE1)
            conn.execute_ddl('DROP ROLE IF EXISTS %s'% TEST_ROLE2)
            conn.execute_ddl('CREATE ROLE %s' % TEST_ROLE2)
            conn.execute_ddl('GRANT ROLE %s TO GROUP %s' % (TEST_ROLE1, TEST_USER1))
            conn.execute_ddl('GRANT ROLE %s TO GROUP %s' % (TEST_ROLE2, TEST_USER2))
            # Grant some catalog privileges to role1 but none to role2
            conn.execute_ddl('GRANT CREATE ON CATALOG TO ROLE %s'% TEST_ROLE1)
            conn.execute_ddl('GRANT SELECT ON CATALOG TO ROLE %s'% TEST_ROLE1)
            conn.execute_ddl('GRANT CREATE_AS_OWNER ON CATALOG TO ROLE %s'% TEST_ROLE1)

            # list Catalogs test (with "root" as requesting_user)
            result = conn.list_catalogs(requesting_user='root')
            self.assertTrue(len(result.catalogs) == 1)
            for catalog in result.catalogs:
                self.assertTrue(catalog.name == 'okera')
                assert TAccessPermissionLevel.ALL in catalog.access_levels

            # list Catalogs test (with no requesting_user)
            result = conn.list_catalogs()
            self.assertTrue(len(result.catalogs) == 1)
            for catalog in result.catalogs:
                self.assertTrue(catalog.name == 'okera')
                assert TAccessPermissionLevel.ALL in catalog.access_levels

            # list Catalogs test (with TEST_USER1 as requesting_use)
            result = conn.list_catalogs(requesting_user=TEST_USER1)
            self.assertTrue(len(result.catalogs) == 1)
            for catalog in result.catalogs:
                self.assertTrue(catalog.name == 'okera')
                assert TAccessPermissionLevel.CREATE in catalog.access_levels
                assert TAccessPermissionLevel.SELECT in catalog.access_levels
                assert TAccessPermissionLevel.CREATE_AS_OWNER in catalog.access_levels

            # list Catalogs test (No access levels for the TEST_USER2)
            result = conn.list_catalogs(requesting_user=TEST_USER2)
            self.assertTrue(len(result.catalogs) == 1)
            for catalog in result.catalogs:
                self.assertTrue(catalog.name == 'okera')
                self.assertTrue(len(catalog.access_levels) == 0)

            # Set up a user with only SELECT and check catalog permission
            role = 'list_catalogs_temp_role'
            user = 'list_catalogs_temp_user'
            ctx.enable_token_auth('root')
            conn.execute_ddl("create role if not exists {}".format(role))
            conn.execute_ddl("GRANT ROLE {} TO GROUP {}".format(role, user))
            conn.execute_ddl("GRANT SELECT ON CATALOG TO ROLE {}".format(role))
            ctx.enable_token_auth(user)
            result = conn.list_catalogs(user)
            for catalog in result.catalogs:
                self.assertTrue(catalog.name == 'okera')
                self.assertTrue(len(catalog.access_levels) == 1)
                assert TAccessPermissionLevel.SELECT in catalog.access_levels

            ctx.enable_token_auth('root')
            conn.execute_ddl("drop role if exists {}".format(role))

if __name__ == "__main__":
    unittest.main()
