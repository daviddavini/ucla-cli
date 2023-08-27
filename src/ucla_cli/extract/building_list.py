from bs4 import BeautifulSoup

def building_list(text):
    soup = BeautifulSoup(text, 'html.parser')
    table = soup.find("table")
    trs = table.find_all("tr")
    models = []
    for tr in trs[1:]:
        tds = tr.find_all("td")    
        models.append({
            "building_code": tds[0].text,
            "building_name": tds[1].text,
        })
    return models
