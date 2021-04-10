import os

urls = open("tmp/urls.txt", "r")                  #Load urls
urls = urls.read().splitlines()

text = ""
unite = ""
for x in urls:

    x = x.rsplit(" ",1)
    
    crop = " "
    if len(x) > 1:
        crop = " -b=" + x[1] + " --complete-ways "
        # -b=-40,10,80,50 --complete-ways 

    url=x[0]
    

    
    line1 = "tools\wget -P tmp " + url
 
    url = url.rsplit("/",1)
    infile = url[1] 
    url = url[1].rsplit("-",1)
    url = url[0]
    outfile = "tmp/" + url + ".o5m"                           #merge regions in osmconvert
    unite = unite + outfile + " "
    outfile = "-o=" + outfile 
    
    line2 = "tools\osmconvert64-0.8.8p tmp/" + infile + crop + outfile
  
    text = text + (line1) + "\n"
    text = text + (line2) + "\n" + "\n"

unite = ("tools\osmconvert64-0.8.8p.exe " + unite)
text = text + unite + "-o=tmp/rivers.o5m"

print text
with open(r'tmp/prepare.bat', "w") as prepare:
    prepare.write((text))   