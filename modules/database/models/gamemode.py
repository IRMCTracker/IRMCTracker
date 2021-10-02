from modules.database.basemodel import *

class Gamemode(BaseModel):
    id = PrimaryKeyField()
    name = CharField(255, unique=True)

    class Meta:
        table_name = 'gamemodes'
