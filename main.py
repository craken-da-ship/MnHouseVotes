
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
        billPageLinks = get_links(billPage)
        allBillVotes = []
        for voteLinks in billPageLinks:
            if "votes/votes.asp" in voteLinks:
                voteLink = voteLinks[9:-17]
                votePage = page_grab(voteLink)
                if votePage == "Page Error":
                    continue
                votes = get_votes(votePage)
                billVotes = {
                    "Vote Link": voteLink,
                    "Votes Affirmative": get_affirmative(votes),
                    "Votes Negative:": get_negative(votes)
                }
                allBillVotes.append(billVotes)
        billDict = {
            "Bill Name": billName,
            "All Bill Votes": billUrl,
            "Votes": allBillVotes
        }
        allBillsList.append(billDict)
