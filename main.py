
from functions import *

allBills = "https://www.house.mn.gov/votes/Votesbydatels93.asp"

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
        if page_grab == "Page Error":
            continue
        billInfo = get_billinfo(billPage)
        allBillVotes = []
        for vote in billInfo:
            votePage = page_grab(vote['Link'])
            if votePage == "Page Error":
                continue
            votes = get_votes(votePage)

            billVotes = {
                "Vote Link": vote['Link'],
                "Description": vote['Description'],
                "Date": vote['Date'],
                "Affirmative Count": vote['Yeas'],
                "Votes Affirmative": get_affirmative(votes),
                "Negative count": vote['Nays'],
                "Votes Negative:": get_negative(votes)
            }
            allBillVotes.append(billVotes)
        billDict = {
            "Bill Name": billName,
            "All Bill Votes": billUrl,
            "Votes": allBillVotes
        }
        allBillsList.append(billDict)

create_pd(allBillsList)
