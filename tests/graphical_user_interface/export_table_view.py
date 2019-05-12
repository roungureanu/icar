import os
import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.table_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.export_table_view as export_table_view


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
            table_ops().columns = ['a', 'b', 'c']

            view = export_table_view.ExportTableView(app)

            labels = []
            buttons = []
            entries = []

            for i in view.grid_slaves():
                if isinstance(i, tk.Label):
                    labels.append(i)
                elif isinstance(i, tk.Button):
                    buttons.append(i)
                elif isinstance(i, tk.Entry):
                    entries.append(i)

            self.assertEqual(len(labels), 1)
            self.assertEqual(len(buttons), 3)

    def test_export_callback(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = ['a', 'b', 'c']

            view = export_table_view.ExportTableView(app)
            view.export_path_string_variable = unittest.mock.Mock()
            view.export_path_string_variable.get = unittest.mock.Mock(return_value='a')

            with unittest.mock.patch('os.path.exists') as mock:
                mock.return_value = False
                view.export_callback()

            view.table_operations.export.assert_called()
            app.replace_frame.assert_called()

    def test_export_callback_existing_file(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = ['a', 'b', 'c']

            view = export_table_view.ExportTableView(app)
            view.export_path_string_variable = unittest.mock.Mock()
            view.export_path_string_variable.get = unittest.mock.Mock(return_value='a')

            with unittest.mock.patch('os.path.exists') as mock:
                mock.side_effect = [True, False]
                view.export_callback()

            view.table_operations.export.assert_called_with(os.path.join('a', 'export(1).xml'))
            app.replace_frame.assert_called()

    def test_export_callback_two_existing_file(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = ['a', 'b', 'c']

            view = export_table_view.ExportTableView(app)
            view.export_path_string_variable = unittest.mock.Mock()
            view.export_path_string_variable.get = unittest.mock.Mock(return_value='a')

            with unittest.mock.patch('os.path.exists') as mock:
                mock.side_effect = [True, True, False]
                view.export_callback()

            view.table_operations.export.assert_called_with(os.path.join('a', 'export(2).xml'))
            app.replace_frame.assert_called()

    def test_export_callback_invalid(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = ['a', 'b', 'c']

            view = export_table_view.ExportTableView(app)
            view.export_path_string_variable = unittest.mock.Mock()
            view.export_path_string_variable.get = unittest.mock.Mock(return_value='')

            view.export_callback()

            view.table_operations.export.assert_not_called()
            app.replace_frame.assert_called()


if __name__ == '__main__':
    unittest.main()
