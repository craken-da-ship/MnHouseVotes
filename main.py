import re
from urllib.request import urlopen

allBills = "https://www.house.mn.gov/votes/Votesbydatels93.asp"


def page_grab(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html


def get_links(page):
    pattern = "<a href.*?>.*?</a.*?>"
    match_results = re.findall(pattern, page, re.IGNORECASE|re.DOTALL)
    return match_results


allBillsHTML = page_grab(allBills)

billLinks = get_links(allBillsHTML)

allBillsList = []
for link in billLinks:
    if "votesbynumber" in link:
        billUrl = link[9:-12]
        billName = link[-10:-4]

        # Add link and bill number to dict
        # follow link and get all links to vote page and add to dict
        # pull link out of code
        billPage = page_grab(billUrl)
        billPageLinks = get_links(billPage)
        allBillVoteLinks = []
        for voteLinks in billPageLinks:
            if "votes/votes.asp" in voteLinks:
                allBillVoteLinks.append(voteLinks[9:-17])
        billDict = {
            "Bill Name": billName,
            "All Bill Votes": billUrl,
            "Links to votes": allBillVoteLinks
        }
        allBillsList.append(billDict)
