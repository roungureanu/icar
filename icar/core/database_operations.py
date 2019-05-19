# 2) Operatii pentru creat/sters baza de date. Operatii pentru modificat baza de date
#     - creat tabele noi V
#     - sters tabele V
import os
import shutil

import icar.helpers.constants as constants


# CREATE DATABASE *DATABASE_NAME*
def create_database(database_name):
    assert isinstance(database_name, str)
    assert database_name.isalnum()
    # if type(database_name) != str:
    #     return (1, 'Error: Invalid database name.')
    # if not database_name.isalnum():
    #     return (1, 'Error: Invalid database name.')
    database_name = database_name.upper()
    dirPath = os.path.join(constants.DATABASES_PATH, database_name)
    assert not os.path.exists(dirPath)
    os.makedirs(dirPath)
    # if os.path.exists(dirPath):
    #     return (1, 'Error: Database already exists.')
    # try:
    #     os.makedirs(dirPath)
    # except Exception:
    #     return (1, 'Error: Couldn\'t create database. Please retry in a few minutes.')
    return (0, 'Success: Database created.')


def database_exists(database_name):
    assert isinstance(database_name, str)
    assert database_name.isalnum()
    # if type(database_name) != str:
    #     return (1, 'Error: Invalid database name.')
    # if not database_name.isalnum():
    #     return (1, 'Error: Invalid database name.')
    return database_name.upper() in os.listdir(constants.DATABASES_PATH)


def list_databases():
    return os.listdir(constants.DATABASES_PATH)


def list_tables(database_name):
    tables = []

    database_path = os.path.join(constants.DATABASES_PATH, database_name.upper())
    for file_ in os.listdir(database_path):
        full_path = os.path.join(database_path, file_)
        if full_path.lower().endswith('.csv'):
            tables.append(os.path.splitext(file_)[0].upper())

    return tables


# DELETE DATABASE *DATABASE_NAME*
def delete_database(database_name):
    assert isinstance(database_name, str)
    assert database_name.isalnum()
    # if type(database_name) != str:
    #     return (1, 'Error: Invalid database name.')
    # if not database_name.isalnum():
    #     return (1, 'Error: Invalid database name.')
    database_name = database_name.upper()
    dirPath = os.path.join(constants.DATABASES_PATH, database_name)
    assert os.path.exists(dirPath)
    shutil.rmtree(dirPath)
    # if not os.path.exists(dirPath):
    #     return (1, 'Error: Database doesn\'t exist.')
    # try:
    #     shutil.rmtree(dirPath)
    # except Exception:
    #     return (1, 'Error: Couldn\'t delete database. Please retry in a few minutes.')
    return (0, 'Success: Database deleted.')


# 3) Operatii pentru creat tabele
#     - definit coloane initiale si tipurile lor - text/numeric)  V
#     - sters tabele V
#     - modificat nume tabele V
#     - eliminat coloane V
#     - redenumit coloane V
#     - adaugat coloane noi (specificat tipul) V

# USE *DATABASE_NAME*

# CREATE TABLE *TABLE_NAME* (IN *DATABASE_NAME* ?) (*COLUMN_NAME_1* *COLUMN_TYPE_1*, ...)
def create_table(database_name, table_name, columns, types, sizes):
    assert isinstance(database_name, str)
    assert database_name.isalnum()
    assert isinstance(table_name, str)
    assert table_name.isalnum()
    # if type(database_name) != str:
    #     return (1, 'Error: Invalid database name.')
    # if not database_name.isalnum():
    #     return (1, 'Error: Invalid database name.')
    # if type(table_name) != str:
    #     return (1, 'Error: Invalid table name.')
    # if not table_name.isalnum():
    #     return (1, 'Error: Invalid table name.')
    database_name = database_name.upper()
    table_name = table_name.upper()
    assert len(columns) == len(types)
    # if len(columns) != len(types):
    #     return (1, 'Error: Invalid column types.')
    dirPath = os.path.join(constants.DATABASES_PATH, database_name)
    assert os.path.exists(dirPath)
    # if not os.path.exists(dirPath):
    #     return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, table_name))
    assert not os.path.exists(filePath)
    # if os.path.exists(filePath):
    #     return (1, 'Error: Table already exists.')
    with open(filePath, 'w') as f:
        text = ''
        for column in columns:
            assert isinstance(column, str)
            # if type(column) != str:
            #     return (1, 'Error: Invalid column name.')
            column = column.upper()
            text = '{}{},'.format(text, column)
        text = '{}\n'.format(text[:-1])
        f.write(text)
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, table_name))
    with open(metadataPath, 'w') as f:
        for i in range(len(columns)):
            types[i] = types[i].upper()
            columns[i] = columns[i].upper()
            assert types[i] in constants.VALID_COLUMN_TYPES
            # if types[i] not in constants.VALID_COLUMN_TYPES:
            #     return (1, 'Error: Invalid type.')
            if type(sizes[i]) != int:
                sizes[i] = 0
            f.write('{},{},{}\n'.format(columns[i], types[i], sizes[i]))
    return (0, 'Success: Table created.')


