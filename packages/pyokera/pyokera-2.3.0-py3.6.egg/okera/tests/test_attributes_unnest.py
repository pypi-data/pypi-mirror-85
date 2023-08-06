# Copyright 2019 Okera Inc. All Rights Reserved.
#
# Some integration tests for managing attributes
#
# pylint: disable=bad-continuation
# pylint: disable=line-too-long
# pylint: disable=too-many-locals
# pylint: disable=too-many-lines

import unittest

from okera.tests import pycerebro_test_common as common

class AttributesTest(unittest.TestCase):

    # skip_cascade is a flag to skip tests for known bugs, remove when fixed
    def _validate(self, conn, db, attr, tags, sql, expected, skip_cascade=False):
        # Create the view and then assign the tag, validate tag INHERITANCE
        conn.execute_ddl("DROP VIEW IF EXISTS %s.v" % db)
        conn.execute_ddl("CREATE VIEW %s.v AS %s" % (db, sql))

        conn.execute_ddl("drop attribute if exists %s.a1" % db)
        conn.execute_ddl("create attribute %s.a1" % db)
        for tag in tags:
            conn.assign_attribute(db, attr, tag[0], tag[1], tag[2], cascade=True)

        print(conn.execute_ddl_table_output('DESCRIBE %s.v' % db))
        self.assertEqual(
            expected,
            str(conn.execute_ddl_table_output('DESCRIBE %s.v' % db)))

        # Recreate the view (tagged already assigned), validate tag CASCADE
        if not skip_cascade:
            conn.execute_ddl("DROP VIEW IF EXISTS %s.v" % db)
            conn.execute_ddl("CREATE VIEW %s.v AS %s" % (db, sql))
            print(conn.execute_ddl_table_output('DESCRIBE %s.v' % db))
            self.assertEqual(
                expected,
                str(conn.execute_ddl_table_output('DESCRIBE %s.v' % db)))

    def test_specific(self):
        # Not a test, just skeleton to test a specific scenario
        db = 'attr_test_db'
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("drop database if exists %s cascade" % db)
            conn.execute_ddl("create database if not exists %s" % db)

            self._validate(conn, db, 'a1',
                [['chase', 'subscription_currency', 'currency.country']],
                'select ** from chase.subscription_currency',
                """
+-----------------------+--------+---------+-----------------+
|          name         |  type  | comment |    attributes   |
+-----------------------+--------+---------+-----------------+
|    currency_country   | string |         | attr_test_db.a1 |
| currency_currencycode | string |         |                 |
+-----------------------+--------+---------+-----------------+""".strip(), skip_cascade=True)

    def test_unnest_attributes(self):
        db = 'attr_test_db'
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("drop database if exists %s cascade" % db)
            conn.execute_ddl("create database if not exists %s" % db)

            # No tags
            self._validate(conn, db, 'a1', [],
                """select productkey, partyroles.item.partykey as partykey
                   from chase.zd1238_4, chase.zd1238_4.partyroles""",
                """
+------------+--------+---------+------------+
|    name    |  type  | comment | attributes |
+------------+--------+---------+------------+
| productkey | string |         |            |
|  partykey  | string |         |            |
+------------+--------+---------+------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'zd1238_4', 'productkey'],
                 ['chase', 'zd1238_4', 'partyroles.partykey']],
                """select productkey, partyroles.item.partykey as partykey
                   from chase.zd1238_4, chase.zd1238_4.partyroles""",
                """
+------------+--------+---------+-----------------+
|    name    |  type  | comment |    attributes   |
+------------+--------+---------+-----------------+
| productkey | string |         | attr_test_db.a1 |
|  partykey  | string |         | attr_test_db.a1 |
+------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'zd1238_4', 'productkey']],
                """select productkey, partyroles.item.partykey as partykey
                   from chase.zd1238_4, chase.zd1238_4.partyroles""",
                """
+------------+--------+---------+-----------------+
|    name    |  type  | comment |    attributes   |
+------------+--------+---------+-----------------+
| productkey | string |         | attr_test_db.a1 |
|  partykey  | string |         |                 |
+------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'zd1238_4', 'partyroles.partykey']],
                """select productkey, partyroles.item.partykey as partykey
                   from chase.zd1238_4, chase.zd1238_4.partyroles""",
                """
+------------+--------+---------+-----------------+
|    name    |  type  | comment |    attributes   |
+------------+--------+---------+-----------------+
| productkey | string |         |                 |
|  partykey  | string |         | attr_test_db.a1 |
+------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex', 'strarray_t', 'str_arr']],
                """select id, str_arr.item
                   from rs_complex.strarray_t, rs_complex.strarray_t.str_arr""",
                """
+------+--------+---------+-----------------+
| name |  type  | comment |    attributes   |
+------+--------+---------+-----------------+
|  id  | bigint |         |                 |
| item | string |         | attr_test_db.a1 |
+------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_t', 'a1']],
                """select unnest_alias.item, unnest_alias.item.f1 as f1
                   from rs_complex.array_struct_t,
                   rs_complex.array_struct_t.a1 unnest_alias""",
                """
+------+--------------+---------+-----------------+
| name |     type     | comment |    attributes   |
+------+--------------+---------+-----------------+
| item |   struct<    |         | attr_test_db.a1 |
|      |   f1:string, |         |                 |
|      |   f2:string  |         |                 |
|      |      >       |         |                 |
|  f1  |    string    |         |                 |
+------+--------------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'subscription_currency', 'currency.country']],
                'select ** from chase.subscription_currency',
                """
+-----------------------+--------+---------+-----------------+
|          name         |  type  | comment |    attributes   |
+-----------------------+--------+---------+-----------------+
|    currency_country   | string |         | attr_test_db.a1 |
| currency_currencycode | string |         |                 |
+-----------------------+--------+---------+-----------------+""".strip())

            # FIXME: this is not cascading correctly
            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_t', 'a1.f1']],
                """select unnest_alias.item, unnest_alias.item.f1 as f1
                   from rs_complex.array_struct_t,
                   rs_complex.array_struct_t.a1 unnest_alias""",
                """
+------+--------------+---------+-----------------+
| name |     type     | comment |    attributes   |
+------+--------------+---------+-----------------+
| item |   struct<    |         |                 |
|      |   f1:string, |         | attr_test_db.a1 |
|      |   f2:string  |         |                 |
|      |      >       |         |                 |
|  f1  |    string    |         | attr_test_db.a1 |
+------+--------------+---------+-----------------+""".strip(), skip_cascade=True)

            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_t', 'a1.f2']],
                """select a1.item.f2 as f2, a1.item.f1 as f1
                   from rs_complex.array_struct_t, rs_complex.array_struct_t.a1""",
                """
+------+--------+---------+-----------------+
| name |  type  | comment |    attributes   |
+------+--------+---------+-----------------+
|  f2  | string |         | attr_test_db.a1 |
|  f1  | string |         |                 |
+------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_t', 'a1.f2'],
                 ['rs_complex', 'array_struct_t', 'a1.f1']],
                """select a1.item.f2 as f2, a1.item.f1 as f1
                   from rs_complex.array_struct_t, rs_complex.array_struct_t.a1""",
                """
