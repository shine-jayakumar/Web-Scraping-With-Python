
'''
Scraper.py

Extracts reviews from Walmart Webpage
Author: Shine Jayakumar
Email: shinejayakumar@yahoo.com

MIT License

Copyright (c) 2021 Shine Jayakumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import time

# path to chromedriver
driver_path = "D:\Software\chromedriver\chromedriver.exe"

# webpage url
page = "https://www.walmart.com/ip/Clorox-Disinfecting-Wipes-225-Count-Value-Pack-Crisp-Lemon-and-Fresh-Scent-3-Pack-75-Count-Each/14898365"

# condition
DATE_TILL = 'december'
YEAR_TILL = '2020'

# output file
OUTFILE = 'output.csv'

# how many times to retry if URL is blocked
NO_OF_RETRIES = 15


driver = webdriver.Chrome(driver_path)

# remove bot challenge div
def remove_bot_challenge():
    remove_bot_challenge = '''
    var body = document.querySelector("body");
    body.removeAttribute("class");
    var bot_challenge_div = document.getElementById("bot-handling-challenge");
    if(bot_challenge_div){bot_challenge_div.remove();}
    '''
    driver.execute_script(remove_bot_challenge)


# extracts reviews from current page and returns a list
def save_reviews():

    reviews_rows = []
    condition_status = False

    # reviews container div
    reviews = driver.find_elements(By.XPATH, "//div[@class='Grid ReviewList-content']")
    print(f'No of reviews found on this page: {len(reviews)}')

    if reviews:
        for review in reviews:
            review_heading = review.find_element_by_class_name('review-heading')
            review_title = ''
            review_date = review.find_element_by_class_name('review-date').find_element_by_class_name('review-date-submissionTime').text
            review_name = review.find_element_by_class_name('review-user').find_element_by_class_name('review-footer-userNickname').text
            review_rating = review_heading.find_element_by_class_name('average-rating').find_elements_by_tag_name('span')[1].text
            review_body = review.find_element_by_class_name('review-text').text

            # Title is missing for several reviews
            try:
                review_title = review_heading.find_element_by_tag_name('h3').text
            except NoSuchElementException as exception:
                pass


            reviews_rows.append([review_date, review_name, review_title, review_body, review_rating])

            # check condition
            if DATE_TILL in review_date.lower() and YEAR_TILL in review_date:
                condition_status = True
                break


    status = {
        "data": reviews_rows,
        "condition_status": condition_status
    }
    return status


def bot_main():
    driver.switch_to.default_content()
    remove_bot_challenge()
    driver.find_element_by_link_text("See all reviews").click()
    time.sleep(2)

    # selecting drop-down
    sort_by_dropdown = driver.find_element(By.XPATH, "//select[@class='field-input field-input--compact']")
    dropdown = Select(sort_by_dropdown)
    dropdown.select_by_value('submission-desc')
    time.sleep(3)
    remove_bot_challenge()
    driver.refresh()

    df_reviews = pd.DataFrame(columns=['Date', 'Name', 'Title', 'Body', 'Rating'])

    condition_reached = False

    while condition_reached is False:

        status = save_reviews()
        condition_reached = status['condition_status']

        if len(df_reviews) > 0:
            df_reviews = df_reviews.append(pd.DataFrame(status['data'], columns=df_reviews.columns), ignore_index=True)
        else:
            df_reviews = pd.DataFrame(status['data'], columns=df_reviews.columns)

        # do not got to next page if condition is reached
        if status['condition_status'] is False:
            time.sleep(2)
            driver.find_element(By.XPATH, "//button[@class='paginator-btn paginator-btn-next']").click()
            time.sleep(2)
            remove_bot_challenge()
            driver.refresh()

    # writing reviews to file
    with open(OUTFILE, 'w', encoding="utf-8") as fh:
        df_reviews.to_csv(fh, index=False, line_terminator='\n')
        print(f'\nExported reviews to: {OUTFILE}')
        print(f'No. of rows written: {len(df_reviews)}')

    driver.quit()



def restart_instance(times):

    cnt = 0
    url_blocked = True
    global driver
    while cnt < times:
        print(f'Retrying...({cnt+1})')
        driver.quit()
        time.sleep(3)
        driver = webdriver.Chrome(driver_path)
        driver.get(page)
        time.sleep(2)
        if "blocked?url" not in driver.current_url:
            url_blocked = False
            print('URL unblocked. Resuming extraction....')
            break

        cnt += 1

    return url_blocked

driver.get(page)
time.sleep(2)
print(f'Getting URL: {driver.current_url}')

if "blocked?url" in driver.current_url:

    print('Bot Challenge Page - Blocked URL. Restarting instance in 3 seconds')

    if restart_instance(NO_OF_RETRIES) is False:
        bot_main()
    else:
        print('URL is currently blocked. Please re-run the script after some time.')

else:
    bot_main()



