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
3. Rename the map with a title that describes the feature class contained within it and **does not contain spaces** (e.g. `TN_Sate_Park_Boundaries`).
4. Right-click on the feature class in the Contents pane and choose *Sharing* -> *Share as Web Layer*. Fill out the tool parameters and hit *Publish*. Give 'er a minute.
5. 
