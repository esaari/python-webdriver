#Verify that the "Recently Seen Ads" are no more than half an hour old.
import re

from selenium import webdriver

browser = webdriver.Firefox()
browser.get("http://www.moat.com")

old_ad_count = 0

#Let's get an array of the 'XX minutes ago' h2 elements using a CSS selector...
elements_list = browser.find_elements_by_css_selector('#search-sub .hpads + h2')

#Get the inner text of the <h2> elements returned in the selector
def get_innerHTML(element):
    return element.get_attribute('innerHTML')

#Use a regex to strip out all non-numeric characters and replace them
#with nothing, then cast to an integer.
def isolate_number(string):
    #Handle the case where ad just displays 'seen today' or nothing at all
    if string != "seen today" or string == "&nbsp;":
        return int(re.sub(r'\D', "", string))

#Take the list of h2 elements and run it through get_innerHTML to isolate the strings
string_list = map(get_innerHTML, elements_list)

#Take the string_list and get only a number out of applicable data
number_list = map(isolate_number, string_list)

#Print the array of numbers so I can see the data
print number_list

#Assert that each number in our list is no more than 30 minutes old
for each_number in number_list:
    try:
        assert each_number <= 30
    except AssertionError:
        old_ad_count += 1

if old_ad_count > 0:
    print "Dang, we've got " + str(old_ad_count) + " old ad(s) on the home page"
else:
    print "Hooray, no old ads!"

#Close the browser session
browser.close()

