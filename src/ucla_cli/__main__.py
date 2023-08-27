import html
import json
import re
from argparse import ArgumentParser

from bs4 import BeautifulSoup, NavigableString
from termcolor import cprint

from ucla_cli import query
from ucla_cli import extract
from ucla_cli.course_titles_view import course_titles_view
from ucla_cli.get_course_summary import get_course_summary
from ucla_cli.results import results
from ucla_cli.clean import clean_course_summary

def extract_location(soup):
    p = soup.find_all(class_="locationColumn")[1].find("p")
    if p.button:
        return p.button.text.strip()
    return p.text.strip()

def extract_course_summary(soup):
    status_data = soup.find_all(class_="statusColumn")[1].find("p")
    return {
        "status": [x for x in status_data.contents if isinstance(x, NavigableString)],
        "waitlist": soup.find_all(class_="waitlistColumn")[1].find("p").contents[0],
        "day": soup.find_all(class_="dayColumn")[1].find("p").text,
        "time": [x for x in soup.find_all(class_="timeColumn")[1].find_all("p")[1].contents if isinstance(x, NavigableString)],
        "location": extract_location(soup),
        "units": soup.find_all(class_="unitsColumn")[1].find("p").contents[0],
        "instructor": soup.find_all(class_="instructorColumn")[1].find("p").contents[0],
    }


class Column:
    def __init__(self, name, fmt):
        self.name = name
        self.fmt = fmt

    def header(self):
        return self.fmt.format(self.name.upper())

    def row(self, data):
        return self.fmt.format(data)


def extract_course_data(soup):
    scripts = soup.find_all(string=re.compile("addCourse"))
    models = []
    for script in scripts:
        m = re.search(r"AddToCourseData\((.*),({.*})\)", script.string)
        course_id = json.loads(m.group(1))
        model = json.loads(m.group(2))
        models.append((course_id, model))
    return models


def soc(args):
    text = results()

    def reduce_subject(x):
        return x.replace(" ", "").lower()

    subject_table = re.search(r"SearchPanelSetup\('(\[.*\])'.*\)", text)
    subject_table = html.unescape(subject_table.group(1))
    subject_table = json.loads(subject_table)
    subject_name_table = {reduce_subject(x["value"]): x["label"] for x in subject_table}
    subject_code_table = {reduce_subject(x["value"]): x["value"] for x in subject_table}
    subject_name = subject_name_table[reduce_subject(args.subject)]
    subject = subject_code_table[reduce_subject(args.subject)]
    # we call results() again with our "main search field"
    # this is just to get the filter options, not the course list
    # but we call course_titles_view() for purely unfiltered course list
    text = results(args.term, subject)
    soup = BeautifulSoup(text, 'html.parser')
    locations = soup.select("#Location_options option")
    locations = {l.contents[0]: l['value'] for l in locations}
    filters = {
        'location': locations
    }
    columns = [
        Column("subject", "{:<7}"),
        Column("numb", "{:<5}"),
    ]
    if args.course_details:
        columns.extend(
            [
                Column("s", "{:1}"),
                Column("enr", "{:>3}"),
                Column("cap", "{:>3}"),
                Column("wai", "{:>3}"),
                Column("wcp", "{:>3}"),
                Column("days", "{:<7}"),
                Column("times", "{:<13}"),
                Column("location", "{:<14}"),
                Column("uni", "{:>3}"),
                Column("instructor", "{:<20}"),
            ]
        )
    columns.append(Column("title", "{}"))
    for c in columns:
        print(c.header(), end=" ")
    print(flush=True)
    page = 1
    last_page = False
    while not last_page:
        text = course_titles_view(args.term, subject, subject_name, page)
        last_page = False
        page += 1
        soup = BeautifulSoup(text, "html.parser")
        models = extract_course_data(soup)
        if not models:
            return
        for course_id, model in models:
            title = soup.find(id=course_id + "-title").contents[0]
            number, name = title.split(" - ")
            if args.course_details:
                sum_soup = get_course_summary(model)
                data = extract_course_summary(sum_soup)
                orig_data = data.copy()
                data = clean_course_summary(data, filters, args.mode)
            row = [subject, number]
            if args.course_details:
                row.extend(
                    [
                        data["status"],
                        data["num_enrolled"],
                        data["total_spots"],
                        data["num_waitlisted"],
                        data["waitlist_capacity"],
                        data["day"],
                        data["time"],
                        data["location"],
                        data["units"],
                        data["instructor"],
                    ]
                )
            row.append(name)
            color = None
            if args.course_details:
                if "Open" in orig_data["status"]:
                    color = "green"
                elif "Waitlist" in orig_data["status"]:
                    color = "yellow"
                elif "Closed" in orig_data["status"]:
                    color = "red"
                elif "Cancelled" in orig_data["status"]:
                    color = "dark_grey"
            for c, d in zip(columns, row):
                cprint(c.row(d), color, end=" ")
            print(flush=True)


def bl(args):
    text = query.building_list()
    buildings = extract.building_list(text)
    columns = [
        Column("code", "{:<8}"),
        Column("name", "{}"),
    ]
    for b in buildings:
        row = [b['building_code'], b['building_name']]
        for c, d in zip(columns, row):
            print(c.row(d), end=" ")
        print(flush=True)


def cgs(args):
    if not args.building:
        bl(args)
    else:
        text = query.classroom_detail(args.term, args.building, args.room)
        data = extract.calendar_data(text)
        for x in data:
            print("{}-{}".format(x['strt_time'], x['stop_time']), x['title'])
        

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser", required=True)
    parser_soc = subparsers.add_parser("classes", help="Search the Schedule of Classes", conflict_handler="resolve")
    parser_soc.add_argument("term")
    parser_soc.add_argument("-s", "--subject", help="Subject Area to search classes for")
    parser_soc.add_argument("-q", "--quiet", action="store_true", help="Just list course subject, name and title")
    parser_soc.add_argument("-h", "--human-readable", action="store_true")
    parser_room = subparsers.add_parser("rooms", help="Search the Classroom Grid Search", conflict_handler="resolve")
    parser_room.add_argument("-t", "--term")
    parser_room.add_argument("-b", "--building", help="Building to search schedule for")
    parser_room.add_argument("-r", "--room", help="Room to search schedule for")
    args = parser.parse_args()

    if args.subparser == "classes":
        args.course_details = not args.quiet
        del args.quiet
        args.mode = "plain" if args.human_readable else "hacker"
        soc(args)
    elif args.subparser == "rooms":
        cgs(args)


if __name__ == "__main__":
    main()
