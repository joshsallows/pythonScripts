import csv
import os

#This is used to give brittany the file module names so that they can be imported into Pure Web

def parseFolderForPureWeb(folder):
    assert folder is not None
    csv_list = []
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".dsav") or filepath.endswith(".DSAV"):
                if filepath.__contains__("DELTA") or filepath.__contains__("ECHO"):
                    moduleId = f'https://raw.githubusercontent.com/endeavor-tech/modulesAndSaves/main/{filename}'
                    learningObjLink = f'https://endeavor-reality.pureweb.io/departureSSO?moduleId={moduleId}'
                    # csv_list.append([filename, f'**Google Link**\n{moduleId}\n**Learning Object**\n{learningObjLink}', 'NewSavesforIADC'])
                    csv_list.append([f'{learningObjLink}'])
    with open('pureWebImport.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_list)

def parseFolderForGoogle(folder):
    assert folder is not None
    csv_list = []
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.lower().endswith(".dsav") or filepath.lower().endswith(".dsts"):
            #     if filepath.__contains__("DELTA") or filepath.__contains__("ECHO"):
                moduleId = f'https://raw.githubusercontent.com/endeavor-tech/modulesAndSaves/main/{filename}'
                learningObjLink = f'https://broker.endpoints.service-project-us-prod-1a95.cloud.goog?app=drilling-simulator&drillSimFile={moduleId}'
                # csv_list.append([filename, f'**Google Link**\n{moduleId}\n**Learning Object**\n{learningObjLink}', 'NewSavesforIADC'])
                csv_list.append([f'{learningObjLink}'])
    with open('googleImport.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_list)

# parseFolderForPureWeb("./modules/")
parseFolderForGoogle("D:\modulesAndSaves")
