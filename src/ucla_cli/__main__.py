import re
import json
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup

def soc(args):
    #url = 'https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex'
    url = 'https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t={}&sBy=subject&subj={}&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex'
    url = url.format(args.term, args.subject)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    scripts = soup.find_all(string=re.compile('addCourse'))
    for script in scripts:
        m = re.search('AddToCourseData\((.*),({.*})\)',script.string)
        course_id = json.loads(m.group(1))
        data = json.loads(m.group(2))
        #title = soup.find(id=course_id+'-title').contents[0]
        print(data['SubjectAreaCode'], data['CatalogNumber'], sep='\t')

parser = ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser', required=True)
parser_soc = subparsers.add_parser('classes', help='Search the Schedule of Classes')
parser_soc.add_argument('term')
parser_soc.add_argument('-s', '--subject', help='Subject Area to search classes for')
args = parser.parse_args()

match args.subparser:
    case 'classes':
        soc(args)

