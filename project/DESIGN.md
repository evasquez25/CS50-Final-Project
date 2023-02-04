WHY DOES IT LOOK THE WAY IT LOOKS? 

I took a lot of inspiration from the CS50 Finance website.
I used most of the layout as the base of my web application.
I changed a few things, like the logo on the top-left 
corner to give it a bit of personality. I also changed the
menu items in the navar. 

The font of the logo is Chalkduster, which is a playful
looking font. I chose this font because I want my website
to look appealing and fun, because budgeting doesn't always
have to be boring and hard. I want users to feel like
budgeting is easy and fun to do. 

The tables in each of the pages are also inspired by 
the Finance website. I used bootstrap to make the pages
look the way they do. Some of the tables have the option
for deleting items from them. I did this becaues this 
website is supposed to give people a flexible way of
managing their money, so they are encouraged to change
things around as they see fit. By adding delete options, 
I'm giving users the freedom to change their budgeting
layout in the future in case they no longer need a certain
category or tool. It also makes the website more interactive. 

I changed the expeness and income pages color layout a bit
too. For expenses, I used red to indicate a subtraction.
For income, I used green for addition. These colors 
make using the website more appealing. 

Additionally, I used a few SQL tables to keep track of 
the money inputed in the income and expenses pages. 
New income inputs will add to the budget_categories 
database which is used in the Overview page. Expenses 
will subtract from this database. 

In the Create New Tool and Distribution tool pages, there
is the option for users to use percentages. In my app.py
code sheet, I used a math strategy to turn integers into
decimals so when a number is multiplied by that decimal
(and the decimal is less than 1), the result will be a
percentage of the original amount. I took inspiration from
a StackOverflow page I found.

I used bootstrap for the buttom designs and colors. 


UNDER THE HOOD

I used many of the features shown in the app.py
from the CS50 Finacne web app. However, I tried
my best to use only the things I needed, and leave
out the things that only applied to the Finance 
application. I also made use of the helpers.py
code sheet, which was very useful in helping me
debug my application. 