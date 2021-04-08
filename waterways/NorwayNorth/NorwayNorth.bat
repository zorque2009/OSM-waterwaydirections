REM 20210402

cd..
cd tmp
del * /Q

copy /y %~dp0"rivers-stats.html"

cd..

REM -------------------                   BEGINNING PREPARE.TXT                   ------------------- 
REM -------------------           TO CROP AN AREA ADD TO THE .o5m LINE            -------------------
REM -------------------     -b=<WEST>,<SOUTH>,<EAST>,<NORTH> --complete-ways      -------------------

tools\wget -P tmp http://download.geofabrik.de/europe/norway-latest.osm.pbf
tools\osmconvert64-0.8.8p tmp/norway-latest.osm.pbf -b=3,66,34,85 --complete-ways -o=tmp/norway.o5m

tools\wget -P tmp http://download.geofabrik.de/europe/finland-latest.osm.pbf
tools\osmconvert64-0.8.8p tmp/finland-latest.osm.pbf -o=tmp/finland.o5m

tools\osmconvert64-0.8.8p.exe tmp/norway.o5m tmp/finland.o5m -o=tmp/rivers.o5m

REM -------------------                END PREPARE.TXT                  ------------------- 

tools\osmfilter.exe tmp\rivers.o5m --keep= --keep-ways="natural=coastline waterway= ( man_made=pipeline and type=water ) ( man_made=pipeline and substance=water )" --drop="waterway=fairway waterway=lock_gate waterway=riverbank waterway=dam" >tmp/waterways.osm



tools\solve.py

cd tmp
copy /y "rivers-stats.html" %~dp0"rivers-stats.html"
copy /y "rivers.html" %~dp0"rivers.html"

cd..
tools\Maperitive\Maperitive.exe

pause