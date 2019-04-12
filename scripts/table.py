# 3) Operatii pentru creat tabele
#     - definit coloane initiale si tipurile lor - text/numeric)  V
#     - sters tabele V
#     - modificat nume tabele V
#     - eliminat coloane V
#     - redenumit coloane V
#     - adaugat coloane noi (specificat tipul) V
from constants import *
import os

# USE *DATABASE_NAME*

# CREATE TABLE *TABLE_NAME* (IN *DATABASE_NAME* ?) (*COLUMN_NAME_1* *COLUMN_TYPE_1*, ...)
def createTable(databaseName, tableName, columns, types, sizes):
    if type(databaseName) != str and databaseName.isalnum() != True:
        return (1, 'Error: Invalid database name.')
    if type(tableName) != str and tableName.isalnum() != True:
        return (1, 'Error: Invalid table name.')
    databaseName = databaseName.upper()
    tableName = tableName.upper()
    if len(columns) != len(types):
        return (1, 'Error: Invalid column types.')
    dirPath = os.path.join(DATABASES_PATH, databaseName)
    if not os.path.exists(dirPath):
        return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, tableName))
    if os.path.exists(filePath):
        return (1, 'Error: Table already exists.')
    with open(filePath, 'w') as f:
        text = ''
        for column in columns:
            if type(column) != str:
                return (1, 'Error: Invalid column name.')
            column = column.upper()
            text = '{}{},'.format(text, column)
        text = '{}\n'.format(text[:-1])
        f.write(text)
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, tableName))
    with open(metadataPath, 'w') as f:
        for i in range(len(columns)):
            types[i] = types[i].upper()
            columns[i] = columns[i].upper()
            if not types[i] in VALID_TYPES:
                return (1, 'Error: Invalid type.')
            if type(sizes[i]) != int:
                sizes[i] = 0
            f.write('{},{},{}\n'.format(columns[i], types[i], sizes[i]))
    return (0, 'Success: Table created.')

# DELETE TABLE *TABLE_NAME* (IN *DATABASE_NAME* ?)
def deleteTable(databaseName, tableName):
    if type(databaseName) != str and databaseName.isalnum() != True:
        return (1, 'Error: Invalid database name.')
    if type(tableName) != str and tableName.isalnum() != True:
        return (1, 'Error: Invalid table name.')
    databaseName = databaseName.upper()
    tableName = tableName.upper()
    dirPath = os.path.join(DATABASES_PATH, databaseName)
    if not os.path.exists(dirPath):
        return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, tableName))
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, tableName))
    if not os.path.exists(filePath):
        return (1, 'Error: Table doesn\'t exist.')
    try:
        os.remove(filePath)
        os.remove(metadataPath)
    except:
        return (1, 'Error: Couldn\'t delete table. Please retry in a few minutes.')
    return (0, 'Success: Table deleted.')

# RENAME TABLE *OLD_TABLE_NAME* INTO *NEW_TABLE_NAME* (IN *DATABASE_NAME* ?)
def renameTable(databaseName, oldTableName, newTableName):
    if type(databaseName) != str and databaseName.isalnum() != True:
        return (1, 'Error: Invalid database name.')
    if type(oldTableName) != str and oldTableName.isalnum() != True:
        return (1, 'Error: Invalid old table name.')
    if type(newTableName) != str and newTableName.isalnum() != True:
        return (1, 'Error: Invalid new table name.')
    databaseName = databaseName.upper()
    oldTableName = oldTableName.upper()
    newTableName = newTableName.upper()
    dirPath = os.path.join(DATABASES_PATH, databaseName)
    if not os.path.exists(dirPath):
        return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, oldTableName))
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, oldTableName))
    if not os.path.exists(filePath):
        return (1, 'Error: Old table doesn\'t exist.')
    newFilePath = '{}.csv'.format(os.path.join(dirPath, newTableName))
    newMetadataPath = '{}.metadata'.format(os.path.join(dirPath, newTableName))
    if os.path.exists(newFilePath):
        return (1, 'Error: New table already exists.')
    try:
        os.rename(filePath, newFilePath)
        os.rename(metadataPath, newMetadataPath)
    except:
        return (1, 'Error: Couldn\'t rename table. Please retry in a few minutes.')
    return (0, 'Success: Table renamed.')

