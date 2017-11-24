from bsddb3 import db

database = db.DB()
DB_File = "ye.idx"

database.open(DB_File, None, db.DB_BTREE, db.DB_DIRTY_READ)

curs = database.cursor()

title = input("Enter a title for your query: ")
#print("Your title: "+title)

iter = curs.first()
while iter:
    print(iter)
    iter = curs.next()