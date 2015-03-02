#Verify that the "Try These" links are random and that they work.

from selenium import webdriver
import requests
from IPython import embed

browser = webdriver.Firefox()
browser.get("http://www.moat.com")

def duplicated_links_present():
    #Compare the length of the original list to a list run through
    #the set function which will remove duplicates
    duplicated = len(link_text) != len(set(link_text))
    return duplicated

#First, make sure we loaded the page
assert "Moat" in browser.title

#Let's get our array of links using a CSS selector...
links = browser.find_elements_by_css_selector("fieldset #search-suggestions-box > a")

#Create a new list of just link text
link_text = []
for each_link in links:
    link_text.append(each_link.text)

#Verify each link works
try:
    link = ""
    for each_link in links:
        link = each_link.get_attribute('href')
        request = requests.get(link)
        assert request.status_code == 200
except AssertionError:
    print "Link " + link + " may not be working"
else:
    print "Test passed: All links are working"

#Assert there are no duplicate links present
try:
    assert duplicated_links_present() == False
except AssertionError:
    print "Test failed: Looks like we might have some duplicate links"
else:
    print "Test passed: No duplicate links!"

#Assert refreshing the page brings up a new set of links
try:
    #Refresh browser to pull up new links
    browser.refresh()
    refreshed_page_links = browser.find_elements_by_css_selector("fieldset #search-suggestions-box > a")
    refreshed_page_link_text = []

    for each_link in refreshed_page_links:
        refreshed_page_link_text.append(each_link.text)
    assert (link_text != refreshed_page_link_text) == True
except AssertionError:
    print "There may be duplicate links"
else:
    print "Test passed: The links are not duplicates"

#Close the browser session
browser.quit()