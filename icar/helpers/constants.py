import os

ROOT = os.path.dirname(  # icar (repository)
    os.path.dirname(  # icar (package)
        os.path.dirname(  # helpers
            os.path.abspath(__file__)  # constants.py
        )
    )
)

MAIN_PACKAGE_PATH = os.path.join(ROOT, 'icar')

RESOURCES_FOLDER_PATH = os.path.join(ROOT, 'resources')

LOGS_FOLDER_PATH = os.path.join(ROOT, 'logs')
LOGGER_CONFIG_PATH = os.path.join(RESOURCES_FOLDER_PATH, 'logger_config.json')

DATABASES_PATH = os.path.join(ROOT, 'databases')

VALID_TYPES = {
    'TEXT': 'TEXT',
    'NUMERIC': 'NUMERIC',
    'BOOLEAN': 'BOOLEAN'
}
