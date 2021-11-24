import csv
import json
import pandas as pd

#Driver code

#Decide the two file paths according to your computer system
csvFilePath = r"UnityAnalytics/Endeavor.One Department ID's.csv"
jsonFilePath = r"UnityAnalytics/departmentID_E1.json"

csv_file = pd.DataFrame(pd.read_csv(csvFilePath, sep = ",", header = 0, index_col = False))
csv_file.to_json(jsonFilePath, orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None, indent=4)