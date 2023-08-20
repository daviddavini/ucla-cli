import html
import json
import re
from argparse import ArgumentParser

from bs4 import BeautifulSoup, NavigableString
from termcolor import cprint

from ucla_cli.course_titles_view import course_titles_view
from ucla_cli.get_course_summary import get_course_summary
from ucla_cli.results import results

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

def clean_time(time):
    if time == []:
        return ""
    if time == ['To be arranged']:
        return "?"
    if time == ['-','-','-']:
        return "?"
    if len(time) % 2 != 0:
        raise ValueError
    intervals = zip(time[::2],time[1::2])
    times = []
    def parse_time(t):
        m = re.match("(\d+):?(\d*)([pa])m", t)
        if not m:
            raise ValueError
        h = int(m.group(1))
        mins = m.group(2)
        mins = int(mins if mins else 0)
        p = 12 if (m.group(3)=='p' and h != 12) else 0
        return h+p+mins/60
    for start, end in intervals:
        s = parse_time(start)
        e = parse_time(end[1:])
        s,e = [round(x) for x in [s,e]]
        times.extend(list(range(s,e)))
    return "".join(c if i in times else '.' for i, c in enumerate('89ABC1234567', 8))

def clean_status_code(status_code):
    return {
        'Open': 'O',
        'Waitlist': 'W',
        'Closed': 'C',
        'Closed by Dept ': 'C',
        'Cancelled': 'X',
        'Tentative': 'T',
        'Not available': 'S',
    }[status_code]


def clean_status(status):
    if status == ["Cancelled"]:
        return 0, 0
    if status == ["Waitlist"]:
        return 0, 0
    m = re.search(r"(\d+) of (\d+) Enrolled", status[1])
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"Class Full \((\d+)\)", status[1])
    if m:
        return int(m.group(1)), int(m.group(1))
    m = re.search(r"Class Full \((\d+)\), Over Enrolled By (\d+)", status[1])
    if m:
        return int(m.group(1)) + int(m.group(2)), int(m.group(1))
    m = re.search(r"\((\d+) capacity, (\d+) enrolled, (\d+) waitlisted\)", status[1])
    if m:
        return int(m.group(2)), int(m.group(1))
    raise ValueError


def clean_waitlist(waitlist):
    if waitlist == "No Waitlist":
        return 0, 0
    m = re.search(r"(\d+) of (\d+) Taken", waitlist)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"Waitlist Full \((\d+)\)", waitlist)
    if m:
        return int(m.group(1)), int(m.group(1))

    m = re.search(r"(\d+) Waitlisted, Contact Instructor/Department", waitlist)
    if m:
        return int(m.group(1)), "?"
    raise ValueError


def clean_day(day):
    if day == "Not scheduled":
        return ""
    if day == "Varies":
        return day
    if day.upper() != day or " " in day:
        raise ValueError
    return "".join([c if c in day else "." for c in "UMTWRFS"])

def clean_instructor(instructor):
    #if instructor == 'No instructors':
    #    return ''
    return instructor

def clean_location(location, locations):
    #if location == "No Location":
    #    return ''
    ms = {l: re.match(l, location) for l in locations}
    matches = {l: m for l,m in ms.items() if m}
    if len(matches) != 1:
        raise ValueError
    l, m = matches.popitem()
    building, room = location[:m.end()], location[m.end():]
    return locations[l] + room

def clean_course_summary(data, filters):
    num_enrolled, total_spots = clean_status(data["status"])
    num_waitlisted, waitlist_capacity = clean_waitlist(data["waitlist"])
    data.update(
        {
            "status": clean_status_code(data["status"][0]),
            "num_enrolled": num_enrolled,
            "total_spots": total_spots,
            "num_waitlisted": num_waitlisted,
            "waitlist_capacity": waitlist_capacity,
            "day": clean_day(data["day"]),
            "time": clean_time(data["time"]),
            "location": clean_location(data["location"], filters['location']),
            "instructor": clean_instructor(data["instructor"]),
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
                data = clean_course_summary(data, filters)
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


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser", required=True)
    parser_soc = subparsers.add_parser("classes", help="Search the Schedule of Classes")
    parser_soc.add_argument("term")
    parser_soc.add_argument("-s", "--subject", help="Subject Area to search classes for")
    parser_soc.add_argument("-q", "--quiet", action="store_true", help="Just list course subject, name and title")
    args = parser.parse_args()
    args.course_details = not args.quiet
    del args.quiet

    if args.subparser == "classes":
        soc(args)


if __name__ == "__main__":
    main()
