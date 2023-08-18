import json
import re
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup, NavigableString

from ucla_cli.get_course_summary import get_course_summary


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
    m = re.search(r"(\d+) of (\d+) Enrolled", status[1])
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"Class Full \((\d+)\), Over Enrolled By (\d+)", status[1])
    if m:
        return int(m.group(1)) + int(m.group(2)), int(m.group(1))
    return 0, 0


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


def pretty_course_name(subject, number):
    return "{:<15}".format(subject + number.lstrip("0"))


def pretty_course_summary_line(data):
    return "{:>3} {:<20} {:<10} {:>3}/{:<3} {:>+3d} {:5} {} {}".format(data["units"], data["instructor"], data["status"], data["num_enrolled"], data["total_spots"], data["num_available"], data["day"], data["time"], data["location"])


def soc(args):
    # url = 'https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex'
    url = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t={}&sBy=subject&subj={}&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
    url = url.format(args.term, args.subject)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    scripts = soup.find_all(string=re.compile("addCourse"))
    for _i, script in list(enumerate(scripts)):
        m = re.search(r"AddToCourseData\((.*),({.*})\)", script.string)
        json.loads(m.group(1))
        model = json.loads(m.group(2))
        name = pretty_course_name(model["SubjectAreaCode"], model["CatalogNumber"])
        soup = get_course_summary(model)
        data = extract_course_summary(soup)
        data = clean_course_summary(data)
        line = pretty_course_summary_line(data)
        print(name, line)


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
