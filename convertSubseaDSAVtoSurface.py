# -*-coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import re
import in_place



def writeXMLToFile(filename, old = "SUBSEA", new = "SURFACE", inplace=False):
	assert filename is not None
	if inplace:
		filename_out = filename
	if inplace == False:
		filename_split = filename.split(".")
		filename_out = f"{filename_split[-2].replace(old, new)}.{filename_split[-1]}"
	
	with open(filename, "r") as file:
		xml_str_orig = file.read()
		xml_str = ET.fromstring(xml_str_orig)

		removeStrata(xml_str, "Mesopelagic Zone")
		adjustFirstFormationDepth(xml_str)
		turnOffSubsea(xml_str)
		removeRiserDrillPlanSegments(xml_str)
		adjustInitialAnnulusStartatSection(xml_str)
		if filename.lower().__contains__("dsav"):
			resizeRiserVector4Segments(xml_str)
		changeRigType(xml_str)

		outString = ET.tostring(
				xml_str, encoding="unicode",
				xml_declaration='xml version="1.0" encoding="utf-16"')
		outString = outString.replace("'cp1252'", '"utf-16"')
		old = 'SimSaveState xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
		new = 'SimSaveState xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
		outString = outString.replace(old, new)

	# finally write everything out to file
	with open(filename_out, "w") as file_out:
		file_out.write(outString)
	# adding the CSCS stuff back into the save game
	try:
		fixCSCS(filename, filename_out)
	except AttributeError: 
		"""a module or save will not load if the cscs does not have the CDATA portion within it"""
		old = "<cscsScript />"
		new = "<cscsScript><![CDATA[]]></cscsScript>"
		secondPassCSCS(filename_out, old, new)


def removeStrata(tree, name):
	""" Removes a strata from WebFormation by passing the name of the formation """
	for stratas in tree.findall(".//Strata/.."):
		for Strata in stratas:
			for tag in Strata:
				if tag.tag == "name" and tag.text == name:
					stratas.remove(Strata)


def adjustFirstFormationDepth(tree):
	"""Changes only the first formation depth, run on after you have removed the water zone"""
	for stratas in tree.findall(".//Strata/.."):
		for Strata in stratas[:1]:
			for tag in Strata:
				if tag.tag == "depth":
					tag.text = "0"


def turnOffSubsea(tree):
	for elements in tree.findall(".//WebSubSea/"):
		if elements.tag == "isSubsea":
			elements.text = "false"


def removeRiserDrillPlanSegments(tree):
	""" Removes a strata from WebFormation by passing the name of the formation """
	for sections in tree.findall(".//Section/.."):
		for Section in sections[0:2]:
			sections.remove(Section)


def adjustInitialAnnulusStartatSection(tree):
	""" subtracts 2 from the initial annulus start at section """
	for tag in tree.findall(".//WebDrillPlan/"):
		if tag.tag == "initialAnnulusStartsAtSection":
			tag.text =str(int(tag.text)-2)


def resizeRiserVector4Segments(tree):
	""" Resizes the top two vector4 elements to match the diamter of the casing """
	#step 1, get the size of the casing from the first drill plan section, this assumes the first section is sized correctly 
	for sections in tree.findall(".//Section/.."):
		for tag in sections[0]:
			if tag.tag == "width":
				diameter = tag.text
	# step2, apply the diameter of the casing to the first 2 vector4 elements.
	for annulusPath in tree.findall(".//Vector4/.."):
		for Vector4 in annulusPath[0:2]:
			for tag in Vector4:
				if tag.tag == "w":
					tag.text = diameter
	

def changeRigType(tree):
	""" subtracts 2 from the initial annulus start at section """
	
	for tag in tree.findall(".//ProgrammerSettings/"):
		if tag.tag == "rigType":
			tag.text = "LAND"


def fixCSCS(file_in, file_out):
	"""open file_in, get the string contents of the file, find the cscs script stuff, close the file;
		open file_out, get the string contents of the file, find the incomplete cscs script stuff, close the file;
		replace the bad cscs stuff with the good cscs stuff;
		open file_out in write mode, and write out the fixed string"""
	with open(file_in, "r") as f:
		a = f.read()
		START = "<cscsScript>"
		END = "</cscsScript>"
		m = re.compile(r'%s.*?%s' % (START, END), re.S)
		s = m.search(a).group(0)
		new = s 
	with open(file_out, "r") as out:
		a = out.read()
		START = "<cscsScript>"
		END = "</cscsScript>"
		m = re.compile(r'%s.*?%s' % (START, END), re.S)
		old = m.search(a).group(0)
	a = a.replace(old, new)
	with open(file_out, "w") as fuck:
		fuck.write(a)


def secondPassCSCS(file_out, old, new, flags=0):
		"""open file_out, read the file line by line looking for the 
		desired line and replace it. write the contents back to the file"""
		print(file_out)
		with open(file_out, "r+") as file:
			a = file.read()
			text_pattern = re.compile(re.escape(old), flags)
			a = text_pattern.sub(new, a)
			file.seek(0)
			file.truncate()
			file.write(a)


def parseFolderforSaves(folder):
	for subdir, dirs, files in os.walk(folder):
		for filename in files:
			filepath = subdir + os.sep + filename
			if filepath.__contains__("SUBSEA"):
				writeXMLToFile(filepath, inplace=False)

folder = "D:\sbpd land"
parseFolderforSaves(folder)
