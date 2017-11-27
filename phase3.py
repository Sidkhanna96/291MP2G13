from bsddb3 import db
import re
import shlex
import copy

#Getting the input from the user for the query
def main():
    flag_print = 0
    quit_flag = True
    print("Enter q to exit")
    while(quit_flag):
        query = input("Enter your query: ")
        char = "output"

        #if the user Enters output it will ask for the query again until a proper query is entered
        #it will also set the flag to print accordingly
        while(char in query and " " not in query):
            result = query.split("=")
            #checking if need to print record or just the key
            if(result[1].lower() =='key'):
                flag_print = 0
                query = input("Enter your query: ")
                
            elif(result[1].lower() == 'full'):
                flag_print = 1
                query = input("Enter your query: ")
            else:
            	print("Not correct State")
            	query = input("Enter your query: ")
                    
        if(len(query)==0):
            print("No query was entered")
        elif(query=="q"):
            quit_flag = False
        else:    
            # processing the query to get the values to print
            ProcessQuery(query,flag_print)


def ProcessQuery(query,flag_print):
    #opening the idx databases

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
    
    #creating cursor for the each idx database file
    curs1 = database1.cursor()  
    curs2 = database2.cursor()  
    curs3 = database3.cursor()  

    #declaring variables
    term_type = ""
    value = ""
    key_result_list = []
    key_value_list=[]
    split_char_list=[":","<",">","="]
    char_bool=False
    
	# Split input into separate commands
    split_query=shlex.split(query) 
    # print(split_query)
    #checking the input for the type of query entered
    for aquery in split_query:
        for char in aquery:
            if(char in split_char_list):
                small_list=[]
                term_type = aquery.split(char)[0]
                small_list.append(term_type)
                value = aquery.split(char)[1]
                small_list.append(value.lower())
                small_list.append(char)
                key_value_list.append(small_list)
                char_bool=True
                break

        if(char_bool==False):
            small_list=[]
            term_type="tao"
            small_list.append(term_type)
            value=aquery
            small_list.append(value.lower())
            small_list.append(char)
            key_value_list.append(small_list)
        char_bool=False

    # print(len(key_value_list))
    for quer in key_value_list:
        if("" in quer and len(quer)<=3):
            print("Must have key-value pair")
            return

    key_phrases=[]
    
    for query_pair in key_value_list:
        key_words=query_pair[1].split()
        if(len(key_words)>1): #Range is a Phrase, store phrase and assess search
        		key_phrases.append(query_pair[1])	
        for word in key_words:
            if(len(word) > 2):
                if(query_pair[0] == 'title'):
                    key_result_list.append(TitleSearch(word, curs1))
                
                elif(query_pair[0]=='author'):
                    key_result_list.append(AuthorSearch(word, curs1))
            
                elif(query_pair[0]=='other'):
                    key_result_list.append(OtherSearch(word,curs1))
            
                elif(query_pair[0]=='year'): 
                    if(query_pair[2]=="<"):
                        key_result_list.append(RangeYearSearch(curs2,'0',word))
                    elif(query_pair[2]==">"):
                        key_result_list.append(RangeYearSearch(curs2,word,'999999'))
                    else:
                        key_result_list.append(YearSearch(word,curs2))
               # elif(query_pair[0]=='output'):
               # 	if(query_pair[1].lower() == "full"):
               # 		flag_print = 1
               # 	elif(query_pair[1].lower() == "key"):
               # 		flag_print = 0
                elif(query_pair[0]=='tao'):
                    key_result_list.append(BlanketSearch(word,curs1))
								
	 # Get intersect of results

    key_set = set.intersection(*map(set,key_result_list))
    final_key_list=[]

    for i in key_set:
        final_key_list.append(i)


    final_key_list2 = copy.deepcopy(final_key_list)
    
    # Check if phrase is assessed and matches
    for key_val in final_key_list2:
        #Assess the titles of each key to see if the phrase is in there
        result=curs3.set(key_val.encode("utf-8"))
        if(result!=None):
            # print(key_phrases)
            #Check if all phrases are inside the title, if not then remove key from list
            for phrase in key_phrases:	
            #     if phrase not in result[1].decode("utf-8").lower():
            #         final_key_list.remove(key_val)
                result = re.findall('\\b' + phrase + '\\b', result[1].decode("utf-8").lower(), flags = re.IGNORECASE)
                if len(result)>0:
                    continue
                else:
                    final_key_list.remove(key_val)

    if(len(final_key_list) != 0):
        for i in final_key_list:
            if(flag_print == 0):
                print(i)
            elif(flag_print == 1):
                result = i.encode("utf-8")
                result2 = curs3.set(result)
                print(result2[1].decode("utf-8"))
    else:
        print("Invalid")


    database1.close()
    database2.close()
    database3.close()	 




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
            

def RangeYearSearch(curs2, lower, upper):
    key_list = []
    result = curs2.set_range(lower.encode("utf-8"))
   
    if(result != None):
        while(result != None):
            if(str(result[0].decode("utf-8")[0:len(upper)])>=upper): 
                break
            #print(result[1].decode("utf-8"))
            elif(str(result[0].decode("utf-8")[0:len(upper)])<=lower):
                result = curs2.next()
            else:
                key_list.append(result[1].decode("utf-8"))
                result = curs2.next() 
    return key_list



if __name__ == '__main__':
    main()