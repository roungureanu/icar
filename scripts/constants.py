import os

DATABASES_PATH = 'DATABASES'
if not os.path.exists(DATABASES_PATH):
    os.mkdir(DATABASES_PATH)

VALID_TYPES = ['TEXT', 'NUMERIC', 'BOOLEAN']