# DELETE TABLE *TABLE_NAME* (IN *DATABASE_NAME* ?)
def delete_table(database_name, table_name):
    assert isinstance(database_name, str)
    assert database_name.isalnum()
    assert isinstance(table_name, str)
    assert table_name.isalnum()
    # if type(database_name) != str:
    #     return (1, 'Error: Invalid database name.')
    # if not database_name.isalnum():
    #     return (1, 'Error: Invalid database name.')
    # if type(table_name) != str:
    #     return (1, 'Error: Invalid table name.')
    # if not table_name.isalnum():
    #     return (1, 'Error: Invalid table name.')
    database_name = database_name.upper()
    table_name = table_name.upper()
    dirPath = os.path.join(constants.DATABASES_PATH, database_name)
    assert(os.path.exists(dirPath))
    # if not os.path.exists(dirPath):
    #     return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, table_name))
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, table_name))
    assert os.path.exists(filePath)
    os.remove(filePath)
    os.remove(metadataPath)
    # if not os.path.exists(filePath):
    #     return (1, 'Error: Table doesn\'t exist.')
    # try:
    #     os.remove(filePath)
    #     os.remove(metadataPath)
    # except Exception:
    #     return (1, 'Error: Couldn\'t delete table. Please retry in a few minutes.')
    return (0, 'Success: Table deleted.')


# RENAME TABLE *OLD_TABLE_NAME* INTO *NEW_TABLE_NAME* (IN *DATABASE_NAME* ?)
def rename_table(database_name, old_table_name, new_table_name):
    assert isinstance(database_name, str)
    assert database_name.isalnum()
    assert isinstance(old_table_name, str)
    assert old_table_name.isalnum()
    assert isinstance(new_table_name, str)
    assert new_table_name.isalnum()
    # if type(database_name) != str:
    #     return (1, 'Error: Invalid database name.')
    # if not database_name.isalnum():
    #     return (1, 'Error: Invalid database name.')
    # if type(old_table_name) != str:
    #     return (1, 'Error: Invalid old table name.')
    # if not old_table_name.isalnum():
    #     return (1, 'Error: Invalid old table name.')
    # if type(new_table_name) != str:
    #     return (1, 'Error: Invalid new table name.')
    # if not new_table_name.isalnum():
    #     return (1, 'Error: Invalid new table name.')
    database_name = database_name.upper()
    old_table_name = old_table_name.upper()
    new_table_name = new_table_name.upper()
    dirPath = os.path.join(constants.DATABASES_PATH, database_name)
    assert os.path.exists(dirPath)
    # if not os.path.exists(dirPath):
    #     return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, old_table_name))
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, old_table_name))
    assert os.path.exists(filePath)
    # if not os.path.exists(filePath):
    #     return (1, 'Error: Old table doesn\'t exist.')
    newFilePath = '{}.csv'.format(os.path.join(dirPath, new_table_name))
    newMetadataPath = '{}.metadata'.format(os.path.join(dirPath, new_table_name))
    assert not os.path.exists(newFilePath)
    os.rename(filePath, newFilePath)
    os.rename(metadataPath, newMetadataPath)
    # if os.path.exists(newFilePath):
    #     return (1, 'Error: New table already exists.')
    # try:
    #     os.rename(filePath, newFilePath)
    #     os.rename(metadataPath, newMetadataPath)
    # except Exception:
    #     return (1, 'Error: Couldn\'t rename table. Please retry in a few minutes.')
    return (0, 'Success: Table renamed.')


