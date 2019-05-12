import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.table_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.delete_records_view as delete_records_view


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

        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops, \
                unittest.mock.patch('icar.interfaces.graphical_user_interface.'
                                    'views.delete_records_view.DeleteRecordsView.delete_records'):
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = delete_records_view.DeleteRecordsView(app)

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

            self.assertEqual(len(labels), 1 + len(view.table_operations.columns))
            self.assertEqual(len(buttons), 2)
            self.assertEqual(len(option_menus), 1)
            self.assertEqual(len(frames), len(view.table_operations.columns))

    def test_filter_rows(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'

        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = delete_records_view.DeleteRecordsView(app)
            view.records = unittest.mock.Mock()
            view.records.destroy = unittest.mock.Mock()
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
            for column in view.filters:
                view.filters[column]['operator_field'].get = unittest.mock.Mock(return_value='==')
                view.filters[column]['value_field'].get = unittest.mock.Mock(return_value='a')

            view.columns_to_select = unittest.mock.Mock()

            columns_to_select_mocks = []
            for i in view.table_operations.columns:
                m = unittest.mock.Mock()
                m.get = unittest.mock.Mock(return_value='a')
                columns_to_select_mocks.append(m)
            view.columns_to_select.curselection = unittest.mock.Mock(return_value=columns_to_select_mocks)

            view.delete_records()

            view.table_operations.delete.assert_called()


if __name__ == '__main__':
    unittest.main()
