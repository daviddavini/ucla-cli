import json
import re
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup, NavigableString

from ucla_cli.get_course_summary import get_course_summary
from termcolor import cprint



def extract_course_summary(soup):
    status_data = soup.find_all(class_="statusColumn")[1].find("p")
    return {
        "status": [x for x in status_data.contents if isinstance(x, NavigableString)],
        "waitlist": soup.find_all(class_="waitlistColumn")[1].find("p").contents[0],
        "day": soup.find_all(class_="dayColumn")[1].find("p").text,
        "time": soup.find_all(class_="timeColumn")[1].find_all("p")[1].text,
        "location": soup.find_all(class_="locationColumn")[1].find("p").contents[0].strip(),
        "units": soup.find_all(class_="unitsColumn")[1].find("p").contents[0],
        "instructor": soup.find_all(class_="instructorColumn")[1].find("p").contents[0],
    }


def clean_status(status):
    if status == ["Cancelled"]:
        return 0, 0
    m = re.search(r"(\d+) of (\d+) Enrolled", status[1])
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"Class Full \((\d+)\)", status[1])
    if m:
        return int(m.group(1)), 0
    m = re.search(r"Class Full \((\d+)\), Over Enrolled By (\d+)", status[1])
    if m:
        return int(m.group(1)) + int(m.group(2)), int(m.group(1))
    m = re.search(r"\((\d+) capacity, (\d+) enrolled, (\d+) waitlisted\)", status[1])
    if m:
        return int(m.group(2)), int(m.group(1))
    raise ValueError


def clean_course_summary(data):
    num_enrolled, total_spots = clean_status(data["status"])
    data.update(
        {
            "status": data["status"][0],
            "num_enrolled": num_enrolled,
            "total_spots": total_spots,
            "num_available": num_enrolled - total_spots,
            "day": data["day"],
            "time": data["time"],
            "location": data["location"],
            "units": data["units"],
        }
    )
    return data



class Column:
    def __init__(self, name, fmt):
        self.name = name
        self.fmt = fmt
    def header(self):
        return self.fmt.format(self.name.upper())
    def row(self, data):
        return self.fmt.format(data)

def soc(args):
    columns = [
        Column("subj", "{}"),
        Column("numb", "{:<5}"),
        Column("uni", "{:>3}"),
        Column("instructor", "{:<20}"),
        Column("status", "{:<15}"),
        Column("enr", "{:>3}"),
        Column("cap", "{:>3}"),
        Column("ovr", "{:>3}"),
        Column("days", "{:>6}"),
        Column("times", "{:<22}"),
        Column("location", "{:<31}"),
        Column("title", "{}"),
    ]
    for c in columns:
        print(c.header(), end=" ")
    print(flush=True)
    # url = 'https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex'
    url = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t={}&sBy=subject&subj={}&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
    url = url.format(args.term, args.subject)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    scripts = soup.find_all(string=re.compile("addCourse"))
    for _i, script in list(enumerate(scripts)):
        m = re.search(r"AddToCourseData\((.*),({.*})\)", script.string)
        course_id = json.loads(m.group(1))
        title = soup.find(id=course_id+'-title').contents[0]
        number, name = title.split(" - ")
        model = json.loads(m.group(2))
        sum_soup = get_course_summary(model)
        data = extract_course_summary(sum_soup)
        data = clean_course_summary(data)
        row = [args.subject, number, data['units'], data['instructor'], data['status'], data['num_enrolled'], data['total_spots'], data['num_available'], data['day'], data['time'], data['location'], name]
        if data['status'] == 'Open':
            color = 'green'
        elif data['status'] == 'Waitlist':
            color = 'yellow'
        elif 'Closed' in data['status']:
            color = 'red'
        elif 'Cancelled' in data['status']:
            color = 'dark_grey'
        else:
            color = None
        for c, d in zip(columns, row):
            cprint(c.row(d), color, end=" ")
        print(flush=True)


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser", required=True)
    parser_soc = subparsers.add_parser("classes", help="Search the Schedule of Classes")
    parser_soc.add_argument("term")
    parser_soc.add_argument("-s", "--subject", help="Subject Area to search classes for")
    args = parser.parse_args()

    if args.subparser == "classes":
        soc(args)


if __name__ == "__main__":
    main()