def remove_column(database_name, table_name, column_name):
    assert isinstance(database_name, str)
    assert database_name.isalnum()
    assert isinstance(table_name, str)
    assert table_name.isalnum()
    assert isinstance(column_name, str)
    assert column_name.isalnum()
    # if type(database_name) != str:
    #     return (1, 'Error: Invalid database name.')
    # if not database_name.isalnum():
    #     return (1, 'Error: Invalid database name.')
    # if type(table_name) != str:
    #     return (1, 'Error: Invalid table name.')
    # if not table_name.isalnum():
    #     return (1, 'Error: Invalid table name.')
    # if type(column_name) != str:
    #     return (1, 'Error: Invalid column name.')
    # if not column_name.isalnum():
    #     return (1, 'Error: Invalid column name.')
    database_name = database_name.upper()
    table_name = table_name.upper()
    column_name = column_name.upper()
    dirPath = os.path.join(constants.DATABASES_PATH, database_name)
    assert os.path.exists(dirPath)
    # if not os.path.exists(dirPath):
    #     return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, table_name))
    assert os.path.exists(filePath)
    # if not os.path.exists(filePath):
    #     return (1, 'Error: Table doesn\'t exist.')
    with open(filePath, 'r') as f:
        data = f.read().splitlines()
    header = data[0]
    columns = header.split(',')
    assert column_name in columns
    # if column_name not in columns:
    #     return (1, 'Error: Column doesn\'t exist.')
    index = columns.index(column_name)
    for i in range(len(data)):
        elems = data[i].split(',')
        del elems[index]
        elems = ','.join(elems)
        data[i] = elems
    data = '\n'.join(data)
    with open(filePath, 'w') as f:
        f.write(data)
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, table_name))
    with open(metadataPath, 'r') as f:
        metadata = f.read().splitlines()
    for i in range(len(metadata)):
        elems = metadata[i].split(',')
        if elems[0] == column_name:
            break
    del metadata[i]
    metadata = '\n'.join(metadata)
    with open(metadataPath, 'w') as f:
        f.write(metadata)
    return (0, 'Success: Column removed.')


def rename_column(database_name, table_name, old_column_name, new_column_name):
    assert isinstance(database_name, str)
    assert database_name.isalnum()
    assert isinstance(table_name, str)
    assert table_name.isalnum()
    assert isinstance(old_column_name, str)
    assert old_column_name.isalnum()
    assert isinstance(new_column_name, str)
    assert new_column_name.isalnum()
    # if type(database_name) != str:
    #     return (1, 'Error: Invalid database name.')
    # if not database_name.isalnum():
    #     return (1, 'Error: Invalid database name.')
    # if type(table_name) != str:
    #     return (1, 'Error: Invalid table name.')
    # if not table_name.isalnum():
    #     return (1, 'Error: Invalid table name.')
    # if type(old_column_name) != str:
    #     return (1, 'Error: Invalid old column name.')
    # if not old_column_name.isalnum():
    #     return (1, 'Error: Invalid old column name.')
    # if type(new_column_name) != str:
    #     return (1, 'Error: Invalid new column name.')
    # if not new_column_name.isalnum():
    #     return (1, 'Error: Invalid new column name.')
    database_name = database_name.upper()
    table_name = table_name.upper()
    old_column_name = old_column_name.upper()
    new_column_name = new_column_name.upper()
    dirPath = os.path.join(constants.DATABASES_PATH, database_name)
    assert os.path.exists(dirPath)
    # if not os.path.exists(dirPath):
    #     return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, table_name))
    assert os.path.exists(filePath)
    # if not os.path.exists(filePath):
    #     return (1, 'Error: Table doesn\'t exist.')
    with open(filePath, 'r') as f:
        data = f.read().splitlines()
    header = data[0]
    columns = header.split(',')
    assert old_column_name in columns
    assert new_column_name not in columns
    # if old_column_name not in columns:
    #     return (1, 'Error: Column doesn\'t exist.')
    # if new_column_name in columns:
    #     return (1, 'Error: Column already exists.')
    index = columns.index(old_column_name)
    columns[index] = new_column_name
    header = ','.join(columns)
    data[0] = header
    data = '\n'.join(data)
    with open(filePath, 'w') as f:
        f.write(data)
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, table_name))
    with open(metadataPath, 'r') as f:
        metadata = f.read().splitlines()
    for i in range(len(metadata)):
        elems = metadata[i].split(',')
        if elems[0] == old_column_name:
            elems[0] = new_column_name
            elems = ','.join(elems)
            metadata[i] = elems
            break
    metadata = '\n'.join(metadata)
    with open(metadataPath, 'w') as f:
        f.write(metadata)
    return (0, 'Success: Column renamed.')


