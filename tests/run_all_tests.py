import unittest

from database_operations import create_database, delete_database, \
    create_table, delete_table, database_exists, list_databases, \
    list_tables, rename_table, add_column, rename_column, remove_column


if __name__ == '__main__':
    tests_to_run = [
        create_database.FunctionTest,
        delete_database.FunctionTest,
        create_table.FunctionTest,
        delete_table.FunctionTest,
        database_exists.FunctionTest,
        list_databases.FunctionTest,
        list_tables.FunctionTest,
        rename_table.FunctionTest,
        add_column.FunctionTest,
        rename_column.FunctionTest,
        remove_column.FunctionTest
    ]

    tests_loader = unittest.TestLoader()

    suites = []
    for test_class in tests_to_run:
        suites.append(
            tests_loader.loadTestsFromTestCase(test_class)
        )

    suite = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(suite)
