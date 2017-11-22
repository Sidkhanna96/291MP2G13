# CMPUT 291 - MiniProject 2 - Code for Phase 2
import os

def main():
    # Sort .txt files
    try:
        createSortedfile('terms.txt')
        createSortedfile('years.txt')
        createSortedfile('recs.txt')
    except:
        print("Sorting Failed. Files do not exist!")

    # (1) a hash index on recs.txt with record key as keys and the full record as data.
    CreateRecsIndex()
    # (2) a B+-tree index on terms.txt with terms as keys and record key as data.
    CreateTermsIndex()
    # (3) a B+-tree index on years.txt with years as keys and record key as data.
    CreateYearsIndex()



def CreateRecsIndex():
    # Code to create Hash index for recs.txt

    return


def CreateTermsIndex():
    # Code to create B+-Tree index for terms.txt

    return

def CreateYearsIndex():
    # Code to create B+-Tree index for years.txt

    return




def createSortedfile(filename):
# Function calls linux sort on the .txt files.
# For now the sorted lines are written to s_'filename'. May need to change later
    try:
        o_name = "s_"+filename
        out = open(o_name, "w")
        out.close()
        command = "sort -u -o "+o_name+" "+filename
        print(command)
        os.system(command)
    except:
        print("Sorting Failed.")

if __name__ == '__main__':
    main()
