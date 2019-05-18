import tkinter as tk

import icar.helpers.constants
import icar.core.database_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class AddColumnView(base_view.BaseView):
    def __init__(self, app):
        self.fields = list()
        self.menu_buttons = list()

        super().__init__(app)

    def create_widgets(self):
        tk.Label(
            self,
            text='Add New Column'
        ).grid(row=0, column=0)
        tk.Label(
            self,
            text='Column Name'
        ).grid(row=1, column=0, sticky=tk.W + tk.E)
        self.new_column_entry = tk.Entry(
            self
        )
        self.new_column_entry.grid(row=1, column=1)
        tk.Label(
            self,
            text='Column Type'
        ).grid(row=2, column=0, sticky=tk.W + tk.E)
        column_types = list(icar.helpers.constants.VALID_COLUMN_TYPES.keys())
        self.new_column_type = tk.StringVar(self, column_types[0])
        tk.OptionMenu(
            self, self.new_column_type, *column_types
        ).grid(row=2, column=1, sticky=tk.W + tk.E)

        tk.Label(
            self,
            text='Column Size'
        ).grid(row=3, column=0, sticky=tk.W + tk.E)
        self.new_column_size = tk.Entry(
            self
        )
        self.new_column_size.grid(row=3, column=1)

        tk.Button(
            self,
            text='Create',
            command=self.add_column_callback
        ).grid(row=4, column=0, sticky=tk.W + tk.E)

        tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        ).grid(row=4, column=1, sticky=tk.W + tk.E)

    def add_column_callback(self):
        column_name = self.new_column_entry.get()
        column_type = self.new_column_type.get()

        assert isinstance(column_name, str)
        assert isinstance(column_type, str)
        assert column_type in icar.helpers.constants.VALID_COLUMN_TYPES

        if column_type == icar.helpers.constants.VALID_COLUMN_TYPES['NUMERIC']:
            column_size = 0
        else:
            try:
                column_size = self.new_column_size.get()
            except Exception:
                column_size = 255

        if column_name:
            icar.core.database_operations.add_column(
                self.app.current_open_database,
                self.app.current_open_table,
                column_name,
                column_type,
                column_size
            )

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )
