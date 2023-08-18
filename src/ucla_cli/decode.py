url = input("URL: ")
from urllib.parse import parse_qs

[url, params] = url.split("?")
params = parse_qs(params)
print(url)
print(params)
