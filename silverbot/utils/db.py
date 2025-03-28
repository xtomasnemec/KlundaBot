from silverbot.db.base import db
from silverbot.db.pet import Character


def init_db():
    db.create_tables([Character])
