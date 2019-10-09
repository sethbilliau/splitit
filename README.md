# SplitIt! Overview

SplitIt! is a website designed to help groups who face the constant problem of splitting the bill accurately and quickly. Our website allows groups to easily assign specific dishes to specific people so that those who buy the most expensive dishes pay more than those who order something cheaper.

## Getting Started
SplitIt lives on Heroku and primarily uses python (including the flask micro framework), html, JavaScript and SQL. To run SplitIt, change directory into the splitit folder, execute the command “flask run,” and open the link that appears in your terminal. SplitIt will begin on a login page. This page will allow you to login to the app. If you have already created login, please enter your credentials. If do not have an existing login, click register on the navigation bar in the top right.

![Login](/screenshots/login.png)
<p align="center">
  <em>SplitIt's login page</em>
</p>

![Register](/screenshots/register.png)
<p align="center">
  <em>SplitIt's Register page</em>
</p>

## Landing Page and Method
The first time you’re using SplitIt, you should create a unique username with an accompanying password. After successfully doing so, you will be redirected to the SplitIt landing page. The landing page requires the user to input the number of people that are splitting a meal along with how the user would like to split it: either equally among all people or by dish. After this page, the user is sent to a “methods” page that allows the user to select the method by which they would like to input data: by uploading a receipt or by manually inputting data.

![Index](/screenshots/index.png)
<p align="center">
  <em>SplitIt's landing page</em>
</p>

![Methods](/screenshots/method.png)
<p align="center">
  <em>SplitIt's Method</em>
</p>

## Upload
If a user selects “upload”, the app will load upload.html, which will, soon, contain OCR functionality. Unfortunately, implementing a complicated OCR function that would create dishes that could be dragged and dropped to group members was a bit ambitious for this project despite successfully being able to run OCR on receipts using the Google Vision API

![Upload](/screenshots/upload.png)
<p align="center">
  <em>SplitIt's Upload page</em>
</p>

## Manual
If a user selects “manual”, the app will allow the user to manually input relevant fields into a form that will split their bill for them equally or by dish.

### Evenly
When split equally, the page will ask for the bill total before tax and tip, the tax amount, and the tip percentage. Once those values are submitted, the application will take the previously given number of people splitting the bill and it will display a table detailing how much money each person in the group owes.

![Evenly](/screenshots/evenlyinput.png)
<p align="center">
  <em>SplitIt's Evenly input page</em>
</p>

![Evenly](/screenshots/evenlyresults.png)
<p align="center">
  <em>SplitIt's Evenly results page</em>
</p>

## By Dish
When splitting the bill by dish, there will be two sections of the manual form. The first section, titled “Split Dishes!” asks for the number of dishes in the meal, the price of each dish, and who is paying for the dish. The second section, titled “Bill Details” asks for the tax amount and the tip percentage. The application automatically adds up all the dish prices inputted into the first section as well as the tax and tip entered in the second section and displays a table with the amount each person in the group will have to pay.

![Methods](/screenshots/error.png)
<p align="center">
  <em>SplitIt's By Dish input page (with an example of data validation)</em>
</p>

![Methods](/screenshots/bydish.png)
<p align="center">
  <em>SplitIt's By Dish input page cont'd</em>
</p>


## Built With


* [Bootswatch](https://bootswatch.com/minty/) - The general design template used
* [Coolors](https://coolors.co/a7c6da-86cd82-72a276-666b6a-628395) - Used to design site color scheme
* [W3Schools](https://www.w3schools.com/howto/howto_js_toggle_hide_show.asp) - Hiding and showing an element
* [W3Schools](https://www.w3schools.com/jquery/html_attr.asp) - Setting the attribute and value of an element for “manual”


## Authors
* **Seth Billiau**
* **Helen Huang**

## Acknowledgments

* Thank you to everyone who helped along the way with trying to integrate the OCR functionality!
