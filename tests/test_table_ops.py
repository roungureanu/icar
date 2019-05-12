import unittest
import sys
sys.path.append('C:\\uni\\CSS\\icar')
from icar.core.table_operations import TableOps


class TestTableOps(unittest.TestCase):

    
    def test_check_db_params0(self):
    
        table_ops = TableOps('', '')
        self.assertEqual(table_ops.check_db_params(), False)
        

    def test_check_db_params1(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.check_db_params(), True)
        

    def test_check_db_params2(self):
        table_ops = TableOps('Friends', 'Enemies')
        self.assertEqual(table_ops.check_db_params(), False)
        

    def test_check_db_params3(self):
        table_ops = TableOps('enemies', 'Dogs')
        self.assertEqual(table_ops.check_db_params(), False)
        

    def test_check_db_params3(self):
        table_ops = TableOps('friends', 'Dogs')
        table_ops.table_metadata_file_path = ""
        self.assertEqual(table_ops.check_db_params(), False)
        

    def test_check_db_params4(self):
        table_ops = TableOps('friendsss', 'Dogs')
        self.assertEqual(table_ops.check_db_params(), False)
        
    def test_set_table0(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.set_table("PEOPLE", "person")
        self.assertEqual(table_ops.database_name, "PEOPLE")
        
    def test_set_table1(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.set_table("PEOPLE", "person")
        self.assertEqual(table_ops.table_name, "person")
        
    def test_set_table2(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.set_table("PEOPE", "persona")
        self.assertEqual(table_ops.table_name, "person")
        
    def test_set_table3(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.set_table("PEOPE", "persona")
        self.assertEqual(table_ops.database_name, "PEOPLE")
        
    def test_preprocess0(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(len(table_ops.metadata), len(table_ops.columns))
        
    def test_preprocess1(self): 
        table_ops = TableOps('Friends', 'Dogs')       
        columns = {'NAME':0,'AGE':1,'WEIGHT':2,'COLOUR':3}
        self.assertEqual(columns, table_ops.columns)
        
    def test_preprocess2(self): 
        table_ops = TableOps('Friends', 'Dogs') 
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        self.assertEqual(lines, table_ops.lines)
        
    def test_preprocess3(self): 
        table_ops = TableOps('Friends', 'Dogs') 
        metadata = {'NAME':["TEXT", '20'],
                    'AGE':["NUMERIC", '10'],
                    'WEIGHT':["NUMERIC", '0'],
                    'COLOUR':["TEXT", '0'],}
        self.assertEqual(metadata, table_ops.metadata)
        
    def test_preprocess4(self): 
        table_ops = TableOps('Friends', 'Dogs') 
        metadata = {'NAME':["TEXT", '20'],
                    'AGE':["NUMERIC", '10'],
                    'WEIGHT':["NUMERIC", '0'],
                    'COLOUR':["TEXT", '0'],}
        table_ops.table_metadata_file_path = "C:\\uni\\CSS\\icar\\databases\\PEOPLE\\PERSON.metadata"
        table_ops.preprocess()
        self.assertNotEqual(table_ops.metadata, metadata)
        
    def test_bool_op0(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op(1, 2, 'eq', 'numeric'), False)
        
    def test_bool_op1(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op('mama', 'mom', 'leq', 'TEXT'), False)
        
    def test_bool_op2(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op('mama', 'mom', 'le', 'TEXT'), True)
        
    def test_bool_op3(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op(1, 1, 'eq', 'text'), True)
        
    def test_bool_op4(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op('too', 'moo', 'eq', 'numeric'), False)
        
    def test_bool_op5(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op(1, 1, 'eq', 'none'), False)
        
    def test_bool_op6(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op(1, 2, 'eq', 'boolean'), True)
        
    def test_bool_op7(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op(1, 2, 'lt', 'numeric'), True)
        
    def test_bool_op8(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op(1, 2, 'gt', 'numeric'), False)
        
    def test_bool_op9(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op(1, 2, 'ne', 'numeric'), True)
        
    def test_bool_op10(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op(1, 2, 'ge', 'numeric'), False)
        
    def test_apply_filter0(self):
        table_ops = TableOps('Friends', 'Dogs')
        result = [['azorel','12','10','white'],]
        fvalue = {'value':'12', 'operator':'eq'}
        self.assertEqual(table_ops.apply_filter(None, 'AGE', fvalue,'and', True), result)
        
    def test_apply_filter1(self):
        table_ops = TableOps('Friends', 'Dogs')
        result = [['azorel','12','10','white'],]
        fvalue = {'value':'12', 'operator':'eq'}
        self.assertEqual(table_ops.apply_filter(None, 'AGE', fvalue,'or', True), result)
        
    def test_apply_filter2(self):
        table_ops = TableOps('Friends', 'Dogs')
        fvalue = {'value':'12', 'operator':'eq'}
        self.assertEqual(table_ops.apply_filter(None, 'ham', fvalue,'and', True), None)
        
    def test_apply_filter3(self):
        table_ops = TableOps('Friends', 'Dogs')
        fvalue = {'value':12, 'operator':'le'}
        self.assertEqual(table_ops.apply_filter(None, 'ham', fvalue,'or', True), None)
        
    def test_apply_filter4(self):
        table_ops = TableOps('Friends', 'Dogs')
        fvalue = {'value':12, 'operator':'le'}
        self.assertEqual(table_ops.apply_filter(None, 'NAME', fvalue,'le', True), None)
        
    def test_apply_filter5(self):
        table_ops = TableOps('Friends', 'Dogs')
        fvalue = {'value':0, 'operator':'eq'}
        self.assertEqual(table_ops.apply_filter(None, 'AGE', fvalue,'and', True), None)
        
    def test_apply_filter6(self):
        table_ops = TableOps('Friends', 'Dogs')
        fvalue = {'value':0, 'operator':'eq'}
        self.assertEqual(table_ops.apply_filter(None, 'AGE', fvalue,'and', False), None)
        
    def test_where0(self):
        table_ops = TableOps('Friends', 'Dogs')
        result = [['azorel','12','10','white'],]
        
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'azorel'
            },
            'AGE': {
                'operator': 'eq',
                'value': '12'
            },
            'op_bool': 'AND'
        }
        table_ops.where(filters, 'select')
        self.assertEqual(table_ops.result, result)
        
    def test_where1(self):
        table_ops = TableOps('Friends', 'Dogs')
        result = [['azorel','12','10','white'],]
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'azorel'
            },
            'AGE': {
                'operator': 'eq',
                'value': '200'
            },
            'op_bool': 'or'
        }
        table_ops.where(filters, 'select')
        self.assertEqual(table_ops.result, result)
        
    def test_where2(self):
        table_ops = TableOps('Friends', 'Dogs')
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'azorel'
            },
            'AGE': {
                'operator': 'eq',
                'value': '3'
            },
            'op_bool': 'AND'
        }
        table_ops.where(filters, 'select')
        self.assertEqual(table_ops.result, [])
        
    def test_where3(self):
        table_ops = TableOps('Friends', 'Dogs')
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'saraf'
            },
            'AGE': {
                'operator': 'eq',
                'value': '300'
            },
            'op_bool': 'OR'
        }
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops.where(filters, 'delete')
        self.assertEqual(table_ops.lines, lines)
        
    def test_where4(self):
        table_ops = TableOps('Friends', 'Dogs')
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'sara'
            },
            'AGE': {
                'operator': 'eq',
                'value': '3'
            },
            'op_bool': 'OR'
        }
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops.where(filters, 'delete')
        self.assertEqual(table_ops.lines, lines[:2])
        
    def test_where5(self):
        table_ops = TableOps('Friends', 'Dogs')
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'sara'
            },
            'AGE': {
                'operator': 'eq',
                'value': '3'
            },
            'op_bool': 'BLA'
        }
        table_ops.where(filters, 'select')
        self.assertEqual(table_ops.result, [])
        
    def test_where6(self):
        table_ops = TableOps('Friends', 'Dogs')
        filters = {
            'NAME': {
                'operator': 'nla',
                'value': 'sara'
            },
            'AGE': {
                'operator': 'eq',
                'value': '3'
            },
            'op_bool': 'or'
        }
        table_ops.where(filters, 'select')
        self.assertEqual(table_ops.result, [])
        
    def test_where7(self):
        table_ops = TableOps('Friends', 'Dogs')
        filters = {
            'NAME': {
                'operator': 'nla',
                'value': 'sara'
            },
            'AGE': {
                'operator': 'eq',
                'value': '3'
            },
        }
        table_ops.where(filters, 'select')
        self.assertEqual(table_ops.result, None)
        
    def test_is_valid0(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.is_valid('mom', 'AGE'), False)
        
    def test_is_valid1(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.is_valid('15', 'AGE'), True)
        
    def test_is_valid2(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.is_valid('ana', 'NAME'), True)
        
    def test_is_valid3(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.is_valid('mom', ''), False)
        
    def test_is_valid4(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.is_valid('1587395934754376876', 'AGE'), False)
        
    def test_is_valid5(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.metadata = {'NAME':["TEXT", '20'],
                    'AGE':["BLA", '10'],
                    'WEIGHT':["NUMERIC", '0'],
                    'COLOUR':["TEXT", '0'],}
        self.assertEqual(table_ops.is_valid('1587395934754376876', 'AGE'), False)
        
    def test_is_valid6(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.metadata = {'NAME':["TEXT", '20'],
                    'AGE':["BOOLEAN", '10'],
                    'WEIGHT':["NUMERIC", '0'],
                    'COLOUR':["TEXT", '0'],}
        self.assertEqual(table_ops.is_valid('1587395934754376876', 'AGE'), False)
        
    def test_is_line0(self):
        table_ops = TableOps('Friends', 'Dogs')
        matrix = [[1, 2], [2, 3], [3, 4]]
        line = [1, 2]
        self.assertEqual(table_ops.is_line(line, matrix), 0)
        
    def test_is_line1(self):
        table_ops = TableOps('Friends', 'Dogs')
        matrix = [[1, 2], [2, 3], [3, 4]]
        line = [1, 3]
        self.assertEqual(table_ops.is_line(line, matrix), -1)
        
    def test_is_line2(self):
        table_ops = TableOps('Friends', 'Dogs')
        matrix = [[1, 2], [2, 3], [3, 4]]
        line = "money"
        self.assertEqual(table_ops.is_line(line, matrix), -1)
        
    def test_is_line3(self):
        table_ops = TableOps('Friends', 'Dogs')
        matrix = [[1, 2], [2, 3], [3, 4]]
        line = None
        self.assertEqual(table_ops.is_line(line, matrix), -1)
        
    def test_is_line4(self):
        table_ops = TableOps('Friends', 'Dogs')
        matrix = [[1, 2], [2, 3], [3, 4]]
        line = [2, 1]
        self.assertEqual(table_ops.is_line(line, matrix), -1)
        
    def test_is_line5(self):
        table_ops = TableOps('Friends', 'Dogs')
        matrix = [[1, 2], [2, 3], [3, 4]]
        line = [1, 2, 3]
        self.assertEqual(table_ops.is_line(line, matrix), -1)
        
    def test_filter_columns0(self):
        table_ops = TableOps('Friends', 'Dogs')
        cols = ['*']
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops.result = lines
        self.assertEqual(table_ops.filter_columns(cols), lines)
        
    def test_filter_columns1(self):
        table_ops = TableOps('Friends', 'Dogs')
        cols = ['NAME', 'AGE']
        lines = [['azorel','12'],
                ['maia','15'],
                ['sara','2']]
        table_ops.result = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        self.assertEqual(table_ops.filter_columns(cols), lines)
        
    def test_filter_columns2(self):
        table_ops = TableOps('Friends', 'Dogs')
        cols = '*'
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops.result = lines
        self.assertEqual(table_ops.filter_columns(cols), lines)
        
    def test_filter_columns3(self):
        table_ops = TableOps('Friends', 'Dogs')
        cols = ['NAME']
        lines = [['azorel'],
                ['maia'],
                ['sara']]
        table_ops.result = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        self.assertEqual(table_ops.filter_columns(cols), lines)
        
    def test_filter_columns4(self):
        table_ops = TableOps('Friends', 'Dogs')
        cols = ['us']
        table_ops.result = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        self.assertEqual(table_ops.filter_columns(cols), None)
        
    def test_select0(self):
        table_ops = TableOps('Friends', 'Dogs')
        result = [['azorel','12','10','white'],]
        
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'azorel'
            },
            'AGE': {
                'operator': 'eq',
                'value': '12'
            },
            'op_bool': 'AND'}
        self.assertEqual(table_ops.select(filters, '*'), result)
        
    def test_select1(self):
        table_ops = TableOps('Friends', 'Dogs')
        result = [['azorel','12','10','white']]
        
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'azorel'
            },
            'bool_op' : ""}
        self.assertEqual(table_ops.select(filters, '*'), result)
        
    def test_delete(self):
        table_ops = TableOps('Friends', 'Dogs')
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'azorel'
            },
            'AGE': {
                'operator': 'eq',
                'value': '12'
            },
            'op_bool': 'AND'}
        lines = [['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops.delete(filters)
        self.assertEqual(table_ops.delete(filters), lines)
        
    def test_insert0(self):
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown'],
                ['zuzu','1',None,None]]
        table_ops = TableOps('Friends', 'Dogs')
        cols = ['NAME', 'AGE']
        vals = ['zuzu', '1']
        table_ops.insert(cols, vals)
        self.assertEqual(table_ops.lines, lines)
        
    def test_insert1(self):
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown'],
                ['zuzu','1','2','3']]
        table_ops = TableOps('Friends', 'Dogs')
        cols = ['*']
        vals = ['zuzu', '1', '2', '3']
        table_ops.insert(cols, vals)
        self.assertEqual(table_ops.lines, lines)
        
    def test_insert2(self):
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops = TableOps('Friends', 'Dogs')
        cols = ['*']
        vals = ['zuzu', '1']
        table_ops.insert(cols, vals)
        self.assertEqual(table_ops.lines, lines)
        
    def test_insert3(self):
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops = TableOps('Friends', 'Dogs')
        cols = ['*']
        vals = [1, True, 'mom']
        self.assertEqual(table_ops.insert(cols, vals), None)
        
    def test_insert4(self):
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops = TableOps('Friends', 'Dogs')
        cols = ['NAME', 'AGE', 'WEIGHT']
        vals = ['no', True, 'mom']
        self.assertEqual(table_ops.insert(cols, vals), None)
        
    def test_update(self):
        filters = {
            'NAME': {
                'operator': 'eq',
                'value': 'azorel'
            },
            'AGE': {
                'operator': 'eq',
                'value': '12'
            },
            'op_bool': 'AND'}
        lines = [['azorel','1','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops = TableOps('Friends', 'Dogs')
        
        cols = ['AGE']
        vals = ['1']
        table_ops.update(filters, cols, vals)
        self.assertEqual(table_ops.lines, lines)
        
    def test_commit(self):
        table_ops = TableOps('Friends', 'Dogs')
        columns = {"NAME":0, "AGE":1, "WEIGHT":2, "COLOUR":3}
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        table_ops.columns = columns
        table_ops.lines = lines
        table_ops.commit()
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.lines, lines)
        
    def test_export(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.export('dest.xml')
        import os
        self.assertTrue(os.path.exists('dest.xml'))
        
    def test_export_import(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.export('dest.xml')
        table_ops1 = TableOps('Friends', 'generic_dogs')
        table_ops1.import_('dest.xml')
        self.assertEqual(table_ops.lines, table_ops1.lines)
        
    def test_export_import1(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.metadata = {}
        with self.assertRaises(Exception):
            table_ops.export('dest.xml')
            table_ops1.import_('dest.xml')
        
    def test_export_import2(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.metadata = {"d":0, "d":1, "s":2, "a":9}
        with self.assertRaises(Exception):
            table_ops.export('dest.xml')
            table_ops1.import_('dest.xml')
        
    def test_export_import3(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.metadata = {'NAME':["TEXT", '20'],
                    'AGE':["BLA", '10'],
                    'WEIGHT':["NUMERIC", '0'],
                    'COLOUR':["TEXT", '0'],}
        table_ops.columns = []
        with self.assertRaises(Exception):
            table_ops.export('dest.xml')
            table_ops1.import_('dest.xml')
                  
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)