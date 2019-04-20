import tkinter as tk

import icar.helpers.constants
import icar.core.database_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class CreateTableView(base_view.BaseView):
    def __init__(self, app):
        self.fields = list()
        self.menu_buttons = list()

        super().__init__(app)

    def create_widgets(self):
        tk.Label(
            self,
            text='Table Name'
        ).grid(row=0, column=0)
        self.table_name_entry = tk.Entry(
            self
        )
        self.table_name_entry.grid(row=0, column=1)

        self.create_menu()

    def create_menu(self, row=1):
        create_button = tk.Button(
            self,
            text='Create',
            command=self.create_table_callback
        )
        create_button.grid(row=row, column=0)

        add_column_button = tk.Button(
            self,
            text='Add Column',
            command=self.add_column_callback
        )
        add_column_button.grid(row=row, column=1)

        cancel_button = tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        )
        cancel_button.grid(row=row, column=2)

        self.menu_buttons.append(create_button)
        self.menu_buttons.append(add_column_button)
        self.menu_buttons.append(cancel_button)

    def add_column_callback(self):
        row = list()

        for button in self.menu_buttons:
            button.destroy()

        column_name_entry_field = tk.Entry(
            self
        )

        valid_column_types = list(icar.helpers.constants.VALID_COLUMN_TYPES.values())

        column_type_option_field_value = tk.StringVar(self, valid_column_types[0])
        column_type_option_field = tk.OptionMenu(
            self,
            column_type_option_field_value,
            *valid_column_types
        )

        delete_field_button = tk.Button(
            self,
            text='Delete',
            command=lambda: self.delete_row(row)
        )
        row.append(column_name_entry_field)
        row.append(column_type_option_field)
        row.append(delete_field_button)

        self.fields.append(
            {
                'column_name_entry_field': column_name_entry_field,
                'column_type_option_field': column_type_option_field,
                'column_type_option_field_value': column_type_option_field_value,
                'delete_field_button': delete_field_button
            }
        )

        column_name_entry_field.grid(row=len(self.fields), column=0)
        column_type_option_field.grid(row=len(self.fields), column=1)
        delete_field_button.grid(row=len(self.fields), column=2)

        self.create_menu(len(self.fields) + 1)

    def delete_row(self, row):
        for item in row:
            item.destroy()

    def create_table_callback(self):
        table_name = self.table_name_entry.get()

        column_names = []
        column_types = []
        column_sizes = []

        for field in self.fields:
            column_name = field['column_name_entry_field'].get()
            column_type = field['column_type_option_field_value'].get()
            column_size = 10

            if column_name:
                column_names.append(column_name)
                column_types.append(column_type)
                column_sizes.append(column_size)

        icar.core.database_operations.create_table(
            self.app.current_open_database,
            table_name,
            column_names,
            column_types,
            column_sizes
        )

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )
