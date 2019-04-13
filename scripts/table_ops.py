import os
import operator

class TableOps:
    def __init__(self, database, table, metadata):
        self.database = database
        self.table = table
        self.metadata_file = metadata
        self.preprocess()
        
        # set table
        # comment functions

    def preprocess(self):
        tb_path = os.path.join(self.database, self.table)
        md_path = os.path.join(self.database, self.metadata_file)
        self.columns = {}
        self.lines = []
        self.metadata = {}
        for line_no, line in enumerate(open(tb_path, 'rt').readlines()):
            if line_no == 0:
                header = line.strip().split(',')
                for i, name in enumerate(header):
                    self.columns[name] = i
                continue
            values = line.strip().split(',')
            self.lines.append(values)
        for line_no, line in enumerate(open(md_path, 'rt').readlines()):
            values = line.strip().split(',')
            self.metadata[values[0]] = values[1:]
            
    def bool_op(self, line_value, th_value, operator, data_type):
        line_value = eval(data_type + "(" + str(line_value) + ")")
        th_value = eval(data_type + "(" + str(th_value) + ")")
        if operator == 'eq':
            return line_value == th_value
        if operator == 'le':
            return line_value <= th_value
        if operator == 'ge':
            return line_value >= th_value
        if operator == 'lt':
            return line_value < th_value
        if operator == 'gt':
            return line_value > th_value
        if operator == 'ne':
            return line_value != th_value
                
    def apply_filter(self, result, fname, fvalue, operator, first):
        value = fvalue['value']            
        if operator == 'or' or operator == '':
            for line in self.lines:
                if self.bool_op(line[self.columns[fname]],
                                     value, fvalue['operator'],
                                     self.metadata[fname][0]):
                        if result is None:
                            result = []
                        result.append(line)
        if operator == 'and':
            if result is None and not first:
                return result
            if first:
                for line in self.lines:
                    if self.bool_op(line[self.columns[fname]],
                                     value, fvalue['operator'],
                                     self.metadata[fname][0]):
                            if result is None:
                                result = []
                            result.append(line)
            else:
                elim = []
                for i, line in enumerate(result):
                    if not self.bool_op(line[self.columns[fname]],
                                     value, fvalue['operator'],
                                     self.metadata[fname][0]):
                            elim.append(i)
                for line_no in elim:
                    del result[line_no]
        return result
   
    def where(self, filters, operation):
        result = []
        first = True
        for fname, fvalue in filters.items():
            if fname != 'op_bool':
                result = self.apply_filter(result, fname, fvalue,
                                                   filters['op_bool'], first)
            first = False
        if operation == 'select':
            self.result = result
            return result
        if operation == 'delete':
            for line in result:
                line_no = self.is_line(line, self.lines)
                if line_no > -1:
                    del self.lines[line_no]
                    
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
        if len(cols) == 1 and cols[0] == '*' and vals == None:
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
                        self.lines[line_no][self.columns[col]] = val
        self.result = new_result    
        return new_result
        
    def select(self, filters, cols):
        self.where(filters, 'select')
        self.filter_columns(cols)
        return self.result
        
    def delete(self, filters):
        self.where(filters, 'delete')
        return self.lines
        
    def insert(self, cols, vals):
        if cols[0] == '*':
            self.lines.append(vals)
            return
        new_line = [None for _ in range(len(self.columns))]
        for val, col in zip(vals, cols):
            new_line[self.columns[col]] = val
        self.lines.append(new_line)
        
    def update(self, filters, cols, vals):
        self.where(filters, 'select')
        self.filter_columns(cols, vals)
        return self.lines
        
    def commit(self):
        tb_path = os.path.join(self.database, self.table)
        f = open(tb_path, 'wt')
        sorted_names = sorted(self.columns.items(), key=operator.itemgetter(1))
        sorted_names = [name for (name, _) in sorted_names]
        line1 = ''.join(name + ',' for name in sorted_names)
        f.write(line1[:-1] + '\n')
        for line in self.lines:
            line1 = ''.join(str(value) + ',' for value in line)
            f.write(line1[:-1] + '\n')
        f.close()
             

filters = {'melci': {'operator': 'eq',
                         'value': 1},
               'op_bool': ''}  
cols = ['melci']
vals = ['9']

table_ops = TableOps('.', 'tb1.txt', 'tb1.metadata')
table_ops.delete(filters)
print(table_ops.lines)
table_ops.commit()