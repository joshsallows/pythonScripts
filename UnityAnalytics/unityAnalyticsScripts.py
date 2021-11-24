import gzip, json, pandas, csv, os, datetime
from json.decoder import JSONDecodeError

outfile = 'Usage/1.json'
infile  = 'Usage/2.json'
outfile_2 = 'Usage/3.json'
csvfile = 'Usage/1.csv'
csvfile_2 = 'Usage/2.csv'
error_file = 'Usage/error_log.csv'
count = 0

def parseFoldersToWorkOnFiles(folder):
    """takes a path as the argument and walks through the directory, unzipping files and putting them into a new json file"""
    assert folder is not None
    with open(outfile, 'wb') as f_out:
        for subdir, dirs, files in os.walk(folder):
            for filename in files:
                filepath = subdir + os.sep + filename

                #if the files are gzipped, should put a try loop on this so it works for gzipped and not gzipped.
                if filepath.endswith(".gz"):
                    with gzip.open(filepath,'rb') as f_in:
                        f_out.write(f_in.read())

                # Not a GZipped file
                # with open(filepath,'rb') as f_in:
                #     f_out.write(f_in.read())    

def addTheThingsToMakeTheParserWork():
    """The first of 2 functions to run to prepare the json file for parsing"""
    with open(infile, 'wb') as i:
        with open(outfile, 'rb') as o:
            string =  b'{ \n"Data" :\n'
            string += b"[\n"
            string += o.read()
            string += b"]\n}"
            i.write(string)

def addCommasInPlaces():
    """The 2nd of 2 functions that need to be run on the json file so the parser can parse it"""
    f = open(infile, 'rt')
    s = str(f.read())
    f.close()
    s = s.replace('"custom"}', '"custom"},',s.count('"custom"}')-1)
    f = open(outfile_2, 'wt')
    f.write(s)
    f.close()

def addTheFileToACSV(count):
    """Create a csv file from json so that you can work on it later on"""

    with open(outfile_2, 'rb') as f:
        ogdata = json.load(f)

    data = ogdata['Data']
    print(len(data))

    with open(csvfile, 'w') as csvFile:
        csv_writer = csv.writer(csvFile)
        for datum in data:
            if count == 0:
                header = datum.keys()
                csv_writer.writerow(header)
                count+=1
            csv_writer.writerow(datum.values())

# def getUsersFromCSVandCreateDictionary(csvFile):
#     error_count = 0
#     """Creates a dictionary that can be used to figure out how much time spent running the simulator."""
#     with open(csvFile, 'r') as read_obj, open(error_file, 'w') as error_obj:
#         df = pandas.read_csv(read_obj, header=0, usecols=(1,3,9), names=('ts','sessionID','custom_params'))
#         userUseageDictionary = {} 
#         csv_writer = csv.writer(error_obj)

#         for n in range(len(df)):
#             ref = df.loc[n]['custom_params']
#             # customParameters = ref.replace("'", '"')
#             # ref = json.loads(customParameters)
#             try:
#                 try:
#                     customParameters = ref.replace("'", '"')
#                     ref = json.loads(customParameters)
#                 except JSONDecodeError as ex:
#                     ref2 = df.loc[n]['custom_params']
#                     if ref2.__contains__("'DEPT': ''''"):
#                         ref2 = ref2.replace("'DEPT': ''''","'DEPT': 'No Department'")
#                     if ref2.__contains__("'EXT_DEPT': ''''"):
#                         ref2 = ref2.replace("'EXT_DEPT': ''''","'EXT_DEPT': 'No Ext_Department'")
#                     if ref2.__contains__("'UUID': ''''"):
#                         ref2 = ref2.replace("'UUID': ''''","'UUID': 'No UUID'")
#                     if ref2.__contains__("'USER': ''''"):
#                         ref2 = ref2.replace("'USER': ''''","'USER': 'No USER'")
#                     customParameters = ref2.replace("'", '"')
#                     ref = json.loads(customParameters)
#                     error_count+=1
                    
#                 except Exception as ex:
#                     error_obj.write(df.loc[n]['custom_params'])
#                     template = "An exception of type {0} occurred. Arguments: \n{1}"
#                     message = template.format(type(ex), ex.args)
#                     print(message)
#                     break

#                 try:
#                     departmentID = ref['DEPT'] #Department ID (Company Name)
#                 except KeyError:
#                     departmentID = "unknown" #the custom_params is missing "DEPT"
#                     break
#                 try:
#                     userID = ref["UUID"]
#                 except KeyError:
#                     print("error UUID")
#                     userID = ref["USER"] #Unique User ID
#                 try:
#                     timeStamp = df.loc[n]['ts'] #Timestamp
#                 except KeyError:
#                     print('no time stamp')
#                 try:
#                     sessionID = df.loc[n]['sessionID']
#                 except KeyError:
#                     print("no session ID")
#                 try:
#                     moduleName = ref['MODULE'] #Module Name
#                 except KeyError:
#                     print("error moduleName")
#                     moduleName = ref['MODULE_NAME']  
#             except:
#                 csv_writer.writerow(df.loc[n])
            
