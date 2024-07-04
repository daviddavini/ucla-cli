from typing import Iterable
import click
from termcolor import cprint

from ucla_cli.display.common import status_color

def comma_separated(strs):
    return ", ".join(strs) if isinstance(strs, list) else strs

def display_course(subject, subject_name, number, name, data, orig_data, course_details):
    cprint(f"{subject_name} {number}: {name}",attrs=["bold"])
    if course_details:
        kvs = {
            "Status": comma_separated(orig_data["status"]),
            "Waitlist": orig_data["waitlist"],
            "Days": data["day"],
            "Time": comma_separated(data["time"]),
            "Location": orig_data["location"],
            "Units": data["units"],
            "Instructor": comma_separated(data["instructor"]),
        }
        max_keylen = max(len(k) for k in kvs.keys())
        for k, v in kvs.items():
            padding = " " * (max_keylen-len(k))
            cprint(k, "blue", end="")
            print(f":{padding} ", end="")
            if k == "Status":
                color = status_color(orig_data["status"])
                cprint(v, color)
            else:
                print(v)
    click.echo()

def display_buildings(buildings):
    for b in buildings:
        cprint(f"{b['building_code']} {b['building_name']}", "bold")