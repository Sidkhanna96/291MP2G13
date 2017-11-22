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