+------+--------+---------+-----------------+
| name |  type  | comment |    attributes   |
+------+--------+---------+-----------------+
|  f2  | string |         | attr_test_db.a1 |
|  f1  | string |         | attr_test_db.a1 |
+------+--------+---------+-----------------+""".strip())

            # FIXME: this is not cascading correctly
            self._validate(conn, db, 'a1',
               [['rs_complex', 'array_struct_t', 'a1.f1'],
                 ['rs_complex', 'array_struct_t', 'a1.f2']],
                """select a1.item as item, a1.item.f1 as f1
                   from rs_complex.array_struct_t, rs_complex.array_struct_t.a1""",
                """
+------+--------------+---------+-----------------+
| name |     type     | comment |    attributes   |
+------+--------------+---------+-----------------+
| item |   struct<    |         |                 |
|      |   f1:string, |         | attr_test_db.a1 |
|      |   f2:string  |         | attr_test_db.a1 |
|      |      >       |         |                 |
|  f1  |    string    |         | attr_test_db.a1 |
+------+--------------+---------+-----------------+""".strip(), skip_cascade=True)

            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_array', 'a1.a2'],
                 ['rs_complex', 'array_struct_array', 'a1.f1']],
                """select a1.item.a2 as a2, a1.item.f1 as f1
                   from rs_complex.array_struct_array,
                   rs_complex.array_struct_array.a1""",
                """
+------+---------------+---------+-----------------+
| name |      type     | comment |    attributes   |
+------+---------------+---------+-----------------+
|  a2  | array<string> |         | attr_test_db.a1 |
|  f1  |     string    |         | attr_test_db.a1 |
+------+---------------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'zd1238_4', 'partyroles.partykey']],
                """select partyroles.item.partykey as partykey,
                          tokenize(partyroles.item.partykey) as tokenized_key
                   from chase.zd1238_4 c, c.partyroles
                   where partyroles.item.partykey =
                      '1a43fd68-31d0-46a4-b3f0-bc42730ed5f7'""",
                """
+---------------+--------+---------+-----------------+
|      name     |  type  | comment |    attributes   |
+---------------+--------+---------+-----------------+
|    partykey   | string |         | attr_test_db.a1 |
| tokenized_key | string |         |                 |
+---------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex_parquet', 'spark_gzip', 'int32'],
                 ['rs_complex_parquet', 'spark_gzip', 'str_arr'],
                 ['rs_complex_parquet', 'spark_gzip', 'int_arr']],
                """select int32, str_arr.item as str_arr, int_arr.item as int_arr
                   from rs_complex_parquet.spark_gzip,
                        rs_complex_parquet.spark_gzip.str_arr,
                        rs_complex_parquet.spark_gzip.int_arr""",
                """
+---------+--------+---------+-----------------+
|   name  |  type  | comment |    attributes   |
+---------+--------+---------+-----------------+
|  int32  |  int   |         | attr_test_db.a1 |
| str_arr | string |         | attr_test_db.a1 |
| int_arr |  int   |         | attr_test_db.a1 |
+---------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'zd1211', 'accountnumber'],
                 ['chase', 'zd1211', 'productdetails.subproducts']],
                """select accountnumber, subproducts.item
                   from chase.zd1211, chase.zd1211.productdetails.subproducts
                   where accountnumber in ('65360119', '26509759')""",
"""
+---------------+--------+---------+-----------------+
|      name     |  type  | comment |    attributes   |
+---------------+--------+---------+-----------------+
| accountnumber | string |         | attr_test_db.a1 |
|      item     | string |         | attr_test_db.a1 |
+---------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_array', 'a1.f1']],
                """select b.* from rs_complex.array_struct_array a, a.a1 b
                   where b.item.f1 = 'ab'""",
"""
+------+---------------+---------+-----------------+
| name |      type     | comment |    attributes   |
+------+---------------+---------+-----------------+
|  f1  |     string    |         | attr_test_db.a1 |
|  f2  |     string    |         |                 |
|  a2  | array<string> |         |                 |
+------+---------------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'product', 'productkey'],
                 ['chase', 'product', 'feescharges.feeamount'],
                 ['chase', 'product', 'feescharges.feename']],
                """select p.productkey, fc.item.feename as feename,
                   fc.item.feeamount as feeamount from chase.product p, p.feescharges fc
                   where fc.item.feeamount = '10.1' and fc.item.feename = 'STOPCHEQUE'""",
"""
+------------+--------+---------+-----------------+
|    name    |  type  | comment |    attributes   |
+------------+--------+---------+-----------------+
| productkey | string |         | attr_test_db.a1 |
|  feename   | string |         | attr_test_db.a1 |
| feeamount  | string |         | attr_test_db.a1 |
+------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'zd1211', 'accountnumber'],
                ['chase', 'zd1211', 'productdetails.subproducts']],
                """select accountnumber, subproducts.item from chase.zd1211,
                   chase.zd1211.productdetails.subproducts
                   where accountnumber in ('65360119', '26509759')""",
"""
+---------------+--------+---------+-----------------+
|      name     |  type  | comment |    attributes   |
+---------------+--------+---------+-----------------+
| accountnumber | string |         | attr_test_db.a1 |
|      item     | string |         | attr_test_db.a1 |
+---------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex_parquet', 'array_struct_t', 'a1'],
                 ['rs_complex_parquet', 'array_struct_t', 'a1.f1']],
                """select t1.item, t1.item.f1 as f1
                   from rs_complex_parquet.array_struct_t, rs_complex.array_struct_t,
                        rs_complex_parquet.array_struct_t.a1 t1
                   join rs_complex.array_struct_t.a1 t2 ON (t1.item.f1 = t2.item.f1)""",
"""
+------+--------------+---------+-----------------+
| name |     type     | comment |    attributes   |
+------+--------------+---------+-----------------+
| item |   struct<    |         | attr_test_db.a1 |
|      |   f1:string, |         | attr_test_db.a1 |
|      |   f2:string  |         |                 |
|      |      >       |         |                 |
|  f1  |    string    |         | attr_test_db.a1 |
+------+--------------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex_parquet', 'array_struct_t', 'a1.f1']],
                """select a1.* from rs_complex_parquet.array_struct_t,
                   rs_complex_parquet.array_struct_t.a1""",
"""
+------+--------+---------+-----------------+
| name |  type  | comment |    attributes   |
+------+--------+---------+-----------------+
|  f1  | string |         | attr_test_db.a1 |
|  f2  | string |         |                 |
+------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex_parquet', 'array_struct_t', 'a1.f1'],
                 ['rs_complex_parquet', 'array_struct_t', 'a1.f2']],
                """select a1.* from rs_complex_parquet.array_struct_t,
                   rs_complex_parquet.array_struct_t.a1""",
