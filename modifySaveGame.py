# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os

def readfile(file):
    assert file is not None
    """open the file and convert the contents to a string"""
    with open(file, 'r') as data:
        return data.read()

def searchAndReplace(tree, tag, text):
    assert tree is not None
    assert tag is not None
    assert text is not None
    tree.find(f".//{tag}").text = text
    return tree

def writeXMLToFile(tree, filename, inplace=False):
    assert tree is not None
    assert filename is not None
    if inplace:
        filename_out = filename
    if inplace==False:
        filename_in = filename.split(".")
        filename_out = f".{filename_in[1]}_REDCLOSED.{filename_in[2]}"
    
    xml_str = ET.tostring(tree, encoding='unicode', method='xml')
    with open(filename_out, "w") as out_file:
        out_file.write(f'<?xml version="1.0" encoding="utf-16"?>\n{xml_str}')

def parseFolderforSaves(folder):
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.__contains__("SURFACE"):
                if filepath.endswith(".dsav") or filepath.endswith(".DSAV"):
                    tree = ET.fromstring(readfile(filepath))
                    writeXMLToFile(searchAndReplace(tree, "greenToGo", "NONE"), filepath)

def parseFolderforSimSaveState(folder):
    assert folder is not None
    for subdir, dirs, files in os.walk(folder):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".dsav") or filepath.endswith(".DSAV"):
                fIN = open(filepath, 'rt')
                data = fIN.read()
                if data.__contains__("<SimSaveState>"):
                    print('found it')
                data = data.replace('<SimSaveState>', '<SimSaveState xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">')
                fIN = open(filepath, 'w')
                fIN.write(data)
                fIN.close()
                    
parseFolderforSimSaveState("./modules/Echo")

# parseFolderforSaves("./modules/Delta")



"""
surface: redclosed, non ported
subsea: and non-ported
"""

