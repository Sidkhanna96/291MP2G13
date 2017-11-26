# CMPUT 291 - MiniProject 2 - Code for Phase 2
import os
import subprocess

def main():
	# Sort .txt files
	try:
		createSortedfile('terms.txt')
		createSortedfile('years.txt')
		createSortedfile('recs.txt')
	except:
		print("Sorting Failed. Files do not exist!")


	try:
		# (1) a hash index on recs.txt with record key as keys and the full record as data.
		CreateIndex('s_recs.txt')
		# (2) a B+-tree index on terms.txt with terms as keys and record key as data.
		CreateIndex('s_terms.txt')
		# (3) a B+-tree index on years.txt with years as keys and record key as data.
		CreateIndex('s_years.txt')
	except:
		print("Could not create index files.")
	return

def CreateIndex(sorted_filename):
	try:
		# Code to create Hash index for recs.txt
		# first create new files for removing Backslash
		noBackSlashFile = "noBack" + sorted_filename
		out = open(noBackSlashFile, "w")
		out.close()
		command = "perl break.pl" + " <" + sorted_filename + "> " + noBackSlashFile
		print(command)
		os.system(command)
		IndexFilename = sorted_filename[2:3] + "e.idx"
		print(IndexFilename)
		if sorted_filename[2:3] == 'r':
			commandForIdx = "< " + noBackSlashFile + " db_load -T -c duplicates=1 -t hash " + IndexFilename
		else:
			commandForIdx = "< " + noBackSlashFile + " db_load -T -c duplicates=1 -t btree " + IndexFilename
		print(commandForIdx)
		os.system(commandForIdx)
	except:
		print("Could not create File with no Backslash or Index file could not be created.")
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
