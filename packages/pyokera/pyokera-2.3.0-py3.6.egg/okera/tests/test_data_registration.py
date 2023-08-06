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
from okera._thrift_api import (
    TDataRegConnection, TRecordServiceException, TCrawlStatus)

class DataRegistrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Initializes one time state that is shared across test cases. This is used
            to speed up the tests. State that can be shared across (but still stable)
            should be here instead of __cleanup()."""
        super(DataRegistrationTest, cls).setUpClass()
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.manage_data_reg_connection(
                "DELETE",
                cls._get_psqltest_data_reg_connection_obj(cls, "test_connection_name"))
            conn.manage_data_reg_connection(
                "DELETE",
                cls._get_psqltest_data_reg_connection_obj(cls, "test_connection_name_2"))
            conn.manage_data_reg_connection(
                "DELETE",
                cls._get_mysqltest_data_reg_connection_obj(cls, "mysql_test_connection"))
            conn.manage_data_reg_connection(
                "DELETE",
                cls._get_mssqltest_data_reg_connection_obj(cls, "mssql_test_connection"))

    def _get_psqltest_data_reg_connection_obj(self, name):
        data_reg_connection = TDataRegConnection()
        data_reg_connection.name = name
        data_reg_connection.type = "JDBC"
        data_reg_connection.data_source_path = 's3://cerebro-datasets/' \
            'jdbc_demo/jdbc_test_psql.conf'
        data_reg_connection.jdbc_driver = "postgresql"
        data_reg_connection.host = "jdbcpsqltest.cyn8yfvyuugz.us-west-2.rds.amazonaws.com"
        data_reg_connection.port = 5432
        data_reg_connection.user_name = "awssm://postgres-jdbcpsqltest-username"
        data_reg_connection.password = "awssm://postgres-jdbcpsqltest-password"
        data_reg_connection.default_catalog = "jdbc_test"
        data_reg_connection.default_schema = "public"
        data_reg_connection.is_active = True
        data_reg_connection.connection_properties = {'ssl':'False'}
        return data_reg_connection

    def _get_mysqltest_data_reg_connection_obj(self, name):
        data_reg_connection = TDataRegConnection()
        data_reg_connection.name = name
        data_reg_connection.type = "JDBC"
        data_reg_connection.data_source_path = None
        data_reg_connection.jdbc_driver = "mysql"
        data_reg_connection.host = 'cerebro-db-test-long-running.cyn8yfvyuugz.' \
            'us-west-2.rds.amazonaws.com'
        data_reg_connection.port = 3306
        data_reg_connection.user_name = "awssm://mysql-username"
        data_reg_connection.password = "awssm://mysql-password"
        data_reg_connection.default_catalog = "jdbc_test"
        data_reg_connection.default_schema = None
        data_reg_connection.is_active = True
        data_reg_connection.connection_properties = {'ssl':'False'}
        return data_reg_connection

    def _get_mssqltest_data_reg_connection_obj(self, name):
        data_reg_connection = TDataRegConnection()
        data_reg_connection.name = name
        data_reg_connection.type = "JDBC"
        data_reg_connection.data_source_path = None
        data_reg_connection.jdbc_driver = "sqlserver"
        data_reg_connection.host = 'mssql-server-test.cyn8yfvyuugz.' \
            'us-west-2.rds.amazonaws.com'
        data_reg_connection.port = 1433
        data_reg_connection.user_name = "awssm://mssql-username"
        data_reg_connection.password = "awssm://mssql-password"
        data_reg_connection.default_catalog = "okera_test"
        data_reg_connection.default_schema = None
        data_reg_connection.is_active = True
        data_reg_connection.connection_properties = {'ssl':'False'}
        return data_reg_connection

    def _verify_mssql_table_schema(self, ret_list_jdbc_datasets, \
        ret_jdbc_schema, ret_jdbc_table):
        for dataset in ret_list_jdbc_datasets:
            if dataset.jdbc_schema == ret_jdbc_schema and \
                dataset.jdbc_table == ret_jdbc_table:
                for col in dataset.schema.cols:
                    if col.name == 'varchar':
                        self.assertTrue(col.type.type_id == 8) #TTypeId=8=VARCHAR
                        self.assertTrue(col.type.len == 20)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'text':
                        self.assertTrue(col.type.type_id == 7)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'tinyint':
                        self.assertTrue(col.type.type_id == 1)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'smallint':
                        self.assertTrue(col.type.type_id == 2)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'int':
                        self.assertTrue(col.type.type_id == 3)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'bigint':
                        self.assertTrue(col.type.type_id == 4)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'date':
                        self.assertTrue(col.type.type_id == 16)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'float_col':
                        self.assertTrue(col.type.type_id == 6)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'decimal':
                        self.assertTrue(col.type.type_id == 10)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision == 10)
                        self.assertTrue(col.type.scale == 2)
                    elif col.name == 'datetime':
                        self.assertTrue(col.type.type_id == 11)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'timestamp':
                        self.assertTrue(col.type.type_id == 15)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'time':
                        self.assertTrue(col.type.type_id == 11)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'char':
                        self.assertTrue(col.type.type_id == 9)
                        self.assertTrue(col.type.len == 10)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'binary':
                        self.assertTrue(col.type.type_id == 15)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'varbinary':
                        self.assertTrue(col.type.type_id == 15)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)

    def _verify_mysql_table_schema(self, ret_list_jdbc_datasets, \
        ret_jdbc_schema, ret_jdbc_table):
        for dataset in ret_list_jdbc_datasets:
            if dataset.jdbc_schema == ret_jdbc_schema and \
                dataset.jdbc_table == ret_jdbc_table:
                for col in dataset.schema.cols:
                    if col.name == 'varchar':
                        self.assertTrue(col.type.type_id == 8) #TTypeId=8=VARCHAR
                        self.assertTrue(col.type.len == 20)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'text':
                        self.assertTrue(col.type.type_id == 8)
                        self.assertTrue(col.type.len == 65355)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'double':
                        self.assertTrue(col.type.type_id == 6)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'date':
                        self.assertTrue(col.type.type_id == 16)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'float':
                        self.assertTrue(col.type.type_id == 6)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'decimal':
                        self.assertTrue(col.type.type_id == 10)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision == 10)
                        self.assertTrue(col.type.scale == 2)
                    elif col.name == 'datetime':
                        self.assertTrue(col.type.type_id == 11)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'timestamp':
                        self.assertTrue(col.type.type_id == 11)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'time':
                        self.assertTrue(col.type.type_id == 11)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'year':
                        self.assertTrue(col.type.type_id == 16)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'char':
                        self.assertTrue(col.type.type_id == 9)
                        self.assertTrue(col.type.len == 10)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'enum':
                        self.assertTrue(col.type.type_id == 9)
                        self.assertTrue(col.type.len == 1)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'set':
                        self.assertTrue(col.type.type_id == 9)
                        self.assertTrue(col.type.len == 5)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)
                    elif col.name == 'bool':
                        self.assertTrue(col.type.type_id == 0)
                        self.assertTrue(col.type.len is None)
                        self.assertTrue(col.type.precision is None)
                        self.assertTrue(col.type.scale is None)

    def test_drc_crud(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            # create test
            drc = self._get_psqltest_data_reg_connection_obj("test_connection_name")
            drcs = conn.manage_data_reg_connection("CREATE", drc)
            self.assertTrue(len(drcs.connections) == 1)

            # update test
            drc.host = "test_host_name_mod"
            drcs = conn.manage_data_reg_connection("UPDATE", drc)
            self.assertTrue(len(drcs.connections) == 1)
            self.assertEqual(drcs.connections[0].host,
                             "test_host_name_mod",
                             "Update data registration object connection failed.")

            # get test
            drcs = conn.manage_data_reg_connection("GET", drc)
            self.assertTrue(len(drcs.connections) == 1)

            # list with filters works as expected
            drcs = conn.manage_data_reg_connection(
                "LIST", drc, ["test_connection_name"])
            self.assertTrue(len(drcs.connections) >= 1)
            connection_names = [names.name for names in drcs.connections]
            self.assertTrue("test_connection_name" in connection_names,
                            "list data registration object connection failed.")

            # create another one
            drc = self._get_psqltest_data_reg_connection_obj("test_connection_name_2")
            drcs = conn.manage_data_reg_connection("CREATE", drc)
            self.assertTrue(len(drcs.connections) == 1)

            # list with empty filter should still return all
            drcs = conn.manage_data_reg_connection(
                "LIST", drc, [])
            self.assertTrue(len(drcs.connections) >= 2)
            connection_names = [names.name for names in drcs.connections]
            self.assertTrue("test_connection_name" in connection_names,
                            "list data registration object connection failed.")
            self.assertTrue("test_connection_name_2" in connection_names,
                            "list data registration object connection failed.")

            # list with pattern search works as expected
            drcs = conn.manage_data_reg_connection(
                "LIST", drc, ["test_connection_name", "test_connection_name_2"])
            self.assertTrue(len(drcs.connections) >= 2)
            ## Fixme: This is broken, looks like was always broken
            # self.assertEqual(drcs.connections[0].name,
            #                  "test_connection_name",
            #                  "list data registration object connection failed.")
            # self.assertEqual(drcs.connections[1].name,
            #                  "test_connection_name_2",
            #                  "list data registration object connection failed.")

            # Fixme:: Not yet working, returns all
            # list with pattern search works as expected
            # drcs = conn.manage_data_reg_connection(
            #     "LIST", drc, [], "test_connection_name_2")
            # print(drcs.connections)
            # self.assertTrue(len(drcs.connections) == 1)
            # self.assertEqual(drcs.connections[0].name,
            #                  "test_connection_name_2",
            #                  "list data registration object connection failed." +
            #                  len(drcs.connections))

            # delete test
            drcs = conn.manage_data_reg_connection("DELETE", drc)
            self.assertTrue(len(drcs.connections) == 0)

            # get again returns empty
            drcs = conn.manage_data_reg_connection("GET", drc)
            self.assertTrue(len(drcs.connections) == 0)

    def test_invalid_jdbc_props(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            # validation for invalid path
            drc = self._get_psqltest_data_reg_connection_obj('test_conn_invalid_path')
            drc.data_source_path = 's3://some-invalid-path/test.conf'
            try:
                drcs = conn.manage_data_reg_connection('CREATE', drc)
                assert drcs
            except TRecordServiceException as ex:
                assert 'JDBC credentials validation failed for data registration ' \
                    'connection with name ' + drc.name in str(ex.detail)

            drc = self._get_psqltest_data_reg_connection_obj('test_conn_invalid_path')
            drcs = conn.manage_data_reg_connection('CREATE', drc)
            self.assertTrue(len(drcs.connections) == 1)
            # validation for invalid path update
            drc.data_source_path = 's3://some-invalid-path/test.conf'
            try:
                drcs = conn.manage_data_reg_connection('UPDATE', drc)
                assert drcs
            except TRecordServiceException as ex:
                assert 'JDBC credentials validation failed for data registration ' \
                    'connection with name ' + drc.name in str(ex.detail)

            drcs = conn.manage_data_reg_connection('DELETE', drc)
            self.assertTrue(len(drcs.connections) == 0)

    def test_discover_crawler_catalog(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            #MySQL Test
            drc = self._get_mysqltest_data_reg_connection_obj('mysql_test_connection')
            drcs = conn.manage_data_reg_connection('DELETE', drc)
            self.assertTrue(len(drcs.connections) == 0)
            drcs = conn.manage_data_reg_connection('CREATE', drc)
            ret_crawler_objects = conn.discover_crawler(drc)
            ret_list_jdbc_datasets = ret_crawler_objects.crawler_discover_datasets[0] \
                .jdbc_datasets
            self.assertTrue(len(ret_crawler_objects.crawler_discover_datasets) == 1)
            self.assertIsNotNone(ret_list_jdbc_datasets)
            self.assertTrue(any(x.jdbc_catalog == 'jdbc_test'\
                for x in ret_list_jdbc_datasets))

            #Microsoft SQL Server Test
            drc = self._get_mssqltest_data_reg_connection_obj('mssql_test_connection')
            drcs = conn.manage_data_reg_connection('DELETE', drc)
            self.assertTrue(len(drcs.connections) == 0)
            drcs = conn.manage_data_reg_connection('CREATE', drc)
            ret_crawler_objects = conn.discover_crawler(drc)
            ret_list_jdbc_datasets = ret_crawler_objects.crawler_discover_datasets[0] \
                .jdbc_datasets

            self.assertTrue(len(ret_crawler_objects.crawler_discover_datasets) == 1)
            self.assertIsNotNone(ret_list_jdbc_datasets)
            self.assertTrue(any(x.jdbc_catalog == 'okera_test'\
                for x in ret_list_jdbc_datasets))

    def test_crawler(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            drc = self._get_psqltest_data_reg_connection_obj('test_conn_crawler')
            drc.data_source_path = 's3://cerebro-datasets/jdbc_demo/jdbc_test_psql.conf'
            resp = conn.manage_crawler(drc)
            self.assertTrue(resp.status == TCrawlStatus.CRAWLING)

            drc = self._get_psqltest_data_reg_connection_obj('test_conn_crawler_s3')
            drc.type = "S3"
            drc.data_source_path = 's3://cerebrodata-test/tpch-nation/'
            resp = conn.manage_crawler(drc)
            self.assertTrue(resp.status == TCrawlStatus.CRAWLING)

    def test_discover_crawler_schema(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            drc = self._get_mssqltest_data_reg_connection_obj('mssql_test_connection')
            drcs = conn.manage_data_reg_connection('DELETE', drc)
            self.assertTrue(len(drcs.connections) == 0)
            drcs = conn.manage_data_reg_connection('CREATE', drc)
            ret_crawler_objects = conn.discover_crawler(drc, 'okera_test')
            ret_list_jdbc_datasets = ret_crawler_objects.crawler_discover_datasets[0] \
                .jdbc_datasets

            self.assertTrue(len(ret_crawler_objects.crawler_discover_datasets) == 1)
            self.assertIsNotNone(ret_list_jdbc_datasets)
            self.assertTrue(any(x.jdbc_catalog == 'okera_test' \
                for x in ret_list_jdbc_datasets))
            #for dataset in ret_list_jdbc_datasets:
            #    print(dataset.jdbc_schema)
            self.assertTrue(any(x.jdbc_schema == 'okera_test.marketing' \
                for x in ret_list_jdbc_datasets))
            self.assertTrue(any(x.jdbc_schema == 'okera_test.dbo' \
                for x in ret_list_jdbc_datasets))
            self.assertFalse(any(x.jdbc_schema == 'okera_test.INFORMATION_SCHEMA' \
                for x in ret_list_jdbc_datasets))
            drcs = conn.manage_data_reg_connection('DELETE', drc)
            self.assertTrue(len(drcs.connections) == 0)

    def test_discover_crawler_table_schema(self):
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            #MySQL Test
            drc = self._get_mysqltest_data_reg_connection_obj('mysql_test_connection')
            drcs = conn.manage_data_reg_connection('DELETE', drc)
            self.assertTrue(len(drcs.connections) == 0)
            drcs = conn.manage_data_reg_connection('CREATE', drc)
            ret_crawler_objects = conn.discover_crawler(drc, 'jdbc_test')
            ret_list_jdbc_datasets = ret_crawler_objects.crawler_discover_datasets[0] \
                .jdbc_datasets

            self.assertTrue(len(ret_crawler_objects.crawler_discover_datasets) == 1)
            self.assertIsNotNone(ret_list_jdbc_datasets)
            self.assertTrue(any(x.jdbc_catalog == 'jdbc_test'\
                for x in ret_list_jdbc_datasets))
            #for dataset in ret_list_jdbc_datasets:
            #    print(dataset)
            self.assertTrue(any(x.jdbc_table == 'all_data_types' \
                for x in ret_list_jdbc_datasets))
            self._verify_mysql_table_schema(ret_list_jdbc_datasets, \
                None, 'all_data_types')
            drcs = conn.manage_data_reg_connection('DELETE', drc)
            self.assertTrue(len(drcs.connections) == 0)

            #Microsoft SQL Server Test
            drc = self._get_mssqltest_data_reg_connection_obj('mssql_test_connection')
            drcs = conn.manage_data_reg_connection('DELETE', drc)
            self.assertTrue(len(drcs.connections) == 0)
            drcs = conn.manage_data_reg_connection('CREATE', drc)
            ret_crawler_objects = conn.discover_crawler(drc, 'okera_test',\
                 'okera_test.dbo')
            ret_list_jdbc_datasets = ret_crawler_objects.crawler_discover_datasets[0]\
                .jdbc_datasets

            self.assertTrue(len(ret_crawler_objects.crawler_discover_datasets) == 1)
            self.assertIsNotNone(ret_list_jdbc_datasets)
            self.assertTrue(any(x.jdbc_catalog == 'okera_test' \
                for x in ret_list_jdbc_datasets))
            self.assertTrue(any(x.jdbc_schema == 'okera_test.dbo' \
                for x in ret_list_jdbc_datasets))
            #for dataset in ret_list_jdbc_datasets:
            #    print(dataset.jdbc_table)
            self.assertTrue(any(x.jdbc_table == 'all_data_types' \
                for x in ret_list_jdbc_datasets))

            for dataset in ret_list_jdbc_datasets:
                if dataset.jdbc_schema == 'okera_test.dbo' and \
                   dataset.jdbc_table == 'dbo.all_data_types':
                    self.assertTrue(any(x.name == 'varchar' \
                        for x in dataset.schema.cols))
            self._verify_mssql_table_schema(ret_list_jdbc_datasets, \
                'okera_test.dbo', 'dbo.all_data_types')
            #for dataset in ret_list_jdbc_datasets:
            #    print(dataset)

            drcs = conn.manage_data_reg_connection('DELETE', drc)
            self.assertTrue(len(drcs.connections) == 0)

if __name__ == "__main__":
    unittest.main()
