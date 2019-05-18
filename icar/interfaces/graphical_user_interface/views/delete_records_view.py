import tkinter as tk

import icar.helpers.constants
import icar.core.database_operations
import icar.core.table_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class DeleteRecordsView(base_view.BaseView):
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

        super().__init__(app)

    def create_widgets(self):
        tk.Label(
            self,
            text='DELETING From Table {}'.format(self.app.current_open_table)
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text='Delete',
            command=self.delete_records
        ).grid(row=0, column=1, sticky=tk.E + tk.W)
        tk.Button(
            self,
            text='Go Back',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        ).grid(row=0, column=2, sticky=tk.E + tk.W)

        self.operator_value = tk.StringVar(self, 'AND')
        tk.OptionMenu(
            self, self.operator_value, *['AND', 'OR']
        ).grid(row=2, column=0, sticky=tk.E + tk.W)
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

    def delete_records(self):
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
        assert isinstance(filters['op_bool'], str)
        for column in self.filters:
            operator = self.filters[column]['operator_field'].get()
            value = self.filters[column]['value_field'].get()
            assert operator in list(operators_map.keys()) + ['']
            assert isinstance(value, str)

            if operator in operators_map and value:
                filters[column] = {
                    'operator': operators_map[operator],
                    'value': value
                }

        self.table_operations.delete(filters)

        self.app.replace_frame(
            icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
        )
