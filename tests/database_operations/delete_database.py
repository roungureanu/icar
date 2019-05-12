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
        self.valid_name = 'DB1'
        self.non_existing_name = 'DB2'
        self.invalid_name = 345

    def test_valid_name(self):
        icar.core.database_operations.create_database(self.valid_name)
        output = icar.core.database_operations.delete_database(self.valid_name)
        self.assertEqual(output, (0, 'Success: Database deleted.'))

    def test_non_existing_name(self):
        icar.core.database_operations.delete_database(self.non_existing_name)
        output = icar.core.database_operations.delete_database(self.non_existing_name)
        self.assertEqual(output, (1, 'Error: Database doesn\'t exist.'))

    def test_invalid_name(self):
        output = icar.core.database_operations.delete_database(self.invalid_name)
        self.assertEqual(output, (1, 'Error: Invalid database name.'))


if __name__ == '__main__':
    unittest.main()