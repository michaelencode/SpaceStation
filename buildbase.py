import sqlite3
from sqlite3 import Error

def builder():
    try:
        sqliteConnection=sqlite3.connect('main.db')
        print(sqlite3.version)

        cursor=sqliteConnection.cursor()

        #Create locker information database
        query="CREATE TABLE IF NOT EXISTS Packageinfo(Location TEXT PRIMARY KEY, Branch TEXT, Avail TEXT, OID TEXT, Passcode TEXT, StageTime TEXT)"
        cursor.execute(query)
        print("Main table created")

        #Create clint users info database
        query="CREATE TABLE IF NOT EXISTS Userinfo(Username TEXT PRIMARY KEY, Password TEXT, Branch Text)"
        cursor.execute(query)
        print("Users information database Created")

        #Create history infor database
        query="CREATE TABLE IF NOT EXISTS History(OID TEXT PRIMARY KEY, Branch TEXT, Location TEXT, Passcode TEXT, StageTime TEXT, SignTime TEXT, Signiture BLOB, Photo BLOB)"
        cursor.execute(query)
        print("History information database Created")

        #Create admin info database
        query="CREATE TABLE IF NOT EXISTS Admin(Username TEXT PRIMARY KEY, Password TEXT, Branch TEXT, Email TEXT)"
        cursor.execute(query)
        print("Admin info database Created")


        #Create Password library
        query="CREATE TABLE IF NOT EXISTS Password(Password)"
        cursor.execute(query)
        print("Password library database Created")

        cursor.close()
        sqliteConnection.commit()

    except Error as e:
        print(e)

    if sqliteConnection:
        sqliteConnection.close()


if __name__=="__main__":
    builder()
    print("System database setup successfully!!!")