"""
+------+--------+---------+-----------------+
| name |  type  | comment |    attributes   |
+------+--------+---------+-----------------+
|  f1  | string |         | attr_test_db.a1 |
|  f2  | string |         | attr_test_db.a1 |
+------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'product', 'limits.transactionlimits.description'],
                 ['chase', 'product', 'limits.transactionlimits.transactionname']],
                """select tlimits.* from chase.product p,
                   p.limits.transactionlimits tlimits""",
"""
+-----------------+--------+---------+-----------------+
|       name      |  type  | comment |    attributes   |
+-----------------+--------+---------+-----------------+
| transactionname | string |         | attr_test_db.a1 |
|   description   | string |         | attr_test_db.a1 |
|  minimumamount  | string |         |                 |
|  maximumamount  | string |         |                 |
|   resetperiod   | string |         |                 |
+-----------------+--------+---------+-----------------+""".strip())

            #
            # FIXME: this is not right. Not inheriting inside f1. The cascade value
            # is actually correct.
            #
            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_array', 'a1'],
                 ['rs_complex', 'array_struct_array', 'a1.f1'],
                 ['rs_complex', 'array_struct_array', 'a1.a2']],
                """select a.*, b.* from rs_complex.array_struct_array a, a.a1 b""",
"""
+------+--------------------+---------+-----------------+
| name |        type        | comment |    attributes   |
+------+--------------------+---------+-----------------+
|  a1  |   array<struct<    |         | attr_test_db.a1 |
|      |      f1:string,    |         |                 |
|      |      f2:string,    |         |                 |
|      |   a2:array<string> |         |                 |
|      |         >>         |         |                 |
|  f1  |       string       |         | attr_test_db.a1 |
|  f2  |       string       |         |                 |
|  a2  |   array<string>    |         | attr_test_db.a1 |
+------+--------------------+---------+-----------------+""".strip(), skip_cascade=True)

            self._validate(conn, db, 'a1',
                [['functional', 'allcomplextypes', 'id'],
                 ['functional', 'allcomplextypes', 'nested_struct_col.f1']],
                """select * from functional.allcomplextypes,
                   functional.allcomplextypes.int_array_col""",
"""
+---------------------------+----------------------------+---------+-----------------+
|            name           |            type            | comment |    attributes   |
+---------------------------+----------------------------+---------+-----------------+
|             id            |            int             |         | attr_test_db.a1 |
|       int_array_col       |         array<int>         |         |                 |
|      array_array_col      |     array<array<int>>      |         |                 |
|       map_array_col       |   array<map<string,int>>   |         |                 |
|      struct_array_col     |       array<struct<        |         |                 |
|                           |          f1:bigint,        |         |                 |
|                           |          f2:string         |         |                 |
|                           |             >>             |         |                 |
|        int_map_col        |      map<string,int>       |         |                 |
|       array_map_col       |   map<string,array<int>>   |         |                 |
|       struct_map_col      |     map<string,struct<     |         |                 |
|                           |          f1:bigint,        |         |                 |
|                           |          f2:string         |         |                 |
|                           |             >>             |         |                 |
|       int_struct_col      |          struct<           |         |                 |
|                           |           f1:int,          |         |                 |
|                           |            f2:int          |         |                 |
|                           |             >              |         |                 |
|     complex_struct_col    |          struct<           |         |                 |
|                           |           f1:int,          |         |                 |
|                           |        f2:array<int>,      |         |                 |
|                           |      f3:map<string,int>    |         |                 |
|                           |             >              |         |                 |
|     nested_struct_col     |          struct<           |         |                 |
|                           |           f1:int,          |         | attr_test_db.a1 |
|                           |          f2:struct<        |         |                 |
|                           |          f11:bigint,       |         |                 |
|                           |          f12:struct<       |         |                 |
|                           |            f21:bigint      |         |                 |
|                           |               >            |         |                 |
|                           |              >             |         |                 |
|                           |             >              |         |                 |
| complex_nested_struct_col |          struct<           |         |                 |
|                           |           f1:int,          |         |                 |
|                           |       f2:array<struct<     |         |                 |
|                           |          f11:bigint,       |         |                 |
|                           |     f12:map<string,struct< |         |                 |
|                           |            f21:bigint      |         |                 |
|                           |               >>           |         |                 |
|                           |              >>            |         |                 |
|                           |             >              |         |                 |
|            item           |            int             |         |                 |
|            year           |            int             |         |                 |
|           month           |            int             |         |                 |
+---------------------------+----------------------------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['functional', 'allcomplextypes', 'array_array_col'],
                 ['functional', 'allcomplextypes', 'nested_struct_col.f2.f12.f21']],
                """select * from functional.allcomplextypes,
                   functional.allcomplextypes.int_map_col""",
