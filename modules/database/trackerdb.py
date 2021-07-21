from .foundation import DB
from .queries import CREATE_SERVERS_TABLE

@DB.execute
def create_tables():
    return [
        CREATE_SERVERS_TABLE
    ]