#Verify the "Share this Ad" feature.

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from IPython import embed

browser = webdriver.Firefox()
browser.get("http://www.moat.com/search/results?q=Reuters")
wait = WebDriverWait(browser, 5)

first_thumbnail = browser.find_elements_by_css_selector(".adcontainer")[0]
creativeId = first_thumbnail.get_attribute("creativeid")


def hover(element):
    hover_action = ActionChains(browser).move_to_element(element)
    hover_action.perform()

hover(first_thumbnail)

wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#popup-container-" + str(creativeId) + " [title='Share'] > a"))
)


share_this_ad_input = browser.find_element_by_css_selector("#popup-container-" + str(creativeId) + " [title='Share'] > input")
share_this_ad_link = browser.find_element_by_css_selector("#popup-container-" + str(creativeId) + " [title='Share'] > a")

share_this_ad_link.click()

shared_ad_url = share_this_ad_input.get_attribute('value')
browser.get(shared_ad_url)

wait.until(
    EC.presence_of_all_elements_located((By.ID, "popup-container-hilight-" + str(creativeId)))
)

new_ad_url = browser.find_element_by_css_selector("#share-this-ad-hilight-" + str(creativeId)).get_attribute('value')

try:
    assert (shared_ad_url == new_ad_url) == True
except AssertionError:
    print "Share this ad feature may not be working"
else:
    print "Test Passed: Share this ad link worked and contains original ad"

