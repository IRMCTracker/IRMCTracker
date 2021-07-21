from .foundation import DB
from .queries import CREATE_TABLES

@DB.execute
def create_tables():
    return CREATE_TABLES