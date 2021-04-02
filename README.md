# OSM-waterwaydirections
A script to detect unconnected and reversed waterways in the OSM database.

Please follow the steps below to make it work, and bear with me, this whole project is beyond my actual coding capabilities, but it runs on my system.

## 1. Make it run
```
\NorwayNorth\NorwayNorth.bat
\tools\prepare.py
\tools\solve.py
```
Replace <YOUR FOLDER> Windows style (with \ as separator)
Replace <YOUR FOLDER UNIX> Unix style (with / as separator)
  
The script is looking in \tools for links to 
- wget
- osmconvert
- osmfilter
- maperitive 

## 2. Prepare your region
It's best to copy the sample folder for each region you want to investigate. 
```
\NorwayNorth\urls.txt
```
Add the download urls from geofabrik.de of the desired region(s), one per line.  There is no limit to the number of files, but too large an output file will crash the system.
Copy the file to the \tmp folder and run \tools\prepare.py
This will create a file tmp\prepare.txt 
You need to remove the ``` ' ``` from the .txt file.

Copy the content of tmp\prepare.txt into your .bat file between the highlighted lines. Add crop command if needed (see sample file or osmconvert documentation)

## 3. Run the script
run the .bat file
Once the files have been downloaded, converted, merged and filtered, the command prompt will tell you the size of the .osm-file. My system can cope with something below 5GB. The processing (without downloading time and wrting of the output file for Maperitive) takes about 10min. Larger files may bring down the system.

## 4. Output
Two .html pages will pop up. One with the faults in the waterways: Amber = the longest system that ends in a single point which is not the coastline, Red = systems of waterways that flow uphill from any point that's connected to the coastline. URLs will open in Josm. Also note the 'Status' URL at the top to show your api rata.
The second .html contains some stats.
Eventually (this can take 30mins) Maperitive will open with a map depicting the findings in blue, amber, red. The respective ruleset is located in \tools
