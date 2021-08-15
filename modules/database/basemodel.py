from peewee import *
from modules.database.foundation import database

class LongTextField(TextField):
    field_type = 'LONGTEXT'

class BaseModel(Model):
    class Meta:
        database = database