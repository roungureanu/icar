import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.database_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.add_column_view as add_column_view


normal_constructor = icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__


def test_constructor(self, app):
    self.app = app


class TestCase(unittest.TestCase):
    def tearDown(self) -> None:
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor

    def test_create_widgets(self):
        app = tk.Frame()

        view = add_column_view.AddColumnView(app)

        labels = []
        entries = []
        buttons = []
        option_menu = None

        for i in view.grid_slaves():
            if isinstance(i, tk.Label):
                labels.append(i)
            elif isinstance(i, tk.Entry):
                entries.append(i)
            elif isinstance(i, tk.OptionMenu):
                option_menu = i
            elif isinstance(i, tk.Button):
                buttons.append(i)

        self.assertEqual(len(labels), 4)
        self.assertEqual(len(entries), 2)
        self.assertEqual(len(buttons), 2)
        self.assertIsNotNone(option_menu)

    def test_add_column_callback(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'b'
        view = add_column_view.AddColumnView(app)
        view.new_column_entry = unittest.mock.Mock(spec=['get'])
        view.new_column_type = unittest.mock.Mock(spec=['get'])
        view.new_column_entry.get = unittest.mock.Mock(return_value='a')
        view.new_column_type.get = unittest.mock.Mock(return_value='a')

        with unittest.mock.patch('icar.core.database_operations.add_column') as add_column:
            view.add_column_callback()

            app.replace_frame.assert_called()
            add_column.assert_called()

    def test_add_column_callback_invalid_column(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'b'
        view = add_column_view.AddColumnView(app)
        view.new_column_entry = unittest.mock.Mock(spec=['get'])
        view.new_column_type = unittest.mock.Mock(spec=['get'])
        view.new_column_entry.get = unittest.mock.Mock(return_value='')
        view.new_column_type.get = unittest.mock.Mock(return_value='a')

        with unittest.mock.patch('icar.core.database_operations.add_column') as add_column:
            view.add_column_callback()

            app.replace_frame.assert_called()
            add_column.assert_not_called()


if __name__ == '__main__':
    unittest.main()
