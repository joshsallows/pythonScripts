# -*- coding: utf-8 -*-
from lxml import etree
import pandas as pd

def createXMLFromDataFrame(dataframe):
    """Uses the data frame object to create an xml file for the drillPlan."""
    assert dataframe is not None
    sections = etree.Element("sections")
    for i in range(len(dataframe)):
        surveyDepth =       str('{0:.2f}'.format(dataframe.loc[i,"MD(m)"]))
        surveyInclination = str('{0:.2f}'.format(dataframe.loc[i,"Inclination"]))
        surveyAzimuth =     str('{0:.2f}'.format(dataframe.loc[i,"Azimuth"]))

        Section = etree.SubElement(sections, "Section")
        etree.SubElement(Section, "name").text = f"{surveyDepth}m {surveyInclination}Inc {surveyAzimuth}Azi"
        etree.SubElement(Section,"width").text = str(dataframe.loc[i,"Hole Diameter"])
        etree.SubElement(Section,"MD").text = surveyDepth
        etree.SubElement(Section,"azimuth").text = surveyAzimuth
        etree.SubElement(Section,"inclination").text = surveyInclination
        etree.SubElement(Section,"build").text = "0"
        etree.SubElement(Section,"turn").text = "0"
        etree.SubElement(Section,"operationNote").text = ""
        i+=1
    et = etree.ElementTree(sections)
    print(type(et))
    print(len(dataframe))
    return et

def writeXMLToFile(tree):
    assert tree is not None
    print(type(tree))
    tree.write(r"/Users/joshsallows/OneDrive - Endeavor Technologies Corp/Companies/HESS/HURON/huron_drill_plan_14534.xml", pretty_print=True)

def parseXLS(XLSFileName):
    """opens and parses and xls file to be used to create the drill plan"""
    assert XLSFileName is not None
    df = pd.read_excel(XLSFileName)
    return df

def countSections(xmlFile):
    assert xmlFile is not None
    root = etree.parse(xmlFile).getroot()
    print(len(root.getchildren()))

# data = r"/Users/joshsallows/OneDrive - Endeavor Technologies Corp/Companies/HESS/HURON/huron_drill_plan.xls"
# dataFile = parseXLS(data)
# writeXMLToFile(createXMLFromDataFrame(dataFile))
# countSections(r"/Users/joshsallows/OneDrive - Endeavor Technologies Corp/Companies/HESS/HURON/huron_drill_plan_28754.xml")
