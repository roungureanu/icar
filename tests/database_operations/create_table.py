import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )))

import icar.core.database_operations

class FunctionTest(unittest.TestCase):
    def setUp(self):
        self.valid_database = 'DB1'
        self.non_existing_db = 'DB2'
        self.invalid_database = False
        self.valid_table = 'TABLE1'
        self.existing_table = 'TABLE2'
        self.invalid_table = 6789
        self.valid_columns = ['COLUMN1', 'COLUMN2', 'COLUMN3']
        self.invalid_columns = [True, 242334, 'TEST']
        self.valid_types = ['TEXT', 'NUMERIC', 'BOOLEAN']
        self.invalid_types = [12, 23]
        self.valid_sizes = [10, 0, 0]
        self.big_sizes = [3458585, 0, 0]

    def test_params_ok(self):
        icar.core.database_operations.delete_table(self.valid_database, self.valid_table)
        icar.core.database_operations.create_database(self.valid_database)
        output = icar.core.database_operations.create_table( \
            self.valid_database, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        self.assertEqual(output, (0, 'Success: Table created.'))

    def test_non_existing_db(self):
        icar.core.database_operations.delete_database(self.non_existing_db)
        output = icar.core.database_operations.create_table( \
            self.non_existing_db, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        self.assertEqual(output, (1, 'Error: Database doesn\'t exist.'))

    def test_invalid_database(self):
        output = icar.core.database_operations.create_table( \
            self.invalid_database, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        self.assertEqual(output, (1, 'Error: Invalid database name.'))

    def test_invalid_table(self):
        output = icar.core.database_operations.create_table( \
            self.valid_database, self.invalid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        self.assertEqual(output, (1, 'Error: Invalid table name.'))

    def test_existing_table(self):
        icar.core.database_operations.create_database(self.valid_database)
        icar.core.database_operations.create_table( \
            self.valid_database, self.existing_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        output = icar.core.database_operations.create_table( \
            self.valid_database, self.existing_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        self.assertEqual(output, (1, 'Error: Table already exists.'))

    def test_invalid_types(self):
        output = icar.core.database_operations.create_table( \
            self.valid_database, self.valid_table, \
            self.valid_columns, self.invalid_types, \
            self.valid_sizes)
        self.assertEqual(output, (1, 'Error: Invalid column types.'))

    def test_big_size(self):
        icar.core.database_operations.delete_table(self.valid_database, self.valid_table)
        icar.core.database_operations.create_database(self.valid_database)
        output = icar.core.database_operations.create_table( \
            self.valid_database, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.big_sizes)
        self.assertEqual(output, (0, 'Success: Table created.'))

    def test_invalid_columns(self):
        icar.core.database_operations.delete_table(self.valid_database, self.valid_table)
        icar.core.database_operations.create_database(self.valid_database)
        output = icar.core.database_operations.create_table( \
            self.valid_database, self.valid_table, \
            self.invalid_columns, self.valid_types, \
            self.valid_sizes)
        self.assertEqual(output, (1, 'Error: Invalid column name.'))


if __name__ == '__main__':
    unittest.main()