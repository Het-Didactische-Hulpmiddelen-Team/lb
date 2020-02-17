import sys
import os
import re
from lbdir import lbDir
from lbfile import lbFile

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

strToAddToHTML = ""
f = open(inputfilepath,'r')
all_lines = f.readlines()
f.close()
elements = []

# inlezen van de file
def getDepth(line):
    return len(re.findall(r"(- )",line))

tempParent = ["none"]
def lastParent():
    return tempParent[len(tempParent) - 1]

for i in range(0, len(all_lines)):
    if i < len(all_lines)-1:
        if getDepth(all_lines[i]) < getDepth(all_lines[i + 1]):
            if getDepth(all_lines[i]) == 0:
                tempParent = ["none"]
            else:
                if getDepth(all_lines[i - 1]) != 0:
                    if getDepth(all_lines[i]) != getDepth(all_lines[i - 1]):
                        tempParent.pop()
            elements.append(lbDir(lastParent(), all_lines[i]))
            tempParent.append(all_lines[i])
        else:
            elements.append(lbFile(lastParent(), all_lines[i]))

for x in elements:
    print(x.parent + "  <-->  " + x.name)
def dirToHTML(dr):
    res = "<li><span>"+dr.name.rstrip("\n\r")+"</span><ul>"
    for x in elements:
        if dr.name in x.parent:
            if x.__class__.__name__ == "lbFile":
                res += "<li>"+x.name.rstrip("\n\r")+"</li>"
            elif x.__class__.__name__ == "lbDir":
                res += dirToHTML(x)
    res += "</ul></li>"
    return res

strToAddToHTML += "<ul>"
for dirr in elements:
    if dirr.__class__.__name__ == "lbDir" and dirr.parent == "none":
        # top mapke, 0 depth
        strToAddToHTML += dirToHTML(dirr)
strToAddToHTML += "</ul>" 

outputfile = open(outputhtmlfilepath, 'r')
regex = r"(<div.*id=\w*[\"\']"+idofelement+"[\"\'].*>[\r\n]*)(?:.*[\r\n])*?(.*<\/div>)"
out = re.sub(regex, r"\1"+strToAddToHTML+r"\n\2", outputfile.read())
outputfile.close()

# write to file
outf = open(outputhtmlfilepath, "w")
outf.write(out)
outf.close()