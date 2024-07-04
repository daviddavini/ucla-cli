from termcolor import cprint

from ucla_cli.display.common import status_color


class Column:
    def __init__(self, name, fmt):
        self.name = name
        self.fmt = fmt

    def header(self):
        return self.fmt.format(self.name.upper())

    def row(self, data):
        return self.fmt.format(data)

columns = None

def display_header(course_details):
    global columns
    columns = [
        Column("subject", "{:<7}"),
        Column("numb", "{:<5}"),
    ]
    if course_details:
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

def display_course(subject, subject_name, number, name, data, orig_data, course_details):
    if not columns:
        display_header(course_details)
    row = [subject, number]
    if course_details:
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
    color = status_color(orig_data["status"])
    for c, d in zip(columns, row):
        cprint(c.row(d), color, end=" ")
    print(flush=True)


def display_buildings(buildings):
    columns = [
        Column("code", "{:<8}"),
        Column("name", "{}"),
    ]
    for b in buildings:
        row = [b['building_code'], b['building_name']]
        for c, d in zip(columns, row):
            print(c.row(d), end=" ")
        print(flush=True)
