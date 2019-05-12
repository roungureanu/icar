import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.table_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.insert_record_view as insert_record_view


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

            view = insert_record_view.InsertRecordView(app)

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

            self.assertEqual(len(labels), len(view.table_operations.columns))
            self.assertEqual(len(buttons), 2)
            self.assertEqual(len(entries), len(view.table_operations.columns))

    def test_insert_record_callback(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = insert_record_view.InsertRecordView(app)
            view.fields = dict()
            for column in view.table_operations.columns:
                view.fields[column] = unittest.mock.Mock()
                view.fields[column].get = unittest.mock.Mock(return_value='a')

            view.insert_record_callback()

            view.table_operations.insert.assert_called()
            app.replace_frame.assert_called()

    def test_insert_record_invalid(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        app.current_open_table = 'a'
        with unittest.mock.patch('icar.core.table_operations.TableOps') as table_ops:
            table_ops().lines = ['a', 'b', 'c']
            table_ops().columns = {'a': [], 'b': [], 'c': []}

            view = insert_record_view.InsertRecordView(app)
            view.fields = dict()
            for column in view.table_operations.columns:
                view.fields[column] = unittest.mock.Mock()
                view.fields[column].get = unittest.mock.Mock(return_value='')

            view.insert_record_callback()

            view.table_operations.insert.assert_not_called()
            app.replace_frame.assert_called()


if __name__ == '__main__':
    unittest.main()
