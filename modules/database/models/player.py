from modules.database.basemodel import *

class Player(BaseModel):
    id = PrimaryKeyField()
    username = CharField(150, unique=True)
    uuid = CharField(255, unique=True)
    hypixel_data = LongTextField()
    minecraft_data = LongTextField()

    class Meta:
        table_name = 'players'
