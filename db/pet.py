from peewee import *

from db.base import BaseModel


class Character(BaseModel):
    gif = CharField(unique=True)
    name = CharField()
    is_oc = BooleanField()
    owner = CharField(null=True)
    priority = IntegerField(default=0)

    @staticmethod
    def get_characters():
        return [
            [c.gif, c.name]
            for c in Character.select().where(Character.is_oc == False).order_by(-Character.priority, Character.name)
        ]

    @staticmethod
    def get_ocs():
        return [[c.gif, c.name, c.owner] for c in Character.select().where(Character.is_oc == True)]
