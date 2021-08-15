from modules.database.basemodel import *

class Vote(BaseModel):
    user_id = IntegerField(unique=True)
    vote = CharField(128, unique=False)

    class Meta:
        table_name = 'votes'
