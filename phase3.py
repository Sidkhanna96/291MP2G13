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
    key_value_list=[]
    split_char_list=[":","<",">"]
    char_bool=False
    if(len(query)>2):
    split_query=query.split()
    for aquery in split_query:
        for char in aquery:
            if(char in split_char_list):
                small_list=[]
                term_type = aquery.split(char)[0]
                small_list.append(term_type)
                value = aquery.split(char)[1]
                small_list.append(value)
                key_value_list.append(small_list)
                char_bool=True
                break
        if(char_bool==False):
            small_list=[]
            term_type="tao"
            small_list.append(term_type)
            value=aquery
            small_list.append(value)
            split_char_list.append(small_list)
        char_bool=False

                    
    for query_pair in key_value_list:    
        if(query_pair[0] == 'title'):
            TitleSearch(query_pair[1], curs1)
        
        elif(query_pair[0]=='author'):
            AuthorSearch(query_pair[1], curs1)
    
        elif(query_pair[0]=='other'):
            OtherSearch(query_pair[1],curs1)
    
        elif(query_pair[0]=='year'): 
            YearSearch(query_pair[1],curs2)
        
        elif(query_pair[0]=='tao'):
            BlanketSearch(query_pair[1],curs1) #what curs_ do I use?


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
        
def BlanketSearch(value, curs1):#? currently copy pasted need to change t_value, etc.
    t_value = "t-"+value
    result = curs1.set(t_value.encode("utf-8"))
    print(result[1].decode("utf-8"))
    dup = curs1.next_dup()
    while(dup != None):
        print(dup[1].decode("utf-8"))
        dup = curs1.next_dup()        

    
if __name__ == '__main__':
    main()