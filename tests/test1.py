#Verify that the "Try These" links are random and that they work.

from selenium import webdriver

browser = webdriver.Firefox()
browser.get("http://www.moat.com")

def duplicated_links_present():
    #Compare the length of the original list to a list run through
    #the set function which will remove duplicates
    duplicated = len(links) != len(set(links))
    return duplicated

#First, make sure we loaded the page
assert "Moat" in browser.title

#Let's get our array of links using a CSS selector...
links = browser.find_elements_by_css_selector("fieldset #search-suggestions-box > a")

#Print out each link, so I know we got a valid list
for each_link in links:
    print each_link.text

#I want to check this value in the console
print duplicated_links_present()

#Finally, assert there are no duplicate links present
try:
    assert duplicated_links_present() == False
except AssertionError:
    print "Test failed: Looks like we might have some duplicate links"
else:
    print "Test passed: No duplicate links!"


#Close the browser session
browser.close()