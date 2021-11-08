from modules.database.basemodel import *

class Player(BaseModel):
    id = PrimaryKeyField()
    username = CharField(150, unique=True)
    uuid = CharField(255, unique=True)
    hypixel_data = LongTextField(null=True)
    minecraft_data = LongTextField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'players'