def add_column(database_name, table_name, column_name, column_type, column_size):
    assert isinstance(database_name, str)
    assert database_name.isalnum()
    assert isinstance(table_name, str)
    assert table_name.isalnum()
    assert isinstance(column_name, str)
    assert column_name.isalnum()
    # if type(database_name) != str:
    #     return (1, 'Error: Invalid database name.')
    # if not database_name.isalnum():
    #     return (1, 'Error: Invalid database name.')
    # if type(table_name) != str:
    #     return (1, 'Error: Invalid table name.')
    # if not table_name.isalnum():
    #     return (1, 'Error: Invalid table name.')
    # if type(column_name) != str:
    #     return (1, 'Error: Invalid column name.')
    # if not column_name.isalnum():
    #     return (1, 'Error: Invalid column name.')
    database_name = database_name.upper()
    table_name = table_name.upper()
    column_name = column_name.upper()
    column_type = column_type.upper()
    assert column_type in constants.VALID_COLUMN_TYPES
    # if column_type not in constants.VALID_COLUMN_TYPES:
    #     return (1, 'Error: Invalid type.')
    if type(column_size) != int or column_size < 0:
        column_size = 0
    dirPath = os.path.join(constants.DATABASES_PATH, database_name)
    assert os.path.exists(dirPath)
    # if not os.path.exists(dirPath):
    #     return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, table_name))
    assert os.path.exists(filePath)
    # if not os.path.exists(filePath):
    #     return (1, 'Error: Table doesn\'t exist.')
    with open(filePath, 'r') as f:
        data = f.read().splitlines()
    header = data[0]
    columns = header.split(',')
    assert column_name not in columns
    # if column_name in columns:
    #     return (1, 'Error: Column already exists.')
    for i in range(len(data)):
        if i == 0:
            data[i] = '{},{}'.format(data[i], column_name)
        else:
            if column_type == constants.VALID_COLUMN_TYPES['NUMERIC']:
                data[i] = '{},0'.format(data[i])
            else:
                data[i] = '{},NULL'.format(data[i])
    data = '\n'.join(data)
    with open(filePath, 'w') as f:
        f.write(data)
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, table_name))
    with open(metadataPath, 'r') as f:
        metadata = f.read().splitlines()
    metadata.append('{},{},{}'.format(column_name, column_type, column_size))
    metadata = '\n'.join(metadata)
    with open(metadataPath, 'w') as f:
        f.write(metadata)
    return (0, 'Success: Column added.')


if __name__ == '__main__':
    create_database('test_db')
    create_table(
        'test_db',
        'test_table',
        ['string_column', 'numeric_column'],
        [constants.VALID_COLUMN_TYPES['TEXT'], constants.VALID_COLUMN_TYPES['NUMERIC']],
        [100, 10]
    )

    # print(delete_database('TEST_DB'))
    #
    # print(create_database('TEST_DB'))
    # print(create_table('TEST_DB', 'TEST_TABEL', ['nume', 'prenume'], ['text', 'text'], [10, 10]))
    #
    # print(rename_table('TEST_DB', 'TEST_TABEL', 'TEST_TABEL_2'))
    #
    # print(create_table('TEST_DB', 'TEST_TABEL_3', ['nume', 'prenume'], ['text', 'text'], [10, 10]))
    # print(delete_table('TEST_DB', 'TEST_TABEL_3'))
    #
    #
    # print(add_column('TEST_DB', 'TEST_TABEL_2', 'ani', 'numeric', 0))
    # print(add_column('TEST_DB', 'TEST_TABEL_2', 'job', 'text', 20))
    #
    # print(remove_column('TEST_DB', 'TEST_TABEL_2', 'job'))
    #
    # print(rename_column('TEST_DB', 'TEST_TABEL_2', 'ani', 'varsta'))
    #
    # print(create_table('TEST_DB', 'TEST_TABEL_4', ['camp1', 'camp2', 'camp3', 'camp4'], ['string', 'text', 'numeric', 'boolean'], [10, 10, 0, 0]))
