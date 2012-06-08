import MySQLdb
import datetime
import time
global db

def open_db():
    global db
    db = MySQLdb.connect(host="localhost",user="root",passwd="1",db="group_talk")
    return db

def close_db():
    global db
    if db is not None:
        db.close()

def insert_users(JID,nickname):
    global db
    if db is None:
        open_db()
    sql = "insert into users (JID,nickname) values (%s,%s)"
    cursor = db.cursor()
    cursor.execute(sql,(JID,nickname))
    cursor.close()

def select_from_users():
    global db
    if db is None:
        open_db()
    sql = "select * from users"
    cursor = db.cursor()
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()

    #for result in results:
    #    print results

def insert_messages(timestamp,nickname,message):
    global db
    if db is None:
        open_db()
    sql = "insert into messages values (null,'hh','hello')"#"insert into messages (send_time,nickname,message) values (%s,%s,%s)"
    cursor = db.cursor()
    cursor.execute(sql)#,(timestamp,nickname,message))
    cursor.close()
if __name__=='__main__':
    open_db()
    dt =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    insert_messages(dt,'hh','hello')
    select_from_users()
    close_db()
