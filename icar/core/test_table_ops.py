from table_operations import TableOps
import unittest
import sys

class TestTableOps(unittest.TestCase):

    def test_check_db_params(self):
    
        table_ops = TableOps('', '')
        self.assertEqual(table_ops.check_db_params(), False)
        
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.check_db_params(), True)
        
        table_ops = TableOps('Friends', 'Enemies')
        self.assertEqual(table_ops.check_db_params(), False)
        
        table_ops = TableOps('enemies', 'Dogs')
        self.assertEqual(table_ops.check_db_params(), False)
        
        table_ops = TableOps('friendsss', 'Dogs')
        self.assertEqual(table_ops.check_db_params(), False)
        
    def test_set_table(self):
        table_ops = TableOps('Friends', 'Dogs')
        table_ops.set_table("PEOPLE", "person")
        self.assertEqual(table_ops.table_name, "person")
        self.assertEqual(table_ops.database_name, "PEOPLE")
        
        table_ops.set_table("PEOPE", "persona")
        self.assertEqual(table_ops.table_name, "person")
        self.assertEqual(table_ops.database_name, "PEOPLE")
        
    def test_preprocess(self):
        table_ops = TableOps('Friends', 'Dogs')
        columns = {'NAME':0,'AGE':1,'WEIGHT':2,'COLOUR':3}
        lines = [['azorel','12','10','white'],
                ['maia','15','6','black'],
                ['sara','2','3','brown']]
        metadata = {'NAME':["TEXT", '20'],
                    'AGE':["NUMERIC", '10'],
                    'WEIGHT':["NUMERIC", '0'],
                    'COLOUR':["TEXT", '0'],}

        self.assertEqual(len(table_ops.metadata), len(table_ops.columns))
        self.assertEqual(columns, table_ops.columns)
        self.assertEqual(lines, table_ops.lines)
        self.assertEqual(metadata, table_ops.metadata)
        
    def test_bool_op(self):
        table_ops = TableOps('Friends', 'Dogs')
        self.assertEqual(table_ops.bool_op(1, 2, 'eq', 'numeric'), False)
        self.assertEqual(table_ops.bool_op('mama', 'mom', 'leq', 'TEXT'), False)
        self.assertEqual(table_ops.bool_op('mama', 'mom', 'le', 'TEXT'), True)
        self.assertEqual(table_ops.bool_op(1, 1, 'eq', 'text'), True)
        self.assertEqual(table_ops.bool_op('too', 'moo', 'eq', 'numeric'), False)
        self.assertEqual(table_ops.bool_op(1, 1, 'eq', 'none'), False)
        self.assertEqual(table_ops.bool_op(1, 2, 'eq', 'boolean'), True)
        
    def test_apply_filter(self):
        table_ops = TableOps('Friends', 'Dogs')
        columns = {'NAME':0,'AGE':1,'WEIGHT':2,'COLOUR':3}
        result = [['azorel','12','10','white'],]
        metadata = {'NAME':["TEXT", '20'],
                    'AGE':["NUMERIC", '10'],
                    'WEIGHT':["NUMERIC", '0'],
                    'COLOUR':["TEXT", '0'],}
        self.assertEqual(table_ops.apply_filter(None, 'age', 12,'eq', True), result)
        self.assertEqual(table_ops.apply_filter(None, 'ham', 12,'eq', True), None)
        self.assertEqual(table_ops.apply_filter(None, 'age', 0,'eq', True), None)
        self.assertEqual(table_ops.apply_filter(None, 'name', 12,'le', True), None)
        
    def test_where(self):
        pass
        
    def test_is_valid(self):
        pass
        
    def test_is_line(self):
        pass
        
    def test_filter_columns(self):
        pass
        
    def test_select(self):
        pass
        
    def test_delete(self):
        pass
        
    def test_insert(self):
        pass
        
    def test_update(self):
        pass
        
    def test_commit(self):
        pass
        
    
        
        
        
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)