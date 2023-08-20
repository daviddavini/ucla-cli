import json
from urllib.parse import parse_qs

import requests
from bs4 import BeautifulSoup


def _decode_url(url):
    url, params = url.split("?")
    params = parse_qs(params)
    params = {key: [json.loads(v) for v in value] for key, value in params.items()}
    return params


def prep_params(params):
    return {key: [json.dumps(v) for v in value] for key, value in params.items()}


def get_course_summary(model):
    raw_params = {
        "model": [model],
        "FilterFlags": [
            {
                "enrollment_status": None,
                "advanced": None,
                "meet_days": None,
                "start_time": None,
                "end_time": None,
                "meet_locations": None,
                "meet_units": None,
                "instructor": None,
                "class_career": None,
                "impacted": None,
                "enrollment_restrictions": None,
                "enforced_requisites": None,
                "individual_studies": None,
                "summer_session": None,
            }
        ],
        "_": [1692258949331],
    }
    params = prep_params(raw_params)
    url = "https://sa.ucla.edu/ro/public/soc/Results/GetCourseSummary"
    resp = requests.get(url, params)
    soup = BeautifulSoup(resp.text, "html.parser")
    if not soup.text:
        raise Exception
    error = soup.find(class_="expanded-error-message")
    if error:
        raise Exception(error.text.strip())
    error = soup.find(class_="error_section")
    if error:
        raise Exception(error.text.strip())
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
