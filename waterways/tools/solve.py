from __future__ import division
from xml.etree import cElementTree
from datetime import datetime
from collections import defaultdict
import webbrowser
import os


nodes = []
systems = defaultdict(list)
tally = []
pair=[]
firstnodes = []

now = datetime.now()
print now.strftime("%X"), "Loading OSM..."

systems["xoastline"]=[]

bluelist = open("bluelist.txt", "r")       #Load bluelist --- node IDs manually added as coastline, i.e. where a river exits the bounding box
bluelist = bluelist.read().splitlines()

for x in bluelist:                                
    systems["xoastline"].append(x)                                      #'x' to allow alphabetic sorting later on
    
cyanlist = open("cyanlist.txt", "r")       #Load cyanlist --- node IDs manually declared "OK", i.e. parts of rivers outside the coastline, to be ignored by the script
cyanlist = cyanlist.read().splitlines()

for x in cyanlist:                                
    systems["cyan"].append(x)

size = os.path.getsize("tmp/waterways.osm")
size = round(size/(1024*1024*1024),1)
print size, "GB"

with open("tmp/waterways.osm", "rt") as f: #Load osm
    tree = cElementTree.parse(f)

irrigation = 0
irricanal = 0
for way in tree.findall('way'):
    nodes = []
    for node in way.findall('nd'):                                      #generate table: source -> drains
        ref = node.attrib.get('ref')
        nodes.append(ref)

    drain = nodes[-1]

    firstnodes.append(nodes[0])
    nodes.pop()
    
    for tag in way.findall('tag'):                                      #separate coastlines
        if ((tag.attrib.get('k') == "natural") and (tag.attrib.get('v') == "coastline")):
            drain = "xoastline"
            nodes.append(ref)                                           #re-add last node
    
    systems[drain].extend(nodes)

now = datetime.now()
print now.strftime("%X"), "Filtering..."
drains = systems.keys() 
drains.extend(firstnodes)
drains.append("sea")
drains.sort(reverse= True)
drainslist = set(drains)
                       
for x in systems:                                                       #filter for start, end and junction nodes
    systems[x] = drainslist & set(systems[x])
    systems[x] = list(systems[x])

now = datetime.now()
print now.strftime("%X"), "Solving..."
  
i=0
for river in drains:                                                    #create waterway systems, going upstream
     
    i+=1
    out = river
    if river == "xoastline":                                            #"sea" or end node of system 
        out = "sea"
        
        
    j=0
    while j < len(systems[river]):                                      #go though upstream nodes of waterway, find waterways that drain into this node, combine
        findnode = systems[river][j]
        systems[out].extend(systems[findnode])
        systems[findnode]=[]

        j+=1

for x in systems:                                                       #filters out waterways that drain elsewhere
    if len(systems[x])>0:
        systems[x].append(x)

 
for x in systems:                                                       #sum up: endnodes, number of nodes that drain into it
    if len(systems[x])>0:
        pair =[]
        pair.append(len(systems[x]))
        pair.append(x)
        tally.append(pair)

 
tally.sort(reverse=False)
for x in tally:                                                         #amber = largest system that does not drain into sea
    if x[1][2] != "a":
        amberlist = x[1]
        

bluepool = []                                                           #all nodes draining to sea
bluepool.extend(systems["xoastline"])
bluepool.extend(systems["sea"])
blueset = set(bluepool)

amberpool = []                                                          #nodes of the amber system
amberpool.extend(systems[amberlist])

cyanpool = []                                                           #nodes draining into nodes declared in cyanlist
cyanpool.extend(systems["cyan"])


redlist = []                                                            #systems with any upstream point also part of bluepool, but end node != "sea"
redpool = []

now = datetime.now()
print now.strftime("%X"), "Creating reds..."

for x in systems:                                                       #creating redlist/redpool
    if x == "xoastline":
        continue
    if x == "sea":
        continue
    if x == amberlist:
        continue
    if x == "cyan":
        continue
    redset = blueset & set(systems[x])
    if len(redset)>0:
        pair =[]

        pair.append(len(systems[x]))#0 count
        pair.append(x)              #1 end node
        pair.append(systems[x])     #2 source nodes
        pair.append([])             #3 for way IDs
        redlist.append(pair)
        
        redpool.extend(systems[x])

redlist.sort(reverse=True)
amberways=[]
cyanways=[]

now = datetime.now()
print now.strftime("%X"), "Assigning colour tags..."

colours = defaultdict(list)

for x in cyanpool:
    colours[x] = "cyan"
for x in amberpool:
    colours[x] = "amber"
for x in redpool:
    colours[x] = "red"
for x in bluepool:
    colours[x] = "blue"
    
red = 0
amber = 0
grey = 0
cyan = 0
blue = 0

for way in tree.findall('way'):                                         #add colour tag to ways and count

    wayID = way.attrib.get('id')
    for node in way.findall('nd'): 
        ref = node.attrib.get('ref')
    
    # red = ref in redpool
    # blue = ref in bluepool
    # amber = ref in amberpool
    # cyan = ref in cyanpool
    # lost = ref in drains
    
    tag = cElementTree.Element("tag")
    tag.set("k", "colour")

    if  colours[ref] == "amber":
        tag.set("v", "amber")
        amberways.append(wayID)
        amber+=1
        
    elif  colours[ref] == "cyan":
        tag.set("v", "cyan")
        cyanways.append(wayID)
        cyan+=1
    
    elif  colours[ref] == "red":
        tag.set("v", "red")
        red+=1
        for x in redlist:
            if (ref in x[2]):
                x[3].append(wayID)
                
    elif colours[ref] == "blue":
        tag.set("v", "blue")
        blue+=1           
  
    else:
        tag.set("v", "grey")
        grey+=1
    
    way.insert(1,tag)

