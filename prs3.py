# prs2 - process rail stops
#       goal is to find neighborhood containing each rail stop
#
import fiona
import shapely
from shapely.geometry import shape

# define a class to store information about rail stops

class RailStop:
     nhood = None


     def __init__(self,rs):
          self.stop = rs
          self.geom = shape(self.stop['geometry'])  # this should be a Point
          self.props = self.stop['properties']
          self.name = self.props['STATION']
          self.type = self.props['TYPE']

     def __str__(self):
          print (self.stop) #testing
          return "STOP " + self.name
 
     def getGeom(self):
          return self.geom

     def isMAXstop(self):
          return (self.type == 'MAX')

     def getName(self):
          return (self.name)

     def setNhood(self,nh):
          self.nhood = nh

     def getNhood(self):
          return(self.nhood)

# read all of the rail stops data into an array of Points
        
rstops = [];

with fiona.open("portland-atlas/shp/trimet-rail-stops/tm_rail_stops.shp") as input:
     for item in input:
          rstops.append(RailStop(item))

print ("found ", len(rstops), " trimet rail stops")

mstops = list(filter(lambda rs: RailStop.isMAXstop(rs), rstops))

print ("found ", len(mstops), " MAX stops")

# define a class to store information about neighborhoods

class Neighborhood:

     name = "Unknown"

     def __init__(self,nh):
          self.nhood = nh
          self.geom = shape(self.nhood['geometry'])  # this should be a Polygon
          self.props = self.nhood['properties']
          self.name = self.props['NAME']
          
     def __str__(self):
          return "NEIGHBORHOOD " + self.name
 
     def contains(self,rstop):
          return self.geom.contains(rstop.getGeom())

     def getName(self):
          return self.name

# read all of the neighborhoods into an array of Polygons

nhoods = [];

with fiona.open("portland-atlas/shp/neighborhoods/PortlandNeighborhoods/neighborhoods_pdx.shp") as input:
     for item in input:
          nhoods.append(Neighborhood(item))

print ("found ", len(nhoods), " neighborhoods")

# which neighborhoods contain which rail stops?

for ms in mstops:
     counter = 0
     for nh in nhoods:
          if (nh.contains(ms)):
               ms.setNhood(nh)


# write the stop:nhood info to a new csv file
with open('rstops_nhoods.csv', 'w', newline='') as outfile:
     
     outfile.write("MAX Stop, Neighborhood\n")
     counter = 1
     for ms in mstops:
          outfile.write(ms.getName())
          outfile.write(",")
          nhood = ms.getNhood()
          if (nhood == None):
               outfile.write("Unknown")
          else:
               outfile.write(ms.getNhood().getName())
          outfile.write("\n")
          counter += 1

print ("Wrote ", counter, " lines to rstops_nhoods.csv")
