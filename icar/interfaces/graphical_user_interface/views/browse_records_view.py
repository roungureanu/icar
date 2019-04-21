import tkinter as tk

import icar.helpers.constants
import icar.core.database_operations
import icar.core.table_operations
import icar.interfaces.graphical_user_interface.core.base_view as base_view
import icar.interfaces.graphical_user_interface.views.main_view


class BrowseRecordsView(base_view.BaseView):
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

        self.lines = self.table_operations.lines
        self.update_rows()

    def create_widgets(self):
        tk.Label(
            self,
            text='Viewing Table {}'.format(self.app.current_open_table)
        ).grid(row=0, column=0)
        tk.Button(
            self,
            text='Filter',
            command=self.filter_rows
        ).grid(row=0, column=1)
        tk.Button(
            self,
            text='Go Back',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        ).grid(row=0, column=2)

        self.operator_value = tk.StringVar(self, '')
        tk.OptionMenu(
            self, self.operator_value, *['AND', 'OR']
        ).grid(row=2, column=0)
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

        self.columns_to_select = tk.Listbox(self, selectmode='multiple')
        for i, column_name in enumerate(self.table_operations.columns):
            self.columns_to_select.insert(i + 1, column_name)
        self.columns_to_select.grid(row=3, column=0)

    def filter_rows(self):
        operators_map = {
            '==': 'eq',
            '!=': 'ne',
            '>=': 'ge',
            '>': 'gt',
            '<=': 'le',
            '<': 'lt'
        }

        self.records.destroy()

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

        columns = [self.columns_to_select.get(i) for i in self.columns_to_select.curselection()]
        if not columns:
            columns = ['*']
        self.lines = self.table_operations.select(filters, columns)

        print(self.lines)

        self.update_rows()

    def update_rows(self):
        self.records = tk.Frame(self)

        canvas = tk.Canvas(self.records)
        content_frame = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(self.records, orient="vertical", command=canvas.yview)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((100, 100), window=content_frame, anchor="nw")

        content_frame.bind(
            "<Configure>",
            lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        for i, item in enumerate(self.lines):
            for j, value in enumerate(item):
                tk.Entry(content_frame, textvariable=tk.StringVar(self, value)).grid(row=i, column=j)

        canvas.configure(yscrollcommand=scrollbar.set)
        self.records.grid(row=3, column=1, columnspan=2)
