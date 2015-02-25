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
    print element
    return element.get_attribute('innerHTML')

#Use a regex to strip out all non-numeric characters and replace them
#with nothing, then cast to an integer.
def isolate_number(string):
    digit_string = re.sub(r'\D', "", string)
    print "STRING>> \n" + digit_string
    if digit_string:
        return digit_string

#Take the list of h2 elements and run it through get_innerHTML to isolate the strings
string_list = map(get_innerHTML, elements_list)
print string_list

#Run the list through the function to strip out all non-numeric characters
number_list = map(isolate_number, string_list)
print number_list

#Assert that each number in our list is no more than 30 minutes old

for each_number in number_list:
    try:
        assert each_number <= 30
    except AssertionError:
        old_ad_count += 1

if old_ad_count > 0:
    "Dang, we've got " + str(old_ad_count) + " old ads on the home page"
else:
    "Hooray, no old ads!"

#Close the browser session
browser.close()

