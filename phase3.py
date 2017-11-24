from bsddb3 import db
import re

def main():
    query = input("Enter your query: ")
    ProcessQuery(query)

def ProcessQuery(query):
    database1 = db.DB()
    database2 = db.DB()
    database3 = db.DB()
    database1.set_flags(db.DB_DUP)
    database2.set_flags(db.DB_DUP)
    database3.set_flags(db.DB_DUP)
    DB_File1 = "te.idx"
    DB_File2 = "ye.idx"
    DB_File3 = "re.idx"
    
    database1.open(DB_File1, None, db.DB_BTREE, db.DB_DIRTY_READ)
    database2.open(DB_File2, None, db.DB_BTREE, db.DB_DIRTY_READ)
    database3.open(DB_File3, None, db.DB_HASH, db.DB_DIRTY_READ)
    
    curs1 = database1.cursor()  
    curs2 = database2.cursor()  
    curs3 = database3.cursor()  

    term_type = ""
    value = ""
    
    # query_vals = re.split(r'[^0-9a-zA-Z_]',query)
    for char in query:
        if(char == ":"):
            term_type = query.split(":")[0]
            value = query.split(":")[1]


    if(term_type == 'title'):
       TitleSearch(value, curs1)
    
    elif(term_type=='author'):
        AuthorSearch(value, curs1)

    elif(term_type=='other'):
       OtherSearch(value,curs1)

    elif(term_type=='year'): 
       YearSearch(value,curs2)



def YearSearch(value, curs2):
    result = curs2.set(value.encode("utf-8"))
    print(result[1].decode("utf-8"))
    dup = curs2.next_dup()
    while(dup != None):
        print(dup[1].decode("utf-8"))
        dup = curs2.next_dup()

def OtherSearch(value, curs1):
    t_value = "o-"+value
    result = curs1.set(t_value.encode("utf-8"))
    print(result[1].decode("utf-8"))
    dup = curs1.next_dup()
    while(dup != None):
        print(dup[1].decode("utf-8"))
        dup = curs1.next_dup()

def AuthorSearch(value, curs1):
    t_value = "a-"+value
    result = curs1.set(t_value.encode("utf-8"))
    print(result[1].decode("utf-8"))
    dup = curs1.next_dup()
    while(dup != None):
        print(dup[1].decode("utf-8"))
        dup = curs1.next_dup()

def TitleSearch(value, curs1):
    t_value = "t-"+value
    result = curs1.set(t_value.encode("utf-8"))
    print(result[1].decode("utf-8"))
    dup = curs1.next_dup()
    while(dup != None):
        print(dup[1].decode("utf-8"))
        dup = curs1.next_dup()

    
if __name__ == '__main__':
    main()