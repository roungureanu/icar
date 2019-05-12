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
        self.invalid_database = 18373
        self.non_existing_database = 'DB2'
        self.valid_table = 'TABLE1'
        self.invalid_table = False
        self.non_existing_table = 'TABLE2'
        self.valid_column = 'COLUMN1'
        self.valid_new_column = 'COLUMN100'
        self.existing_column = 'COLUMN2'
        self.valid_columns = [self.valid_column, self.existing_column]
        self.invalid_column = 98498
        self.valid_types = ['NUMERIC', 'BOOLEAN']
        self.valid_sizes = [0, 0]
        self.valid_column_type = 'TEXT'
        self.valid_column_size = 27
        self.invalid_column_type = 'DOUBLE'

    def test_params_ok(self):
        icar.core.database_operations.delete_table(self.valid_database, self.valid_table)
        icar.core.database_operations.create_database(self.valid_database)
        icar.core.database_operations.create_table(\
            self.valid_database, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        output = icar.core.database_operations.add_column(\
            self.valid_database, self.valid_table, self.valid_new_column, \
            self.valid_column_type, self.valid_column_size)
        self.assertEqual(output, (0, 'Success: Column added.'))

    def test_invalid_database(self):
        output = icar.core.database_operations.add_column(\
            self.invalid_database, self.valid_table, self.valid_new_column, \
            self.valid_column_type, self.valid_column_size)
        self.assertEqual(output, (1, 'Error: Invalid database name.'))

    def test_invalid_table_name(self):
        output = icar.core.database_operations.add_column(\
            self.valid_database, self.invalid_table, self.valid_new_column, \
            self.valid_column_type, self.valid_column_size)
        self.assertEqual(output, (1, 'Error: Invalid table name.'))

    def test_invalid_column_name(self):
        output = icar.core.database_operations.add_column(\
            self.valid_database, self.valid_table, self.invalid_column, \
            self.valid_column_type, self.valid_column_size)
        self.assertEqual(output, (1, 'Error: Invalid column name.'))

    def test_invalid_type(self):
        output = icar.core.database_operations.add_column(\
            self.valid_database, self.valid_table, self.valid_new_column, \
            self.invalid_column_type, self.valid_column_size)
        self.assertEqual(output, (1, 'Error: Invalid type.'))

    def test_non_existing_database(self):
        icar.core.database_operations.delete_database(self.non_existing_database)
        output = icar.core.database_operations.add_column(\
            self.non_existing_database, self.valid_table, self.valid_new_column, \
            self.valid_column_type, self.valid_column_size)
        self.assertEqual(output, (1, 'Error: Database doesn\'t exist.'))

    def test_non_existing_table(self):
        icar.core.database_operations.delete_table(self.valid_database, self.non_existing_table)
        icar.core.database_operations.create_database(self.valid_database)
        output = icar.core.database_operations.add_column(\
            self.valid_database, self.non_existing_table, self.valid_new_column, \
            self.valid_column_type, self.valid_column_size)
        self.assertEqual(output, (1, 'Error: Table doesn\'t exist.'))

    def test_existing_column(self):
        icar.core.database_operations.delete_table(self.valid_database, self.valid_table)
        icar.core.database_operations.create_database(self.valid_database)
        icar.core.database_operations.create_table(\
            self.valid_database, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        output = icar.core.database_operations.add_column(\
            self.valid_database, self.valid_table, self.existing_column, \
            self.valid_column_type, self.valid_column_size)
        self.assertEqual(output, (1, 'Error: Column already exists.'))


if __name__ == '__main__':
    unittest.main()