# MnHouseVotes
 
List of all votes in the house. Currently, only for 2023-2024 session. 
The intial scraping and excel creation is done via python. 
Then the rest of the work is done in excel. 

## Steps after script to recreate final sheet
Copy columns from normalized 
to expanded without chaning the order of anything. 
Once copied create two new tabs, one for Vote Per Rep, 
one for list of reps. Rename first tabe "All Votes"

Insert list of reps as table and name table.

In Cell H1 and H2 Create Table with Header of 
"Choose your Representative" and table name of "Reps"
In H2 do data validation to Allow List and source of
='Reps'!$A$4:$A$130


Starting on Row 2 on Vote Per Rep create columns 
- Column1
- Bill Name
- Description
- Date
- Vote

Line 3 in A through E use the following excel formulas.

+ Cell A2: ='All Votes'!A2
+ Cell B2: ='All Votes'!B2
+ Cell C2: ='All Votes'!E2
+ Cell D2: ='All Votes'!F2
+ Cell E2: =IF(ISNUMBER(SEARCH(Reps[Choose your Representative],'All Votes'!H2)), "Yes", IF(ISNUMBER(SEARCH(Reps[Choose your Representative],'All Votes'!J2)), "No", "Absent"))

Drag fill format cells A3-E3 till end of number of votes taken. 
In the uploaded example that is line 1743

## Future plans withing python script

- Create only one spreadsheet with all columns. 
- Create the additional tabs and propogate fields
- Create all the formula logic