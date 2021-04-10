REM 20210409

cd..
cd tmp
del * /Q

copy /y %~dp0"rivers-stats.html"
copy /y %~dp0"urls.txt"

cd..

tools\prepare.py

call tmp\prepare.bat

tools\osmfilter.exe tmp\rivers.o5m --keep= --keep-ways="natural=coastline waterway= ( man_made=pipeline and type=water ) ( man_made=pipeline and substance=water )" --drop="waterway=fairway waterway=lock_gate waterway=riverbank waterway=dam" >tmp/waterways.osm

tools\solve.py

cd tmp
copy /y "rivers - stats.html" %~dp0"rivers-stats.html"
copy /y "rivers.html" %~dp0"rivers.html"

cd..
tools\Maperitive\Maperitive.exe

pause