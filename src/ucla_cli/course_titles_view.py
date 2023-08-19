import json
import requests


def course_titles_view(search_data, term, subject, page):
    cookies = {
                'f5avraaaaaaaaaaaaaaaa_session_': 'FCFGLLGEFBDHHKCCCANHDMBHOEAKEGBKFEDIFHLDOEFFPINMKHDCAEHOHJHLJMELLJODBFOHPLOKNNAFPLIAIOLGIGOACEPLEDJJKENJICOHLLDMJEPJIHHAAPLKLADK',
                'f5avraaaaaaaaaaaaaaaa_session_': 'AHMKOAICLBLODPEHCJNNGODLLNCDBLPLAONFGNGJNPAJLNJOMHAPBEBONAJNAFHNEIEDMMCHOAJFILGJGBBAPFELFDCCPNCIIGDODJIBIIKDFDKDGAOHFPGDAPABFIDE',
                'f5avraaaaaaaaaaaaaaaa_session_': 'POHCDJKICLCHCKGJPADMCOCMDKNCABPNJHJLHBFJJLHBNIICNLJJOJIIJCICEDCPHHADBFHDOBKGBDMJMCAABDNELFIIPDFPHFIPHNIAIPCFHKCNBFDPOLIIOAKDEMGD',
                '_ga_Z2CGJ2TLK4': 'GS1.1.1692195452.1.1.1692195560.0.0.0',
                'ASP.NET_SessionId': 'tn4soawjkjg4zisn0l4nyqvx',
                'BIGipServersa.ucla.edu-SSL-pool': '1124175509.47873.0000',
                '__utma': '107622912.2119037293.1692195452.1692195801.1692195801.1',
                '__utmc': '107622912',
                '__utmz': '107622912.1692195801.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
                '_ga': 'GA1.1.2119037293.1692195452',
                '_ga_EWLBL9HEXX': 'GS1.1.1692198453.2.0.1692198453.0.0.0',
                'iwe_term_student': '23F',
                'f5avraaaaaaaaaaaaaaaa_session_': 'PILFAOCOGHBBMHDMKGIOAHBNKGGJDKBFDHKPEFLPIHGIFOPENNJNLFKDOAONFOCIPMEDJCBPHAMBHGMIBOFAGPCALLHPAACJLLLABGPJOGBDEABIIINEOIHMIGKOFNFJ',
                '_shibstate_1692422678_2348': 'https%3A%2F%2Fsa.ucla.edu%2Fdirectlink%2F203',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=FCFGLLGEFBDHHKCCCANHDMBHOEAKEGBKFEDIFHLDOEFFPINMKHDCAEHOHJHLJMELLJODBFOHPLOKNNAFPLIAIOLGIGOACEPLEDJJKENJICOHLLDMJEPJIHHAAPLKLADK; f5avraaaaaaaaaaaaaaaa_session_=AHMKOAICLBLODPEHCJNNGODLLNCDBLPLAONFGNGJNPAJLNJOMHAPBEBONAJNAFHNEIEDMMCHOAJFILGJGBBAPFELFDCCPNCIIGDODJIBIIKDFDKDGAOHFPGDAPABFIDE; f5avraaaaaaaaaaaaaaaa_session_=POHCDJKICLCHCKGJPADMCOCMDKNCABPNJHJLHBFJJLHBNIICNLJJOJIIJCICEDCPHHADBFHDOBKGBDMJMCAABDNELFIIPDFPHFIPHNIAIPCFHKCNBFDPOLIIOAKDEMGD; _ga_Z2CGJ2TLK4=GS1.1.1692195452.1.1.1692195560.0.0.0; ASP.NET_SessionId=tn4soawjkjg4zisn0l4nyqvx; BIGipServersa.ucla.edu-SSL-pool=1124175509.47873.0000; __utma=107622912.2119037293.1692195452.1692195801.1692195801.1; __utmc=107622912; __utmz=107622912.1692195801.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ga=GA1.1.2119037293.1692195452; _ga_EWLBL9HEXX=GS1.1.1692198453.2.0.1692198453.0.0.0; iwe_term_student=23F; f5avraaaaaaaaaaaaaaaa_session_=PILFAOCOGHBBMHDMKGIOAHBNKGGJDKBFDHKPEFLPIHGIFOPENNJNLFKDOAONFOCIPMEDJCBPHAMBHGMIBOFAGPCALLHPAACJLLLABGPJOGBDEABIIINEOIHMIGKOFNFJ; _shibstate_1692422678_2348=https%3A%2F%2Fsa.ucla.edu%2Fdirectlink%2F203',
        'Referer': 'https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="115", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    params = {
        'search_by': ['subject'],
        'model': [
            json.dumps(
                {
                    "term_cd": "23F",
                    "ses_grp_cd": "%",
                    "class_no": None,
                    "crs_catlg_no": None,
                    #"subj_area_cd": "MATH   ",
                    "subj_area_cd": search_data['subj_area_cd'],
                    #"subj_area_name": "Mathematics (MATH)",
                    "subj_area_name": search_data['SubjectAreaName'],
                    "class_prim_act_fl": "y",
                },
                separators=(',', ':'),
            )
        ],
        'pageNumber': [page],
        'filterFlags': [
            json.dumps(
                {
                    "enrollment_status": "O,W,C,X,T,S",
                    "advanced": "y",
                    "meet_days": "M,T,W,R,F",
                    "start_time": "8:00 am",
                    "end_time": "7:00 pm",
                    "meet_locations": None,
                    "meet_units": None,
                    "instructor": None,
                    "class_career": None,
                    "impacted": "N",
                    "enrollment_restrictions": None,
                    "enforced_requisites": None,
                    "individual_studies": "n",
                    "summer_session": None,
                },
                separators=(',', ':'),
            )
        ],
        #'_': ['1692429337029'],
    }
    #    url = 'https://sa.ucla.edu/ro/public/soc/Results/CourseTitlesView?search_by=subject&model=%7B%22term_cd%22%3A%2223F%22%2C%22ses_grp_cd%22%3A%22%25%22%2C%22class_no%22%3Anull%2C%22crs_catlg_no%22%3Anull%2C%22subj_area_cd%22%3A%22MATH+++%22%2C%22subj_area_name%22%3A%22Mathematics+(MATH)%22%2C%22class_prim_act_fl%22%3A%22y%22%7D&pageNumber={}&filterFlags=%7B%22enrollment_status%22%3A%22O%2CW%2CC%2CX%2CT%2CS%22%2C%22advanced%22%3A%22y%22%2C%22meet_days%22%3A%22M%2CT%2CW%2CR%2CF%22%2C%22start_time%22%3A%228%3A00+am%22%2C%22end_time%22%3A%227%3A00+pm%22%2C%22meet_locations%22%3Anull%2C%22meet_units%22%3Anull%2C%22instructor%22%3Anull%2C%22class_career%22%3Anull%2C%22impacted%22%3A%22N%22%2C%22enrollment_restrictions%22%3Anull%2C%22enforced_requisites%22%3Anull%2C%22individual_studies%22%3A%22n%22%2C%22summer_session%22%3Anull%7D&_=1692429337029'.format(page)
    url = "https://sa.ucla.edu/ro/public/soc/Results/CourseTitlesView"
    response = requests.get(
        url,
        params,
        cookies=cookies,
        headers=headers,
    )
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    print(course_titles_view("23F", "COM SCI", 1))
