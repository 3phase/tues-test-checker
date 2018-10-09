import os
import sys
import zipfile
import requests
import json
from fpdf import FPDF

def create_pdf_service_fields():
    pdf.add_page()
    pdf.set_xy(0, 8)
    pdf.set_y(8)
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(65)
    pdf.cell(50, 10, 'TUES, WD18/19', 0, 1, 'C')
    pdf.cell(65)
    pdf.cell(50, 5, 'Personalized Report', 0, 1, 'C')
    pdf.set_font('Arial', '', 15)
    pdf.cell(65)
    pdf.cell(50, 10, file_name, 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(65)
    pdf.cell(50, 3, '(raw output on the last page)', 0, 2, 'C')
    pdf.ln(5)

def file_scope_definition(file_name):
    pdf.ln(15)
    pdf.set_font('arial', 'B', 12)
    pdf.cell(w=10, ln=2, txt=file_name, border=0, align='L')
    pdf.ln(8)

def publish_err(msg, line = -1):
    pdf.set_font('arial', '', 11)
    pdf.multi_cell(w=0, h=4, txt=msg, border=0, align='L')
    pdf.ln(3)

def publish_raw(data):
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_y(8)
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(65)
    pdf.cell(50, 10, 'Raw Output', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(w=0, h=4, txt=data, border=0, align='L')

def string_bases(string):
    if 'character encoding' in string:
        return 'encoding'
    elif 'without seeing a doctype' in string:
        return 'doctype'
    elif 'required instance of child element “title”' in string:
        return 'no_title'
    elif '\<center\> element is obsolete' in string:
        return 'obsolete_center'
    else:
        return 'unrecognized'


BASE_FOLDER = os.path.abspath('./') + '/'
EXTRACTIONS_FOLDER = 'extractions/'
total_score_html = 100
pdf = FPDF()
raw_output = ''
page_err_msgs = []
total_page_err_msgs = []
req_target = 'https://validator.w3.org/nu/?out=json'

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

create_pdf_service_fields()

for file in html_pages:
    file_scope_definition(file)
    path = './' + EXTRACTIONS_FOLDER +  file_name_without_extention + '/' + file
    data = open(path, 'rb').read()

    request = requests.post(req_target, data=data, headers={'Content-Type':'text/html'})
    json_data = json.loads(request.text)

    for message in json_data['messages']:
        if (message['type'] == 'error'):
            err_shortcode = string_bases(message['message'])
            msg = message['message'].replace("“", "\"")
            msg = msg.replace("”", "\"")
            page_err_msgs.append(msg)
        raw_output += json.dumps(json_data)

    for msg in set(page_err_msgs):
        publish_err(msg)

    total_page_err_msgs += page_err_msgs

result = len(set(total_page_err_msgs))
# Some kind of formula
print(6 - 1/6*result)

publish_raw(raw_output)
pdf.output(file_name_without_extention + '.pdf', 'F')
