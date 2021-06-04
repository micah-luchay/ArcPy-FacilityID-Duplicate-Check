import arcpy, csv, os

databaseLocation = arcpy.GetParameterAsText(0) # Location of the database to read the feature class FacilityIDs
csvFileOutputLocation = arcpy.GetParameterAsText(1) # Location to write the duplicate IDs to in a CSV file
sewerBoolean = arcpy.GetParameter(2) # Boolean value for sewer newtork
waterBoolean = arcpy.GetParameter(3) # Boolean value for water network
stormBoolean = arcpy.GetParameter(4) # Boolean value for storm network

arcpy.env.workspace = databaseLocation #set the workspace
csvFileOutputLocation = os.path.join(csvFileOutputLocation + '\\Duplicate_Facility_IDs.csv') # create path for the CSV File Output location

def searchFeatureClass(fc): # function to search for the facilityIDs and write them to the CSV File

    featureClassName = fc.split('\\')[-1] # save the name of the feature class

    FacilityIDList = [] # stores all FacilityIDs, even if not a duplicate
    DuplicateIDList = [] # stores all duplicate FacilityIDs in this list

    with arcpy.da.SearchCursor(fc, "FACILITYID") as cursor: #start a search cursor on the feature class
        for row in cursor:

            if row[0] not in FacilityIDList and row[0] != None and row[0] != 'CAP' and row[0] != 'TAP': # store all FacilityID values to the list to compare future facilityIDs to values in the list
                FacilityIDList.append(row[0])

            elif row[0] in FacilityIDList and row[0] != None and row[0] != 'CAP' and row[0] != 'TAP': # check to see if the FacilityID already exists in the FacilityIDList. If so, it's a duplicate! Store in the DuplicateIDList
                DuplicateIDList.append(row[0])

    if DuplicateIDList: # if there are duplicate IDs in the list, making it not null- write them to the file

        for each in DuplicateIDList:
            writer.writerow([each,featureClassName]) # write the duplicates to the file

    FacilityIDList = [] # reset the FacilityIDList, just to play it safe

if sewerBoolean == False and waterBoolean == False and stormBoolean == False: # user didn't specify and datasets to check!
    arcpy.AddMessage("Select a network to check dummy! Sheesh")
    sys.exit()


with open(csvFileOutputLocation, mode = 'wb') as csvFile: # create the csv file


    writer = csv.writer(csvFile, delimiter = ',') # create a writer object
    writer.writerow(['FACILITYID', 'Feature Class']) # write the header to the csv file
    datasets = arcpy.ListDatasets() # List all the datasets in the current workspace

    sewerDatasetPath = os.path.join(databaseLocation, datasets[1]) # save the dataset workpaths as variables
    waterDatasetPath = os.path.join(databaseLocation, datasets[3])
    stormDatasetPath = os.path.join(databaseLocation, datasets[2])


    if sewerBoolean == True: # if the user checked the sewer network to have its duplicate IDs checked

        arcpy.env.workspace = sewerDatasetPath # set the workspace to the sewer dataset for the ListFeatureClasses method to work
        for each in arcpy.ListFeatureClasses(): # Loop through each feature class to extract its path

            if each == 'Sewer_Net_Junctions': # doesn't have a facilityID
                continue

            fcPath = os.path.join(sewerDatasetPath,each) # create a path for each feature class
            arcpy.AddMessage('Checking ' + fcPath) # Give the user some update
            searchFeatureClass(fcPath)


    if waterBoolean == True: # if the user checked the water network to have its duplicate IDs checked

         arcpy.env.workspace = waterDatasetPath  # set the workspace to the water dataset for the ListFeatureClasses method to work
         for each in arcpy.ListFeatureClasses(): # Loop through each feature class to extract its path

            if each == 'waSamplingStation': # waSamplingStation lacks a FacilityID Column - skip!
                continue

            if each == 'waTestStation': # waTestStation lacks a FacilityID Column- skip!
                continue

            if each == 'WaterNetwork_Net_Junctions': # doesn't have a facilityID
                continue

            fcPath = os.path.join(waterDatasetPath,each) # create a path for each feature class
            arcpy.AddMessage('Checking ' + fcPath) # Give the user some update
            searchFeatureClass(fcPath)

    if stormBoolean == True:
         arcpy.env.workspace = stormDatasetPath
         for each in arcpy.ListFeatureClasses():

            fcPath = os.path.join(stormDatasetPath,each)
            arcpy.AddMessage('Checking ' + fcPath)
            searchFeatureClass(fcPath)




