# -*- coding: utf-8 -*-
from lxml import etree
import pandas as pd
import random

def createXMLFromDataFrame(dataframe):
    """Uses the data frame object to create an xml file for the drillPlan."""
    assert dataframe is not None
    stratas = etree.Element("stratas")
    for i in range(len(dataframe)):
        depthM =       str('{0:.2f}'.format(dataframe.loc[i,"MD(m)"]))
        depthF =       str('{0:.2f}'.format(dataframe.loc[i,"MD"]))
        pressureGradient = str('{0:.2f}'.format(dataframe.loc[i,"PP(kPa/m)"]))
        fracturePressure =     str('{0:.2f}'.format(dataframe.loc[i,"FracP(kPa/m)"]))

        Strata = etree.SubElement(stratas, "Strata")
        etree.SubElement(Strata, "name").text = f"formation @ {depthM}m/{depthF}ft"
        etree.SubElement(Strata,"depth").text = depthM
        etree.SubElement(Strata,"pressureGradient").text = pressureGradient
        etree.SubElement(Strata,"fracturePressure").text = fracturePressure
        etree.SubElement(Strata,"maxROP").text = str(random.randint(100,300))
        etree.SubElement(Strata,"influxGas").text = "0"
        etree.SubElement(Strata,"influxLiquid").text = "0"
        
        RockType = etree.SubElement(Strata,"RockType")
        etree.SubElement(RockType,"name").text = "shale"
        etree.SubElement(RockType,"porosity").text = str(random.randint(0,11))
        etree.SubElement(RockType,"permeability").text = str(random.randint(0,11))
        etree.SubElement(RockType,"staticFriction").text = str(random.randint(0,11))
        etree.SubElement(RockType,"kineticFriction").text =str(random.randint(0,11))
        etree.SubElement(RockType,"strength").text = str(random.randint(0,11))
        etree.SubElement(RockType,"texture").text = str(random.randint(1,6))

        i+=1
    et = etree.ElementTree(stratas)
    print(type(et))
    print(len(dataframe))
    return et

def writeXMLToFile(tree):
    assert tree is not None
    print(type(tree))
    tree.write(r"/Users/joshsallows/OneDrive - Endeavor Technologies Corp/Companies/HESS/HURON/huron_formation_plan2.xml", pretty_print=True)

def parseXLS(XLSFileName):
    """opens and parses and xls file to be used to create the drill plan"""
    assert XLSFileName is not None
    df = pd.read_excel(XLSFileName)
    return df

def parseXML(XMLFileName):
    tree = etree.parse(XMLFileName)
    return tree
def modifyXML(XMLTree, minDepth, maxDepth):
    """XML Tree is the xml tree, can be a file path or from another function.
    minDepth is the minimum depth that the function will allow a change to be made
    maxDepth is the maximum depth that the function will allow a change to be made"""
    tree = XMLTree
    root = tree.getroot()
    minDepth = minDepth
    maxDepth = maxDepth #only updates formations above this depth
    for child in root.iter():
        for grandchild in child:
            if grandchild.tag == "depth":
                depth = float(grandchild.text)
                if depth < maxDepth and depth > minDepth:
                    child[2].text = "9"

    return tree

# data = r"/Users/joshsallows/OneDrive - Endeavor Technologies Corp/Companies/HESS/HURON/huron_formation_plan.xls"
# dataFile = parseXLS(data)
# writeXMLToFile(createXMLFromDataFrame(dataFile))
data = r"/Users/joshsallows/OneDrive - Endeavor Technologies Corp/Companies/HESS/HURON/huron_formation_plan.xml"
xmlFileTree = writeXMLToFile(modifyXML(parseXML(data), 0, 2835))
# for child in xmlFileTree.getroot():
#     for item in child:
#         if item.tag == "depth":
#             if int(item) < 701:
#                 item.text = 9