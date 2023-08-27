import requests

def building_list():
    url = "https://registrar.ucla.edu/faculty-staff/classrooms-and-scheduling/building-list"
    resp = requests.get(url)
    return resp.text

if __name__ == "__main__":
    print(building_list())
