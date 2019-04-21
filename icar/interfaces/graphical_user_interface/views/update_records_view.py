import tkinter as tk

import icar.helpers.constants
import icar.core.database_operations
import icar.core.table_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class UpdateRecordsView(base_view.BaseView):
    def __init__(self, app):
        self.table_operations = icar.core.table_operations.TableOps(
            app.current_open_database,
            app.current_open_table
        )
        self.filters = {
            column_name: {
                'operator_field': None,
                'value_field': None
            }
            for column_name in self.table_operations.columns
        }

        self.new_values = {
            column_name: None
            for column_name in self.table_operations.columns
        }

        super().__init__(app)

    def create_widgets(self):
        tk.Label(
            self,
            text='Updating Table {}'.format(self.app.current_open_table)
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text='Update',
            command=self.update_records
        ).grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        tk.Button(
            self,
            text='Go Back',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        ).grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

        self.operator_value = tk.StringVar(self, 'AND')
        tk.OptionMenu(
            self, self.operator_value, *['AND', 'OR']
        ).grid(row=2, column=0, sticky=tk.W + tk.E)
        for i, column_name in enumerate(self.table_operations.columns.keys()):
            tk.Label(self, text=column_name).grid(row=1, column=i + 1)

            filters = tk.Frame(self)

            self.filters[column_name]['operator_field'] = tk.StringVar(filters, '')
            self.filters[column_name]['value_field'] = tk.StringVar(filters, '')

            tk.OptionMenu(
                filters,
                self.filters[column_name]['operator_field'],
                *['', '==', '!=', '>', '>=', '<', '<=']
            ).grid(row=0, column=0)
            tk.Entry(
                filters,
                textvariable=self.filters[column_name]['value_field']
            ).grid(row=0, column=1)

            filters.grid(row=2, column=i + 1)

        tk.Label(self, text='New Values').grid(row=4, column=0)
        for i, column_name in enumerate(self.table_operations.columns.keys()):
            tk.Label(
                self, text=column_name
            ).grid(row=3, column=i + 1, sticky=tk.W + tk.E)
            self.new_values[column_name] = tk.StringVar(self, '')
            tk.Entry(
                self, textvariable=self.new_values[column_name]
            ).grid(row=4, column=i + 1, sticky=tk.W + tk.E, columnspan=2)

    def update_records(self):
        operators_map = {
            '==': 'eq',
            '!=': 'ne',
            '>=': 'ge',
            '>': 'gt',
            '<=': 'le',
            '<': 'lt'
        }

        filters = {
            'op_bool': self.operator_value.get()
        }
        for column in self.filters:
            operator = self.filters[column]['operator_field'].get()
            value = self.filters[column]['value_field'].get()

            if operator in operators_map and value:
                filters[column] = {
                    'operator': operators_map[operator],
                    'value': value
                }

        columns = []
        values = []

        for column in self.new_values:
            value = self.new_values[column].get()
            if value:
                columns.append(column)
                values.append(value)

        if columns:
            self.table_operations.update(filters, columns, values)

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )
