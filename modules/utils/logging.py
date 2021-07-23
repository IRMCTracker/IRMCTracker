import logging

def add_handler(name, path, stream_level, file_level, logger_level):
    # Create a custom logger
    logger = logging.getLogger(name)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(path)
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


def add_main_logger_handler():
    return add_handler('IRMCTracker','storage/logs/latest.log', logging.INFO,logging.INFO, logging.INFO)

def add_debug_logger_handler():
    return add_handler('IRMCTracker Debug','storage/logs/debug.log', logging.DEBUG,logging.DEBUG, logging.DEBUG)

def get_logger():
    return logging.getLogger('IRMCTracker')
    
def get_debug_logger():
    return logging.getLogger('IRMCTracker Debug')