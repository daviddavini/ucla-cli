import re
import json
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup, NavigableString

from .get_course_summary import get_course_summary

def soc(args):
    #url = 'https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex'
    url = 'https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t={}&sBy=subject&subj={}&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex'
    url = url.format(args.term, args.subject)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    scripts = soup.find_all(string=re.compile('addCourse'))
    for i, script in list(enumerate(scripts)):
        m = re.search('AddToCourseData\((.*),({.*})\)',script.string)
        course_id = json.loads(m.group(1))
        model = json.loads(m.group(2))
        #title = soup.find(id=course_id+'-title').contents[0]
        soup = get_course_summary(model)
        data_row = soup.find(class_='data_row')
        columns = data_row.find_all(class_=re.compile('Column'))
        data = soup.find_all(class_='statusColumn')[1].find('p')
        status = [x for x in data.contents if isinstance(x, NavigableString)]
        waitlist = soup.find_all(class_='waitlistColumn')[1].find('p').contents[0]
        day = soup.find_all(class_='dayColumn')[1].find('p').text
        time = soup.find_all(class_='timeColumn')[1].find_all('p')[1].text
        location = soup.find_all(class_='locationColumn')[1].find('p').contents[0].strip()
        units = soup.find_all(class_='unitsColumn')[1].find('p').contents[0]
        instructor = soup.find_all(class_='instructorColumn')[1].find('p').contents[0]
        print(i, model['SubjectAreaCode'], model['CatalogNumber'], end=' ')
        print("{: <60}".format("  ".join(status)), waitlist, day, time, location, units, instructor, sep='\t')

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser', required=True)
    parser_soc = subparsers.add_parser('classes', help='Search the Schedule of Classes')
    parser_soc.add_argument('term')
    parser_soc.add_argument('-s', '--subject', help='Subject Area to search classes for')
    args = parser.parse_args()

    match args.subparser:
        case 'classes':
            soc(args)

if __name__ == "__main__":
    main()
