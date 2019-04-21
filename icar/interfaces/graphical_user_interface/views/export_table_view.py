import os
import tkinter as tk
import tkinter.filedialog

import icar.helpers.constants
import icar.core.database_operations
import icar.core.table_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class ExportTableView(base_view.BaseView):
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
            text='Choose Directory',
            command=self.choose_directory_callback
        ).grid(row=0, column=0)
        self.export_path_string_variable = tk.StringVar(self, 'No path chosen')
        tk.Label(
            self,
            textvariable=self.export_path_string_variable
        ).grid(row=0, column=1)

        tk.Button(
            self,
            text='Export',
            command=self.export_callback
        ).grid(row=1, column=0, sticky=tk.W + tk.E)

        tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        ).grid(row=1, column=1, sticky=tk.W + tk.E)

    def export_callback(self):
        if self.export_path_string_variable:
            unique_number = 1
            path = os.path.join(
                self.export_path_string_variable.get(),
                'export.xml'
            )
            while os.path.exists(path):
                rest, ext = os.path.splitext(path)
                path = rest + '({})'.format(unique_number) + ext
                unique_number = unique_number + 1

            self.table_operations.export(path)

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )

    def choose_directory_callback(self):
        path = tkinter.filedialog.askdirectory(parent=self, initialdir=os.getcwd(), title='Please select a directory')
        self.export_path_string_variable.set(path)
