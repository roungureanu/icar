import tkinter as tk

import icar.core.database_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class CreateDatabasePage(base_view.BaseView):
    def create_widgets(self):
        tk.Label(
            self,
            text='Database Name'
        ).grid(row=0, column=0)
        self.entry = tk.Entry(
            self
        )
        self.entry.grid(row=0, column=1)
        create_button = tk.Button(
            self,
            text='Create',
            command=self.create_database_callback
        )
        create_button.grid(row=1, column=0, sticky=tk.W + tk.E)

        cancel_button = tk.Button(
            self,
            text='Cancel',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        )
        cancel_button.grid(row=1, column=1, sticky=tk.W + tk.E)

    def create_database_callback(self):
        database_name = self.entry.get()
        if not database_name:
            self.app.operation_result_message = 'No database name given.'
        elif icar.core.database_operations.database_exists(database_name):
            self.app.operation_result_message = 'The database already exists.'
        else:
            icar.core.database_operations.create_database(database_name)
            self.app.operation_result_message = 'Created database "{}"'.format(database_name)

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )
