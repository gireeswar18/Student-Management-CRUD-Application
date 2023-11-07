import sqlite3
mydb = sqlite3.connect("project.db")
c = mydb.cursor()
try:
    c.execute("create table student (regno varchar(255), name varchar(255), email varchar(255), mobile varchar(255))")
    print("Done")

except:
    print("Fail")