# OverwriteWebLayers.py
Automate the overwriting of ArcGIS Online web layers/service definitions from local feature classes using ArcGIS Pro, arcpy, and the ArcGIS API for Python.
## Overview
The script connects to ArcGIS.com (using credentials stored locally—*yeah, yeah, I know*) and populates a Python dictionary object with a list of **map objects** and corresponding **map names** found within a referenced ArcGIS Pro Project. Next, the script searches for service definitions owned by the user whose credentials are input and populates a second Python dictionary with a list of **service names** and **service IDs**. Finally, the script **iterates through** the two dictionaries and, where a map name matches a service name, stages a temporary service file and uses this to **replace the service definition** on ArcGIS Online, updating the AGOL data with new data from your local storage.

This workflow allows the user to add or remove published feature classes from the list of weekly updates simply by adding or removing a map from the project. **Note that in the case of an addition, an existing service definition with a name that matches the map name must already exist on AGOL. It is recommended that this initial service definition be generated from the same map using the “Publish Web Layer” option in ArcGIS Pro, thus ensuring a matching name.**

Schema changes to the published data feature class should not cause any issue with the script or with the newly updated feature layer; however, if a field is removed or renamed, any references to this field in other AGOL objects, such as Web Maps and StoryMaps, may "break."
## What you need
- ArcGIS Pro
- Python 3.X
- An ArcGIS Online account with an associated ArcGIS Pro license
## Instructions
#### Publish the feature to AGOL manually the first time
1. Create an ArcGIS Pro project dedicated to running this script. Take note of the project name (e.g. `WeeklyUpdates.aprx`) and the folder in which your project is saved (e.g. `C:\ArcGIS\Projects\WeeklyUpdates`)
2. Create a new map in your project and add **only one** feature class to the map.
3. Create or review metada for the feature class that will be published; this metadata will cascade to the uploaded service definition.
4. Rename the map with a title that describes the feature class contained within it and **does not contain spaces** (e.g. `TN_Sate_Park_Boundaries`).
5. Right-click on the feature class in the Contents pane and choose *Sharing* -> *Share as Web Layer*. Fill out the tool parameters and hit *Publish*. Give 'er a minute.

You've now created a feature layer and corresponding service definition (whose name should match the name of your map) in AGOL. You can repeat steps 2-5 for any number of feature classes you wish to publish to AGOL. The script will iterate through every map contained in your project file and try to match it to an AGOL service definition.
#### Update Python script parameters
This script is pretty clear about where parameters needs to reflect your own set-up, and there aren't many to change. See below.
```
############################ BEGIN ASSIGNING VARIABLES ############################

# Set the path to the project
prjFolder = r"C:/GIS/Projects"
prjPath = os.path.join(prjFolder, ExampleProject.aprx)

# Set login credentials (user name is case sensitive, fyi)
portal = "https://www.arcgis.com/" # or use another portal
user = User.Name
password = Password!123
		       
# Set sharing settings
shrOrg = # True or False
shrEveryone = # True or False
shrGroups = # Leave blank (" ") or list 'em

############################# END ASSIGNING VARIABLES #############################
```
#### Run the script
1. Run the script through your favorite IDE using Python 3.X (which comes with your Pro installation)
2. Set up the script to run periodically in Task Scheduler or equivalent, based on how often your local copies are edited
## Credits
This script was adapted from [Updating your hosted feature services with ArcGIS Pro and the ArcGIS API for Python](https://www.esri.com/arcgis-blog/products/api-python/analytics/updating-your-hosted-feature-services-with-arcgis-pro-and-the-arcgis-api-for-python/), an ArcGIS blog post by Kevin Hibma.

I found that using the [search method on the ContentManagement class](https://developers.arcgis.com/python/api-reference/arcgis.gis.toc.html?highlight=gis%20content%20search#contentmanager) brought up all kinds of troublesome resuls and developed the iterating-through-two-dictionary-objects process as a solution. Thus far, it's worked like a charm for me. If you come across any issues with this search method, I'd love to hear about them.
