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
        self.existing_database = 'DB1'
        self.non_existing_database = 'DB2'
        self.invalid_database = 5678

    def test_existing_db(self):
        icar.core.database_operations.create_database(self.existing_database)
        output = icar.core.database_operations.database_exists(self.existing_database)
        self.assertEqual(output, True)

    def test_non_existing_db(self):
        icar.core.database_operations.delete_database(self.non_existing_database)
        output = icar.core.database_operations.database_exists(self.non_existing_database)
        self.assertEqual(output, False)

    def test_invalid_database(self):
        output = icar.core.database_operations.database_exists(self.invalid_database)
        self.assertEqual(output, (1, 'Error: Invalid database name.'))


if __name__ == '__main__':
    unittest.main()