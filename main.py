import re
from urllib.request import urlopen

allBills = "https://www.house.mn.gov/votes/Votesbydatels93.asp"


def page_grab(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html


allBillsHTML = page_grab(allBills)

pattern = "<a href.*?>.*?</a.*?>"

match_results = re.findall(pattern, allBillsHTML, re.IGNORECASE)

for link in match_results:
    if "votesbynumber" in link:
        print(link)
