#Verify that the ad counts are correct, even when they are over 100.
import random
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()
browser.get("http://www.moat.com")
wait = WebDriverWait(browser, 2000)


links = browser.find_elements_by_css_selector("fieldset #search-suggestions-box > a")
link_to_click = random.choice(links)
link_name = link_to_click.text

print link_name
try:
    link_to_click.click()
    wait.until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.query-summary')
        ))
except TimeoutException:
    print "Search results page for " + link_name + " may not have loaded"

query_summary = browser.find_element_by_css_selector(".search-form .query-summary")
result_count = int(re.sub(r'\D', "", query_summary.text))
thumbnail_count = 0
show_more_ads_button = browser.find_element_by_css_selector("x")

#print thumbnail_count
print result_count
print thumbnail_count

def scroll_element_into_view(browser, element):
    y = element.location['y']
    browser.execute_script('window.scrollTo(0, {0})'.format(y))

while thumbnail_count <= result_count:
    thumbnail_count = len(browser.find_elements_by_css_selector(".adcontainer"))
    scroll_element_into_view(browser, show_more_ads_button)
    show_more_ads_button.click()
    print thumbnail_count



#Close the browser session
browser.close()