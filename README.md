## Web-Scraping with Python 
[![](https://img.shields.io/github/license/shine-jayakumar/Covid19-Exploratory-Analysis-With-SQL)](https://github.com/shine-jayakumar/Covid19-Exploratory-Analysis-With-SQL/blob/Master/LICENSE "![](https://img.shields.io/github/license/shine-jayakumar/Covid19-Exploratory-Analysis-With-SQL)")

In this project, we’re going to programmatically extract customer reviews from Walmart’s webpage using Python. The script will automatically navigate to the next page simulating user interaction. We’d also see how to bypass the webpage’s bot-challenge  


**Table of Contents**

- [Packages](#Packages "Packages")
- [Bypass Bot Challenge](#Bypass-Bot-Challenge "Bypass Bot Challenge")


## Packages
- Selenium
- Pandas

## Bypass Bot Challenge
The page implements bot-challenge in two ways:
1)	The bot-challenge page loads on top of the main page and prevents users from interacting with the webpage until the user presses and hold the mouse button for 4-5 second. Once the action is complete, the script loads the main page and allows users to interact with the page.

![Bot Challenge Scenario 1](https://github.com/shine-jayakumar/Web-Scrapping-With-Python/blob/main/Bot-challenge.JPG)

2)	The bot-challenge script blocks the main url and doesn’t load the main page at all. 

![Bot Challenge Scenario 2](https://github.com/shine-jayakumar/Web-Scrapping-With-Python/blob/main/Bot-challenge1.JPG)

### Solution:
**Scenario 1**: 
We’re going to use JavaScript to locate and remove the DIV element which contains the bot challenge. 
This would let us have access to the main page, however, the page wouldn’t still allow the users to interact with the page yet. For this, we need to remove the CLASS tag from the BODY element. 
Since the bot challenge shows up on every page, it would be sensible to create a function to perform this operation.

**Scenario 2**:
To tackle the second scenario, We're simply going to refresh the webpage until the url is unblocked



Disclaimer: ***This script and information provided in this project is for educational purposes only***
