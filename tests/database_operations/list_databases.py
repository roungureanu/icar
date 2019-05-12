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

    def test_result_type(self):
        output = icar.core.database_operations.list_databases()
        self.assertEqual(type(output), type([1, 1]))

    def test_result(self):
        icar.core.database_operations.create_database(self.valid_database)
        output = icar.core.database_operations.list_databases()
        return self.valid_database in output


if __name__ == '__main__':
    unittest.main()