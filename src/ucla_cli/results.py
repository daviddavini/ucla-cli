import requests

def results(term, subject):
    # url = 'https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t=23F&sBy=subject&subj=MATH+++&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex'
    #url = "https://sa.ucla.edu/ro/public/soc/Results?SubjectAreaName=Mathematics+(MATH)&t={}&sBy=subject&subj={}&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
    #url = url.format(term, subject)
    url = "https://sa.ucla.edu/ro/public/soc/Results"
    params = {'SubjectAreaName': ['Mathematics (MATH)'], 't': [term], 'sBy': ['subject'], 'subj': [subject], 'undefined': ['Go'], 'btnIsInIndex': ['btn_inIndex']}
    resp = requests.get(url, params)
    return resp.text

