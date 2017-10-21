import sqlite3
import pymysql
import configparser

def sqlite_create_db(db, schema):
    con = sqlite3.connect(db)
    with con:
        c = con.cursor()
        with open(schema, 'r') as f:
            c.executescript(f.read())

def mysql_create_db(host, user, password, db, schema):
    con = pymysql.connect(host = host, user = user, password = password, db = db)
    with con:
        c = con.cursor()
        with open(schema, 'r') as f:
            c.execute(f.read())

if __name__ == "__main__":
    path = "settings.ini"

    config = configparser.ConfigParser()
    config.read(path)

    db_schema = config.get("db-schema", "schema")
    
    sqlite_db = config.get("sqlite", "file")

    mysql_host = config.get("mysql", "host")
    mysql_user = config.get("mysql", "user")
    mysql_password = config.get("mysql", "password")
    mysql_db = config.get("mysql", "db")

    sqlite_create_db(sqlite_db, db_schema)
    mysql_create_db(mysql_host, mysql_user, mysql_password, mysql_db, db_schema)

