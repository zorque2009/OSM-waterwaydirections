# ------------------- REPLACE <YOUR FOLDER> WINDOWS STYLE (WITH \ AS SEPARATOR) -------------------
# ------------------- REPLACE <YOUR FOLDER UNIX> UNIX STYLE (WITH / AS SEPARATOR) -------------------

urls = open("<YOUR FOLDER UNIX>/waterways/tmp/urls.txt", "r")                  #Load urls
urls = urls.read().splitlines()

text = ""
unite = ""
for x in urls:

    line1 = "<YOUR FOLDER>\waterways\tools\wget " + x
    print repr(line1)
 
    x = x.rsplit("/",1)
    infile = x[1] 
    x = x[1].rsplit("-",1)
    x = x[0]
    outfile = x + ".o5m"
    unite = unite + outfile + " "
    outfile = "-o=" + outfile 
    
    outfile = "-o=" + x + ".o5m"
    
    line2 = "<YOUR FOLDER>\waterways\tools\osmconvert64-0.8.8p " + infile + " " + outfile
    print repr(line2)
  
    text = text + repr(line1) + "\n"
    text = text + repr(line2) + "\n" + "\n"

unite = repr("<YOUR FOLDER>\waterways\tools\osmconvert64-0.8.8p.exe " + unite)
text = text + unite + "-o=rivers.o5m"

with open(r'<YOUR FOLDER UNIX>/waterways/tmp/prepare.txt', "w") as prepare:
    prepare.write((text))
    

nothing = raw_input('done')

    
