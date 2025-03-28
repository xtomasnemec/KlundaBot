from peewee import *

db = SqliteDatabase("silverbot.db")


class BaseModel(Model):
    class Meta:
        database = db
