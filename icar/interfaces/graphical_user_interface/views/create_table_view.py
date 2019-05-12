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
        ).grid(row=0, column=0, sticky=tk.E + tk.W)
        self.table_name_entry = tk.Entry(
            self
        )
        self.table_name_entry.grid(row=0, column=1, columnspan=2, sticky=tk.E + tk.W)

        column_name_label = tk.Label(self, text='Column Name')
        column_type_label = tk.Label(self, text='Column Type')
        column_size_label = tk.Label(self, text='Column Size')

        column_name_label.grid(row=1, column=0, sticky=tk.W + tk.E)
        column_type_label.grid(row=1, column=1, sticky=tk.W + tk.E)
        column_size_label.grid(row=1, column=2, sticky=tk.W + tk.E)

        self.create_menu()
        self.add_column_callback()

    def create_menu(self, row=2):
        create_button = tk.Button(
            self,
            text='Create',
            command=self.create_table_callback
        )
        create_button.grid(row=row, column=0, sticky=tk.E + tk.W)

        add_column_button = tk.Button(
            self,
            text='Add Column',
            command=self.add_column_callback
        )
        add_column_button.grid(row=row, column=1, sticky=tk.E + tk.W)

        cancel_button = tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        )
        cancel_button.grid(row=row, column=2, sticky=tk.E + tk.W)

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
        )

        column_size_entry_field = tk.Entry(
            self
        )

        row.append(column_name_entry_field)
        row.append(column_type_option_field)
        row.append(delete_field_button)
        row.append(column_size_entry_field)

        entry = {
            'column_name_entry_field': column_name_entry_field,
            'column_type_option_field': column_type_option_field,
            'column_type_option_field_value': column_type_option_field_value,
            'delete_field_button': delete_field_button,
            'column_size_entry_field': column_size_entry_field
        }
        self.fields.append(entry)
        delete_field_button.configure(command=lambda: self.delete_row(row, entry))

        column_name_entry_field.grid(row=len(self.fields) + 1, column=0, sticky=tk.E + tk.W)
        column_type_option_field.grid(row=len(self.fields) + 1, column=1, sticky=tk.E + tk.W)
        column_size_entry_field.grid(row=len(self.fields) + 1, column=2, sticky=tk.E + tk.W)
        delete_field_button.grid(row=len(self.fields) + 1, column=3, sticky=tk.E + tk.W)

        self.create_menu(len(self.fields) + 2)

    def delete_row(self, row, entry):
        if len(self.fields) == 1:
            return

        for item in row:
            item.destroy()

        for field in self.fields:
            if field == entry:
                self.fields.remove(field)
                break

    def create_table_callback(self):
        table_name = self.table_name_entry.get()

        column_names = []
        column_types = []
        column_sizes = []

        for field in self.fields:
            column_name = field['column_name_entry_field'].get()
            column_type = field['column_type_option_field_value'].get()
            column_size = field['column_size_entry_field'].get()

            if column_type == icar.helpers.constants.VALID_COLUMN_TYPES['NUMERIC']:
                column_size = 0
            else:
                try:
                    column_size = int(column_size)
                except Exception:
                    column_size = 255

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
