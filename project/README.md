SMART Budget

YouTube Link: https://youtu.be/Ja5y8LFSrGw 

The purpose of my website to allow users to budget 
their money in a flexible and easy way.

WHAT'S NEEDED FOR THE WEBSITE?

I implemented my web application through VS Code and 
I used flask run to access the actual website through 
the GitHub server, just like we were requried to do 
so for finance. My website will only need the files 
included with this submission. I used Python, HTML, 
SQL, CSS, and Jinja to code my website. 

HOW TO USE THE WEBSITE?

The website is pretty straight forward. There are 
5 section in the navbar: Overview, Expenses, Income, 
Distribution Tool, and Create New Tool. The Overview
page will allow user to see a table of their 
budgeting categories, how much they have saved in each
category, and any notes they chose to add to help
them remember why they created each category. Additonally, 
there are some delete buttons on the right which will
allow users to delete any categories they no longer
want. At the bottom of the page, the Create New Budget
Category section will allow users to create new budgeting
categories, which will be added to the table above it after 
pressing the Create button. 

The expenses page will allow users to register any
expeneses they had. They have to had the date of the expense,
amount, a breif description, and the category they want
to subtract the amount from. After pressing the Add button, 
the amount they inputed will be subtracted from the total 
amount in the category they subtracted. The transaction will
be reflected in a history table in the same page, just below 
input fields. 

The income page works similarly to the expenses page, but
instead of subtracting the inputed amount from the total 
of the selected category, it will add to that category.

The Distribution Tool page will help users know how much
money they should allocate to each category if they want to
split a certain amount between different categories. For
example, if a user wants to split $500 across different
budgeting categories, then they input 500 in the text field,
and depending on the percentage per category they chose, 
the amounts will be shown next to each category. For new
users, they will have to create a new tool first in the 
Create New Tool page. 

In the New Tool Page, users will be able to create category
allocations based on percentages out of 100%. For example, 
if a user has three categories (Savings, Flexible, and College), 
then they can choose to allocate 50% of any amount to college, 
30% to savings, and 20% to flexible. The user can then go to 
the Distribution Tool website to input any amount they want to
distribute using their new tool. 

This website was inspired by the CS50 Finance website. 