import os
import tkinter as tk
import tkinter.filedialog

import icar.helpers.constants
import icar.core.database_operations
import icar.core.table_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class ImportTableView(base_view.BaseView):
    def __init__(self, app):
        self.fields = list()
        self.menu_buttons = list()

        self.table_operations = icar.core.table_operations.TableOps(
            app.current_open_database,
            app.current_open_table
        )

        super().__init__(app)

    def create_widgets(self):
        tk.Button(
            self,
            text='Choose a File',
            command=self.choose_directory_callback
        ).grid(row=0, column=0)
        self.import_path_string_variable = tk.StringVar(self, 'No path chosen')
        tk.Label(
            self,
            textvariable=self.import_path_string_variable
        ).grid(row=0, column=1)

        tk.Button(
            self,
            text='Import',
            command=self.import_callback
        ).grid(row=1, column=0, sticky=tk.W + tk.E)

        tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        ).grid(row=1, column=1, sticky=tk.W + tk.E)

    def import_callback(self):
        assert isinstance(self.import_path_string_variable.get(), str)

        if self.import_path_string_variable:
            path = self.import_path_string_variable.get()
            try:
                self.table_operations.import_(path)
                self.app.operation_result_message = 'Imported table successfully.'
            except Exception as exc:
                self.app.operation_result_message = 'Failed to import table because: {}'.format(exc)

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )

    def choose_directory_callback(self):
        path = tkinter.filedialog.askopenfilename(parent=self, initialdir=os.getcwd(), title='Select a file to import')
        assert isinstance(path, str)
        self.import_path_string_variable.set(path)
