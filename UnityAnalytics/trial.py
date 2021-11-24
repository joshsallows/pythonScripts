import json
  
# JSON string:
# Multi-line string
x = "{'MODULE_NAME': 'IADC MODULE B 6 - PUMP KILL MUD IN ACCORDANCE WITH THE 2nd CIRCULATION OF DRILLER'S METHOD', 'DEVICE_UUID': '0cdefc070be97c170898d4e6da57e0c6f52d189b', 'DEPARTMENT_ID': 'ONLINE', 'UUID': '9475fde9-1e9a-46f8-b2cb-9281a20610b5'}"
x = x.replace("'", )
# parse x:
y = json.loads(x)
  
# the result is a Python dictionary:
print(y)