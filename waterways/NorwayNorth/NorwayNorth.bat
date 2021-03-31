REM 20210311
REM ------------------- REPLACE <YOUR FOLDER> WINDOWS STYLE (WITH \ AS SEPARATOR) -------------------

cd <YOUR FOLDER>\waterways\tmp
del * /Q

copy /y %~dp0"rivers - stats.html"

REM -------------------                   BEGINNING PREPARE.TXT                   ------------------- 
REM -------------------           TO CROP AN AREA ADD TO THE .o5m LINE            -------------------
REM -------------------     -b=<WEST>,<SOUTH>,<EAST>,<NORTH> --complete-ways      -------------------

<YOUR FOLDER>\waterways\tools\wget http://download.geofabrik.de/europe/norway-latest.osm.pbf
<YOUR FOLDER>\waterways\tools\osmconvert64-0.8.8p norway-latest.osm.pbf -b=3,66,34,85 --complete-ways -o=norway-latest.o5m

<YOUR FOLDER>\waterways\tools\wget http://download.geofabrik.de/europe/finland-latest.osm.pbf
<YOUR FOLDER>\waterways\tools\osmconvert64-0.8.8p finland-latest.osm.pbf -o=finland-latest.o5m

<YOUR FOLDER>\waterways\tools\osmconvert64-0.8.8p.exe norway-latest.o5m finland-latest.o5m -o=rivers.o5m

REM -------------------                END PREPARE.TXT                  ------------------- 

<YOUR FOLDER>\waterways\tools\osmfilter.exe rivers.o5m --keep= --keep-ways="natural=coastline waterway= ( man_made=pipeline and type=water ) ( man_made=pipeline and substance=water )" --drop="waterway=fairway waterway=lock_gate waterway=riverbank waterway=dam" >waterways.osm

<YOUR FOLDER>\waterways\tools\solve.py

copy /y "rivers - stats.html" %~dp0"rivers - stats.html"
copy /y "rivers.html" %~dp0"rivers.html"

<YOUR FOLDER>\waterways\tools\Maperitive.exe

pause