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
        self.invalid_database = False
        self.non_existing_db = 'DB2'
        self.valid_table = 'TABLE1'
        self.valid_new_table = 'TABLE2'
        self.existing_table = 'TABLE3'
        self.non_existing_table = 'TABLE4'
        self.invalid_table = True
        self.valid_columns = ['COLUMN1', 'COLUMN2', 'COLUMN3']
        self.invalid_columns = [True, 242334, 'TEST']
        self.valid_types = ['TEXT', 'NUMERIC', 'BOOLEAN']
        self.invalid_types = [12, 23]
        self.valid_sizes = [10, 0, 0]
        self.big_sizes = [3458585, 0, 0]

    def test_params_ok(self):
        icar.core.database_operations.delete_table(self.valid_database, self.valid_new_table)
        icar.core.database_operations.create_database(self.valid_database)
        icar.core.database_operations.create_table(\
            self.valid_database, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        output = icar.core.database_operations.rename_table( \
            self.valid_database, self.valid_table, self.valid_new_table)
        self.assertEqual(output, (0, 'Success: Table renamed.'))

    def test_non_existing_db(self):
        icar.core.database_operations.delete_database(self.non_existing_db)
        output = icar.core.database_operations.rename_table( \
            self.non_existing_db, self.valid_table, self.valid_new_table)
        self.assertEqual(output, (1, 'Error: Database doesn\'t exist.'))

    def test_existing_new_table(self):
        icar.core.database_operations.delete_database(self.valid_database)
        icar.core.database_operations.create_database(self.valid_database)
        icar.core.database_operations.create_table( \
            self.valid_database, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        icar.core.database_operations.create_table( \
            self.valid_database, self.existing_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        output = icar.core.database_operations.rename_table(\
            self.valid_database, self.valid_table, self.existing_table)
        self.assertEqual(output, (1, 'Error: New table already exists.'))

    def test_non_existing_old_table(self):
        icar.core.database_operations.delete_table(self.valid_database, self.non_existing_table)
        icar.core.database_operations.create_database(self.valid_database)
        output = icar.core.database_operations.rename_table(\
            self.valid_database, self.non_existing_table, self.valid_new_table)
        self.assertEqual(output, (1, 'Error: Old table doesn\'t exist.'))

    def test_invalid_database(self):
        output = icar.core.database_operations.rename_table( \
            self.invalid_database, self.valid_table, self.valid_new_table)
        self.assertEqual(output, (1, 'Error: Invalid database name.'))

    def test_invalid_old_table(self):
        output = icar.core.database_operations.rename_table( \
            self.valid_database, self.invalid_table, self.valid_new_table)
        self.assertEqual(output, (1, 'Error: Invalid old table name.'))

    def test_invalid_new_table(self):
        output = icar.core.database_operations.rename_table( \
            self.valid_database, self.valid_table, self.invalid_table)
        self.assertEqual(output, (1, 'Error: Invalid new table name.'))


if __name__ == '__main__':
    unittest.main()