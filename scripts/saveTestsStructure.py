import sys
import os
import re

# First parameter is a relative path to the
# folder u want to list the tests of
# second is optional == regex for tests files
regex = ".*-tests\.cpp$"
outputfile = 'structureOutput.txt'
if len(sys.argv) > 1:
    pathToTests = sys.argv[1]
    if len(sys.argv) > 2:
        outputfile = sys.argv[2]
        if(len(sys.argv) > 3):
            regex = sys.argv[3]
else:
    exitstr = "This script requires at least 1 parameter:\n"
    exitstr += "  1: Path to the folder you wish to list all tests of.\n"
    exitstr += "  2: (Optional) The path/name of the output file. Defaults to '"+outputfile+"'.\n      !This file will be overwritten!\n"
    exitstr += "  3: (Optional) The regex you wish to use on all filenames. Defaults to '"+regex+"' \n"
    sys.exit(exitstr)

# little info for user
print("Listing all files in folder: " + pathToTests)
print("Searching for files matching this Regex: " + regex)
print("Outputting structured list to: " + outputfile)

# clear out file
open(outputfile, 'w').close()
# open output file for res
outFile = open(outputfile, "w")

# list all folders
def scan_folder(folder, depth):
    for entry in os.listdir(folder):
        temp = ""
        for x in range(depth):
            temp += "- "
        # only print if matches the right regex
        if re.match(regex, entry):
            outFile.write(temp + entry + "\n")
        if os.path.isdir(os.path.join(folder, entry)):
            #always print subfolders
            outFile.write(temp + entry + "\n")
            scan_folder(os.path.join(folder, entry), depth + 1)
  
scan_folder(pathToTests, 0)

outFile.close()