print "blue", blue
print "amber", amber
print "red", red
print "grey", grey
print "cyan", cyan
total = (blue+red+grey+amber+cyan)
print "total", total

now = datetime.now()
print now.strftime("%X"), "Writing html..."

g = open("tmp/rivers.html",'wb')                #html output page

header = """
<html>
<head>
<style>
table, th, td {
  border: 1px solid black;
}
</style>
</head>
<body>
<table style="width:100%">
  <tr>
    <th>Amber</th>
    <th>Amberurl</th>
    <th>Red</th>
    <th>Redurl</th>
  </tr>
  <tr>"""

ambercell = """<td>""" + str(len(tally)-len(redlist)-3) + """</td>"""
redcell = """<td>""" + str(len(redlist)) + """</td>"""

amberurl = ""

for y in amberways:                                                     #all elements in system
    amberurl = amberurl + "way(" + str(y) + ");" 

overpasslimit = 1000000                                                 #kind of redundant since url uses JOSM remote

if len(amberurl)>overpasslimit:
    filename = amberlist + ".html"
    outfile = open(filename, 'w')
    amberurl = """<a href=""" "https://overpass-turbo.eu/?Q=''><br>(" + amberurl + ");(._;>;);out meta;"
    outfile.write(amberurl)
    amberurl = """<td><a href=""" + filename + """ target='_blank'>"""
else:
    amberurl = """<td><a href=""" "http://127.0.0.1:8111/import?url=https://overpass-api.de/api/interpreter?data=(" + amberurl     
    amberurl = amberurl + ");(._;&gt;;);out%20meta; target='_blank'>"

amberurl = amberurl + amberlist + "</a>" + """<br>""" + """</td>"""

redcount = min(100, max(int(len(redlist)/2), 10))                       #output 50% of red systems, min 10, max 100

urlcell = ""
i=0
stubsquery = ""

for x in redlist:                                                       #all red systems
    i+=1
   
    query = "" 
    for y in x[3]:                                                      #all elements in system
        query += "way(" + y + ");" 
            
    if i<redcount:
        urlcell += str(x[0]) + ": "
    
        if len(query)>overpasslimit:
            filename = x[1] + ".html"
            outfile = open(filename, 'w')
            redurl = """<a href=""" "https://overpass-turbo.eu/?Q=''><br>(" + query   + ");(._;>;);out meta;"
            outfile.write(redurl)
            redurl = """<a href=""" + filename + """ target='_blank'>"""
        else:
            redurl = """<a href=""" "http://127.0.0.1:8111/import?new_layer=true&url=https://overpass-api.de/api/interpreter?data=(" + query     
            redurl = redurl + ");(._;&gt;;);out%20meta; target='_blank'>"
        urlcell += redurl + x[1] + "</a>" + """<br>"""
        
    if x[0]==2:
        stubsquery += query

filename = "stubs.html"                         #stubs = single waterways pointing away from the sea
outfile = open(filename, 'w')
stubsquery = "(" + stubsquery + ");out geom;"
outfile.write(stubsquery) 
            
urlcell = """<td>""" + urlcell + """</td>"""

footer = """</tr></table></body>
</html>"""

table = """<td><a href='https://overpass-api.de/api/status' target='_blank'>Status</a></td>""" + header + ambercell + amberurl + redcell + urlcell


g.write(table)
g.close()

with open(r'tmp/rivers-stats.html', "r") as stats:                        #nice stats html
    page = stats.read()


blueperc = round(blue/total*100)
amberperc = round(amber/total*100)
redperc = round(red/total*100)
cyanperc = round(cyan/total*100)
greyperc = 100 - blueperc - amberperc - redperc - cyanperc

now = datetime.now()
page += """<table>
  <tr>
    <th>""" + now.strftime("%x") + """</th>
    <th id="blue" width=" """ + str(blueperc) + """%"> """ + str(blue) + """</th>
    <th id="amber" width=" """ + str(amberperc) + """%"> """ + str(amber) + """</th>
    <th id="red" width=" """ + str(redperc) + """%"> """ + str(red) + """</th>
    <th id="grey" width=" """ + str(greyperc) + """%"> """ + str(grey) + """</th>
    <th id="cyan" width=" """ + str(cyanperc) + """%"> """ + str(cyan) + """</th>
  </tr>
</table>"""
with open(r'tmp/rivers-stats.html', "w") as stats:
    stats.write(page)

webbrowser.open('file://' + os.path.realpath('tmp/rivers-stats.html'))
webbrowser.open('file://' + os.path.realpath('tmp/rivers.html'))

now = datetime.now()
print now.strftime("%X"), "Writing osm..."                              #osm output file to draw nice pic in Maperitive

tree.write("tmp/waterways.osm")

now = datetime.now()
print now.strftime("%X"), "End..." 