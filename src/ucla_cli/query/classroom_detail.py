import requests

def classroom_detail(term, building_code, room_code):
    #url = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassroomDetail?term=23F&classroom=KAPLAN++%7C++00348++"
    url = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassroomDetail"
    params = {
        "term": term,
        "classroom": "{}|{}".format(building_code, room_code),
    }
    resp = requests.get(url, params)
    return resp.text

if __name__ == "__main__":
    print(classroom_detail("23F", "KAPLAN  ", "  00348  "))
