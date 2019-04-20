import tkinter as tk

import icar.core.database_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class DeleteDatabasePage(base_view.BaseView):
    def create_widgets(self):
        tk.Label(
            self,
            text='Database To DELETE'
        ).grid(row=0, column=0)

        self.database_to_delete_variable = tk.StringVar(self, value='Choose Database')

        available_databases = icar.core.database_operations.list_databases()
        self.database_picker = tk.OptionMenu(self, self.database_to_delete_variable, *available_databases)
        self.database_picker.grid(row=0, column=1)

        create_button = tk.Button(
            self,
            text='DELETE',
            command=self.delete_database_callback
        )
        create_button.grid(row=1, column=0)

        cancel_button = tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        )
        cancel_button.grid(row=1, column=1)

    def delete_database_callback(self):
        database_name = self.database_to_delete_variable.get()

        if database_name != 'Choose Database':
            icar.core.database_operations.delete_database(database_name)
            self.app.operation_result_message = 'Deleted database successfully.'

        if database_name == self.app.current_open_database:
            self.app.current_open_database = None
            self.app.current_open_table = None

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )
