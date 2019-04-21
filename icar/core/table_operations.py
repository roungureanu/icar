import os
import operator

import icar.core.xml_parser
import icar.helpers.utils as utils
import icar.helpers.constants as constants
import icar.core.database_operations


class TableOps:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name

        self.database_file_path = os.path.join(constants.DATABASES_PATH, database_name.upper())
        self.table_file_path = os.path.join(self.database_file_path, '{}.csv'.format(table_name))
        self.table_metadata_file_path = os.path.join(self.database_file_path, '{}.metadata'.format(table_name))

        if self.check_db_params():
            self.preprocess()
        else:
            exit()
        
    def check_db_params(self):
        if not os.path.isdir(self.database_file_path):
            print("Error: The path for the database you indicated does not exist or is not a folder.")
            return False
        if not os.path.isfile(self.table_file_path):
            print("Error: The path for the table you indicated does not exist or is not a file.")
            return False
        if not os.path.isfile(self.table_metadata_file_path):
            print("Error: The path for the metadata file you indicated does not exist or is not a file.")
            return False
        return True
        
    def set_table(self, database, table, metadata):
        self.__init__(database, table)

    def preprocess(self):
        self.columns = {}
        self.lines = []
        self.metadata = {}
        no_cols = -1
        for line_no, line in enumerate(open(self.table_file_path, 'rt').readlines()):
            if line_no == 0:
                header = line.strip().split(',')
                no_cols = len(header)
                for i, name in enumerate(header):
                    self.columns[name] = i
                continue
            values = line.strip().split(',')
            if no_cols != len(values):
                print("Error: The table has inconsistent format.")
                return
            self.lines.append(values)
        for line_no, line in enumerate(open(self.table_metadata_file_path, 'rt').readlines()):
            values = line.strip().split(',')
            self.metadata[values[0]] = values[1:]
        if len(self.columns) != len(self.metadata):
            print("Error: The metadata file is not consistent with the table file.")
            return
        for name in self.metadata:
            if name not in self.columns:
                print("Error: The metadata file is not consistent with the table file.")

    def bool_op(self, line_value, th_value, operator, data_type):
        # check for invalid operator or datatype
        try:
            if data_type.upper() == 'NUMERIC':
                line_value = float(str(line_value))
                th_value = float(str(th_value))
            elif data_type.upper() == 'TEXT':
                line_value = str(line_value)
                th_value = str(str(th_value))
            elif data_type.upper() == 'BOOLEAN':
                line_value = bool(str(line_value))
                th_value = bool(str(th_value))
            else:
                print("Error: The datatype " + data_type + " is not supported by the database manager.")
                return False
        except:
            print("Error: The value " + th_value + " for the where clause should be of type " + data_type + '.')
            return False
        

        if operator.upper() == 'EQ':
            return line_value == th_value
        elif operator.upper() == 'LE':
            return line_value <= th_value
        elif operator.upper() == 'GE':
            return line_value >= th_value
        elif operator.upper() == 'LT':
            return line_value < th_value
        elif operator.upper() == 'GT':
            return line_value > th_value
        elif operator.upper() == 'NE':
            return line_value != th_value
        else:
            print('Error: Invalid operator ' + operator + '. The accepted operators are: eq, le, ge, lt, gt, ne.')
            exit()
                
    def apply_filter(self, result, fname, fvalue, operator, first):
        value = fvalue['value']
        try:
            if fname not in self.columns:
                raise Exception("The name " + fname + " is not a valid column name.")
            if operator.upper() == 'OR' or operator.upper() == '':
                for line in self.lines:
                    if self.bool_op(
                        line[self.columns[fname]],
                        value, fvalue['operator'],
                        self.metadata[fname][0]
                    ):
                        if result is None:
                            result = []
                        result.append(line)
            elif operator.upper() == 'AND':
                if result is None and not first:
                    return result
                if first:
                    for line in self.lines:
                        if self.bool_op(
                            line[self.columns[fname]],
                            value, fvalue['operator'],
                            self.metadata[fname][0]
                        ):
                                if result is None:
                                    result = []
                                result.append(line)
                else:
                    elim = []
                    for i, line in enumerate(result):
                        if not self.bool_op(
                            line[self.columns[fname]],
                            value, fvalue['operator'],
                            self.metadata[fname][0]
                        ):
                                elim.append(i)
                    for line_no in elim:
                        del result[line_no]
            else:
                raise Exception("Wrong value for the operator between the clauses of where.")
        except Exception as error:
                print('Error: ' + repr(error))
        return result
   
    def where(self, filters, operation):
        result = []
        first = True
        if 'op_bool' not in filters:
            print(
                'Error: The operator op_bool is missing from the filters dictionary. '
                'If there is just one operation, make it an empty string.'
            )
            return
        for fname, fvalue in filters.items():
            if fname.upper() != 'OP_BOOL':
                result = self.apply_filter(
                    result, fname, fvalue, filters['op_bool'], first
                )
            first = False
        if operation.upper() == 'SELECT':
            self.result = result
            return result
        if operation.upper() == 'DELETE':
            for line in result:
                line_no = self.is_line(line, self.lines)
                if line_no > -1:
                    del self.lines[line_no]
        
    def is_valid(self, val, col):
        md = self.metadata[col]
        try:
            if md[0].upper() == 'NUMERIC':
                line_value = float(str(val))
            elif md[0].upper() == 'TEXT':
                line_value = str(val)
            elif md[0].upper() == 'BOOLEAN':
                line_value = bool(str(val))
            else:
                print("Error: The data type" + md[0] + " is not supported by the database manager.")
                return False
        except:
            print("Error: The value for the column " + col + " should be of type " + md[0] + '.')
            return False
            
        if len(md) > 1 and int(md[1]) > 0:
            if len(val) > int(md[1]):
                print("Error: The value for the column " + col + " sould have the length " + str(md[1]) + '.')
                return False
        return True
                    
    def is_line(self, line, matrix):
        index = -1
        if len(matrix[0]) != len(line):
            return index
        for i, m_line in enumerate(matrix):
            is_line = True
            for e1, e2 in zip(m_line, line):
                if e1 != e2:
                    is_line = False
                    break
            if is_line:
                return i
        return -1
        
    def filter_columns(self, cols, vals=None):
        if self.result is None:
            return None
        if len(cols) == 1 and cols[0] == '*' and vals is None:
            return self.result
        new_result = []
        for line in self.result:
            if vals is None:
                new_result.append([line[self.columns[i]] for i in cols])
            else:
                if cols[0] == '*':
                    cols = self.columns.keys()
                line_no = self.is_line(line, self.lines)
                if line_no > -1:
                    for val, col in zip(vals, cols):
                        if self.is_valid(val, col):
                            self.lines[line_no][self.columns[col]] = val
                        else:
                            return None
        self.result = new_result    
        return new_result
    
    # performs a select operation
    # @param filters = a dictionary with the params used for where
    # @param cols = an array with the columns written after select in the statement
    # @return result = list of lists, the results of the select(the indicated lines and columns)
    def select(self, filters, cols):
        self.where(filters, 'select')
        self.filter_columns(cols)
        return self.result
        
    # performs a delete operation
    # @param filters  = a dict with the params used for where
    # @return lines = list of lists, the data of the table after the indicated lines were deleted
    def delete(self, filters):
        self.where(filters, 'delete')
        self.commit()
        return self.lines
        
    # performs an insert operation
    # @param cols = an array with the column names where values will be inserted, can be ['*']
    # @param vals = an array with the corresponding values
    # @return lines = list of lists, the data of the table after the new values were inserted
    def insert(self, cols, vals):
        if cols[0] == '*':
            self.lines.append(vals)
            self.commit()
            return self.lines
        new_line = [None for _ in range(len(self.columns))]
        for val, col in zip(vals, cols):
            if self.is_valid(val, col):
                new_line[self.columns[col]] = val
            else:
                print(val, col)
                return None
        self.lines.append(new_line)
        self.commit()
        return self.lines
        
    # performs a select operation
    # @param filters = a dictionary with the params used for where
    # @param cols = an array with the columns written after select in the statement
    # @return lines = list of lists, the data of the table after the indicated entries were updated
    def update(self, filters, cols, vals):
        self.where(filters, 'select')
        self.filter_columns(cols, vals)
        self.commit()
        return self.lines
        
    # writes the data in memory to the table(overwrites it)
    def commit(self):
        f = open(self.table_file_path, 'wt')
        sorted_names = sorted(self.columns.items(), key=operator.itemgetter(1))
        sorted_names = [name for (name, _) in sorted_names]
        line1 = ''.join(name + ',' for name in sorted_names)
        f.write(line1[:-1] + '\n')
        for line in self.lines:
            line1 = ''.join(str(value) + ',' for value in line)
            f.write(line1[:-1] + '\n')
        f.close()

    def export(self, destination_path):
        metadata_node = icar.core.xml_parser.Node(
            'table_metadata',
            [
                icar.core.xml_parser.Node(
                    'column',
                    [
                        icar.core.xml_parser.Node(
                            'name',
                            [icar.core.xml_parser.TextNode(column_name)]
                        ),
                        icar.core.xml_parser.Node(
                            'type',
                            [icar.core.xml_parser.TextNode(column_type)]
                        ),
                        icar.core.xml_parser.Node(
                            'size',
                            [icar.core.xml_parser.TextNode(column_size)]
                        ),
                    ]
                )
                for column_name, (column_type, column_size) in self.metadata.items()
            ]
        )
        content_node = icar.core.xml_parser.Node(
            'table_entries',
            [
                icar.core.xml_parser.Node(
                    'entry',
                    [
                        icar.core.xml_parser.Node(
                            'value',
                            [icar.core.xml_parser.TextNode(value)]
                        )
                        for value in entry
                    ]
                )
                for entry in self.lines
            ]
        )

        tree = icar.core.xml_parser.Node(
            'root',
            [
                metadata_node,
                content_node
            ]
        )

        with open(destination_path, 'w') as handle:
            handle.write(tree.dumps())

    def validate_import_xml(self, tree: icar.core.xml_parser.Node):
        if len(tree.children) != 2:
            raise Exception('Tree has more than 2 nodes')

        metadata_node, entries_node = tree.children

        if metadata_node.element != 'table_metadata':
            raise Exception('First node is not a table_metadata node.')

        if entries_node.element != 'table_entries':
            raise Exception('Second node is not a table_entries node.')

        table_metadata = [
            {
                node.element: node.children[0].text
                for node in column_node.children
            }
            for column_node in metadata_node.children
        ]

        for entry in table_metadata:
            if {'name', 'type', 'size'}.difference(entry):
                raise Exception('Column entries have missing fields. Required fields are: name, type and size.')

    def import_(self, source_path):
        parser = icar.core.xml_parser.Parser(source_path)
        tree = parser.tree

        self.validate_import_xml(tree)
        metadata_node, entries_node = tree.children

        table_metadata = [
            {
                node.element: node.children[0].text
                for node in column_node.children
            }
            for column_node in metadata_node.children
        ]

        column_names = []
        column_types = []
        column_sizes = []

        for column in table_metadata:
            column_names.append(column['name'])
            column_types.append(column['type'])
            column_sizes.append(column['size'])

        entries = [
            [
                value_node.children[0]
                for value_node in entry_node.children
            ]
            for entry_node in entries_node.children
        ]

        entries_length = {len(entry) for entry in entries}
        if len(entries_length) != 1:
            raise Exception('There are entries with missing values..')

        entry_length = list(entries_length)[0]

        if len(table_metadata) != entry_length:
            raise Exception('The number of values of the entries does not match the number of columns')

        if len(set(column_names)) != len(column_names):
            raise Exception('There are duplicate columns.')

        if set(column_types).difference(icar.helpers.constants.VALID_COLUMN_TYPES.keys()):
            raise Exception('Columns have invalid types.')

        icar.core.database_operations.delete_table(self.database_name, self.table_name)
        icar.core.database_operations.create_table(
            self.database_name,
            self.table_name,
            column_names,
            column_types,
            column_sizes
        )
        self.preprocess()
        for entry in entries:
            self.insert(['*'], entry)


if __name__ == "__main__":
    filters = {
        'NAME': {
            'operator': 'eq',
            'value': 'robert'
        },
        'op_bool': ''
    }
    cols = ['NAME']
    # cols = ['scoici', 'raci']
    vals = [2, 4, 3, 6]

    export_path = os.path.join(
        constants.RESOURCES_FOLDER_PATH, 'export.xml'
    )

    table_ops = TableOps('TEST', 'PERSON')
    # table_ops.export(export_path)
    # table_ops.import_(export_path)
    # print(table_ops.lines)
    # print('')
    # print('select * where melci=1')
    try:
        res = table_ops.select(filters, cols)
        print(res)
    except Exception as exc:
        print('!!!', utils.get_traceback(exc))
    # print('')

    # filters = {'scoici': {'operator': 'gt',
    #                          'value': 5},
    #                'op_bool': ''}
    # print(table_ops.lines)
    # print('')
    # print('delete where scoici>5')
    # print(table_ops.delete(filters))
    # print('')
    #
    # print(table_ops.lines)
    # print('')
    # print('insert (2, 4, 3, 6)')
    # print(table_ops.insert(cols, vals))
    # print('')

    # filters = {'melci': {'operator': 'eq',
    #                          'value': 1},
    #                'op_bool': ''}
    # print(table_ops.lines)
    # print('')
    # print('update * where melci=1 newvalues (2, 4, 3, 6)')
    # print(table_ops.update(filters, cols, vals))
    # print('')
