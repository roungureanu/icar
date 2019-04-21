import tkinter as tk

import icar.core.database_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class DeleteTablePage(base_view.BaseView):
    def create_widgets(self):
        tk.Label(
            self,
            text='Table To DELETE'
        ).grid(row=0, column=0)

        self.table_to_delete_variable = tk.StringVar(self, value='Choose Table')

        database_name = self.app.current_open_database
        available_tables = icar.core.database_operations.list_tables(database_name)
        self.table_picker = tk.OptionMenu(self, self.table_to_delete_variable, *available_tables)
        self.table_picker.grid(row=0, column=1)

        delete_button = tk.Button(
            self,
            text='DELETE',
            command=self.delete_table_callback
        )
        delete_button.grid(row=1, column=0, sticky=tk.W + tk.E)

        cancel_button = tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        )
        cancel_button.grid(row=1, column=1, sticky=tk.W + tk.E)

    def delete_table_callback(self):
        database_name = self.app.current_open_database
        table_name = self.table_to_delete_variable.get()

        if table_name != 'Choose Table':
            icar.core.database_operations.delete_table(database_name, table_name)
            self.app.operation_result_message = 'Deleted table successfully.'

        if table_name == self.app.current_open_table:
            self.app.current_open_table = None

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )
