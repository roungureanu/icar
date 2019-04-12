from table import *
from database import *

print deleteDatabase('TEST_DB')

print createDatabase('TEST_DB')
print createTable('TEST_DB', 'TEST_TABEL', ['nume', 'prenume'], ['text', 'text'], [10, 10])

print renameTable('TEST_DB', 'TEST_TABEL', 'TEST_TABEL_2')

print createTable('TEST_DB', 'TEST_TABEL_3', ['nume', 'prenume'], ['text', 'text'], [10, 10])
print deleteTable('TEST_DB', 'TEST_TABEL_3')


print addColumn('TEST_DB', 'TEST_TABEL_2', 'ani', 'numeric', 0)
print addColumn('TEST_DB', 'TEST_TABEL_2', 'job', 'text', 20)

print removeColumn('TEST_DB', 'TEST_TABEL_2', 'job')

print renameColumn('TEST_DB', 'TEST_TABEL_2', 'ani', 'varsta')

print createTable('TEST_DB', 'TEST_TABEL_4', ['camp1', 'camp2', 'camp3', 'camp4'], ['string', 'text', 'numeric', 'boolean'], [10, 10, 0, 0])
