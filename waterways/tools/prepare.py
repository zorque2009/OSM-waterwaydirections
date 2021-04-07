import os

os.chdir("..")

urls = open("tmp/urls.txt", "r")                  #Load urls
urls = urls.read().splitlines()

text = ""
unite = ""
for x in urls:

    line1 = "tools\wget -P tmp " + x
 
    x = x.rsplit("/",1)
    infile = x[1] 
    x = x[1].rsplit("-",1)
    x = x[0]
    outfile = "tmp/" + x + ".o5m"                           #merge regions in osmconvert
    unite = unite + outfile + " "
    outfile = "-o=" + outfile 
    
    line2 = "tools\osmconvert64-0.8.8p tmp/" + infile + " " + outfile
  
    text = text + (line1) + "\n"
    text = text + (line2) + "\n" + "\n"

unite = ("tools\osmconvert64-0.8.8p.exe " + unite)
text = text + unite + "-o=tmp/rivers.o5m"

print text
with open(r'tmp/prepare.txt', "w") as prepare:
    prepare.write((text))
    

nothing = raw_input('done')

    
