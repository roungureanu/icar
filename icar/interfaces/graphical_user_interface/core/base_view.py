import abc
import tkinter as tk


class BaseView(tk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        self.create_widgets()

    @abc.abstractmethod
    def create_widgets(self):
        pass
