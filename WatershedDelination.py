# pip install geojson   # Needed to make the GeoJSON files
#I had ArcGIS Desktop 10.6 so the other libraries were included with ArcGIS.
#Bill Chappell 1/2019 for John Clune.

'''
Project was to take a list of points and have the USGS site return a delinated watershed boundary for it.
My point file has a couple hundred points, so this script wil read a file and passd the Lat, Lng to the api
and take the response and formated a GeoJSON file for it. From there I converted the new watershed polygons
to Esri Shapefiles using GDAL/OGR library.

Note: Sometimes the process failed, maybe memory issue, internet, USGS, whatever caused it. I just checked
my folder for the last file, and removed from my point file the ones done and restarted it.
'''

import json
import requests
from geojson import Polygon, Feature, FeatureCollection, dump

# My test file of points has a record number (ID), a SiteName, Lat, Lng as a CSV, No Header
with open("c:/usgs/NewPts.csv", 'r') as f:
    for line in f:
        print("working on")
        print (line)
        b = line.split(",")

        theID = b[0]  
        theSite = b[1]  
        theLat = b[2]   
        theLng = b[3]

        url = 'https://streamstats.usgs.gov/streamstatsservices/watershed.geojson'

        # rcode is the state, (Pennsylvania)
        payload = {'rcode':'PA','xlocation':theLng,'ylocation':theLat,'crs':4326,'includeparameters':'false','includeflowtypes':'false','includefeatures':'true','simplify':'true'}

        r = requests.get(url,params=payload, timeout=None)
                     
        print(r.status_code)

        # The response as text
        obj = r.text

        gjson = json.loads(obj)

        # Creating the GeoJSON structure for the polygon

        #print polygon coordinates
        #print(gjson['featurecollection'][1]['feature']['features'][0]['geometry']['coordinates'])
        features = []
        wsidnumber = theSite

        polycoords = (gjson['featurecollection'][1]['feature']['features'][0]['geometry']['coordinates'])
        polygon = Polygon(polycoords)
        features.append(Feature(geometry=polygon, properties={"wsid": theSite, "link":theID}))

        feature_collection = FeatureCollection(features)

        # Writing the Geojson file
        with open('c:/usgs/new/geojsonfiles/gj'+ theID +'.geojson', 'w') as f:
            dump(feature_collection, f)

        print("Done gj" + theID +" file created")
        print(" ------------------")

print("All Done")


'''
Once I had the GeoJSON files from the service, Using a CMD window, path to the folder
then

dir *.geojson /b > files.txt    gave me a list of the GeoJSON files.txt

Next I had to convert them to Shapefiles. I decided to use the GDAL/OGR library,
it's available online as part of FWTOOLS or OSGEO's package, or just download QGIS.

In the folder were the GeoJSON files were, I just typed in this text to convert the whole folder.

for /R %f in (*.geojson) do ogr2ogr -f "ESRI Shapefile" "%~dpnf.shp" "%f"

'''