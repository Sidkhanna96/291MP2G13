from bsddb3 import db
import re
import shlex

def main():
    query = input("Enter your query: ")
    ProcessQuery(query)
    #RangeYearSearch("2006", "2010")

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
    key_result_list = []
    # query_vals = re.split(r'[^0-9a-zA-Z_]',query)
    key_value_list=[]
    split_char_list=[":","<",">"]
    char_bool=False
    split_query=shlex.split(query)
    #print(split_query)
    for aquery in split_query:
        for char in aquery:
            if(char in split_char_list):
                small_list=[]
                term_type = aquery.split(char)[0]
                small_list.append(term_type)
                value = aquery.split(char)[1]
                small_list.append(value.lower())
                key_value_list.append(small_list)
                char_bool=True
                break

        if(char_bool==False):
            small_list=[]
            term_type="tao"
            small_list.append(term_type)
            value=aquery
            small_list.append(value.lower())
            key_value_list.append(small_list)
        char_bool=False
    #print(key_value_list)
           
    for query_pair in key_value_list:    
        key_words=query_pair[1].split()
        for word in key_words:
            if(query_pair[0] == 'title'):
                key_result_list.append(TitleSearch(word, curs1))
            
            elif(query_pair[0]=='author'):
                key_result_list.append(AuthorSearch(word, curs1))
        
            elif(query_pair[0]=='other'):
                key_result_list.append(OtherSearch(word,curs1))
        
            elif(query_pair[0]=='year'): 
                key_result_list.append(YearSearch(word,curs2))
            
            elif(query_pair[0]=='tao'):
                key_result_list.append(BlanketSearch(word,curs1))

# Get intersect of results
    key_set = set.intersection(*map(set,key_result_list))
    for i in key_set:
        print(i)




def BlanketSearch(value, curs1):
    key_list = []
    t_keys = TitleSearch(value, curs1)
    a_keys = AuthorSearch(value, curs1)
    o_keys = OtherSearch(value,curs1)
    for i in t_keys:
        key_list.append(i)
    for i in a_keys:
        key_list.append(i)
    for i in o_keys:
        key_list.append(i)
    return key_list

def YearSearch(value, curs2):
    key_list = []
    result = curs2.set(value.encode("utf-8"))
    if(result!=None):
        #print(result[1].decode("utf-8"))
        key_list.append(result[1].decode("utf-8"))
        dup = curs2.next_dup()
        while(dup != None):
            #print(dup[1].decode("utf-8"))
            key_list.append(dup[1].decode("utf-8"))
            dup = curs2.next_dup()
    return key_list

def OtherSearch(value, curs1):
    t_value = "o-"+value
    key_list = []
    result = curs1.set(t_value.encode("utf-8"))
    if(result!=None):
        #print(result[1].decode("utf-8"))
        key_list.append(result[1].decode("utf-8"))
        dup = curs1.next_dup()
        while(dup != None):
            #print(dup[1].decode("utf-8"))
            key_list.append(dup[1].decode("utf-8"))
            dup = curs1.next_dup()
    return key_list

def AuthorSearch(value, curs1):
    t_value = "a-"+value
    key_list = []
    result = curs1.set(t_value.encode("utf-8"))
    if(result!=None):
        #print(result[1].decode("utf-8"))
        key_list.append(result[1].decode("utf-8"))
        dup = curs1.next_dup()
        while(dup != None):
            #print(dup[1].decode("utf-8"))
            key_list.append(dup[1].decode("utf-8"))
            dup = curs1.next_dup()
    return key_list

def TitleSearch(value, curs1):
    t_value = "t-"+value
    key_list = []
    result = curs1.set(t_value.encode("utf-8"))
    if(result!=None):
        #print(result[1].decode("utf-8"))
        key_list.append(result[1].decode("utf-8"))
        dup = curs1.next_dup()
        while(dup != None):
            key_list.append(dup[1].decode("utf-8"))
            #print(dup[1].decode("utf-8"))
            dup = curs1.next_dup()
    return key_list
            

def RangeYearSearch(lower,upper):
    database2 = db.DB()
    database2.set_flags(db.DB_DUP)
    DB_File2 = "ye.idx"
    database2.open(DB_File2, None, db.DB_BTREE, db.DB_DIRTY_READ)

    curs2 = database2.cursor()  
    key_list = []
    result = curs2.set_range(lower.encode("utf-8")) 
   
    if(result != None):
        while(result != None):
            if(str(result[0].decode("utf-8")[0:len(upper)])>=upper): 
                break
            #print(result[1].decode("utf-8"))
            key_list.append(result[1].decode("utf-8"))
            result = curs2.next() 
    return key_list


if __name__ == '__main__':
    main()