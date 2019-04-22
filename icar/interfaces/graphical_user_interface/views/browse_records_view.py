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
        ).grid(row=0, column=1, sticky=tk.E + tk.W, columnspan=2)
        tk.Button(
            self,
            text='Go Back',
            command=lambda: self.app.replace_frame(
                icar.interfaces.graphical_user_interface.views.main_view.MainPage(self.app)
            )
        ).grid(row=0, column=3, sticky=tk.E + tk.W, columnspan=2)

        self.operator_value = tk.StringVar(self, 'AND')
        tk.OptionMenu(
            self, self.operator_value, *['AND', 'OR']
        ).grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        self.columns_to_select = tk.Listbox(
            self,
            selectmode='multiple',
            # background='green'
        )
        for i, column_name in enumerate(self.table_operations.columns):
            self.columns_to_select.insert(i + 1, column_name)
        self.columns_to_select.grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

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

        # TODO: Remove when this gets fixed :(
        # if filters['op_bool'] == 'AND':
        #     filters['op_bool'] = ''

        self.lines = self.table_operations.select(filters, columns)

        print(self.lines)

        self.update_rows()

    def update_rows(self):
        self.records = tk.Frame(self)

        canvas = tk.Canvas(
            self.records,
            # background='red'
        )
        content_frame = tk.Frame(self.records)
        yscrollbar = tk.Scrollbar(self.records, orient="vertical", command=canvas.yview)
        yscrollbar.pack(side="right", fill="y")
        xscrollbar = tk.Scrollbar(self.records, orient="horizontal", command=canvas.xview)
        xscrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        content_frame.bind(
            "<Configure>",
            lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        for i, column_name in enumerate(self.table_operations.columns.keys()):
            tk.Label(content_frame, text=column_name).grid(row=0, column=i, columnspan=1)

            filters = tk.Frame(content_frame)

            self.filters[column_name]['operator_field'] = tk.StringVar(filters, '')
            self.filters[column_name]['value_field'] = tk.StringVar(filters, '')

            tk.OptionMenu(
                filters,
                self.filters[column_name]['operator_field'],
                *['', '==', '!=', '>', '>=', '<', '<=']
            ).grid(row=0, column=0, sticky=tk.W + tk.E)
            tk.Entry(
                filters,
                textvariable=self.filters[column_name]['value_field']
            ).grid(row=0, column=1, sticky=tk.W + tk.E)

            filters.grid(row=1, column=i, sticky=tk.W + tk.E)

        for i, item in enumerate(self.lines):
            for j, value in enumerate(item):
                tk.Label(
                    content_frame,
                    text=value
                ).grid(row=i + 2, column=j, sticky=tk.N + tk.S + tk.E + tk.W, columnspan=1)

        canvas.configure(yscrollcommand=yscrollbar.set)
        canvas.configure(xscrollcommand=xscrollbar.set)
        self.records.grid(row=1, column=1, columnspan=4, rowspan=2)
