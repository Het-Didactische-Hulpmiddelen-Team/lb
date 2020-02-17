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

strToAddToHTML = "<ul>"
f = open(inputfilepath,'r')
all_lines_variable = f.readlines()
f.close()

def getDepth(line):
    return len(re.findall(r"(- )", line))

for i in range(0, len(all_lines_variable)-1):
    l = all_lines_variable[i].rstrip()
    depth = getDepth(l)
    print(depth)
    if depth == 0:
        strToAddToHTML += "<li> <span>"+l+"</span>"
    elif depth < getDepth(all_lines_variable[i-1]):
        for y in range(getDepth(all_lines_variable[i-1]) - depth): 
            strToAddToHTML += "</ul></li>"
        strToAddToHTML += "<li><span>"+l+"</span>"
    elif depth == getDepth(all_lines_variable[i-1]) + 1:
        if depth == getDepth(all_lines_variable[i+1]):
            strToAddToHTML += "<ul><li>"+l+"</li>"
        elif depth == getDepth(all_lines_variable[i+1]) - 1:
            strToAddToHTML += "<li><span>"+l+"</span>"
    elif depth == getDepth(all_lines_variable[i-1]):
        strToAddToHTML += "<li>"+l+"</li>"
        if depth > getDepth(all_lines_variable[i+1]):
            strToAddToHTML += "</ul> </li>"
 
strToAddToHTML += "</ul>"
print(strToAddToHTML)

outputfile = open(outputhtmlfilepath, 'r')
regex = r"(<div.*id=\w*[\"\']"+idofelement+"[\"\'].*>[\r\n]*)(?:.*[\r\n])*?(.*<\/div>)"
out = re.sub(regex, r"\1TEST\n\2", outputfile.read())
outputfile.close()

# now just print, later change out file
print(out)
