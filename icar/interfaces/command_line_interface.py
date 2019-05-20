import icar.core.database_operations as database
import icar.core.table_operations as table_operations
import re


class Application(object):
    def __init__(self):
        self.stop_required = False
        self.database_name = ""

    def run(self):
        while not self.should_stop():
            command = input('> ')

            if command.lower() in {'exit', 'stop', 'quit', 'bye', 'q'}:
                print('bye :(')
                self.stop_required = True
                break

            result = self.process_command(command.lower())
            print(result)

    def create_filters(self, conditions):
        if " and " in conditions:
            op_bool = "and"
        elif " or " in conditions:
            op_bool = "or"
        else:
            op_bool = ""

        filters = {"op_bool": op_bool.upper()}

        if op_bool != "":
            conditions = [it.strip() for it in conditions.split(op_bool)]
        else:
            conditions = [conditions]

        for c in conditions:
            cond = c.split()
            # cond = [it.upper() for it in c.split()]
            if len(cond) != 3:
                return "Invalid condition {}".format(c)
            filters[cond[0].upper()] = {
                'operator': cond[1].upper(), 'value': cond[2]}
        return filters

    def process_command(self, command):
        # CREATE DATABASE *DATABASE_NAME*
        if command.startswith('create database'):
            m = re.search("create database ([a-z 0-9]+)", command)
            try:
                assert m != None
            except Exception as exc:
                return "Parse exception"

            name = m.group(1)
            
            try:
                result = database.create_database(name)
            except Exception as exc:
                return "Exception: Database already exists " + str(exc)
            
            return result[1]

        # DELETE DATABASE *DATABASE_NAME*
        if command.startswith('delete database'):
            m = re.search("delete database ([a-z 0-9]+)", command)
            try:
                assert m != None
            except Exception as exc:
                return "Parse exception"

            name = m.group(1)
            try:
                result = database.delete_database(name)
            except Exception as exc:
                return "Exception: Specified database does not exist " + str(exc)
            return result[1]

        # CREATE TABLE *TABLE_NAME* (IN *DATABASE_NAME* ?) (*COLUMN_NAME_1* *COLUMN_TYPE_1*, ...)
        if command.startswith('create table'):
            m = re.search(
                "create table (?P<t_name>.*) in (?P<d_name>.*) \((?P<col_names_types>.*)\)", command)
            table_name = m.group('t_name')
            database_name = m.group('d_name')
            col_names_types = m.group('col_names_types')
            columns, types, sizes = [], [], []
            fields = col_names_types.split(',')
            for field in fields:
                field = field.strip().split()
                if len(field) == 2 and field[-1] == "boolean":
                    field.append(0)
                if len(field) != 3:
                    return "Invalid column description."
                columns.append(field[0])
                types.append(field[1])
                sizes.append(int(field[2]))

            try:
                result = database.create_table(
                    database_name, table_name, columns, types, sizes)
            except Exception as exc:
                return "Exception: Could not create table " + str(exc)
            return result[1]

        # DELETE TABLE *TABLE_NAME* (IN *DATABASE_NAME* ?)
        if command.startswith('delete table'):
            m = re.search(
                "delete table (?P<t_name>.*) in (?P<d_name>.*)", command)
            table_name = m.group('t_name')
            database_name = m.group('d_name')
            try:
                result = database.delete_table(database_name, table_name)
            except Exception as exc:
                return "Exception: Could not delete table " + str(exc) 

            return result[1]

        # RENAME TABLE *OLD_TABLE_NAME* INTO *NEW_TABLE_NAME* (IN *DATABASE_NAME* ?)
        if command.startswith('rename table'):
            m = re.search(
                "rename table (?P<old_t_name>.*) into (?P<new_t_name>.*) in (?P<d_name>.*)", command)
            database_name = m.group('d_name')
            old_table_name = m.group('old_t_name')
            new_table_name = m.group('new_t_name')

            try:
                result = database.rename_table(
                    database_name, old_table_name, new_table_name)
            except Exception as exc:
                return "Exception: Could not rename table " + str(exc)

            return result[1]

        # ALTER TABLE *TABLE_NAME* IN *DATABASE_NAME* DROP COLUMN *COLUMN_NAME*
        if command.startswith('alter table') and 'drop column' in command:
            m = re.search(
                "alter table (?P<t_name>.*) in (?P<d_name>.*) drop column (?P<c_name>.*)", command)
            table_name = m.group('t_name')
            database_name = m.group('d_name')
            column_name = m.group('c_name')

            try:
                result = database.remove_column(
                    database_name, table_name, column_name)
            except Exception as exc:
                return "Exception: Could not drop column " + str(exc)

            return result[1]

        # ALTER TABLE *TABLE_NAME* IN *DATABASE_NAME* ADD COLUMN *COLUMN_NAME* *DATA_TYPE* *COLUMN_SIZE*
        if command.startswith('alter table') and 'add column' in command:
            m = re.search(
                "alter table (?P<t_name>.*) in (?P<d_name>.*) add column (?P<col_name_type>.*)", command)
            table_name = m.group('t_name')
            database_name = m.group('d_name')
            col_name_type = m.group('col_name_type').split()
            col_name_type = [it.strip() for it in col_name_type]

            if len(col_name_type) == 2 and col_name_type[-1] == 'boolean':
                col_name_type.append(0)
            if len(col_name_type) != 3:
                return "Invalid column data."

            column_name, column_type, column_size = col_name_type
            
            try:
                result = database.add_column(
                    database_name, table_name, column_name, column_type, column_size)
            except Exception as exc:
                return "Exception: Could not add column " + str(exc)

            return result[1]

        # ALTER TABLE *TABLE_NAME* IN *DATABASE_NAME* RENAME COLUMN *OLD_COLUMN_NAME* TO *NEW_COLUMN_NAME*
        if command.startswith('alter table') and 'rename column' in command:
            m = re.search(
                "alter table (?P<t_name>.*) in (?P<d_name>.*) rename column (?P<old_c_name>.*) to (?P<new_c_name>.*)", command)
            table_name = m.group('t_name')
            database_name = m.group('d_name')
            old_column_name = m.group('old_c_name')
            new_column_name = m.group('new_c_name')

            try:
                result = database.rename_column(
                    database_name, table_name, old_column_name, new_column_name)
            except Exception as exc:
                return "Exception: Could not rename column " + str(exc)

            return result[1]

        # SET DATABASE *DATABASE_NAME*
        if command.startswith('set database'):
            m = re.search("set database (?P<d_name>.*)", command)
            self.database_name = m.group('d_name')
            return "Current database: {} ready for INSERT, SELECT, ...".format(self.database_name.upper())

        # INSERT INTO *TABLE_NAME* (*COLUMN_1*, *COLUMN_2*, ...) VALUES (*VALUE_1*, *VALUE_2*, ...)
        if command.startswith('insert'):
            m = re.search(
                "insert into (?P<t_name>.*) \((?P<columns>.*)\) values \((?P<values>.*)\)", command)
            if self.database_name == "":
                return "No database is set. Use command:\nSET DATABASE *DATABASE_NAME*"
            database_name = self.database_name
            table_name = m.group('t_name')
            columns = [it.strip().upper()
                       for it in m.group('columns').split(',')]
            values = [it.strip() for it in m.group('values').split(',')]

            try:
                ops = table_operations.TableOps(database_name, table_name)
                result = ops.insert(columns, values)
            except Exception as exc:
                return str(exc)

            ret = "TABLE: {}\n".format(table_name)
            for row in result:
                for col in row:
                    ret += "{} ".format(col)
                ret += '\n'
            return ret

        # SELECT *COLUMNS* FROM *TABLE_NAME* WHERE *COLUMN_1* *OP_1* *VALUE_!* *UNIQUE_OP_BOOL* *COLUMN_2* *OP_2* *VALUE_2* *UNIQUE_OP_BOOL* ...
        if command.startswith('select'):
            m = re.search(
                "select (?P<columns>.*) from (?P<t_name>.*) where (?P<conditions>.*)", command)
            self.database_name = "friends"  # just for testing
            if self.database_name == "":
                return "No database is set. Use command:\nSET DATABASE *DATABASE_NAME*"
            database_name = self.database_name
            table_name = m.group('t_name')
            columns = [it.strip().upper()
                       for it in m.group('columns').split(',')]
            conditions = m.group('conditions')

            filters = self.create_filters(conditions)

            try:
                ops = table_operations.TableOps(database_name, table_name)
                result = ops.select(filters, columns)
            except Exception as exc:
                return "Exception: " + str(exc)

            ret = "TABLE: {}\n".format(table_name)
            for row in result:
                for col in row:
                    ret += "{} ".format(col)
                ret += '\n'
            return ret

        # UPDATE *TABLE_NAME* SET *COLUMN_1* = *VALUE_1*, *COLUMN_2* = *VALUE_2*, ... WHERE *CONDITION*
        if command.startswith('update'):
            m = re.search(
                "update (?P<t_name>.*) set (?P<columns_values>.*) where (?P<conditions>.*)", command)
            self.database_name = "friends"  # just for testing
            if self.database_name == "":
                return "No database is set. Use command:\nSET DATABASE *DATABASE_NAME*"
            database_name = self.database_name
            table_name = m.group('t_name')
            columns_values = m.group('columns_values').split(',')
            conditions = m.group('conditions')

            columns, values = [], []
            for cv in columns_values:
                cv = cv.strip().split('=')
                columns.append(cv[0].strip().upper())
                values.append(cv[1].strip())

            filters = self.create_filters(conditions)

            print(filters)

            try:
                ops = table_operations.TableOps(database_name, table_name)
                result = ops.update(filters, columns, values)
            except Exception as exc:
                return str(exc)

            ret = "TABLE: {}\n".format(table_name)
            for row in result:
                for col in row:
                    ret += "{} ".format(col)
                ret += '\n'
            return ret

            return ret

        # EXPORT *TABLE_NAME* IN *DATABASE_NAME* AT PATH *EXPORT_FILE_PATH*.xml
        if command.startswith('export'):
            m = re.search("export (?P<t_name>.*) in (?P<d_name>.*) at path (?P<path>.*)", command)
            database_name = m.group('d_name')
            table_name = m.group('t_name')
            path = m.group('path')

            try:
                ops = table_operations.TableOps(database_name, table_name)
                result = ops.export(path)
            except Exception as exc:
                return str(exc)

            return "Export done at path {}".format(path)

        # IMPORT *TABLE_NAME* IN *DATABASE_NAME* AT PATH *IMPORT_FILE_PATH*.xml
        if command.startswith('import'):
            m = re.search("import (?P<t_name>.*) in (?P<d_name>.*) at path (?P<path>.*)", command)
            database_name = m.group('d_name')
            table_name = m.group('t_name')
            path = m.group('path')

            try:
                ops = table_operations.TableOps(database_name, table_name)
                result = ops.import_(path)
            except Exception as exc:
                return str(exc)
                
            return "Imported table at path {}".format(path)

    def should_stop(self):
        return self.stop_required


if __name__ == '__main__':
    app = Application()
    app.run()
