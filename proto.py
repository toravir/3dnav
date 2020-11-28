#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import math
import wget
import time

# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("testRoute.gpx")
collection = DOMTree.documentElement
if collection.hasAttribute("gpx"):
   print "Root element : %s" % collection.getAttribute("gpx")

trkPts = collection.getElementsByTagName("trkpt")
numPts = len(trkPts)
outFileNum = 1

# Print detail of each movie.
for idx in xrange(0, numPts-1):
   trkPt = trkPts[idx]
   nxtPt = trkPts[idx+1]
   #print "*****Trk Pt*****"
   curLat = 0.0
   curLon = 0.0
   nxtLat = 0.0
   nxtLon = 0.0

   if trkPt.hasAttribute("lat"):
      #print "curLat: %s" % trkPt.getAttribute("lat")
      curLat = float(trkPt.getAttribute("lat"))
   if trkPt.hasAttribute("lon"):
      #print "curLon: %s" % trkPt.getAttribute("lon")
      curLon = float(trkPt.getAttribute("lon"))

   if nxtPt.hasAttribute("lat"):
      #print "nxtLat: %s" % nxtPt.getAttribute("lat")
      nxtLat = float(nxtPt.getAttribute("lat"))
   if nxtPt.hasAttribute("lon"):
      #print "nxtLon: %s" % trkPt.getAttribute("lon")
      nxtLon = float(nxtPt.getAttribute("lon"))

   #error check if all tags/attrib are present

   elev = trkPt.getElementsByTagName('ele')[0]

   dlon = curLon - nxtLon
   dlat = curLat - nxtLat
   heading = 0
   if (dlon == 0) and (dlat == 0):
       # We did not move ?? we should ignore
       continue
   if (dlon == 0):
       #we are moving along the same Longitude (NS)
       if (curLat > nxtLat):
           heading = 0
       else:
           heading = 180
   if (dlat == 0):
       #we are moving along the same Latitude (EW)
       if (curLon > nxtLon):
           heading = 270
       else:
           heading = 90

   # If the distance between two points are large, then 
   # make up some points 

   # If the distance between two points are small, then
   # drop some points

   if (dlon != 0) and (dlat !=0):
       slope = dlat/dlon
       deg = math.degrees(math.atan(slope))
       # if deg is +ve, we need to subtract from 90 - so that we
       # get the angle from the top
       # if deg is -ve, we need to add the absolute value of deg to
       # 90 - the angle from the top to horizontal
       deg = 90 - deg
       if (curLon > nxtLon):
           # we are heading west
           deg += 180
       heading = deg

   print "&location="+str(curLat)+","+str(curLon)+"&heading="+str(heading)
   url = "https://maps.googleapis.com/maps/api/streetview?&size=1024x1024&fov=60&pitch=-5&key=AIzaSyBgKuwtOS-Az4nEJF188AbRE1fMnHOv2aA"
   url=url+"&location="+str(curLat)+","+str(curLon)+"&heading="+str(heading)
   wget.download(url, out=str(outFileNum)+".jpg")
   time.sleep(1)
   outFileNum=outFileNum+1
   #print "Elev: %s" % elev.childNodes[0].data
