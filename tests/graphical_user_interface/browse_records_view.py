import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.table_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.browse_records_view as browse_records_view


normal_constructor = icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__
normal_update_rows = browse_records_view.BrowseRecordsView.update_rows


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
                                    'views.browse_records_view.BrowseRecordsView.update_rows'):
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = ['a', 'b', 'c']

            view = browse_records_view.BrowseRecordsView(app)
            view.table_operations.columns = ['a', 'b', 'c']

            labels = []
            buttons = []
            option_menu = None

            for i in view.grid_slaves():
                if isinstance(i, tk.Label):
                    labels.append(i)
                elif isinstance(i, tk.OptionMenu):
                    option_menu = i
                elif isinstance(i, tk.Button):
                    buttons.append(i)

            self.assertEqual(len(labels), 1)
            self.assertEqual(len(buttons), 2)
            self.assertIsNotNone(option_menu)

    def test_update_rows(self):
        app = tk.Frame()
        app.current_open_database = 'a'
        app.current_open_table = 'a'

        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = browse_records_view.BrowseRecordsView(app)
            self.assertNotEqual(len(view.records.pack_slaves()), 0)

    def test_filter_rows(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'

        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops, \
                unittest.mock.patch('icar.interfaces.graphical_user_interface.'
                                    'views.browse_records_view.BrowseRecordsView.update_rows'):
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = ['a', 'b', 'c']

            view = browse_records_view.BrowseRecordsView(app)
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

            view.filter_rows()

            view.table_operations.select.assert_called()


if __name__ == '__main__':
    unittest.main()
