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
        self.valid_table = 'TABLE1'
        self.valid_columns = ['C1', 'C2', 'C3']
        self.valid_types = ['BOOLEAN', 'TEXT', 'TEXT']
        self.valid_sizes = [0, 24, 64]

    def test_result_type(self):
        icar.core.database_operations.create_database(self.valid_database)
        output = icar.core.database_operations.list_tables(self.valid_database)
        self.assertEqual(type(output), type([1, 1]))

    def test_result(self):
        icar.core.database_operations.create_database(self.valid_database)
        icar.core.database_operations.create_table(\
            self.valid_database, self.valid_table, \
            self.valid_columns, self.valid_types, \
            self.valid_sizes)
        output = icar.core.database_operations.list_tables(self.valid_database)
        return self.valid_table in output


if __name__ == '__main__':
    unittest.main()