def removeColumn(databaseName, tableName, columnName):
    if type(databaseName) != str and databaseName.isalnum() != True:
        return (1, 'Error: Invalid database name.')
    if type(tableName) != str and tableName.isalnum() != True:
        return (1, 'Error: Invalid table name.')
    if type(columnName) != str and columnName.isalnum() != True:
        return (1, 'Error: Invalid column name.')
    databaseName = databaseName.upper()
    tableName = tableName.upper()
    columnName = columnName.upper()
    dirPath = os.path.join(DATABASES_PATH, databaseName)
    if not os.path.exists(dirPath):
        return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, tableName))
    if not os.path.exists(filePath):
        return (1, 'Error: Table doesn\'t exist.')
    with open(filePath, 'r') as f:
        data = f.read().splitlines()
    header = data[0]
    columns = header.split(',')
    if not columnName in columns:
        return (1, 'Error: Column doesn\'t exist.')
    index = columns.index(columnName)
    for i in range(len(data)):
        elems = data[i].split(',')
        del elems[index]
        elems = ','.join(elems)
        data[i] = elems
    data = '\n'.join(data)
    with open(filePath, 'w') as f:
        f.write(data)
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, tableName))
    with open(metadataPath, 'r') as f:
        metadata = f.read().splitlines()
    for i in range(len(metadata)):
        elems = metadata[i].split(',')
        if elems[0] == columnName:
            break
    del metadata[i]
    metadata = '\n'.join(metadata)
    with open(metadataPath, 'w') as f:
        f.write(metadata)
    return (0, 'Success: Column removed.')
    
def renameColumn(databaseName, tableName, oldColumnName, newColumnName):
    if type(databaseName) != str and databaseName.isalnum() != True:
        return (1, 'Error: Invalid database name.')
    if type(tableName) != str and tableName.isalnum() != True:
        return (1, 'Error: Invalid table name.')
    if type(oldColumnName) != str and oldColumnName.isalnum() != True:
        return (1, 'Error: Invalid old column name.')
    if type(newColumnName) != str and newColumnName.isalnum() != True:
        return (1, 'Error: Invalid new column name.')
    databaseName = databaseName.upper()
    tableName = tableName.upper()
    oldColumnName = oldColumnName.upper()
    newColumnName = newColumnName.upper()
    dirPath = os.path.join(DATABASES_PATH, databaseName)
    if not os.path.exists(dirPath):
        return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, tableName))
    if not os.path.exists(filePath):
        return (1, 'Error: Table doesn\'t exist.')
    with open(filePath, 'r') as f:
        data = f.read().splitlines()
    header = data[0]
    columns = header.split(',')
    if not oldColumnName in columns:
        return (1, 'Error: Column doesn\'t exist.')
    index = columns.index(oldColumnName)
    columns[index] = newColumnName
    header = ','.join(columns)
    data[0] = header
    data = '\n'.join(data)
    with open(filePath, 'w') as f:
        f.write(data)
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, tableName))
    with open(metadataPath, 'r') as f:
        metadata = f.read().splitlines()
    for i in range(len(metadata)):
        elems = metadata[i].split(',')
        if elems[0] == oldColumnName:
            elems[0] = newColumnName
            elems = ','.join(elems)
            metadata[i] = elems
            break
    metadata = '\n'.join(metadata)
    with open(metadataPath, 'w') as f:
        f.write(metadata)
    return (0, 'Success: Column renamed.')

def addColumn(databaseName, tableName, columnName, columnType, columnSize):
    if type(databaseName) != str and databaseName.isalnum() != True:
        return (1, 'Error: Invalid database name.')
    if type(tableName) != str and tableName.isalnum() != True:
        return (1, 'Error: Invalid table name.')
    if type(columnName) != str and columnName.isalnum() != True:
        return (1, 'Error: Invalid column name.')
    databaseName = databaseName.upper()
    tableName = tableName.upper()
    columnName = columnName.upper()
    columnType = columnType.upper()
    if not columnType in VALID_TYPES:
        return (1, 'Error: Invalid type.')
    if type(columnSize != int):
        columnSize = 0
    dirPath = os.path.join(DATABASES_PATH, databaseName)
    if not os.path.exists(dirPath):
        return (1, 'Error: Database doesn\'t exist.')
    filePath = '{}.csv'.format(os.path.join(dirPath, tableName))
    if not os.path.exists(filePath):
        return (1, 'Error: Table doesn\'t exist.')
    with open(filePath, 'r') as f:
        data = f.read().splitlines()
    for i in range(len(data)):
        if i == 0:
            data[i] = '{},{}'.format(data[i], columnName)
        else:
            data[i] = '{},NULL'.format(data[i])
    data = '\n'.join(data)
    with open(filePath, 'w') as f:
        f.write(data)
    metadataPath = '{}.metadata'.format(os.path.join(dirPath, tableName))
    with open(metadataPath, 'r') as f:
        metadata = f.read().splitlines()
    metadata.append('{},{},{}'.format(columnName, columnType, columnSize))
    metadata = '\n'.join(metadata)
    with open(metadataPath, 'w') as f:
        f.write(metadata)
    return (0, 'Success: Column added.')
    