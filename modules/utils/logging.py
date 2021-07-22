import logging

def a():
    return 'b'

def add_handler():
    # Create a custom logger
    logger = logging.getLogger('IRMCTracker')

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('storage/logs/latest.log')
    c_handler.setLevel(logging.ERROR)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    
    # Set logger logging level
    logger.setLevel(logging.DEBUG)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

def get_logger():
    return logging.getLogger('IRMCTracker')