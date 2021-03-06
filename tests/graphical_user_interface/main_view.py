import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.database_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.main_view as main_view


normal_constructor = icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__


def test_constructor(self, app):
    self.app = app


class TestCase(unittest.TestCase):
    def tearDown(self) -> None:
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor

    def test_operation_result_message_create_widgets(self):
        app = tk.Frame()
        app.operation_result_message = 'a'
        view = main_view._OperationResultMessage(app, app)

        label = None

        for i in view.pack_slaves():
            if isinstance(i, tk.Label):
                label = i

        self.assertEqual(label['text'], 'a')

    def test_current_open_database(self):
        app = tk.Frame()
        app.current_open_database = 'a'
        view = main_view._CurrentOpenDatabase(app, app)

        label = None

        for i in view.grid_slaves():
            if isinstance(i, tk.Label):
                label = i

        self.assertEqual(label['text'], 'Currently using database: a')

    def test_current_open_database_no_db_open(self):
        app = tk.Frame()
        app.current_open_database = None
        view = main_view._CurrentOpenDatabase(app, app)

        label = None

        for i in view.grid_slaves():
            if isinstance(i, tk.Label):
                label = i

        self.assertEqual(label['text'], 'Not using any database.')

    def test_current_open_table(self):
        app = tk.Frame()
        app.current_open_table = 'a'
        view = main_view._CurrentOpenTable(app, app)

        label = None

        for i in view.grid_slaves():
            if isinstance(i, tk.Label):
                label = i

        self.assertEqual(label['text'], 'Currently open table: a')

    def test_current_current_open_table_no_table_opened(self):
        app = tk.Frame()
        app.current_open_table = None
        view = main_view._CurrentOpenTable(app, app)

        label = None

        for i in view.grid_slaves():
            if isinstance(i, tk.Label):
                label = i

        self.assertEqual(label['text'], 'Not using any table.')

    def test_menu_create_widgets_no_db(self):
        app = tk.Frame()
        app.current_open_database = None
        app.current_open_table = None
        app.operation_result_message = None
        with unittest.mock.patch('icar.core.database_operations.list_databases') as list_databases:
            list_databases.return_value = []
            view = main_view._Menu(app, app)
            self.assertEqual(len(view.grid_slaves()), 1)

    def test_menu_create_widgets_with_db(self):
        app = tk.Frame()
        app.current_open_database = None
        app.current_open_table = None
        app.operation_result_message = None
        with unittest.mock.patch('icar.core.database_operations.list_databases') as list_databases:
            list_databases.return_value = ['a']
            view = main_view._Menu(app, app)
            self.assertEqual(len(view.grid_slaves()), 3)

    def test_menu_create_widgets_with_open_db_and_no_existing_table(self):
        app = tk.Frame()
        app.current_open_database = 'a'
        app.current_open_table = None
        app.operation_result_message = None
        with unittest.mock.patch('icar.core.database_operations.list_databases') as list_databases, \
                unittest.mock.patch('icar.core.database_operations.list_tables') as list_tables:
            list_databases.return_value = ['a']
            list_tables.return_value = []
            view = main_view._Menu(app, app)
            self.assertEqual(len(view.grid_slaves()), 4)

    def test_menu_create_widgets_with_open_db_and_existing_table(self):
        app = tk.Frame()
        app.current_open_database = 'a'
        app.current_open_table = None
        app.operation_result_message = None
        with unittest.mock.patch('icar.core.database_operations.list_databases') as list_databases, \
                unittest.mock.patch('icar.core.database_operations.list_tables') as list_tables:
            list_databases.return_value = ['a']
            list_tables.return_value = ['a']
            view = main_view._Menu(app, app)
            self.assertEqual(len(view.grid_slaves()), 6)

    def test_menu_create_widgets_with_open_db_and_open_table(self):
        app = tk.Frame()
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        app.operation_result_message = None
        with unittest.mock.patch('icar.core.database_operations.list_databases') as list_databases, \
                unittest.mock.patch('icar.core.database_operations.list_tables') as list_tables:
            list_databases.return_value = ['a']
            list_tables.return_value = ['a']
            view = main_view._Menu(app, app)
            self.assertEqual(len(view.grid_slaves()), 7)

    def test_current_main_page(self):
        app = tk.Frame()
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        app.operation_result_message = ''
        view = main_view.MainPage(app)

        frames = {
            main_view._CurrentOpenTable,
            main_view._CurrentOpenDatabase,
            main_view._OperationResultMessage,
            main_view._Menu
        }
        found_frames = set(map(type, view.grid_slaves()))

        self.assertEqual(found_frames, frames)

    def test_operation_menu_callback(self):
        with unittest.mock.patch('icar.interfaces.graphical_user_interface.views.main_view._Menu.create_widgets'), \
                unittest.mock.patch('icar.interfaces.graphical_user_interface.views.'
                                    'insert_record_view.InsertRecordView'):
            app = tk.Frame()
            app.current_open_database = 'a'
            app.current_open_table = 'a'
            app.replace_frame = unittest.mock.Mock()

            view = main_view._Menu(app, app)
            view.table_operation_menu_variable = unittest.mock.Mock()
            view.table_operation_menu_variable.get = unittest.mock.Mock(return_value='Insert Record')

            view.table_operation_menu_callback()
            app.replace_frame.assert_called()

    def test_operation_menu_callback_invalid(self):
        with unittest.mock.patch('icar.interfaces.graphical_user_interface.views.main_view._Menu.create_widgets'):
            app = tk.Frame()
            app.current_open_database = 'a'
            app.current_open_table = 'a'
            app.replace_frame = unittest.mock.Mock()

            view = main_view._Menu(app, app)
            view.table_operation_menu_variable = unittest.mock.Mock()
            view.table_operation_menu_variable.get = unittest.mock.Mock(return_value='a')

            view.table_operation_menu_callback()
            app.replace_frame.assert_not_called()

    def test_update_current_open_database(self):
        with unittest.mock.patch('icar.interfaces.graphical_user_interface.views.main_view._Menu.create_widgets'), \
                unittest.mock.patch('icar.interfaces.graphical_user_interface.views.main_view.MainPage'):
            app = tk.Frame()
            app.current_open_database = 'a'
            app.current_open_table = 'a'
            app.replace_frame = unittest.mock.Mock()

            view = main_view._Menu(app, app)
            view.current_database_to_open = unittest.mock.Mock()
            view.current_database_to_open.get = unittest.mock.Mock(return_value='a')

            view.update_current_open_database()
            app.replace_frame.assert_called()

    def test_update_current_open_table(self):
        with unittest.mock.patch('icar.interfaces.graphical_user_interface.views.main_view._Menu.create_widgets'), \
                unittest.mock.patch('icar.interfaces.graphical_user_interface.views.main_view.MainPage'):
            app = tk.Frame()
            app.current_open_database = 'a'
            app.current_open_table = 'a'
            app.replace_frame = unittest.mock.Mock()

            view = main_view._Menu(app, app)
            view.current_table_to_open = unittest.mock.Mock()
            view.current_table_to_open.get = unittest.mock.Mock(return_value='a')

            view.update_current_open_table()
            app.replace_frame.assert_called()


if __name__ == '__main__':
    unittest.main()
