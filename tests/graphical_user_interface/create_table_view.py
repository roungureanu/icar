import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.database_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.create_table_view as create_table_view


normal_constructor = icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__
create_menu = create_table_view.CreateTableView.create_menu
create_widgets = create_table_view.CreateTableView.create_widgets
add_column_callback = create_table_view.CreateTableView.add_column_callback


def test_constructor(self, app):
    self.app = app


class TestCase(unittest.TestCase):
    def tearDown(self) -> None:
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor

    def test_create_widgets(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor
        create_table_view.CreateTableView.add_column_callback = unittest.mock.Mock()
        create_table_view.CreateTableView.create_menu = unittest.mock.Mock()
        create_table_view.CreateTableView.create_widgets = create_widgets

        app = tk.Frame()

        view = create_table_view.CreateTableView(app)

        labels = []
        entry = None

        for i in view.grid_slaves():
            if isinstance(i, tk.Label):
                labels.append(i)
            elif isinstance(i, tk.Entry):
                entry = i

        self.assertEqual(len(labels), 4)
        self.assertIsNotNone(entry)

    def test_create_menu(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor
        create_table_view.CreateTableView.create_menu = create_menu
        create_table_view.CreateTableView.create_widgets = unittest.mock.Mock()

        app = tk.Frame()

        view = create_table_view.CreateTableView(app)
        view.create_menu()

        buttons = []

        for i in view.grid_slaves():
            if isinstance(i, tk.Button):
                buttons.append(i)

        self.assertEqual(len(buttons), 3)

    def test_add_column_callback(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor

        with unittest.mock.patch('icar.interfaces.graphical_user_interface.views'
                                 '.create_table_view.CreateTableView.create_menu'), \
                unittest.mock.patch('icar.interfaces.graphical_user_interface.views'
                                    '.create_table_view.CreateTableView.create_widgets'):
            app = tk.Frame()

            view = create_table_view.CreateTableView(app)
            view.add_column_callback()
            self.assertEqual(len(view.fields), 1)

    def test_delete_row_single_field(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)

        view = create_table_view.CreateTableView(app)
        view.fields = ['a']
        view.delete_row([unittest.mock.Mock() for _ in range(3)], 'a')
        self.assertEqual(len(view.fields), 1)

    def test_delete_row_multiple_fields(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)

        view = create_table_view.CreateTableView(app)
        view.fields = ['a', 'b']
        view.delete_row([unittest.mock.Mock() for _ in range(3)], 'a')
        self.assertEqual(len(view.fields), 1)

    def test_create_callback(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'

        view = create_table_view.CreateTableView(app)
        view.table_name_entry = unittest.mock.Mock()
        view.table_name_entry.get = unittest.mock.Mock(return_value='a')

        m = {
            'column_name_entry_field': unittest.mock.Mock(),
            'column_type_option_field_value': unittest.mock.Mock(),
            'column_size_entry_field': unittest.mock.Mock()
        }
        for key in m:
            m[key].get = unittest.mock.Mock(return_value='a')
        view.fields = [m]

        with unittest.mock.patch('icar.core.database_operations.create_table') as create_table:
            view.create_table_callback()
            create_table.assert_called()
            app.replace_frame.assert_called()

    def test_create_callback_invalid(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'

        view = create_table_view.CreateTableView(app)
        view.table_name_entry = unittest.mock.Mock()
        view.table_name_entry.get = unittest.mock.Mock(return_value='a')

        m = {
            'column_name_entry_field': unittest.mock.Mock(),
            'column_type_option_field_value': unittest.mock.Mock(),
            'column_size_entry_field': unittest.mock.Mock()
        }
        for key in m:
            m[key].get = unittest.mock.Mock(return_value='')
        view.fields = [m]

        with unittest.mock.patch('icar.core.database_operations.create_table') as create_table:
            view.create_table_callback()
            create_table.assert_not_called()
            app.replace_frame.assert_called()


if __name__ == '__main__':
    unittest.main()