"""
+---------------------------+----------------------------+---------+-----------------+
|            name           |            type            | comment |    attributes   |
+---------------------------+----------------------------+---------+-----------------+
|             id            |            int             |         |                 |
|       int_array_col       |         array<int>         |         |                 |
|      array_array_col      |     array<array<int>>      |         | attr_test_db.a1 |
|       map_array_col       |   array<map<string,int>>   |         |                 |
|      struct_array_col     |       array<struct<        |         |                 |
|                           |          f1:bigint,        |         |                 |
|                           |          f2:string         |         |                 |
|                           |             >>             |         |                 |
|        int_map_col        |      map<string,int>       |         |                 |
|       array_map_col       |   map<string,array<int>>   |         |                 |
|       struct_map_col      |     map<string,struct<     |         |                 |
|                           |          f1:bigint,        |         |                 |
|                           |          f2:string         |         |                 |
|                           |             >>             |         |                 |
|       int_struct_col      |          struct<           |         |                 |
|                           |           f1:int,          |         |                 |
|                           |            f2:int          |         |                 |
|                           |             >              |         |                 |
|     complex_struct_col    |          struct<           |         |                 |
|                           |           f1:int,          |         |                 |
|                           |        f2:array<int>,      |         |                 |
|                           |      f3:map<string,int>    |         |                 |
|                           |             >              |         |                 |
|     nested_struct_col     |          struct<           |         |                 |
|                           |           f1:int,          |         |                 |
|                           |          f2:struct<        |         |                 |
|                           |          f11:bigint,       |         |                 |
|                           |          f12:struct<       |         |                 |
|                           |            f21:bigint      |         | attr_test_db.a1 |
|                           |               >            |         |                 |
|                           |              >             |         |                 |
|                           |             >              |         |                 |
| complex_nested_struct_col |          struct<           |         |                 |
|                           |           f1:int,          |         |                 |
|                           |       f2:array<struct<     |         |                 |
|                           |          f11:bigint,       |         |                 |
|                           |     f12:map<string,struct< |         |                 |
|                           |            f21:bigint      |         |                 |
|                           |               >>           |         |                 |
|                           |              >>            |         |                 |
|                           |             >              |         |                 |
|            key            |           string           |         |                 |
|           value           |            int             |         |                 |
|            year           |            int             |         |                 |
|           month           |            int             |         |                 |
+---------------------------+----------------------------+---------+-----------------+""".strip())

            #
            # TODO: maps are not supported
            #
            self._validate(conn, db, 'a1',
                [['functional', 'allcomplextypes', 'complex_nested_struct_col.f2.f12.key']],
                """select f12.key from functional.allcomplextypes,
                   functional.allcomplextypes.complex_nested_struct_col.f2.f12""",
"""
+------+--------+---------+------------+
| name |  type  | comment | attributes |
+------+--------+---------+------------+
| key  | string |         |            |
+------+--------+---------+------------+""".strip())

            self._validate(conn, db, 'a1',
                [['functional', 'allcomplextypes', 'int_array_col']],
                """select a.id, int_array_col.item from
                   functional.allcomplextypes a, a.int_array_col""",
"""
+------+------+---------+-----------------+
| name | type | comment |    attributes   |
+------+------+---------+-----------------+
|  id  | int  |         |                 |
| item | int  |         | attr_test_db.a1 |
+------+------+---------+-----------------+""".strip())

    def test_full_unnest_attributes(self):
        db = 'attr_test_db'
        ctx = common.get_test_context()
        with common.get_planner(ctx) as conn:
            conn.execute_ddl("drop database if exists %s cascade" % db)
            conn.execute_ddl("create database if not exists %s" % db)

            # No tags
            self._validate(conn, db, 'a1', [],
                'select ** from chase.zd1238_4',
                """
+--------------------------------------------------+---------+---------+------------+
|                       name                       |   type  | comment | attributes |
+--------------------------------------------------+---------+---------+------------+
|                 subscriptionkey                  |  string |         |            |
|             partyroles_item_partykey             |  string |         |            |
|            partyroles_item_tenantkey             |  string |         |            |
|               partyroles_item_role               |  string |         |            |
|           partyroles_item_partyrolekey           |  string |         |            |
|           partyroles_item_createddate            |  string |         |            |
|           partyroles_item_updateddate            |  string |         |            |
|                    productkey                    |  string |         |            |
|                  productversion                  |   int   |         |            |
|                   producttype                    |  string |         |            |
|              parentsubscriptionkey               |  string |         |            |
|               parentaccountnumber                |  string |         |            |
|                  accountnumber                   |  string |         |            |
|                     sortcode                     |  string |         |            |
|                   productname                    |  string |         |            |
|             requiredexternalid_item              |  string |         |            |
|                 currency_country                 |  string |         |            |
|              currency_currencycode               |  string |         |            |
|                  periodiccycle                   |  string |         |            |
|                subscriptionstatus                |  string |         |            |
|                   createddate                    |  string |         |            |
|                   updateddate                    |  string |         |            |
|   feeconfigurations_item_applicationfrequency    |  string |         |            |
|  feeconfigurations_item_chargeincludedindicator  | boolean |         |            |
|       feeconfigurations_item_chargingcycle       |  string |         |            |
|     feeconfigurations_item_decision_tablekey     |  string |         |            |
|    feeconfigurations_item_decision_input_item    |  string |         |            |
| feeconfigurations_item_event_eventidentification |  string |         |            |
|      feeconfigurations_item_event_eventname      |  string |         |            |
|         feeconfigurations_item_feeamount         |  string |         |            |
|     feeconfigurations_item_feecap_capamount      |  string |         |            |
|   feeconfigurations_item_feecap_capoccurrence    |  string |         |            |
|   feeconfigurations_item_feecap_cappingperiod    |  string |         |            |
|        feeconfigurations_item_feecategory        |  string |         |            |
|     feeconfigurations_item_feeidentification     |  string |         |            |
|          feeconfigurations_item_feename          |  string |         |            |
|       feeconfigurations_item_feerate_rate        |  string |         |            |
|   feeconfigurations_item_feerate_notionalvalue   |  string |         |            |
|          feeconfigurations_item_feetype          |  string |         |            |
|        feeconfigurations_item_maximumfee         |  string |         |            |
|        feeconfigurations_item_minimumfee         |  string |         |            |
|          feeconfigurations_item_taxrate          |  string |         |            |
|   feeconfigurations_item_statementdescription    |  string |         |            |
|  feeconfigurations_item_validityperiod_enddate   |  string |         |            |
| feeconfigurations_item_validityperiod_startdate  |  string |         |            |
|             kafka_message_timestamp              |  bigint |         |            |
+--------------------------------------------------+---------+---------+------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'zd1238_4', 'productkey'],
                 ['chase', 'zd1238_4', 'partyroles.partykey']],
                'select ** from chase.zd1238_4',
                """
+--------------------------------------------------+---------+---------+-----------------+
|                       name                       |   type  | comment |    attributes   |
+--------------------------------------------------+---------+---------+-----------------+
|                 subscriptionkey                  |  string |         |                 |
|             partyroles_item_partykey             |  string |         | attr_test_db.a1 |
|            partyroles_item_tenantkey             |  string |         |                 |
|               partyroles_item_role               |  string |         |                 |
|           partyroles_item_partyrolekey           |  string |         |                 |
|           partyroles_item_createddate            |  string |         |                 |
|           partyroles_item_updateddate            |  string |         |                 |
|                    productkey                    |  string |         | attr_test_db.a1 |
|                  productversion                  |   int   |         |                 |
|                   producttype                    |  string |         |                 |
|              parentsubscriptionkey               |  string |         |                 |
|               parentaccountnumber                |  string |         |                 |
|                  accountnumber                   |  string |         |                 |
|                     sortcode                     |  string |         |                 |
|                   productname                    |  string |         |                 |
|             requiredexternalid_item              |  string |         |                 |
|                 currency_country                 |  string |         |                 |
|              currency_currencycode               |  string |         |                 |
|                  periodiccycle                   |  string |         |                 |
|                subscriptionstatus                |  string |         |                 |
|                   createddate                    |  string |         |                 |
|                   updateddate                    |  string |         |                 |
|   feeconfigurations_item_applicationfrequency    |  string |         |                 |
|  feeconfigurations_item_chargeincludedindicator  | boolean |         |                 |
|       feeconfigurations_item_chargingcycle       |  string |         |                 |
|     feeconfigurations_item_decision_tablekey     |  string |         |                 |
|    feeconfigurations_item_decision_input_item    |  string |         |                 |
| feeconfigurations_item_event_eventidentification |  string |         |                 |
|      feeconfigurations_item_event_eventname      |  string |         |                 |
|         feeconfigurations_item_feeamount         |  string |         |                 |
|     feeconfigurations_item_feecap_capamount      |  string |         |                 |
|   feeconfigurations_item_feecap_capoccurrence    |  string |         |                 |
|   feeconfigurations_item_feecap_cappingperiod    |  string |         |                 |
|        feeconfigurations_item_feecategory        |  string |         |                 |
|     feeconfigurations_item_feeidentification     |  string |         |                 |
|          feeconfigurations_item_feename          |  string |         |                 |
|       feeconfigurations_item_feerate_rate        |  string |         |                 |
|   feeconfigurations_item_feerate_notionalvalue   |  string |         |                 |
|          feeconfigurations_item_feetype          |  string |         |                 |
|        feeconfigurations_item_maximumfee         |  string |         |                 |
|        feeconfigurations_item_minimumfee         |  string |         |                 |
|          feeconfigurations_item_taxrate          |  string |         |                 |
|   feeconfigurations_item_statementdescription    |  string |         |                 |
|  feeconfigurations_item_validityperiod_enddate   |  string |         |                 |
| feeconfigurations_item_validityperiod_startdate  |  string |         |                 |
|             kafka_message_timestamp              |  bigint |         |                 |
+--------------------------------------------------+---------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex', 'strarray_t', 'str_arr']],
                'select ** from rs_complex.strarray_t',
                """
+--------------+--------+---------+-----------------+
|     name     |  type  | comment |    attributes   |
+--------------+--------+---------+-----------------+
|      id      | bigint |         |                 |
| str_arr_item | string |         | attr_test_db.a1 |
+--------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_t', 'a1.f1']],
                'select ** from rs_complex.array_struct_t',
                """
+------------+--------+---------+-----------------+
|    name    |  type  | comment |    attributes   |
+------------+--------+---------+-----------------+
| a1_item_f1 | string |         | attr_test_db.a1 |
| a1_item_f2 | string |         |                 |
+------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_t', 'a1.f1'],
                 ['rs_complex', 'array_struct_t', 'a1.f2']],
                'select ** from rs_complex.array_struct_t',
                """
+------------+--------+---------+-----------------+
|    name    |  type  | comment |    attributes   |
+------------+--------+---------+-----------------+
| a1_item_f1 | string |         | attr_test_db.a1 |
| a1_item_f2 | string |         | attr_test_db.a1 |
+------------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_array', 'a1.a2'],
                 ['rs_complex', 'array_struct_array', 'a1.f1'],
                 ['rs_complex', 'array_struct_array', 'a1.f2']],
                'select ** from rs_complex.array_struct_array',
                """
