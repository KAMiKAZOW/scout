#!/usr/bin/python

# A tests for scout
#

import sys
sys.path.insert(0, '..')
import __init__ as scout
if not hasattr(scout, 'ScoutCore'):
    raise ImportError('No main scout module found')

import unittest


class SimpleDatabaseTestCase(unittest.TestCase):

    def _check_simple_results_row(self, row):
        self.assertEqual(len(row), 2)
        self.assertEqual(type(row[0]), type(u''))
        self.assertEqual(type(row[1]), type(u''))
        self.assertEqual(row[0], row[1].split('-')[0])

    def setUp(self):
        self.database = scout.Database(':memory:')
        
        c = self.database.conn.cursor()

        self.term = 'package3-module2'
        self.sql_begin = "SELECT package, module FROM modules LEFT JOIN packages ON modules.id_pkg=packages.id_pkg"

        sql = """
CREATE TABLE modules (id_modules INT PRIMARY KEY NOT NULL, module VARCHAR(64) NOT NULL, id_pkg INT NOT NULL);
CREATE TABLE packages(id_pkg INT PRIMARY KEY NOT NULL, package VARCHAR(64) NOT NULL);
INSERT INTO packages(id_pkg, package) VALUES(1, 'package1');
INSERT INTO packages(id_pkg, package) VALUES(2, 'package2');
INSERT INTO packages(id_pkg, package) VALUES(3, 'package3');

INSERT INTO modules(id_modules, module, id_pkg) VALUES(1, 'package1-module1', 1);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(2, 'package1-module2', 1);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(3, 'package1-module3', 1);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(4, 'package2-module1', 2);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(5, 'package2-module2', 2);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(6, 'package2-module3', 2);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(7, 'package3-module1', 3);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(8, 'package3-module2', 3);
INSERT INTO modules(id_modules, module, id_pkg) VALUES(9, 'package3-module3', 3);

CREATE INDEX modules_module_idx ON modules(module);"""

        for cmd in sql.splitlines():
            c.execute(cmd)

    def tearDown(self):
        del self.database

    def testExecuteString(self):
        sql = self.sql_begin + " WHERE module LIKE '%%%s%%'" % self.term

        res = self.database.execute(sql)
        self._check_simple_results_row(res)

        self.assertEqual(self.term.split('-')[0], res[0])
        self.assertEqual(self.term, res[1])




suiteDatabase = unittest.makeSuite(SimpleDatabaseTestCase, 'test')

runner = unittest.TextTestRunner()
runner.run(suiteDatabase)