#             if departmentID not in userUseageDictionary.keys(): #first time seeing the company so make a new one
#                 userUseageDictionary[departmentID] = {}
#             if userID not in userUseageDictionary[departmentID].keys():
#                 userUseageDictionary[departmentID][userID] = {"Sessions": {}, "TotalTime": 1}
#                 userUseageDictionary[departmentID][userID]["Sessions"][sessionID] = {"ModuleName": moduleName, "TimeStamps": [timeStamp], 'ModuleTime' : 1}
#             elif sessionID not in userUseageDictionary[departmentID][userID]["Sessions"].keys():
#                 userUseageDictionary[departmentID][userID]["Sessions"][sessionID] = {"ModuleName": moduleName, "TimeStamps": [timeStamp], 'ModuleTime' : 1}
#                 userUseageDictionary[departmentID][userID]['TotalTime'] +=1
#             elif sessionID in userUseageDictionary[departmentID][userID]["Sessions"].keys():
#                 userUseageDictionary[departmentID][userID]["Sessions"][sessionID]["TimeStamps"].append(timeStamp)
#                 userUseageDictionary[departmentID][userID]['Sessions'][sessionID]['ModuleTime'] +=1
#                 userUseageDictionary[departmentID][userID]['TotalTime'] +=1
#             else:
#                 print("have not thought about this case yet")
#         print("manipulated {0} records because there was something wrong with how they were saved".format(error_count))     
#         return userUseageDictionary

def findAndReplace(infile,outfile):
    """simple find and replace function"""
    f = open(infile, 'rt')
    s = str(f.read())
    f.close()
    # s= s.replace('"IADC', "'IADC")
    s = s.replace('""', "'")
    s = s.replace("'S ", "S ")
    f = open(outfile, 'wt')
    f.write(s)
    f.close()

def outputtoFile_companySpecific(dictionary):
    """take the dictionary and create some csv files that can be used to read who did what and for how long"""
    for departmentID in dictionary.keys():
        fileName = "Usage/companySpecificData/" + departmentID + ".csv"
        with open(fileName, 'w') as obj:
            csv_columns = ["Department ID", "User ID", "Date", "Course", "Session ID", "Time in Session (h)", "Cummulative Time (h)"]
            writer = csv.writer(obj)

            for userID, course in dictionary[departmentID].items():
                cummulativeTime = float(course["TotalTime"])/60
                for item in course["Sessions"]:

                    sessionID = item
                    moduleID = course["Sessions"][item]['ModuleName']
                    date = datetime.datetime.fromtimestamp(float(course["Sessions"][item]['TimeStamps'][0])/1000)
                    timeInSession = float(course["Sessions"][item]['ModuleTime'])/60

                    list_w = [departmentID,userID,date,moduleID,sessionID,timeInSession,cummulativeTime]
                    writer.writerow(list_w)
    print('time to check the files')

def outputtoFile(dictionary):
    """take the dictionary and create some csv files that can be used to read who did what and for how long"""
    fileName = "Usage/companySpecificData/" + 'combinedfile' + ".csv"
    with open(fileName, 'w') as obj:
        csv_columns = ["Department ID", "User ID", "Date", "Course", "Session ID", "Time in Session (h)", "Cummulative Time (h)"]
        writer = csv.writer(obj)

        for departmentID in dictionary.keys():
            for userID, course in dictionary[departmentID].items():
                cummulativeTime = float(course["TotalTime"])/60
                for item in course["Sessions"]:
                    sessionID = item
                    moduleID = course["Sessions"][item]['ModuleName']
                    date = datetime.datetime.fromtimestamp(float(course["Sessions"][item]['TimeStamps'][0])/1000)
                    timeInSession = float(course["Sessions"][item]['ModuleTime'])/60

                    list_w = [departmentID,userID,date,moduleID,sessionID,timeInSession,cummulativeTime]
                    writer.writerow(list_w)

