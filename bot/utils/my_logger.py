import os
import logging
from logging import handlers


def configure_logger():
    # Create a logger
    logging.basicConfig(level=logging.INFO)
    # Create a folder for log files
    log_folder = os.path.join('bot', 'data', 'logs')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    # Create a rotating file handler
    log_file = os.path.join(log_folder, 'python_logs.log')
    handler = handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=1e7,
        backupCount=5,
        encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    # Add the handler to the root logger
    logging.getLogger().addHandler(handler)
