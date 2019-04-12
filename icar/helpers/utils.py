import os
import json
import logging
import logging.config

import icar.helpers.constants as constants


def retrieve_logger(folder_name):
    folder_path = os.path.join(constants.LOGS_FOLDER_PATH, folder_name)

    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

    with open(constants.LOGGER_CONFIG_PATH, 'r') as handle:
        config = json.load(handle)

    config['handlers']['file']['filename'] = os.path.join(folder_path, 'log.log')

    logging.config.dictConfig(config)

    return logging.getLogger()


if __name__ == '__main__':
    logger = retrieve_logger('main')
    logger.info('hello world')
