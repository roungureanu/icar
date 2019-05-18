import tkinter as tk

import icar.helpers.constants
import icar.core.database_operations
import icar.core.table_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class InsertRecordView(base_view.BaseView):
    def __init__(self, app):
        self.fields = dict()
        self.table_operations = icar.core.table_operations.TableOps(
            app.current_open_database,
            app.current_open_table
        )

        super().__init__(app)

    def create_widgets(self):
        create_button = tk.Button(
            self,
            text='Insert',
            command=self.insert_record_callback
        )

        for i, column_name in enumerate(self.table_operations.columns):
            tk.Label(
                self,
                text=column_name
            ).grid(row=i + 1, column=0)
            value_entry = tk.Entry(
                self
            )
            value_entry.grid(row=i + 1, column=1)

            self.fields[column_name] = value_entry

        create_button.grid(row=len(self.table_operations.columns) + 1, column=0, sticky=tk.W + tk.E)

        cancel_button = tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        )
        cancel_button.grid(row=len(self.table_operations.columns) + 1, column=1, sticky=tk.W + tk.E)

    def insert_record_callback(self):
        values = [
            entry_field.get()
            for entry_field in self.fields.values()
        ]

        assert all(map(lambda item: isinstance(item, str), values))

        if len(values) == len(self.table_operations.columns):
            self.table_operations.insert(
                list(self.table_operations.columns.keys()),
                values
            )

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )
