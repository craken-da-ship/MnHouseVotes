import re
from urllib.request import urlopen


def page_grab(url):
    try:
        page = urlopen(url)
    except:
        html = "page Error"
    else:
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

    return html


def get_links(page):
    pattern = "<a href.*?>.*?</a.*?>"
    match_results = re.findall(pattern, page, re.IGNORECASE | re.DOTALL)
    return match_results


def get_voteinfo(page):
    pattern = "<b>Date.*?Bill #.*?Description.*?Yeas.*?Nays.*?</td>"
    match_results = re.findall(pattern, page, re.IGNORECASE | re.DOTALL)
    return match_results


def get_votes(page):
    pattern = "Those who voted.*?</TABLE.*?>"
    match_results = re.findall(pattern, page, re.IGNORECASE | re.DOTALL)
    return match_results


def get_affirmative(votes):
    names = []
    for vote in votes:
        if "affirmative" in vote:
            pattern = '<td width="20%"><font size=2 face=arial>.*? </font></td>'
            parsed = re.findall(pattern, vote, re.IGNORECASE | re.DOTALL)
            for item in parsed:
                name = re.sub('<[^>]+>', '', item)
                names.append(name)

    return names


def get_negative(votes):
    names = []
    for vote in votes:
        if "negative" in vote:
            pattern = '<td width="20%"><font size=2 face=arial>.*? </font></td>'
            parsed = re.findall(pattern, vote, re.IGNORECASE | re.DOTALL)
            for item in parsed:
                name = re.sub('<[^>]+>', '', item)
                names.append(name)

    return names

