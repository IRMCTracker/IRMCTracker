import logging
from os import makedirs

def add_handler(name, filename, stream_level, file_level, logger_level):
    # Create a custom logger
    logger = logging.getLogger(name)

    # Create handlers
    c_handler = logging.StreamHandler()
    
    # Getting the storage logs path
    log_path = 'storage/data/logs/'

    makedirs(name=log_path, exist_ok=True)

    f_handler = logging.FileHandler(filename=log_path + filename, encoding='utf-8')
    c_handler.setLevel(stream_level)
    f_handler.setLevel(file_level)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    
    # Set logger logging level
    logger.setLevel(logger_level)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    return logger

def add_discord_logger_handler():
    return add_handler('discord', 'discord.log', logging.WARN, logging.DEBUG, logging.DEBUG)

def add_main_logger_handler():
    return add_handler('IRMCTracker','latest.log', logging.INFO,logging.INFO, logging.INFO)

def add_debug_logger_handler():
    return add_handler('IRMCTracker Debug','debug.log', logging.DEBUG,logging.DEBUG, logging.DEBUG)

def get_logger():
    return logging.getLogger('IRMCTracker')
    
def get_debug_logger():
    return logging.getLogger('IRMCTracker Debug')