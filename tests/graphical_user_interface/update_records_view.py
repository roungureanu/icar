import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.table_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.update_records_view as update_records_view


normal_constructor = icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__


def test_constructor(self, app):
    self.app = app


class TestCase(unittest.TestCase):
    def tearDown(self) -> None:
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor

    def test_create_widgets(self):
        app = tk.Frame()
        app.current_open_database = 'a'
        app.current_open_table = 'a'

        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = update_records_view.UpdateRecordsView(app)

            labels = []
            buttons = []
            entries = []
            option_menus = []
            frames = []

            for i in view.grid_slaves():
                if isinstance(i, tk.Label):
                    labels.append(i)
                elif isinstance(i, tk.OptionMenu):
                    option_menus.append(i)
                elif isinstance(i, tk.Frame):
                    frames.append(i)
                elif isinstance(i, tk.Button):
                    buttons.append(i)
                elif isinstance(i, tk.Entry):
                    entries.append(i)

            self.assertEqual(len(labels), 2 + 2 * len(view.table_operations.columns))
            self.assertEqual(len(buttons), 2)
            self.assertEqual(len(entries), len(view.table_operations.columns))
            self.assertEqual(len(option_menus), 1)
            self.assertEqual(len(frames), len(view.table_operations.columns))

    def test_update_records(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = update_records_view.UpdateRecordsView(app)
            view.table_operations.columns = ['a', 'b', 'c']
            view.operator_value = unittest.mock.Mock()
            view.operator_value.get = unittest.mock.Mock(return_value='a')
            view.filters = {
                column: {
                    'operator_field': unittest.mock.Mock(),
                    'value_field': unittest.mock.Mock()
                }
                for column in view.table_operations.columns
            }
            view.new_values = dict()
            for column in view.filters:
                view.filters[column]['operator_field'].get = unittest.mock.Mock(return_value='==')
                view.filters[column]['value_field'].get = unittest.mock.Mock(return_value='a')
                view.new_values[column] = unittest.mock.Mock()
                view.new_values[column].get = unittest.mock.Mock(return_value='a')

            view.update_records()

            view.table_operations.update.assert_called()
            app.replace_frame.assert_called()

    def test_update_records_invalid(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = update_records_view.UpdateRecordsView(app)
            view.table_operations.columns = ['a', 'b', 'c']
            view.operator_value = unittest.mock.Mock()
            view.operator_value.get = unittest.mock.Mock(return_value='a')
            view.filters = {
                column: {
                    'operator_field': unittest.mock.Mock(),
                    'value_field': unittest.mock.Mock()
                }
                for column in view.table_operations.columns
            }
            view.new_values = dict()
            for column in view.filters:
                view.filters[column]['operator_field'].get = unittest.mock.Mock(return_value='==')
                view.filters[column]['value_field'].get = unittest.mock.Mock(return_value='a')
                view.new_values[column] = unittest.mock.Mock()
                view.new_values[column].get = unittest.mock.Mock(return_value='')

            view.update_records()

            view.table_operations.update.assert_not_called()
            app.replace_frame.assert_called()


if __name__ == '__main__':
    unittest.main()
