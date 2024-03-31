from db.base import db
from db.pet import Character


def init_db():
    db.create_tables([Character])
