import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.database_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.create_database_view as create_database_view


normal_constructor = icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__


def test_constructor(self, app):
    self.app = app


class TestCase(unittest.TestCase):
    def tearDown(self) -> None:
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = normal_constructor

    def test_create_widgets(self):
        app = tk.Frame()

        view = create_database_view.CreateDatabasePage(app)

        label = None
        entry = None
        buttons = []

        for i in view.grid_slaves():
            if isinstance(i, tk.Label):
                label = i
            elif isinstance(i, tk.Entry):
                entry = i
            elif isinstance(i, tk.Button):
                buttons.append(i)

        self.assertIsNotNone(label)
        self.assertIsNotNone(entry)
        self.assertEqual(len(buttons), 2)

    def test_create_database_callback(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        view = create_database_view.CreateDatabasePage(app)
        view.entry = unittest.mock.Mock(spec=['get'])
        view.entry.get = unittest.mock.Mock(return_value='a')

        with unittest.mock.patch('icar.core.database_operations.database_exists') as database_exists, \
                unittest.mock.patch('icar.core.database_operations.create_database') as create_database:
            database_exists.return_value = False

            view.create_database_callback()

            app.replace_frame.assert_called()
            create_database.assert_called()

    def test_create_database_callback_already_existing(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = test_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        view = create_database_view.CreateDatabasePage(app)
        view.entry = unittest.mock.Mock(spec=['get'])
        view.entry.get = unittest.mock.Mock(return_value='a')

        with unittest.mock.patch('icar.core.database_operations.database_exists') as database_exists, \
                unittest.mock.patch('icar.core.database_operations.create_database') as create_database:
            database_exists.return_value = True

            view.create_database_callback()

            create_database.assert_not_called()


if __name__ == '__main__':
    unittest.main()
