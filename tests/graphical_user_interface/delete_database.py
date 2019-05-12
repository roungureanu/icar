import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.database_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.delete_database_view as delete_database_view


normal_constructor = icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__


def test_constructor(self, app):
    self.app = app


class TestCase(unittest.TestCase):
    def tearDown(self) -> None:
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor

    def test_create_widgets(self):
        app = tk.Frame()
        view = delete_database_view.DeleteDatabasePage(app)

        label = None
        option_menu = None
        buttons = []

        for i in view.grid_slaves():
            if isinstance(i, tk.Label):
                label = i
            elif isinstance(i, tk.OptionMenu):
                option_menu = i
            elif isinstance(i, tk.Button):
                buttons.append(i)

        self.assertIsNotNone(label)
        self.assertIsNotNone(option_menu)
        self.assertEqual(len(buttons), 2)

    def test_delete_database_callback(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'b'
        view = delete_database_view.DeleteDatabasePage(app)
        view.database_to_delete_variable = unittest.mock.Mock(spec=['get'])
        view.database_to_delete_variable.get = unittest.mock.Mock(return_value='a')

        with unittest.mock.patch('icar.core.database_operations.delete_database') as delete_database:
            view.delete_database_callback()

            app.replace_frame.assert_called()
            delete_database.assert_called()
            self.assertEqual(app.current_open_database, 'b')

    def test_delete_database_callback_selected_database(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        app.current_open_database = 'a'
        view = delete_database_view.DeleteDatabasePage(app)
        view.database_to_delete_variable = unittest.mock.Mock(spec=['get'])
        view.database_to_delete_variable.get = unittest.mock.Mock(return_value='a')

        with unittest.mock.patch('icar.core.database_operations.delete_database') as delete_database:
            view.delete_database_callback()

            app.replace_frame.assert_called()
            delete_database.assert_called()
            self.assertIsNone(app.current_open_database)


if __name__ == '__main__':
    unittest.main()
