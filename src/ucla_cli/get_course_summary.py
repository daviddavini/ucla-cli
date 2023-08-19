import json

import requests
from bs4 import BeautifulSoup


def get_course_summary(model):
    params = {
        "model": [json.dumps(model)],
        "FilterFlags": [
            json.dumps(
                {
                    "enrollment_status": "O,W,C,X,T,S",
                    "advanced": "y",
                    "meet_days": "M,T,W,R,F",
                    "start_time": "8:00 am",
                    "end_time": "8:00 pm",
                    "meet_locations": None,
                    "meet_units": None,
                    "instructor": None,
                    "class_career": None,
                    "impacted": "N",
                    "enrollment_restrictions": None,
                    "enforced_requisites": None,
                    "individual_studies": "n",
                    "summer_session": None,
                }
            )
        ],
        #"_": ["1692258949331"],
    }
    url = "https://sa.ucla.edu/ro/public/soc/Results/GetCourseSummary"
    resp = requests.get(url, params)
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup


if __name__ == "__main__":
    print(
        get_course_summary(
            {
                "Term": "23F",
                "SubjectAreaCode": "EPS SCI",
                "CatalogNumber": "0001    ",
                "IsRoot": True,
                "SessionGroup": "%",
                "ClassNumber": "%",
                "SequenceNumber": None,
                "Path": "EPSSCI0001",
                "MultiListedClassFlag": "n",
                "Token": "MDAwMSAgICBFUFNTQ0kwMDAx",
            }
        )
    )