def fileRenameSoAHumanCanRead(folder):
    assert folder is not None
    krew = "departmentID_Krew.json"
    eOne =  "departmentID_E1.json"
    with open(krew, 'r') as read_krew, open(eOne, 'r') as read_eOne:
        krew_dict = json.load(read_krew)
        eOne_dict = json.load(read_eOne)
        for subdir, dirs, files in os.walk(folder):
            for filename in files:
                originalName = filename.strip(".csv")
                oldfile = os.path.join(folder,filename)
                for company in eOne_dict:
                    if company[" Department ID"] == originalName:
                        newName = company["Company"] + ".csv"
                        newFile = os.path.join(folder, newName)
                        os.rename(oldfile, newFile)
                for company in krew_dict:
                    if company["Department ID"] == originalName:
                        newName = company["Company"] + ".csv"
                        newFile = os.path.join(folder, newName)
                        os.rename(oldfile, newFile)
                
def getUsersFromCSVandCreateDictionary(csvFile):
    error_count = 0
    """Creates a dictionary that can be used to figure out how much time spent running the simulator."""
    with open(csvFile, 'r') as read_obj, open(error_file, 'w') as error_obj:
        df = pandas.read_csv(read_obj, header=0, usecols=(1,3,9), names=('ts','sessionID','custom_params'))
        userUseageDictionary = {} 
        csv_writer = csv.writer(error_obj)

        for n in range(len(df)):
            ref = df.loc[n]['custom_params']
            customParameters = ref.replace("'", '"')
            if customParameters.__contains__('"DEPT": """"'):
                customParameters = customParameters.replace('"DEPT": """"','"DEPT": "NO DEPARTMENT"')
            if customParameters.__contains__('"EXT_DEPT": """"'):
                customParameters = customParameters.replace('"EXT_DEPT": """"','"EXT_DEPT": "NoExtDepartment"')
            if customParameters.__contains__('"UUID": """"'):
                customParameters = customParameters.replace('"UUID": """"','"UUID": "NoUUID"')
            if customParameters.__contains__('"USER": """"'):
                customParameters = customParameters.replace('"USER": """"','"UUID": "NoUSER"')
            ref = json.loads(customParameters)
            
            try:
                departmentID = ref["DEPT"]
            except KeyError as ex:
                departmentID = "NO DEPARTMENT"
            try:
                userID = ref["USER"]
            except KeyError as ex:
                userID = "OFFLINE USER"
            try:
                sessionID = df.loc[n]["sessionID"]
            except KeyError as ex:
                sessionID = "OFFLINE SESSION"
            try:
                moduleName = ref["MODULE"]
            except KeyError as ex:
                moduleName = "MISSING MODULE"
            try:
                timeStamp = df.loc[n]["ts"]
            except KeyError as ex:
                timeStamp = "MISSING TIMESTAMP"

            if departmentID == "NO DEPARTMENT":
                if moduleName.lower().__contains__("baker"):
                    departmentID = "6701d9e0-95e7-4853-af20-9b3b4d715561"
                if moduleName.lower().__contains__("sbpd"):
                    departmentID = "e312ce6c-52fa-4f2d-99f9-da39e5c7b3bf"
            
            if departmentID not in userUseageDictionary.keys(): #first time seeing the company so make a new one
                userUseageDictionary[departmentID] = {}
            if userID not in userUseageDictionary[departmentID].keys():
                userUseageDictionary[departmentID][userID] = {"Sessions": {}, "TotalTime": 1}
                userUseageDictionary[departmentID][userID]["Sessions"][sessionID] = {"ModuleName": moduleName, "TimeStamps": [timeStamp], 'ModuleTime' : 1}
            elif sessionID not in userUseageDictionary[departmentID][userID]["Sessions"].keys():
                userUseageDictionary[departmentID][userID]["Sessions"][sessionID] = {"ModuleName": moduleName, "TimeStamps": [timeStamp], 'ModuleTime' : 1}
                userUseageDictionary[departmentID][userID]['TotalTime'] +=1
            elif sessionID in userUseageDictionary[departmentID][userID]["Sessions"].keys():
                userUseageDictionary[departmentID][userID]["Sessions"][sessionID]["TimeStamps"].append(timeStamp)
                userUseageDictionary[departmentID][userID]['Sessions'][sessionID]['ModuleTime'] +=1
                userUseageDictionary[departmentID][userID]['TotalTime'] +=1
            else:
                print("have not thought about this case yet")
        return userUseageDictionary



"""The Function Calls that I used to get the data, run them in order from top to bottom to get the final result"""
parseFoldersToWorkOnFiles("Usage/September1_November18")
addTheThingsToMakeTheParserWork()
addCommasInPlaces()
addTheFileToACSV(count)
findAndReplace(csvfile, csvfile_2)
useageDictionary = getUsersFromCSVandCreateDictionary(csvfile_2)
outputtoFile(dictionary=useageDictionary)
outputtoFile_companySpecific(dictionary=useageDictionary)
fileRenameSoAHumanCanRead("Usage/companySpecificData")

    