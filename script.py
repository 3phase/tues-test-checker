import os
import sys
import zipfile
import requests
import json

BASE_FOLDER = 'D:/School/TUES-Teach/WD18-19/'
EXTRACTIONS_FOLDER = 'extractions/'

file_name = sys.argv[1]
file_name_without_extention = file_name.split('.')[0]
zip_ref = zipfile.ZipFile(file_name, 'r')
zip_ref.extractall(BASE_FOLDER + EXTRACTIONS_FOLDER)
zip_ref.close()

target_folder = BASE_FOLDER + EXTRACTIONS_FOLDER + file_name_without_extention
# print(target_folder)
html_pages = []
directory = os.fsencode(target_folder)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".html"):
        html_pages.append(filename)
        continue
    else:
        continue

req_target = 'https://validator.w3.org/nu/?out=json'

path = './' + EXTRACTIONS_FOLDER + '/' + file_name_without_extention + '/' + html_pages[0]
data = open(path, 'rb').read()

request = requests.post(req_target, data=data, headers={'Content-Type':'text/html'})
json_data = json.loads(request.text)
print(json_data)
