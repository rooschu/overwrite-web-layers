
###################################################################################
#                                                                                 #
#  This script updates existing feature layers on AGOL by replacing the           #
#  associated service definition file with one newly generated from locally       #
#  hosted data.                                                                   #
#                                                                                 #
#  If this script is to run successfully, certain parameters must be met prior    #
#  to its execution. For complete documentation of the workflow, visit:           #
#  https://drive.google.com/open?id=1k6b3NOAo9TztbP1DHPB3J1UFNpGAA1Q8             #
#                                                                                 #
#  Rachel Schultz | rachel.schultz@tn.gov                                         #
#                                                                            	  #
###################################################################################

# Import modules
import arcpy
import os, sys
from arcgis.gis import GIS

############################ BEGIN ASSIGNING VARIABLES ############################

# Set the path to the project
prjFolder = # path to .aprx
prjPath = os.path.join(prjFolder, # Whatever the name of your project is, e.g. "WeeklyUpdates.aprx")

# Set login credentials (user name is case sensitive, fyi)
portal = "https://www.arcgis.com/" # or use another portal
user = # Your ArcGIS Online user name
password = # Probably not "password"

############################# END ASSIGNING VARIABLES #############################

# Set sharing settings
shrOrg = True
shrEveryone = True
shrGroups = ""

# Assign name and location for temporary staging files
tempPath = prjFolder
sddraft = os.path.join(tempPath, "TempFile.sddraft")
sd = os.path.join(tempPath, "TempFile.sd")

# Connect to ArcGIS online
print("Connecting to {}".format(portal))
gis = GIS(portal, user, password)
print("Successfully logged in as: " + gis.properties.user.username + "\n")

# Assign environment and project, and create empty dictionaries
arcpy.env.overwriteOutput = True
prj = arcpy.mp.ArcGISProject(prjPath)
mapDict = {}
servDict = {}

# Populate map dictionary with map names and objects from earlier defined project
for map in prj.listMaps():
	mapDict[map.name]=map
	
# Search for service definition files under the current user's account and populate
# service definition dictionary with names and ID numbers
sdItem = gis.content.search(query="owner: " + user + " AND type:Service Definition", max_items=100)
for serv in sdItem:
	if str(serv.name).endswith(".sd"):
		servDict[str(serv.name)[:-3]]=serv.id
	
# Iterate through maps in project and, if a matching service definition is found,
# overwrite that service definition with the data in the local map
for sdName, sdID in servDict.items():
	for mapName, mapItem in mapDict.items():
		if mapName == sdName:
			updateItem = gis.content.get(sdID)
			arcpy.mp.CreateWebLayerSDDraft(mapItem, sddraft, sdName, 'MY_HOSTED_SERVICES', 'FEATURE_ACCESS', True, True)
			arcpy.StageService_server(sddraft, sd)
			updateItem.update(data=sd)
			print("Overwriting {}...".format(sdName))
			fs = updateItem.publish(overwrite=True)
			if shrOrg or shrEveryone or shrGroups:
				print("Setting sharing options...")
				fs.share(org=shrOrg, everyone=shrEveryone, groups=shrGroups)
			print("Successfully updated {}.\n".format(fs.title))		
      
