import unittest

import graphical_user_interface.application
import graphical_user_interface.add_column_view
import graphical_user_interface.browse_records_view
import graphical_user_interface.create_database_view
import graphical_user_interface.create_table_view
import graphical_user_interface.delete_database
import graphical_user_interface.delete_records_view
import graphical_user_interface.delete_table_view
import graphical_user_interface.export_table_view
import graphical_user_interface.import_table_view
import graphical_user_interface.insert_record_view
import graphical_user_interface.main_view
import graphical_user_interface.remove_column_view
import graphical_user_interface.update_records_view

import test_table_ops
import test_xml_parser

from database_operations import create_database, delete_database, \
    create_table, delete_table, database_exists, list_databases, \
    list_tables, rename_table, add_column, rename_column, remove_column


if __name__ == '__main__':
    tests_to_run = [
        test_table_ops.TestTableOps,
        test_xml_parser.TestCase,
        graphical_user_interface.application.TestCase,
        graphical_user_interface.add_column_view.TestCase,
        graphical_user_interface.browse_records_view.TestCase,
        graphical_user_interface.create_database_view.TestCase,
        graphical_user_interface.create_table_view.TestCase,
        graphical_user_interface.delete_database.TestCase,
        graphical_user_interface.delete_records_view.TestCase,
        graphical_user_interface.delete_table_view.TestCase,
        graphical_user_interface.export_table_view.TestCase,
        graphical_user_interface.import_table_view.TestCase,
        graphical_user_interface.insert_record_view.TestCase,
        graphical_user_interface.main_view.TestCase,
        graphical_user_interface.remove_column_view.TestCase,
        graphical_user_interface.update_records_view.TestCase,
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
