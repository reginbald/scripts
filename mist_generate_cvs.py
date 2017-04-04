#!/usr/bin/env python
"""
Generates a CSV file from http://mist.valispace.com/rest based on user input.
* Prequisites
 - Install Python on your computer, https://www.python.org/downloads/
 - Run the following command: 'pip install coreapi-cli'
* How to run
 - Run the following command: 'python mist_generate_cvs.py'
"""
__author__ = "Jon Reginbald Ivarsson"
__copyright__ = "Copyright 2017, MIST - THE MINIATURE STUDENT SATELLITE"
__credits__ = ["Jon Reginbald Ivarsson"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jon Reginbald Ivarsson"
__email__ = "jriv@kth.se"
__status__ = "Production"

import getpass
import csv
import coreapi

print "Please enter your Valispace username and password"
USERNAME = raw_input("Username: ")
PASSWORD = getpass.getpass("Password: ")

VALIS = raw_input("Enter vali ids you want to export separated with commas: ")
VALIS = [x.strip() for x in VALIS.split(',')]

AUTH = coreapi.auth.BasicAuthentication(
    username=USERNAME,
    password=PASSWORD
)

CLIENT = coreapi.Client(auth=AUTH)

if len(VALIS) == 1 and VALIS[0] == '': # get default valis
    print "Retrieving default valis"
    DATA = CLIENT.get('http://mist.valispace.com/rest/import-export/3')
    VALIS = map(str, DATA['export_valis'])

EXPORT = []
for vali in VALIS:
    print "Retrieving vali data with id: " + vali
    DATA = CLIENT.get('http://mist.valispace.com/rest/vali/'+vali)
    DATA['parent_data'] = CLIENT.get('http://mist.valispace.com/rest/component/' +
                                     str(DATA['parent']))
    EXPORT.append(DATA)

print "Generating CSV file"
with open('export.csv', 'w') as csvfile:
    FIELDNAMES = ['vali', 'name', 'value', 'unit', 'formula',
                  'margin_plus', 'margin_minus', 'minimum',
                  'maximum', 'type', 'type_name', 'parent', 'parent_name']
    WRITER = csv.DictWriter(csvfile, fieldnames=FIELDNAMES, delimiter=";")
    WRITER.writeheader()

    for e in EXPORT:
        WRITER.writerow({
            'vali': e['id'],
            'name': e['name'],
            'value': e['value'],
            'unit': e['unit'],
            'formula':e['formula'],
            'margin_plus':e['margin_plus'],
            'margin_minus':e['margin_minus'],
            'minimum':e['minimum'],
            'maximum':e['maximum'],
            'type':e['type'],
            'type_name':e['type_name'],
            'parent':e['parent'],
            'parent_name':e['parent_data']['name']
        })

print "CVS file generated"
