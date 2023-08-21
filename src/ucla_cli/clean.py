import re 

def clean_time(time, mode):
    if mode == "plain":
        return "".join(time)
    if mode == "hacker":
        return clean_time_hacker(time)

def parse_time(t):
    m = re.match("(\d+):?(\d*)([pa])m", t)
    if not m:
        raise ValueError
    h = int(m.group(1))
    mins = m.group(2)
    mins = int(mins if mins else 0)
    p = 12 if (m.group(3)=='p' and h != 12) else 0
    return h+p+mins/60

def clean_time_hacker(time):
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
    for start, end in intervals:
        s = parse_time(start)
        e = parse_time(end[1:])
        s,e = [round(x) for x in [s,e]]
        times.extend(list(range(s,e)))
    return "".join(c if i in times else '.' for i, c in enumerate('89ABC1234567', 8))

def clean_status_code(status_code, mode):
    if mode == "plain":
        return status_code
    if mode == "hacker":
        return {
            'Open': 'O',
            'Waitlist': 'W',
            'Closed': 'C',
            'Closed by Dept ': 'C',
            'Cancelled': 'X',
            'Tentative': 'T',
            'Not available': 'S',
        }[status_code]
    raise ValueError


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


def clean_day(day, mode):
    if mode == "plain":
        return day
    if mode == "hacker":
        return clean_day_hacker(day)
    raise ValueError
        
def clean_day_hacker(day):
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

def clean_course_summary(data, filters, mode):
    num_enrolled, total_spots = clean_status(data["status"])
    num_waitlisted, waitlist_capacity = clean_waitlist(data["waitlist"])
    data = {
        "status": clean_status_code(data["status"][0], mode),
        "num_enrolled": num_enrolled,
        "total_spots": total_spots,
        "num_waitlisted": num_waitlisted,
        "waitlist_capacity": waitlist_capacity,
        "day": clean_day(data["day"], mode),
        "time": clean_time(data["time"], mode),
        "location": clean_location(data["location"], filters['location']),
        "instructor": clean_instructor(data["instructor"]),
        "units": data["units"],
    }
    return data
