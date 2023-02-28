import sqlite3
import passcodegenerator as p

def lockers():
    conn=sqlite3.connect('main.db')
    cursor=conn.cursor()
    query="SELECT * FROM Packageinfo ORDER BY SUBSTRING(location,4,20)"
    cursor.execute(query)
    conn.commit()
    lockers_info=[]
    for row in cursor:
        lockers_info.append(row)

    conn.close()
    return lockers_info

def add_locker(branch,location):
    password=p.my_password()
    conn=sqlite3.connect('main.db')
    cursor=conn.cursor()
    query="INSERT INTO Packageinfo(Location, Branch, Avail,Passcode) VALUES('{Location}','{Branch}','Yes','{Passcode}')".format(Location=location,Branch=branch,Passcode=password)
    cursor.execute(query)
    conn.commit()
    conn.close()

def check_location():
    conn=sqlite3.connect('main.db')
    cursor=conn.cursor()
    query='SELECT Location FROM packageinfo'
    cursor.execute(query)
    conn.commit()
    check_info=[]
    for row in cursor:
        check_info.append(row[0])

    conn.close()
    return check_info

def edit_locker(location,avail,oid,stagetime):
    conn=sqlite3.connect('main.db')
    cursor=conn.cursor()
    query="UPDATE Packageinfo SET Avail='{avail}', OID='{oid}', StageTime='{stagetime}' WHERE Location='{location}'".format(location=location,avail=avail,oid=oid,stagetime=stagetime)
    cursor.execute(query)
    conn.commit()
    conn.close()

def delete_locker(location,branch):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    query = "DELETE FROM Packageinfo WHERE Location='{location}'".format(location=location)

    cursor.execute(query)
    conn.commit()
    conn.close()

def verify_locker(password,branch):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    query = "SELECT * FROM packageinfo WHERE Passcode='{passcode}' AND Branch='{branch}'".format(passcode=password,branch=branch)
    rows=cursor.execute(query).fetchall()
    if rows:
        zloid=rows[0]
        return zloid
    else:
        return rows
    conn.commit()
    conn.close()


def avail_locker(location):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    query = "UPDATE Packageinfo SET Avail='No', OID='', StageTime='' WHERE Location='{location}'".format(
        location=location)
    cursor.execute(query)
    conn.commit()
    conn.close()

def open_locker(location):
    pass