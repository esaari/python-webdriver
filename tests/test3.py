#Verify that the ad counts are correct, even when they are over 100.
import random
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from IPython import embed

browser = webdriver.Firefox()
browser.get("http://www.moat.com")
wait = WebDriverWait(browser, 5)

links = browser.find_elements_by_css_selector("fieldset #search-suggestions-box > a")
link_to_click = random.choice(links)
link_name = link_to_click.text

print "Brand name: " + link_name

try:
    #Click the link and then verify the results summary loaded
    link_to_click.click()
    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".query-summary")
        ))
except TimeoutException:
    print "Search results page for " + link_name + " may not have loaded"

query_summary = browser.find_element_by_css_selector(".search-form .query-summary")
result_count = int(re.sub(r'\D', "", query_summary.text))
thumbnail_elements = browser.find_elements_by_css_selector("div .frame")
thumbnail_count = len(thumbnail_elements)

print "Number of results... " + str(result_count)

while thumbnail_count < result_count:
    #Print current number of thumbs so we at least know we keep incrementing
    print "Number of thumbs currently displayed: " + str(len(browser.find_elements_by_css_selector("div .frame")))
    #Use Javascript to click the button, faster/more reliable than webdriver click
    browser.execute_script("$('.more-holder button').click()")
    #Wait until thumbs have loaded
    wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div .frame"))
    )
    #Update the thumbnail count
    thumbnail_count = len(browser.find_elements_by_css_selector("div .frame"))

try:
    assert thumbnail_count == result_count
except AssertionError:
    print "Expected " + str(result_count) + " ad thumbnails, only " + str(thumbnail_count) + " seemed to display"
else:
    print "Test passed: " + str(thumbnail_count) + " of " + str(result_count) + " ads displayed"

#Close the browser session
browser.quit()