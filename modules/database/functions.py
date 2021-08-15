from .foundation import database
from .models import *

tables = [Server, Vote]

def create_tables():
    database.create_tables(tables)