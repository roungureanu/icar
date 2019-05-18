import tkinter as tk

import icar.helpers.constants
import icar.core.table_operations
import icar.core.database_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class RemoveColumnView(base_view.BaseView):
    def __init__(self, app):
        self.fields = list()
        self.menu_buttons = list()

        self.table_operations = icar.core.table_operations.TableOps(
            app.current_open_database,
            app.current_open_table
        )

        super().__init__(app)

    def create_widgets(self):
        tk.Label(
            self,
            text='Remove Column'
        ).grid(row=0, column=0)
        tk.Label(
            self,
            text='Column Name'
        ).grid(row=1, column=0, sticky=tk.W + tk.E)
        column_names = list(self.table_operations.columns)
        self.column_to_delete = tk.StringVar(self, column_names[0])
        tk.OptionMenu(
            self, self.column_to_delete, *column_names
        ).grid(row=1, column=1, sticky=tk.W + tk.E)

        tk.Button(
            self,
            text='Delete',
            command=self.delete_column_callback
        ).grid(row=2, column=0, sticky=tk.W + tk.E)

        tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        ).grid(row=2, column=1, sticky=tk.W + tk.E)

    def delete_column_callback(self):
        column_name = self.column_to_delete.get()

        assert isinstance(column_name, str)

        if column_name:
            icar.core.database_operations.remove_column(
                self.app.current_open_database,
                self.app.current_open_table,
                column_name
            )

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )
