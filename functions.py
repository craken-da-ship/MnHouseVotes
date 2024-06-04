import re
from urllib.request import urlopen
import pandas
import pandas as pd


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


def get_billinfo(billpage):
    billpagepattern = "<b>Date.*?Bill #.*?Description.*?Yeas.*?Nays.*?</td>"
    infoblock = re.findall(billpagepattern, billpage, re.IGNORECASE | re.DOTALL)
    patterns = ["<br /.*?SF.*?<br />",
                "<br /.*?HF.*?<br />",
                "<b>Description.*?<br />.*?<br />.*?<br />",
                "<b>Yeas</b><br />.*?[0-9]+.*?</td>",
                "<b>Nays</b><br />.*?[0-9]+.*?</td>",
                "<a href.*?>.*?</a.*?>"]

    bill = []
    for info in infoblock:
        for pattern in patterns:
            match_results = re.findall(pattern, info, re.IGNORECASE | re.DOTALL)
            if match_results and ("HF" in pattern or "SF" in pattern):
                if "HF" in pattern:
                    parsed = re.findall(r'\>(.*?)\<', match_results[0], re.DOTALL)
                    date = parsed[0].splitlines()[0]
                    billname = parsed[5].splitlines()[1]
                elif "SF" in pattern:
                    parsed = re.findall(r'\>(.*?)\<', match_results[0], re.DOTALL)
                    date = parsed[0].splitlines()[0]
                    billname = parsed[5].splitlines()[1]
                else:
                    continue
            elif "Description" in pattern:
                parsed = re.findall(r'\>(.*?)\<', match_results[0], re.DOTALL)
                description = (parsed[4].splitlines())[1]
            elif "Yeas" in pattern:
                yeas = re.findall("[0-9]+", match_results[0], re.IGNORECASE | re.DOTALL)
            elif "Nays" in pattern:
                nays = re.findall("[0-9]+", match_results[0], re.IGNORECASE | re.DOTALL)
            elif "href" in pattern:
                link = match_results[0][9:-17]
            else:
                continue
        billinfo = {
            "Bill Name": billname,
            "Date": date,
            "Description": description,
            "Yeas": yeas[0],
            "Nays": nays[0],
            "Link": link
        }
        bill.append(billinfo)
    return bill


def create_pd(bills):
    df = pd.DataFrame(data=bills)
    expanded = df.explode('Votes')
    normalized = pd.json_normalize(expanded['Votes'])
    expanded.to_excel("expanded.xlsx")
    normalized.to_excel("normalized.xlsx")
