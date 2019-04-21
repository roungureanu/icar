import tkinter as tk
import tkinter.ttk as ttk

import icar.core.database_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.create_database_view as create_database_view
import icar.interfaces.graphical_user_interface.views.delete_database_view as delete_database_view
import icar.interfaces.graphical_user_interface.views.create_table_view as create_table_view
import icar.interfaces.graphical_user_interface.views.delete_table_view as delete_table_view
import icar.interfaces.graphical_user_interface.views.insert_record_view as insert_record_view
import icar.interfaces.graphical_user_interface.views.browse_records_view as browse_records_view
import icar.interfaces.graphical_user_interface.views.delete_records_view as delete_records_view
import icar.interfaces.graphical_user_interface.views.update_records_view as update_records_view
import icar.interfaces.graphical_user_interface.views.export_table_view as export_table_view
import icar.interfaces.graphical_user_interface.views.import_table_view as import_table_view
import icar.interfaces.graphical_user_interface.views.add_column_view as add_column_view
import icar.interfaces.graphical_user_interface.views.remove_column_view as remove_column_view


class _Menu(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.create_widgets()

    def update_current_open_database(self, *args):
        self.app.current_open_database = self.current_database_to_open.get()
        self.app.replace_frame(MainPage(self.app))

    def update_current_open_table(self, *args):
        self.app.current_open_table = self.current_table_to_open.get()
        self.app.replace_frame(MainPage(self.app))

    def create_widgets(self):
        self.create_database = tk.Button(
            self,
            text='Create Database',
            command=lambda: self.app.replace_frame(create_database_view.CreateDatabasePage(self.app))
        )
        self.create_database.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.current_database_to_open = tk.StringVar(self, value='Open Database')
        self.current_database_to_open.trace(
            'w',
            self.update_current_open_database
        )

        available_databases = icar.core.database_operations.list_databases()
        if available_databases:
            self.open_database = tk.OptionMenu(self, self.current_database_to_open, *available_databases)
            self.open_database.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

            self.delete_database = tk.Button(
                self,
                text='Delete Database',
                command=lambda: self.app.replace_frame(delete_database_view.DeleteDatabasePage(self.app))
            )
            self.delete_database.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

        if self.app.current_open_database:
            available_tables = icar.core.database_operations.list_tables(self.app.current_open_database)

            self.current_table_to_open = tk.StringVar(self, value='Open Table')
            self.current_table_to_open.trace(
                'w',
                self.update_current_open_table
            )

            self.create_table = tk.Button(
                self,
                text='Create Table',
                command=lambda: self.app.replace_frame(create_table_view.CreateTableView(self.app))
            )
            self.create_table.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

            if available_tables:
                self.open_table = tk.OptionMenu(self, self.current_table_to_open, *available_tables)
                self.open_table.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

            if available_tables:
                self.delete_table = tk.Button(
                    self,
                    text='Delete Table',
                    command=lambda: self.app.replace_frame(delete_table_view.DeleteTablePage(self.app))
                )
                self.delete_table.grid(row=1, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

                # self.rename_table = tk.Button(
                #     self,
                #     text='Rename Table',
                #     command=lambda: None
                # )
                # self.rename_table.grid(row=0, column=5)

            if self.app.current_open_table:
                self.table_operation_menu_variable = tk.StringVar(self, 'Table Manipulation')
                self.table_operation_menu_variable.trace(
                    'w',
                    self.table_operation_menu_callback
                )
                self.table_operations_menu = tk.OptionMenu(
                    self,
                    self.table_operation_menu_variable,
                    *[
                        'Insert Record',
                        'Browse Records',
                        'Delete Records',
                        'Update Records',
                        'Add Column',
                        'Remove Column',
                        'Export',
                        'Import'
                    ]
                )
                self.table_operations_menu.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W, columnspan=3)

    def table_operation_menu_callback(self, *args):
        option_picked = self.table_operation_menu_variable.get()
        if option_picked == 'Insert Record':
            self.app.replace_frame(insert_record_view.InsertRecordView(self.app))
        elif option_picked == 'Browse Records':
            self.app.replace_frame(browse_records_view.BrowseRecordsView(self.app))
        elif option_picked == 'Delete Records':
            self.app.replace_frame(delete_records_view.DeleteRecordsView(self.app))
        elif option_picked == 'Update Records':
            self.app.replace_frame(update_records_view.UpdateRecordsView(self.app))
        elif option_picked == 'Add Column':
            self.app.replace_frame(add_column_view.AddColumnView(self.app))
        elif option_picked == 'Remove Column':
            self.app.replace_frame(remove_column_view.RemoveColumnView(self.app))
        elif option_picked == 'Export':
            self.app.replace_frame(export_table_view.ExportTableView(self.app))
        elif option_picked == 'Import':
            self.app.replace_frame(import_table_view.ImportTableView(self.app))


class _OperationResultMessage(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)

        self.app = app

        self.create_widgets()

    def create_widgets(self):
        if self.app.operation_result_message:
            tk.Label(
                self,
                text=self.app.operation_result_message
            ).pack()


class _CurrentOpenDatabase(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.create_widgets()

    def create_widgets(self):
        if self.app.current_open_database:
            message = 'Currently using database: {}'.format(self.app.current_open_database)
        else:
            message = 'Not using any database.'

        tk.Label(
            self,
            text=message
        ).grid(row=0, column=0)


class _CurrentOpenTable(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.create_widgets()

    def create_widgets(self):
        if self.app.current_open_table:
            message = 'Currently open table: {}'.format(self.app.current_open_table)
        else:
            message = 'Not using any table.'

        tk.Label(
            self,
            text=message
        ).grid(row=0, column=0)


class MainPage(base_view.BaseView):
    def create_widgets(self):
        self.winfo_toplevel().title('Databases Browser')

        _Menu(self, self.app).grid(row=0, column=0, sticky=tk.W + tk.E)
        _OperationResultMessage(self, self.app).grid(row=1, column=0, sticky=tk.W)
        _CurrentOpenDatabase(self, self.app).grid(row=2, column=0, sticky=tk.W + tk.E)
        _CurrentOpenTable(self, self.app).grid(row=3, column=0, sticky=tk.W)
