# Copyright 2017 Okera Inc. All Rights Reserved.
#
# Tests that should run on any configuration. The server auth can be specified
# as an environment variables before running this test.

# pylint: disable=no-member
# pylint: disable=no-self-use
# pylint: disable=protected-access
# pylint: disable=too-many-public-methods
# pylint: disable=bad-continuation
# pylint: disable=bad-indentation

import unittest

from okera import _thrift_api
from okera.tests import pycerebro_test_common as common

from okera._thrift_api import (
    TListFilesOp, TListFilesParams
)

def authorize_uri(planner, user, action, uri):
    params = TListFilesParams()
    params.op = action
    params.object = uri
    params.requesting_user = user
    params.authorize_only = True
    return planner.service.client.ListFiles(params)

class FsTest(unittest.TestCase):
    def test_grant(self):
        ctx = common.get_test_context()
        planner = common.get_planner(ctx)

        URI_BASE = 's3://cerebrodata-test/nytaxi-data'
        TEST_USER = 'fs_test_user'

        ddls = [
            "DROP ROLE IF EXISTS %s_role" % (TEST_USER),
            "CREATE ROLE %s_role" % (TEST_USER),
            "GRANT ROLE %s_role TO GROUP %s" % (TEST_USER, TEST_USER),
            "GRANT SELECT ON URI '%s/csv' TO ROLE %s_role" % (URI_BASE, TEST_USER),
            "GRANT SHOW ON URI '%s/parquet' TO ROLE %s_role" % (URI_BASE, TEST_USER),
            "GRANT ALL ON URI '%s/orc' TO ROLE %s_role" % (URI_BASE, TEST_USER),
            "GRANT SELECT ON URI '%s/uber' TO ROLE %s_role" % (URI_BASE, TEST_USER),
            "GRANT SHOW ON URI '%s/uber' TO ROLE %s_role" % (URI_BASE, TEST_USER),
            "GRANT INSERT ON URI '%s/uber' TO ROLE %s_role" % (URI_BASE, TEST_USER),
            "GRANT DELETE ON URI '%s/uber' TO ROLE %s_role" % (URI_BASE, TEST_USER),
            "GRANT INSERT ON URI '%s/parquet' TO ROLE %s_role" % (URI_BASE, TEST_USER),
            "GRANT DELETE ON URI '%s/parquet' TO ROLE %s_role" % (URI_BASE, TEST_USER),
        ]
        for ddl in ddls:
            planner.execute_ddl(ddl)

        # For list, check that we only have access if we granted SHOW or ALL
        authorize_uri(planner, TEST_USER, TListFilesOp.LIST, '%s/parquet' % URI_BASE)
        authorize_uri(planner, TEST_USER, TListFilesOp.LIST, '%s/orc' % URI_BASE)
        authorize_uri(planner, TEST_USER, TListFilesOp.LIST, '%s/uber' % URI_BASE)
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException,
                                    'does not have access'):
            authorize_uri(planner, TEST_USER, TListFilesOp.LIST, '%s/csv' % URI_BASE)

        # For read, check that we only have access if we granted SELECT or ALL
        authorize_uri(planner, TEST_USER, TListFilesOp.READ, '%s/orc/000067_0' % URI_BASE)
        authorize_uri(planner, TEST_USER, TListFilesOp.READ,
                      '%s/uber/10mb_chunksfk' % URI_BASE)
        authorize_uri(planner, TEST_USER, TListFilesOp.READ,
                      '%s/csv/trips_xcp.csv.gz' % URI_BASE)
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException,
                                    'does not have access'):
            authorize_uri(planner, TEST_USER, TListFilesOp.READ,
                          '%s/parquet/000067_0' % URI_BASE)

        # For write, check that we only have access if we granted INSERT or ALL
        authorize_uri(planner, TEST_USER, TListFilesOp.WRITE, '%s/parquet' % URI_BASE)
        authorize_uri(planner, TEST_USER, TListFilesOp.WRITE, '%s/orc' % URI_BASE)
        authorize_uri(planner, TEST_USER, TListFilesOp.WRITE, '%s/uber' % URI_BASE)
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException,
                                    'does not have access'):
            authorize_uri(planner, TEST_USER, TListFilesOp.WRITE, '%s/csv' % URI_BASE)

        # For delete, check that we only have access if we granted DELETE or ALL
        authorize_uri(planner, TEST_USER, TListFilesOp.DELETE, '%s/parquet' % URI_BASE)
        authorize_uri(planner, TEST_USER, TListFilesOp.DELETE, '%s/orc' % URI_BASE)
        authorize_uri(planner, TEST_USER, TListFilesOp.DELETE, '%s/uber' % URI_BASE)
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException,
                                    'does not have access'):
            authorize_uri(planner, TEST_USER, TListFilesOp.DELETE, '%s/csv' % URI_BASE)

    def test_ls(self):
        ctx = common.get_test_context()
        planner = common.get_planner(ctx)
        result = planner.ls('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/')
        self.assertEqual(
                ['s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'],
                result)
        result = planner.ls(
                's3://cerebrodata-test/fs_test_do_not_add_files_here/sample')
        self.assertEqual(
                ['s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'],
                result)
        result = planner.ls(
                's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt')
        self.assertEqual(
                ['s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'],
                result)
        result = planner.ls(
                's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt2')
        self.assertEqual([], result)
        planner.close()

    def test_cat(self):
        ctx = common.get_test_context()
        planner = common.get_planner(ctx)
        result = planner.cat(
                's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt')
        self.assertEqual('This is a sample test file.\nIt should consist of two lines.',
                         result)
        planner.close()

    def test_errors(self):
        ctx = common.get_test_context()
        planner = common.get_planner(ctx)
        with self.assertRaises(ValueError):
            planner.cat(
                's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/not-a-file')
        planner.close()

    def test_as_testuser(self):
        ctx = common.get_test_context()
        ctx.enable_token_auth(token_str='testuser')
        planner = common.get_planner(ctx)

        # Test user has access to this directory by URI
        result = planner.ls('s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/')
        self.assertEqual([
                's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'],
                result)
        result = planner.ls(
                's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt')
        self.assertEqual(
                ['s3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt'],
                result)
        result = planner.ls(
                's3://cerebrodata-test/fs_test_do_not_add_files_here/sample/sample.txt2')
        self.assertEqual([], result)

        # Test user does not have access to this directory
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException,
                                    'does not have access'):
            result = planner.ls('s3://cerebro-datasets/nytaxi-data/')

