import re
import json

def calendar_data(text):
    m = re.search(r"createFullCalendar\(\$.parseJSON\(\'(\[.*\])\'\)\)", text)
    calendar_data = json.loads(m.group(1))
    return calendar_data
