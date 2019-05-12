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
        self.non_existing_database = 'DB2'
        self.valid_table = 'TABLE1'
        self.invalid_table = 333
        self.non_existing_table = 'TABLE2'
        self.valid_columns = ['C1', 'C2']
        self.valid_types = ['NUMERIC', 'NUMERIC']
        self.valid_sizes = [0, 0]

    def test_params_ok(self):
        icar.core.database_operations.create_database(self.valid_database)
        icar.core.database_operations.create_table( \
            self.valid_database, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        output = icar.core.database_operations.delete_table(self.valid_database, self.valid_table)
        self.assertEqual(output, (0, 'Success: Table deleted.'))

    def test_invalid_database(self):
        output = icar.core.database_operations.delete_table(self.invalid_database, self.valid_table)
        self.assertEqual(output, (1, 'Error: Invalid database name.'))

    def test_invalid_table_name(self):
        output = icar.core.database_operations.delete_table(self.valid_database, self.invalid_table)
        self.assertEqual(output, (1, 'Error: Invalid table name.'))

    def test_non_existing_database(self):
        icar.core.database_operations.delete_database(self.non_existing_database)
        output = icar.core.database_operations.delete_database(self.non_existing_database)
        self.assertEqual(output, (1, 'Error: Database doesn\'t exist.'))

    def test_non_existing_table(self):
        icar.core.database_operations.delete_table(self.valid_database, self.non_existing_table)
        icar.core.database_operations.create_database(self.valid_database)
        output = icar.core.database_operations.delete_table(self.valid_database, self.non_existing_table)
        self.assertEqual(output, (1, 'Error: Table doesn\'t exist.'))


if __name__ == '__main__':
    unittest.main()