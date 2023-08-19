import json
import requests

def get_level_separated_search_data(term, subject):
    #url = "https://sa.ucla.edu/ro/ClassSearch/Public/Search/GetLevelSeparatedSearchData?input=%7B%22search_by%22%3A%22subject%22%2C%22term_cd%22%3A%2223f%22%2C%22subj_area_cd%22%3A%22COM+SCI%22%2C%22ses_grp_cd%22%3A%22%25%22%7D&level=2"
    url = "https://sa.ucla.edu/ro/ClassSearch/Public/Search/GetLevelSeparatedSearchData"
    params = {'input': [json.dumps({"search_by":"subject","term_cd":term,"subj_area_cd":subject,"ses_grp_cd":"%", "crs_catlg_no_cd":"0004AL"})], 'level': ['3']}
    resp = requests.get(url, params)
    return resp.text

if __name__ == "__main__":
    print(get_level_seperated_search_data("23F","PHYSICS"))
