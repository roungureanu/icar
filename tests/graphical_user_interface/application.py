import unittest
import unittest.mock

import tkinter as tk

import icar.interfaces.graphical_user_interface_application
import icar.interfaces.graphical_user_interface.views.main_view as main_view


class TestCase(unittest.TestCase):
    def test_constructor_and_replace_frame(self):
        application = icar.interfaces.graphical_user_interface_application.Application(tk.Tk())
        self.assertIsNotNone(application._current_frame)

    def test_constructor_and_replace_frame_2(self):
        application = icar.interfaces.graphical_user_interface_application.Application(tk.Tk())
        current_frame = application._current_frame
        application.replace_frame(main_view.MainPage(application))
        self.assertNotEqual(current_frame, application._current_frame)

    def test_rooted_center(self):
        self.assertIsNotNone(icar.interfaces.graphical_user_interface_application.retrieve_centered_root())


if __name__ == '__main__':
    unittest.main()
