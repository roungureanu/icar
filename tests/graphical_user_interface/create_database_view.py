import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface.core.base_view
import icar.core.database_operations

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.create_database_view as create_database_view


def page_constructor(self, app):
    self.app = app


class TestCase(unittest.TestCase):
    def test_create_widgets(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = page_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        view = create_database_view.CreateDatabasePage(app)

        with unittest.mock.patch('tkinter.Label'), \
                unittest.mock.patch('tkinter.Entry'), \
                unittest.mock.patch('tkinter.Button'):
            view.create_widgets()

    def test_create_database_callback(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = page_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        view = create_database_view.CreateDatabasePage(app)
        view.entry = unittest.mock.Mock(spec=['get'])
        view.entry.get = unittest.mock.Mock(return_value='a')

        icar.core.database_operations.database_exists = unittest.mock.Mock(return_value=False)
        icar.core.database_operations.create_database = unittest.mock.Mock()

        view.create_database_callback()

        app.replace_frame.assert_called()
        icar.core.database_operations.create_database.assert_called()

    def test_create_database_callback_already_existing(self):
        icar.interfaces.graphical_user_interface.core.base_view.BaseView.__init__ = page_constructor

        app = unittest.mock.Mock(icar.interfaces.graphical_user_interface_application.Application)
        view = create_database_view.CreateDatabasePage(app)
        view.entry = unittest.mock.Mock(spec=['get'])
        view.entry.get = unittest.mock.Mock(return_value='a')

        icar.core.database_operations.database_exists = unittest.mock.Mock(return_value=True)
        icar.core.database_operations.create_database = unittest.mock.Mock()

        view.create_database_callback()

        icar.core.database_operations.create_database.assert_not_called()


if __name__ == '__main__':
    unittest.main()
