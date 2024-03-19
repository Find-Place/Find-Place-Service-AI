from model.Db import Db
def create_db():
    database = Db()
    database.cofig_schema()
    database.insert()
    database.index()
    database.database.load()
    return database.database

def connect_db():
    database = Db()
    database.cofig_schema()
    database.database.load()
    return database.database


def drop():
    Db().reset_collection()