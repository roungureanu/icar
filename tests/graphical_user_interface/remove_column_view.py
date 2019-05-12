import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.database_operations
import icar.core.table_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.remove_column_view as remove_column_view


normal_constructor = icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__


def test_constructor(self, app):
    self.app = app


class TestCase(unittest.TestCase):
    def tearDown(self) -> None:
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor

    def test_create_widgets(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor

        app = tk.Frame()
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = remove_column_view.RemoveColumnView(app)

            labels = []
            option_menu = None
            buttons = []

            for i in view.grid_slaves():
                if isinstance(i, tk.Label):
                    labels.append(i)
                elif isinstance(i, tk.OptionMenu):
                    option_menu = i
                elif isinstance(i, tk.Button):
                    buttons.append(i)

            self.assertEqual(len(labels), 2)
            self.assertIsNotNone(option_menu)
            self.assertEqual(len(buttons), 2)

    def test_delete_column_callback(self):
        with unittest.mock.patch('icar.core.database_operations.remove_column') as remove_column, \
                unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

            app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
            app.current_open_database = 'a'
            app.current_open_table = 'a'

            view = remove_column_view.RemoveColumnView(app)
            view.column_to_delete = unittest.mock.Mock(spec=['get'])
            view.column_to_delete.get = unittest.mock.Mock(return_value='a')

            view.delete_column_callback()

            app.replace_frame.assert_called()
            remove_column.assert_called()

    def test_delete_column_callback_invalid(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'

        with unittest.mock.patch('icar.core.database_operations.remove_column') as remove_column, \
                unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = remove_column_view.RemoveColumnView(app)
            view.column_to_delete = unittest.mock.Mock(spec=['get'])
            view.column_to_delete.get = unittest.mock.Mock(return_value='')
            view.delete_column_callback()

            app.replace_frame.assert_called()
            remove_column.assert_not_called()


if __name__ == '__main__':
    unittest.main()
