import sys
import os
import re

inputfilepath = ""
outputhtmlfilepath = ""
idofelement = "navigation-menu"

# check if enough args are given
if len(sys.argv) < 3:
    exitstr = "This script requires at least 2 parameter:\n"
    exitstr += "  1: Path/name of the file created by the saveTestsStructure.py.\n"
    exitstr += "  2: Path/name of the html file you want to add the data to.\n"
    exitstr += "  3: (Optional) The id of the DIV element you want the script to create the HTML code in.\n"
    exitstr += "                The div can have other attributes like class, style, ... and van be written in several lines.\n"
    exitstr += "                Defaults to 'navigation-menu'.\n"
    sys.exit(exitstr)

# set variables
inputfilepath = sys.argv[1]
outputhtmlfilepath = sys.argv[2]
if(len(sys.argv) > 3):
    idofelement = sys.argv[3]
    
# printing some info to the terminal for the user    
print("Using "+inputfilepath+" as inputfile")
print("Generated HTML will be added to the file '"+outputhtmlfilepath+"' inside the element with ID '"+idofelement+"'.")

outputfile = open(outputhtmlfilepath, 'r')
regex = r"(<div.*id=\w*[\"\']"+idofelement+"[\"\'].*>[\r\n]*)(?:.*[\r\n])*?(.*<\/div>)"
out = re.sub(regex, r"\1TEST\n\2", outputfile.read())
outputfile.close()

# now just print, later change out file
print(out)