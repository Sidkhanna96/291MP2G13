import os
import re

def main():
    inputfile = input('Enter file name: ')
    with open(inputfile) as infile:
        # Iterate line by line
        term_file = open("terms.txt", "w")
        year_file = open("years.txt", "w")
        recs_file = open("recs.txt", "w")
        for line in infile:
            # Extract Key
            key = re.findall(r'key="(.*?)"', line)
            try:
                # Extract values for terms.txt - title, author(s), journal, publisher, booktitle

                title = re.findall(r'<title>(.*?)</title>', line)
                # print(title)
                for term in title:
                    index_vals = re.split(r'[^0-9a-zA-Z_]',term)
                    #print(index_vals)
                    for val in index_vals:
                        if(len(val)>2):
                            term_file.write('t-'+val.lower()+':'+key[0]+"\n")

                otherlist = re.findall(r'<journal>(.*?)</journal>', line) \
                            + re.findall(r'<publisher>(.*?)</publisher>',line) \
                            + re.findall(r'<booktitle>(.*?)</booktitle>', line)
                for term in otherlist:
                    index_vals = re.split(r'[^0-9a-zA-Z_]', term)
                    # print(index_vals)
                    for val in index_vals:
                        if (len(val) > 2):
                            term_file.write('o-' + val.lower() + ':' + key[0]+"\n")

                authorlist = re.findall(r'<author>(.*?)</author>', line)
                for term in authorlist:
                    index_vals = re.split(r'[^0-9a-zA-Z_]',term)
                    #print(index_vals)
                    for val in index_vals:
                        if(len(val)>2):
                            term_file.write('a-'+val.lower()+':'+key[0]+"\n")



                # Extract value for years.txt - year
                year = re.findall(r'<year>(.*?)</year>', line)
                year_file.write(year[0]+":"+key[0]+"\n")

                # Extract values for recs.txt
                recs_file.write(key[0]+":"+line)

            except:
                pass
        term_file.close()
        year_file.close()
        recs_file.close()

if __name__ == '__main__':
    try:    #Delete files if exist
        os.remove("terms.txt")
        os.remove("years.txt")
        os.remove("recs.txt")
    except:
        pass
    main()



