# SplitIt! Design
## Introduction

In SplitIt!, login.html, register.html, layout.html, apology.html, and helpers.py are all heavily influenced by CS50 finance. Inputs from index.html and method.html are stored in a SQL database called split.db in a database called users. Users stores a user’s login information and session id. It also stores values called count and method. These allows the site to know whether a user wanted to split a bill equally or by dish and how many people were in a person’s party.

## Manual
The function manual() in application.py is the centerpiece of our application along with its accompanying web formatting manual.html. Upon a successful GET request, “manual” queries the database to see if the user has chosen to split “evenly” or “bydish” and to check how many people a user said they wanted to split the bill between. It then passes those variables to manual.html.

## Evenly
First, manual.html checks to see which method (“evenly” or “bydish”) was chosen. If the method chosen was “evenly”, manual.html uses Jinja to render a webpage with only one section asking for the bill subtotal, tax, and tip percentage (inputted as a whole number), using html form validation to ensure proper inputs.

Upon a successful POST request from manual.html, application.py once again queries the database for a user’s count and method. If the user split it evenly, application.py checks for valid inputs from manual and then converts those inputs into useful numerical values, calculating each person’s share of the meal. Since calculating each person’s share of the meal by dividing the bill grand total by the number of people splitting it may result in shares with fractions of pennies, application.py correct for this by rounding all shares down to the nearest penny and calculating how many pennies in total (call the number of pennies n) were removed from our bill grand total. Application.py then renders the template evenly.html with appropriate values. Evenly.html prints a table with each person total, adding back on the aforementioned n pennies as whole pennies to the first n people splitting the bill.

### By Dish
If the method chosen was “bydish”, manual.html uses Jinja to render a webpage with two sections, one information on dishes and one for additional bill information. To explain this process, we will first describe its raw html and then describe how JS makes the site dynamic.

### Raw HTML
Referring to a global variable, MAXDISHES, declared above, the section on dish information first asks the user how many dishes they are going to input initialized at 1 with inputs ranging from 1 to the value of MAXDISHES. Then utilizing a for loop, this section assigns each dish from 1 to MAXDISHES to a row div with a unique id. Inside of each row div are inputs prompting the user for that dish’s value and for dish’s buyer. The section on additional bill information, like in evenly, prompts the user for tax percentage (inputted as a whole number).

### JS
When splitting by dish, the webpage uses JS to display certain divs dynamically based on the user input for number of dishes. Upon a successful GET request, JS hides the presence of the row divs for dish 2 through the MAXDISHES and only shows input fields for dish 1. When the user changes the number of dishes, JS reveals the number of dishes selected and requires a price for each dish, printing an alert via html form validation.

### POST
Application.py checks for valid inputs from manual.html for tax and tip and initializes three important variables subtotal, shared, and totals. Shared and subtotal are initialized to zeros while totals is initialized to a list of zeros with each the ith zero representing the total contribution for the ith person who is splitting the meal.

Then, application.py checks to see if the user inputted a value for the price each dish in manual.html. If there is an input for a dish’s price, application.py converts those inputs to usable numerical values and adds the dish’s price to subtotal. If the dish is a shared dish, it is added to shared. If the dish is being purchased by the ith person, it adds that value to the index in our list corresponding to that person.

After iterating through each dish in the form, application.py converts tax and tip into usable values, calculating each person’s share of tax and tip based on their proportion of the meal and adding it to their index in total. Once again, we correct for partial cents using the process described above and display each person’s share in a table called bydish.html.

## Style:
The style comes mostly from https://bootswatch.com/ using the “Minty” theme. This is where the header menu, the colored borders (the boxes around the forms on each page), and the button design come from. The color scheme was based on careful color curation using this website: https://coolors.co/a7c6da-86cd82-72a276-666b6a-628395.

## Additional Functionality:
### Change Password:
Password.html prompts a user for their username, old password, new password and confirmation, validating inputs with JS. The function password() in application.py ensures that the user’s username and old password are correct, returning an apology page if not. Upon correct login credentials, it alters the user’s login credentials in the users database in split.db.

![password](/screenshots/password.png)
<p align="center">
  <em>SplitIt's Password page</em>
</p>

### Venmo:
When registering, you have an option to input a venmo username. If you decide to do so, it will be saved in the database split. You can always add or change your venmo username once you have logged in to the page. If you have a venmo username, you will see a link that sends you to venmo when you arrive at your final page.

![venmo](/screenshots/venmo.png)
<p align="center">
  <em>SplitIt's Venmo Add/Change page</em>
</p>