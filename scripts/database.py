# 2) Operatii pentru creat/sters baza de date. Operatii pentru modificat baza de date
#     - creat tabele noi V
#     - sters tabele V
from constants import *
import shutil
import os

# CREATE DATABASE *DATABASE_NAME*
def createDatabase(databaseName):
    if type(databaseName) != str and databaseName.isalnum() != True:
        return (1, 'Error: Invalid database name.')
    databaseName = databaseName.upper()
    dirPath = os.path.join(DATABASES_PATH, databaseName)
    if os.path.exists(dirPath):
        return (1, 'Error: Database already exists.')
    try:
        os.mkdir(dirPath)
    except:
        return (1, 'Error: Couldn\'t create database. Please retry in a few minutes.')
    return (0, 'Success: Database created.')

# DELETE DATABASE *DATABASE_NAME*
def deleteDatabase(databaseName):
    if type(databaseName) != str and databaseName.isalnum() != True:
        return (1, 'Error: Invalid database name.')
    databaseName = databaseName.upper()
    dirPath = os.path.join(DATABASES_PATH, databaseName)
    if not os.path.exists(dirPath):
        return (1, 'Error: Database doesn\'t exist.')
    try:
        shutil.rmtree(dirPath)
    except:
        return (1, 'Error: Couldn\'t delete database. Please retry in a few minutes.')
    return (0, 'Success: Database deleted.')