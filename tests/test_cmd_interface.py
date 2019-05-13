import unittest
import unittest.mock
import icar.interfaces.command_line_interface as cmd
# import icar.core.database_operations as db_ops
import icar.core.table_operations as tb_ops


class CmdTest(unittest.TestCase):
	def test_create_database(self):
		with unittest.mock.patch('icar.core.database_operations.create_database') as create_database:
			app = cmd.Application()
			app.process_command("create database fruits")
			create_database.assert_called_once_with("fruits")

	def test_delete_database(self):
		with unittest.mock.patch('icar.core.database_operations.delete_database') as delete_database:
			app = cmd.Application()
			app.process_command("delete database fruits")
			delete_database.assert_called_once_with("fruits")

	def test_create_table(self):
		with unittest.mock.patch('icar.core.database_operations.create_table') as create_table:
			app = cmd.Application()
			app.process_command("create table dogs in friends (name text 20, age numeric 10, smart boolean)")
			create_table.assert_called_once_with("friends", "dogs", ["name", "age", "smart"], ['text', 'numeric', 'boolean'], [20, 10, 0])	

	def test_delete_table(self):
		with unittest.mock.patch('icar.core.database_operations.delete_table') as delete_table:
			app = cmd.Application()
			app.process_command("delete table pisici in friends")
			delete_table.assert_called_once_with("friends", "pisici")

	def test_rename_table(self):
		with unittest.mock.patch('icar.core.database_operations.rename_table') as rename_table:
			app = cmd.Application()
			app.process_command("rename table pisici into dusmani in friends")
			rename_table.assert_called_once_with("friends", "pisici", "dusmani")

	def test_alter_table_drop_column(self):
		with unittest.mock.patch('icar.core.database_operations.remove_column') as remove_column:
			app = cmd.Application()
			app.process_command("alter table dogs in friends drop column smart")
			remove_column.assert_called_once_with("friends", "dogs", "smart")

	def test_alter_table_add_column(self):
		with unittest.mock.patch('icar.core.database_operations.add_column') as add_column:
			app = cmd.Application()
			app.process_command("alter table dogs in friends add column size numeric 30")
			add_column.assert_called_once_with('friends', 'dogs', 'size', 'numeric', '30')		

	def test_alter_table_rename_column(self):
		with unittest.mock.patch('icar.core.database_operations.rename_column') as rename_column:
			app = cmd.Application()
			app.process_command("alter table dogs in friends rename column size to weight")
			rename_column.assert_called_once_with('friends', 'dogs', 'size', 'weight')		

	def test_set_database(self):
		app = cmd.Application()
		message = app.process_command("set database test")
		self.assertEqual(message, "Current database: TEST ready for INSERT, SELECT, ...")

	def test_insert(self):
		with unittest.mock.patch.object(tb_ops.TableOps, "insert") as insert:
			app = cmd.Application()
			app.process_command("set database friends")
			app.process_command("insert into dogs (name, age, weight, colour) values (toto, 12, 10, white)")
			insert.assert_called_once_with(['NAME', 'AGE', 'WEIGHT', 'COLOUR'], ['toto', '12', '10', 'white'])

	def test_select(self):
		with unittest.mock.patch.object(tb_ops.TableOps, "select") as select:
			app = cmd.Application()
			app.process_command("set database friends")
			app.process_command("select name, weight, colour from dogs where name eq toto and age lt 15")
			select.assert_called_once_with({'op_bool': 'AND', 'NAME': {'operator': 'EQ', 'value': 'toto'}, 'AGE': {'operator': 'LT', 'value': '15'}}, ['NAME', 'WEIGHT', 'COLOUR'])

	def test_update(self):
		with unittest.mock.patch.object(tb_ops.TableOps, "update") as update:
			app = cmd.Application()
			app.process_command("set database friends")
			app.process_command("update dogs set name = toto where name eq tototo")
			update.assert_called_once_with({'op_bool': '', 'NAME': {'operator': 'EQ', 'value': 'tototo'}}, ['NAME'], ['toto'])

	def test_export(self):
		with unittest.mock.patch.object(tb_ops.TableOps, "export") as export:
			app = cmd.Application()
			app.process_command("set database friends")
			app.process_command("export dogs in friends at path path\\myexport.xml")
			export.assert_called_once_with('path\\myexport.xml')

	def test_import(self):
		with unittest.mock.patch.object(tb_ops.TableOps, "import_") as import_:
			app = cmd.Application()
			app.process_command("set database friends")
			app.process_command("import generic_dogs in friends at path path\\myimport.xml")
			import_.assert_called_once_with('path\\myimport.xml')	

	def test_create_filters(self):
		app = cmd.Application()
		ret = app.create_filters("name eq toto and age lt 15")
		self.assertEqual(ret, {'AGE': {'operator': 'LT', 'value': '15'}, 'NAME': {'operator': 'EQ', 'value': 'toto'}, 'op_bool': 'AND'})

if __name__ == '__main__':
    unittest.main()