+-----------------+--------+---------+-----------------+
|       name      |  type  | comment |    attributes   |
+-----------------+--------+---------+-----------------+
|    a1_item_f1   | string |         | attr_test_db.a1 |
|    a1_item_f2   | string |         | attr_test_db.a1 |
| a1_item_a2_item | string |         | attr_test_db.a1 |
+-----------------+--------+---------+-----------------+""".strip())

# FIXME: map is not supported.
#            self._validate(conn, db, 'a1',
#                [['rs_complex_parquet', 'spark_gzip', 'int32'],
#                 ['rs_complex_parquet', 'spark_gzip', 'str_arr'],
#                 ['rs_complex_parquet', 'spark_gzip', 'int_arr']],
#                'select ** from rs_complex_parquet.spark_gzip',
#                """
#+---------+--------+---------+-----------------+
#|   name  |  type  | comment |    attributes   |
#+---------+--------+---------+-----------------+
#|  int32  |  int   |         | attr_test_db.a1 |
#| str_arr | string |         | attr_test_db.a1 |
#| int_arr |  int   |         | attr_test_db.a1 |
#+---------+--------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'zd1211', 'accountnumber'],
                 ['chase', 'zd1211', 'productdetails.subproducts']],
                'select ** from chase.zd1211',
"""
+------------------------------------------------------------------------------------------------------------------+---------+---------+-----------------+
|                                                       name                                                       |   type  | comment |    attributes   |
+------------------------------------------------------------------------------------------------------------------+---------+---------+-----------------+
|                                                 subscriptionkey                                                  |  string |         |                 |
|                                             partyroles_item_partykey                                             |  string |         |                 |
|                                            partyroles_item_tenantkey                                             |  string |         |                 |
|                                               partyroles_item_role                                               |  string |         |                 |
|                                           partyroles_item_partyrolekey                                           |  string |         |                 |
|                                           partyroles_item_createddate                                            |  string |         |                 |
|                                           partyroles_item_updateddate                                            |  string |         |                 |
|                                                   productname                                                    |  string |         |                 |
|                                                  effectivedate                                                   |  string |         |                 |
|                                                    productkey                                                    |  string |         |                 |
|                                                  productversion                                                  |   int   |         |                 |
|                                              parentsubscriptionkey                                               |  string |         |                 |
|                                               parentaccountnumber                                                |  string |         |                 |
|                                                  accountnumber                                                   |  string |         | attr_test_db.a1 |
|                                                     sortcode                                                     |  string |         |                 |
|                                                subscriptionstatus                                                |  string |         |                 |
|                                                   createddate                                                    |  string |         |                 |
|                                                   updateddate                                                    |  string |         |                 |
|                                              linkedsubscriptionkey                                               |  string |         |                 |
|                                           productdetails_effectivedate                                           |  string |         |                 |
|                                            productdetails_productkey                                             |  string |         |                 |
|                                             productdetails_tenantkey                                             |  string |         |                 |
|                                          productdetails_productcategory                                          |  string |         |                 |
|                                            productdetails_productname                                            |  string |         |                 |
|                                            productdetails_producttype                                            |  string |         |                 |
|                                        productdetails_productdescription                                         |  string |         |                 |
|                                          productdetails_productsegment                                           |  string |         |                 |
|                                            productdetails_createddate                                            |  string |         |                 |
|                                             productdetails_createdby                                             |  string |         |                 |
|                                            productdetails_updateddate                                            |  string |         |                 |
|                                             productdetails_updatedby                                             |  string |         |                 |
|                                           productdetails_publisheddate                                           |  string |         |                 |
|                                            productdetails_publishedby                                            |  string |         |                 |
|                                            productdetails_closeddate                                             |  string |         |                 |
|                                             productdetails_closedby                                              |  string |         |                 |
|                                              productdetails_status                                               |  string |         |                 |
|                                           productdetails_majorversion                                            |   int   |         |                 |
|                                             productdetails_tags_item                                             |  string |         |                 |
|                                         productdetails_linkedproduct_id                                          |  string |         |                 |
|                                         productdetails_subproducts_item                                          |  string |         | attr_test_db.a1 |
|                                      productdetails_requiredexternalid_item                                      |  string |         |                 |
|                           productdetails_limits_transactionlimits_item_transactionname                           |  string |         |                 |
|                             productdetails_limits_transactionlimits_item_description                             |  string |         |                 |
|                            productdetails_limits_transactionlimits_item_minimumamount                            |  string |         |                 |
|                            productdetails_limits_transactionlimits_item_maximumamount                            |  string |         |                 |
|                             productdetails_limits_transactionlimits_item_resetperiod                             |  string |         |                 |
|                                productdetails_limits_schemelimits_item_schemename                                |  string |         |                 |
|                               productdetails_limits_schemelimits_item_description                                |  string |         |                 |
|                              productdetails_limits_schemelimits_item_minimumamount                               |  string |         |                 |
|                              productdetails_limits_schemelimits_item_maximumamount                               |  string |         |                 |
|                               productdetails_limits_schemelimits_item_resetperiod                                |  string |         |                 |
|                           productdetails_limits_accountbalancelimits_item_balancetype                            |  string |         |                 |
|                           productdetails_limits_accountbalancelimits_item_description                            |  string |         |                 |
|                          productdetails_limits_accountbalancelimits_item_minimumamount                           |  string |         |                 |
|                          productdetails_limits_accountbalancelimits_item_maximumamount                           |  string |         |                 |
|                               productdetails_limits_productlimits_item_productkey                                |  string |         |                 |
|                               productdetails_limits_productlimits_item_productname                               |  string |         |                 |
|                               productdetails_limits_productlimits_item_producttype                               |  string |         |                 |
|                               productdetails_limits_productlimits_item_description                               |  string |         |                 |
|                              productdetails_limits_productlimits_item_maximumnumber                              |   int   |         |                 |
|                            productdetails_limits_fundinglimits_item_fundingmechanism                             |  string |         |                 |
|                               productdetails_limits_fundinglimits_item_description                               |  string |         |                 |
|                              productdetails_limits_fundinglimits_item_minimumamount                              |  string |         |                 |
|                              productdetails_limits_fundinglimits_item_maximumamount                              |  string |         |                 |
|                              productdetails_limits_fundinglimits_item_defaultamount                              |  string |         |                 |
|                                   productdetails_cards_item_cardstatusdefault                                    |  string |         |                 |
|                                          productdetails_cards_item_type                                          |  string |         |                 |
|                                         productdetails_cards_item_scheme                                         |  string |         |                 |
|                           productdetails_cards_item_channeldefaultsettings_contactless                           | boolean |         |                 |
|                             productdetails_cards_item_channeldefaultsettings_chippin                             | boolean |         |                 |
|                               productdetails_cards_item_channeldefaultsettings_atm                               | boolean |         |                 |
|                               productdetails_cards_item_channeldefaultsettings_cnp                               | boolean |         |                 |
|                            productdetails_cards_item_channeldefaultsettings_magstripe                            | boolean |         |                 |
|                          productdetails_cards_item_channeldefaultsettings_international                          | boolean |         |                 |
|                             productdetails_cards_item_channeldefaultsettings_online                              | boolean |         |                 |
|                                productdetails_termsandconditions_item_identifier                                 |  string |         |                 |
|                                   productdetails_termsandconditions_item_name                                    |  string |         |                 |
|                                productdetails_termsandconditions_item_description                                |  string |         |                 |
|                                  productdetails_termsandconditions_item_version                                  |  string |         |                 |
|                                productdetails_termsandconditions_item_createddate                                |  string |         |                 |
|                                 productdetails_termsandconditions_item_createdby                                 |  string |         |                 |
|                                productdetails_termsandconditions_item_updateddate                                |  string |         |                 |
|                                 productdetails_termsandconditions_item_updatedby                                 |  string |         |                 |
|                               productdetails_termsandconditions_item_publisheddate                               |  string |         |                 |
|                                  productdetails_termsandconditions_item_status                                   |  string |         |                 |
|                              productdetails_termsandconditions_item_files_item_url                               |  string |         |                 |
|                             productdetails_termsandconditions_item_files_item_format                             |  string |         |                 |
|                          productdetails_internaldocumentation_salesaccesschannels_item                           |  string |         |                 |
|                         productdetails_internaldocumentation_servingaccesschannels_item                          |  string |         |                 |
|                              productdetails_internaldocumentation_mobilewallet_item                              |  string |         |                 |
|                                 productdetails_internaldocumentation_producturl                                  |  string |         |                 |
|                               productdetails_internaldocumentation_fraudriskrating                               |  string |         |                 |
|                             productdetails_internaldocumentation_fincrimeriskrating                              |  string |         |                 |
|                               productdetails_subscriptioncreationrule_lockedstatus                               | boolean |         |                 |
|                        productdetails_subscriptioncreationrule_requiredsignatoriesnumber                         |   int   |         |                 |
|                        productdetails_subscriptioncreationrule_defaultsubscriptionstatus                         |  string |         |                 |
|                                       productdetails_currency_currencycode                                       |  string |         |                 |
|                                         productdetails_currency_country                                          |  string |         |                 |
|                                        productdetails_teams_item_teamkey                                         |  string |         |                 |
|                                         productdetails_teams_item_write                                          | boolean |         |                 |
|                                    productdetails_customattributes_item_name                                     |  string |         |                 |
|                                    productdetails_customattributes_item_value                                    |  string |         |                 |
|                                     productdetails_documents_item_identifier                                     |  string |         |                 |
|                                        productdetails_documents_item_name                                        |  string |         |                 |
|                                    productdetails_documents_item_description                                     |  string |         |                 |
|                                      productdetails_documents_item_version                                       |  string |         |                 |
|                                    productdetails_documents_item_createddate                                     |  string |         |                 |
|                                     productdetails_documents_item_createdby                                      |  string |         |                 |
|                                    productdetails_documents_item_updateddate                                     |  string |         |                 |
|                                     productdetails_documents_item_updatedby                                      |  string |         |                 |
|                                   productdetails_documents_item_publisheddate                                    |  string |         |                 |
|                                       productdetails_documents_item_status                                       |  string |         |                 |
|                                   productdetails_documents_item_files_item_url                                   |  string |         |                 |
|                                 productdetails_documents_item_files_item_format                                  |  string |         |                 |
|                                   productdetails_feescharges_item_feecategory                                    |  string |         |                 |
|                                     productdetails_feescharges_item_feetype                                      |  string |         |                 |
|                                  productdetails_feescharges_item_feedescription                                  |  string |         |                 |
|                                productdetails_feescharges_item_feetransactioncode                                |  string |         |                 |
|                                 productdetails_feescharges_item_transactioncode                                  |  string |         |                 |
|                                     productdetails_feescharges_item_taxrate                                      |  string |         |                 |
|                               productdetails_feescharges_item_statementdescription                               |  string |         |                 |
|                                     productdetails_feescharges_item_feename                                      |  string |         |                 |
|                                    productdetails_feescharges_item_feeamount                                     |  string |         |                 |
|                             productdetails_feescharges_item_taxstatementdescription                              |  string |         |                 |
|                               productdetails_feescharges_item_calculationfrequency                               |  string |         |                 |
|                               productdetails_feescharges_item_applicationfrequency                               |  string |         |                 |
|                                   productdetails_feescharges_item_feerate_rate                                   |  string |         |                 |
|                              productdetails_feescharges_item_feerate_notionalvalue                               |  string |         |                 |
|                             productdetails_feescharges_item_feerate_maximumfeeamount                             |  string |         |                 |
|                             productdetails_feescharges_item_feerate_minimumfeeamount                             |  string |         |                 |
|                             productdetails_feescharges_item_validityperiod_startdate                             |  string |         |                 |
|                              productdetails_feescharges_item_validityperiod_enddate                              |  string |         |                 |
|                              productdetails_feescharges_item_validityperiod_period                               |  string |         |                 |
|                           productdetails_feescharges_item_validityperiod_periodamount                            |  string |         |                 |
|                               productdetails_feescharges_item_feecap_cappingperiod                               |  string |         |                 |
|                               productdetails_feescharges_item_feecap_feecapamount                                |  string |         |                 |
|                             productdetails_feescharges_item_feecap_feecapoccurrence                              |  string |         |                 |
|                     productdetails_feescharges_item_feerules_item_inputparameters_item_name                      |  string |         |                 |
|                     productdetails_feescharges_item_feerules_item_inputparameters_item_value                     |  string |         |                 |
|                   productdetails_feescharges_item_feerules_item_inputparameters_item_operator                    |  string |         |                 |
|                     productdetails_feescharges_item_feerules_item_outputparameters_item_name                     |  string |         |                 |
|                    productdetails_feescharges_item_feerules_item_outputparameters_item_value                     |  string |         |                 |
|                             productdetails_feescharges_item_notificationapplication                              |   int   |         |                 |
|                                 productdetails_creditinterest_fixedvariabletype                                  |  string |         |                 |
|                                    productdetails_creditinterest_includefees                                     | boolean |         |                 |
|                                   productdetails_creditinterest_roundingmethod                                   |  string |         |                 |
|                                      productdetails_creditinterest_daycount                                      |  string |         |                 |
|                                    productdetails_creditinterest_interestrate                                    |  string |         |                 |
|                                 productdetails_creditinterest_tierbandcalcmethod                                 |  string |         |                 |
|                                productdetails_creditinterest_applicationfrequency                                |  string |         |                 |
|                                productdetails_creditinterest_compoundingfrequency                                |  string |         |                 |
|                                productdetails_creditinterest_calculationfrequency                                |  string |         |                 |
|                                  productdetails_creditinterest_balancecriteria                                   |  string |         |                 |
|                          productdetails_creditinterest_interesttierband_item_startrange                          |  string |         |                 |
|                           productdetails_creditinterest_interesttierband_item_endrange                           |  string |         |                 |
|                         productdetails_creditinterest_interesttierband_item_tierbandrate                         |  string |         |                 |
|                              productdetails_creditinterest_interestrateindex_index                               |  string |         |                 |
|                               productdetails_creditinterest_interestrateindex_term                               |  string |         |                 |
|                            productdetails_creditinterest_interestrateindex_identifier                            |  string |         |                 |
|                               productdetails_creditinterest_interestrateindex_url                                |  string |         |                 |
|                                  productdetails_overdraft_applicationfrequency                                   |  string |         |                 |
|                                     productdetails_overdraft_balancecriteria                                     |  string |         |                 |
|                                  productdetails_overdraft_calculationfrequency                                   |  string |         |                 |
|                                  productdetails_overdraft_compoundingfrequency                                   |  string |         |                 |
|                                        productdetails_overdraft_daycount                                         |  string |         |                 |
|                                      productdetails_overdraft_interestrate                                       |  string |         |                 |
|                              productdetails_overdraft_overdrafttierband_item_buffer                              |  string |         |                 |
|                             productdetails_overdraft_overdrafttierband_item_endrange                             |  string |         |                 |
|                           productdetails_overdraft_overdrafttierband_item_interestrate                           |  string |         |                 |
|            productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_applicationfrequency             |  string |         |                 |
|            productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_calculationfrequency             |  string |         |                 |
|                  productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feeamount                  |  string |         |                 |
|            productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feecap_cappingperiod             |  string |         |                 |
|             productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feecap_feecapamount             |  string |         |                 |
|           productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feecap_feecapoccurrence           |  string |         |                 |
|                 productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feecategory                 |  string |         |                 |
|               productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feedescription                |  string |         |                 |
|   productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feerules_item_inputparameters_item_name   |  string |         |                 |
|  productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feerules_item_inputparameters_item_value   |  string |         |                 |
| productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feerules_item_inputparameters_item_operator |  string |         |                 |
|  productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feerules_item_outputparameters_item_name   |  string |         |                 |
|  productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feerules_item_outputparameters_item_value  |  string |         |                 |
|             productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_feetransactioncode              |  string |         |                 |
|            productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_statementdescription             |  string |         |                 |
|                   productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_taxrate                   |  string |         |                 |
|          productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_validityperiod_startdate           |  string |         |                 |
|           productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_validityperiod_enddate            |  string |         |                 |
|            productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_validityperiod_period            |  string |         |                 |
|         productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_validityperiod_periodamount         |  string |         |                 |
|           productdetails_overdraft_overdrafttierband_item_overdraftfeescharges_notificationapplication           |   int   |         |                 |
|                            productdetails_overdraft_overdrafttierband_item_startrange                            |  string |         |                 |
|                             productdetails_overdraft_overdrafttierband_item_tiername                             |  string |         |                 |
|                        productdetails_overdraft_overdrafttierband_item_tierstatusdefault                         |  string |         |                 |
|                                     productdetails_overdraft_roundingmethod                                      |  string |         |                 |
|                              productdetails_overdraft_termsandconditions_identifier                              |  string |         |                 |
|                                 productdetails_overdraft_termsandconditions_name                                 |  string |         |                 |
|                             productdetails_overdraft_termsandconditions_description                              |  string |         |                 |
|                               productdetails_overdraft_termsandconditions_version                                |  string |         |                 |
|                             productdetails_overdraft_termsandconditions_createddate                              |  string |         |                 |
|                              productdetails_overdraft_termsandconditions_createdby                               |  string |         |                 |
|                             productdetails_overdraft_termsandconditions_updateddate                              |  string |         |                 |
|                              productdetails_overdraft_termsandconditions_updatedby                               |  string |         |                 |
|                            productdetails_overdraft_termsandconditions_publisheddate                             |  string |         |                 |
|                                productdetails_overdraft_termsandconditions_status                                |  string |         |                 |
|                            productdetails_overdraft_termsandconditions_files_item_url                            |  string |         |                 |
|                          productdetails_overdraft_termsandconditions_files_item_format                           |  string |         |                 |
|                                   productdetails_overdraft_tierbandcalcmethod                                    |  string |         |                 |
|                                 productdetails_overdraft_notificationapplication                                 |   int   |         |                 |
|                               productdetails_eligibility_ageeligibility_maximumage                               |   int   |         |                 |
|                               productdetails_eligibility_ageeligibility_minimumage                               |   int   |         |                 |
|                     productdetails_eligibility_creditcheckeligibility_maximumpersonalincome                      |  string |         |                 |
|                          productdetails_eligibility_creditcheckeligibility_maximumscore                          |  string |         |                 |
|                     productdetails_eligibility_creditcheckeligibility_minimumpersonalincome                      |  string |         |                 |
|                          productdetails_eligibility_creditcheckeligibility_minimumscore                          |  string |         |                 |
|                          productdetails_eligibility_creditcheckeligibility_scoringmodel                          |  string |         |                 |
|                        productdetails_eligibility_creditcheckeligibility_scoringprovider                         |  string |         |                 |
|                      productdetails_eligibility_creditcheckeligibility_scoringsegment_item                       |  string |         |                 |
|                          productdetails_eligibility_creditcheckeligibility_scoringtype                           |  string |         |                 |
|                              productdetails_eligibility_ideligibility_item_idproof                               |  string |         |                 |
|                               productdetails_eligibility_ideligibility_item_idtype                               |  string |         |                 |
|                                productdetails_eligibility_ideligibility_item_url                                 |  string |         |                 |
|                      productdetails_eligibility_industryeligibility_customindustryname_item                      |  string |         |                 |
|                           productdetails_eligibility_industryeligibility_siccode_item                            |  string |         |                 |
|                  productdetails_eligibility_legalstructureeligibility_item_countryincluded_item                  |  string |         |                 |
|                     productdetails_eligibility_legalstructureeligibility_item_legalstructure                     |  string |         |                 |
|                   productdetails_eligibility_legalstructureeligibility_item_stateincluded_item                   |  string |         |                 |
|                             productdetails_eligibility_officereligibility_maxamount                              |  string |         |                 |
|                             productdetails_eligibility_officereligibility_minamount                              |  string |         |                 |
|                            productdetails_eligibility_officereligibility_officertype                             |  string |         |                 |
|                             productdetails_eligibility_othereligibility_item_amount                              |  string |         |                 |
|                           productdetails_eligibility_othereligibility_item_description                           |  string |         |                 |
|                            productdetails_eligibility_othereligibility_item_indicator                            | boolean |         |                 |
|                              productdetails_eligibility_othereligibility_item_name                               |  string |         |                 |
|                             productdetails_eligibility_othereligibility_item_period                              |  string |         |                 |
|                              productdetails_eligibility_othereligibility_item_type                               |  string |         |                 |
|                    productdetails_eligibility_professioneligibility_customprofessionname_item                    |  string |         |                 |
|                          productdetails_eligibility_professioneligibility_soccode_item                           |  string |         |                 |
|                    productdetails_eligibility_residencyeligibility_item_countryincluded_item                     |  string |         |                 |
|                        productdetails_eligibility_residencyeligibility_item_minimumperiod                        |  string |         |                 |
|                     productdetails_eligibility_residencyeligibility_item_minimumperiodamount                     |  string |         |                 |
|                       productdetails_eligibility_residencyeligibility_item_residencestatus                       |  string |         |                 |
|                        productdetails_eligibility_residencyeligibility_item_residencytype                        |  string |         |                 |
|                     productdetails_eligibility_residencyeligibility_item_stateincluded_item                      |  string |         |                 |
|                         productdetails_eligibility_tradinghistoryeligibility_item_amount                         |  string |         |                 |
|                      productdetails_eligibility_tradinghistoryeligibility_item_description                       |  string |         |                 |
|                       productdetails_eligibility_tradinghistoryeligibility_item_indicator                        | boolean |         |                 |
|                       productdetails_eligibility_tradinghistoryeligibility_item_minmaxtype                       |  string |         |                 |
|                         productdetails_eligibility_tradinghistoryeligibility_item_period                         |  string |         |                 |
|                      productdetails_eligibility_tradinghistoryeligibility_item_tradingtype                       |  string |         |                 |
|                                      productdetails_statement_statementtype                                      |  string |         |                 |
|                                     productdetails_statement_statementperiod                                     |  string |         |                 |
|                                  productdetails_statement_statementdescription                                   |  string |         |                 |
|                                        productdetails_statement_startday                                         |   int   |         |                 |
|                                       productdetails_statement_startmonth                                        |   int   |         |                 |
|                                   productdetails_statements_item_statementtype                                   |  string |         |                 |
|                                  productdetails_statements_item_statementperiod                                  |  string |         |                 |
|                               productdetails_statements_item_statementdescription                                |  string |         |                 |
|                                     productdetails_statements_item_startday                                      |   int   |         |                 |
|                                    productdetails_statements_item_startmonth                                     |   int   |         |                 |
|                                             kafka_message_timestamp                                              |  bigint |         |                 |
+------------------------------------------------------------------------------------------------------------------+---------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['chase', 'party', 'document.imagetype']],
                'select ** from chase.party',
"""
+--------------------------------+-----------+---------+-----------------+
|              name              |    type   | comment |    attributes   |
+--------------------------------+-----------+---------+-----------------+
|            partykey            |   string  |         |                 |
|           tenantkey            |   string  |         |                 |
|           givenname            |   string  |         |                 |
|            lastname            |   string  |         |                 |
|           middlename           |   string  |         |                 |
|         preferredname          |   string  |         |                 |
|          mobilenumber          |   string  |         |                 |
|             email              |   string  |         |                 |
|   address_item_addressline1    |   string  |         |                 |
|   address_item_addressline2    |   string  |         |                 |
|   address_item_addressline3    |   string  |         |                 |
|   address_item_addressline4    |   string  |         |                 |
|   address_item_addressline5    |   string  |         |                 |
|     address_item_postcode      |   string  |         |                 |
|       address_item_city        |   string  |         |                 |
|      address_item_country      |   string  |         |                 |
|       address_item_state       |   string  |         |                 |
|    address_item_addresstype    |   string  |         |                 |
|      address_item_status       |   string  |         |                 |
|    address_item_createddate    |   string  |         |                 |
|    address_item_updateddate    |   string  |         |                 |
|           birthdate            |    int    |         |                 |
|             status             |   string  |         |                 |
|     devices_item_deviceid      |   string  |         |                 |
|     devices_item_pushtoken     |   string  |         |                 |
|    devices_item_devicetype     |   string  |         |                 |
|    devices_item_createddate    |   string  |         |                 |
|    devices_item_updateddate    |   string  |         |                 |
|  ecis_item_externalidentifier  |   string  |         |                 |
|       ecis_item_provider       |   string  |         |                 |
|     ecis_item_createddate      |   string  |         |                 |
|     ecis_item_updateddate      |   string  |         |                 |
|        document_item_id        |   string  |         |                 |
|     document_item_partykey     |   string  |         |                 |
|    document_item_imagetype     |   string  |         | attr_test_db.a1 |
|  document_item_documentnumber  |   string  |         |                 |
|  document_item_issuingcountry  |   string  |         |                 |
|   document_item_dateofexpiry   |   string  |         |                 |
|   document_item_dateofbirth    |   string  |         |                 |
|     document_item_surname      |   string  |         |                 |
|    document_item_firstname     |   string  |         |                 |
|   document_item_placeofbirth   |   string  |         |                 |
|   document_item_createddate    |   string  |         |                 |
|   document_item_updateddate    |   string  |         |                 |
|          createddate           |   string  |         |                 |
|          updateddate           |   string  |         |                 |
|      citizenship_partykey      |   string  |         |                 |
| citizenship_nationalities_item |   string  |         |                 |
|    citizenship_createddate     |   string  |         |                 |
|    citizenship_updateddate     |   string  |         |                 |
|    kafka_message_timestamp     | timestamp |         |                 |
+--------------------------------+-----------+---------+-----------------+""".strip())

            self._validate(conn, db, 'a1',
                [['rs_complex', 'array_struct_array', 'a1.f1'],
                 ['rs_complex', 'array_struct_array', 'a1.a2']],
                'select ** from rs_complex.array_struct_array',
"""
+-----------------+--------+---------+-----------------+
|       name      |  type  | comment |    attributes   |
+-----------------+--------+---------+-----------------+
|    a1_item_f1   | string |         | attr_test_db.a1 |
|    a1_item_f2   | string |         |                 |
| a1_item_a2_item | string |         | attr_test_db.a1 |
+-----------------+--------+---------+-----------------+""".strip())

# TODO: map support
#            self._validate(conn, db, 'a1',
#                [['functional', 'allcomplextypes', 'id'],
#                 ['functional', 'allcomplextypes', 'nested_struct_col.f1']],
#                'select ** from functional.allcomplextypes',
#"""
#+---------------------------+----------------------------+---------+-----------------+
#|            name           |            type            | comment |    attributes   |
#+---------------------------+----------------------------+---------+-----------------+
#|             id            |            int             |         | attr_test_db.a1 |
#|       int_array_col       |         array<int>         |         |                 |
#|      array_array_col      |     array<array<int>>      |         |                 |
#|       map_array_col       |   array<map<string,int>>   |         |                 |
#|      struct_array_col     |       array<struct<        |         |                 |
#|                           |          f1:bigint,        |         |                 |
#|                           |          f2:string         |         |                 |
#|                           |             >>             |         |                 |
#|        int_map_col        |      map<string,int>       |         |                 |
#|       array_map_col       |   map<string,array<int>>   |         |                 |
#|       struct_map_col      |     map<string,struct<     |         |                 |
#|                           |          f1:bigint,        |         |                 |
#|                           |          f2:string         |         |                 |
#|                           |             >>             |         |                 |
#|       int_struct_col      |          struct<           |         |                 |
#|                           |           f1:int,          |         |                 |
#|                           |            f2:int          |         |                 |
#|                           |             >              |         |                 |
#|     complex_struct_col    |          struct<           |         |                 |
#|                           |           f1:int,          |         |                 |
#|                           |        f2:array<int>,      |         |                 |
#|                           |      f3:map<string,int>    |         |                 |
#|                           |             >              |         |                 |
#|     nested_struct_col     |          struct<           |         |                 |
#|                           |           f1:int,          |         | attr_test_db.a1 |
#|                           |          f2:struct<        |         |                 |
#|                           |          f11:bigint,       |         |                 |
#|                           |          f12:struct<       |         |                 |
#|                           |            f21:bigint      |         |                 |
#|                           |               >            |         |                 |
#|                           |              >             |         |                 |
#|                           |             >              |         |                 |
#| complex_nested_struct_col |          struct<           |         |                 |
#|                           |           f1:int,          |         |                 |
#|                           |       f2:array<struct<     |         |                 |
#|                           |          f11:bigint,       |         |                 |
#|                           |     f12:map<string,struct< |         |                 |
#|                           |            f21:bigint      |         |                 |
#|                           |               >>           |         |                 |
#|                           |              >>            |         |                 |
#|                           |             >              |         |                 |
#|            item           |            int             |         |                 |
#|            year           |            int             |         |                 |
#|           month           |            int             |         |                 |
#+---------------------------+----------------------------+---------+-----------------+""".strip())

if __name__ == "__main__":
    unittest.main()