class RegisteredTest(unittest.TestCase):
    def test_basic(self):
        ctx = common.get_test_context()
        planner = common.get_planner(ctx)
        result = planner.get_catalog_objects_at('file:/opt/okera/data/users')
        self.assertTrue('file:/opt/okera/data/users' in result)
        self.assertTrue('okera_sample.users' in result['file:/opt/okera/data/users'])
        self.assertTrue('cerebro_sample.users' in result['file:/opt/okera/data/users'])

        result = planner.get_catalog_objects_at('file:/opt/okera/data/')
        self.assertTrue('file:/opt/okera/data/sample' in result)
        self.assertTrue('file:/opt/okera/data/users' in result)

        result = planner.get_catalog_objects_at('s3://cerebrodata-test/users')
        self.assertEqual(0, len(result))

        # Two datasets registered here
        result = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebro-datasets/transactions']
        self.assertEqual(2, len(datasets), msg=str(datasets))

        # Should not capture results from '/decimal-test1'
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/decimal-test')
        self.assertEqual(1, len(result), msg=str(result))
        result = result['s3://cerebrodata-test/decimal-test']
        self.assertEqual(2, len(result), msg=str(result))

        result = planner.cat('s3://cerebrodata-test/alltypes')
        self.assertEqual('true|0|1|2|3|4.0|5.0|hello|vchar1|char1|2015-01-01|3.141592',
                         result.split('\n')[0])

        planner.close()

    def test_as_testuser(self):
        ctx = common.get_test_context()
        ctx.enable_token_auth(token_str='testuser')
        planner = common.get_planner(ctx)

        result = planner.get_catalog_objects_at('file:/opt/okera/data/')
        self.assertTrue('file:/opt/okera/data/sample' in result)
        self.assertTrue('file:/opt/okera/data/users' in result)

        result = planner.get_catalog_objects_at('s3://cerebrodata-test/users')
        self.assertEqual(0, len(result))

        result1 = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions')
        self.assertEqual(1, len(result1))

        result2 = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions///')
        self.assertEqual(1, len(result2))

        result3 = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions/')
        self.assertEqual(1, len(result3))

        # Two datasets registered here, but this user only has one. Make sure it is
        # ACLed correctly.
        result = planner.get_catalog_objects_at('s3://cerebro-datasets/transactions')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebro-datasets/transactions']
        self.assertEqual(1, len(datasets))
        self.assertTrue('demo_test.transactions' in datasets)

        # Test user does not have access to this directory
        with self.assertRaisesRegex(_thrift_api.TRecordServiceException,
                                    'does not have access'):
            planner.get_catalog_objects_at('s3://cerebrodata-test/decimal-test')

        # Reading a path but this user only has column level permissions so only
        # a subset of the columns come back.
        result = planner.cat('s3://cerebrodata-test/alltypes')
        self.assertEqual('2,4.0,hello', result.split('\n')[0])
        planner.close()

    def test_masking(self):
        ctx = common.get_test_context()
        ctx.enable_token_auth(token_str='root')
        planner = common.get_planner(ctx)
        result = planner.cat('s3://cerebrodata-test/ccn').split('\n')[0]
        self.assertEqual('user1,4539797705756008', result)
        planner.close()

        ctx.enable_token_auth(token_str='testuser')
        planner = common.get_planner(ctx)
        result = planner.cat('s3://cerebrodata-test/ccn').split('\n')[0]
        self.assertEqual('user1,XXXXXXXXXXXX6008', result)
        planner.close()

    def test_dropping(self):
        ctx = common.get_test_context()
        planner = common.get_planner(ctx)
        planner.execute_ddl("DROP DATABASE IF EXISTS ofs CASCADE")
        planner.execute_ddl("CREATE DATABASE ofs")
        planner.execute_ddl(
            "CREATE EXTERNAL TABLE ofs.t1(s string) " +
            "LOCATION 's3://cerebrodata-test/empty-path-test'")

        result = planner.get_catalog_objects_at('s3://cerebrodata-test/empty-path-test')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebrodata-test/empty-path-test']
        self.assertEqual(1, len(datasets))
        self.assertEqual('ofs.t1', datasets[0])

        # Create T2
        planner.execute_ddl(
            "CREATE EXTERNAL TABLE ofs.t2(s string) " +
            "LOCATION 's3://cerebrodata-test/empty-path-test'")
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/empty-path-test')
        datasets = result['s3://cerebrodata-test/empty-path-test']
        self.assertEqual(2, len(datasets))
        self.assertTrue('ofs.t1' in datasets)
        self.assertTrue('ofs.t2' in datasets)

        # Drop t2, path should be gone
        planner.execute_ddl("DROP TABLE ofs.t2")
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/empty-path-test')
        self.assertEqual(1, len(result))
        datasets = result['s3://cerebrodata-test/empty-path-test']
        self.assertEqual(1, len(datasets))
        self.assertEqual('ofs.t1', datasets[0])

        # Drop t1, path should be gone
        planner.execute_ddl("DROP TABLE ofs.t1")
        result = planner.get_catalog_objects_at('s3://cerebrodata-test/empty-path-test')
        self.assertEqual(0, len(result))

if __name__ == "__main__":
    unittest.main()
