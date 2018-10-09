import os
import sys
import zipfile
import requests
import json
from fpdf import FPDF

def create_pdf_service_fields():
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 13.0)
    pdf.set_y(8)
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(65)
    pdf.cell(50, 10, 'TUES, WD18/19', 0, 1, 'C')
    # Line break
    pdf.cell(65)
    pdf.cell(50, 5, 'Personalized Report', 0, 1, 'C')
    pdf.set_font('Arial', '', 15)
    pdf.cell(65)
    pdf.cell(50, 10, 'Sample Name, ' + file_name, 0, 2, 'C')
    pdf.ln(20)


def publish_err(shorthand, line = -1):
    if shorthand == 'encoding':
        pdf.cell(w=10, ln=2, txt='There\'s no indicated encoding. Error message: ' + shorthand, border=0, align='L')
        pdf.ln(8)
    elif shorthand == 'no_doctype':
        pdf.cell(w=10, ln=2, txt='There\'s no doctype included. Error message: ' + shorthand, border=0, align='L')
        pdf.ln(8)
    elif shorthand == 'no_title':
        pdf.cell(w=10, ln=2, txt='There\'s no title in the head. Error message: ' + shorthand, border=0, align='L')
        pdf.ln(8)
    elif shorthand == 'unrecognized':
        pdf.cell(w=10, ln=2, txt='An unrecognized error appeared. Error message: ' + shorthand, border=0, align='L')
        pdf.ln(8)

def string_bases(string):
    if 'character encoding' in string:
        return 'encoding'
    elif 'without seeing a doctype':
        return 'no_doctype'
    elif 'required instance of child element "title"':
        return 'no_title'
    else:
        return 'unrecognized'

pdf = FPDF()

BASE_FOLDER = os.path.abspath('./') + '/'
EXTRACTIONS_FOLDER = 'extractions/'

file_name = sys.argv[1]
file_name_without_extention = file_name.split('.')[0]
zip_ref = zipfile.ZipFile(file_name, 'r')
zip_ref.extractall(BASE_FOLDER + EXTRACTIONS_FOLDER)
zip_ref.close()

target_folder = BASE_FOLDER + EXTRACTIONS_FOLDER + file_name_without_extention
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

create_pdf_service_fields()

publish_err('encoding')
publish_err('doctype')
publish_err('unrecognized')
pdf.output('test.pdf', 'F')

# for file in html_pages:
#     path = './' + EXTRACTIONS_FOLDER +  file_name_without_extention + '/' + file
#     data = open(path, 'rb').read()
#
#     request = requests.post(req_target, data=data, headers={'Content-Type':'text/html'})
#     json_data = json.loads(request.text)
#
#     print("Information about page " + file + "\n")
#     for message in json_data['messages']:
#         if (message['type'] == 'error'):
#             err_shortcode = string_bases(message['message'])
#             # print(message['message'])
#             publish_err(err_shortcode)
#
#     print("\n")
