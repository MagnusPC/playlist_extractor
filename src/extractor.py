from array import array
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
interaction = ActionChains(driver)

driver.get("https://open.spotify.com/playlist/6RAdTOh6toX0KHSxjoqG1z")
# driver.minimize_window()

driver.implicitly_wait(30)

# prepare loop count
amount_of_songs = driver.find_element(By.CSS_SELECTOR, 'span.w1TBi3o5CTM7zW1EB3Bm:nth-child(1)').text # the number of songs in playlist header
print(amount_of_songs)

# convert str to list of int
amount_as_int = int(amount_of_songs.split()[0])
print(amount_as_int, 'is', type(amount_as_int))
amount_as_int = list(range(amount_as_int))
print(amount_as_int[:10], "...")

# get rid of popups to be able to send keys
driver.maximize_window()
driver.implicitly_wait(30)

interaction.move_to_element(driver.find_element(By.CSS_SELECTOR, "#onetrust-consent-sdk"))

cookie_btn = driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
interaction.move_to_element(cookie_btn).perform() # navigate to element tillad cookies 
interaction.click(cookie_btn).perform()

interaction.send_keys("\ue00c").perform() # escape key, escapes ad popup

# navigate to the start of the list
first_row_element = driver.find_element(By.CSS_SELECTOR, "div.JUa6JJNj7R_Y3i4P8YUX:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
interaction.click(first_row_element).perform()

# prepare variables
found_elements = []
found_unique_elements = set()
index = 1 # start from 1, replaces "#" in selector
end_reached = False

# prepare node selector
selector = "div.JUa6JJNj7R_Y3i4P8YUX:nth-child(2) > div:nth-child(2) > div:nth-child(#)"

# start collecting row elements
while not end_reached:
    selector = selector[:73] + str(index) + ")"
    try:
        print("|")
        # access element
        # if element is relevant append to list
            #that is if element is not temporary (only UpiE7J6vPrJIa59qxts4) 
            #   - kan enten være at elementet er direkte den klasse eller at substring af child er den klasse
        # else if child element is not of class IjYxRc5luMiDPhKhZVUH UpiE7J6vPrJIa59qxts4 (JgERXNoqNav5zOHiZGfG) break
        # move focus to next row
        # if element is of class qnYVzttodnzg9WdrVQ1p break
        print("i, li, e, s: ", index, element, selector)
    except:
        print("exception occured")
    # if element is not a row in list else if loop count = song count = end reached true


# HERE
# instead of using page down to scroll songs into view (and by that loading them)
# use the mouse press to access the first row and just scroll with down-key
# may be able to chain it with accessing the highlighted element and saving that to a list






# return focus to main window to pass keypresses
an_element = driver.find_element(By.CSS_SELECTOR, ".main-view-container__scroll-node > div:nth-child(1)")
interaction.context_click(an_element).perform()

# prepare playlist view for scraping
interaction.send_keys("\ue00f\ue00f").perform() # pagedown x2

# prepare css-selector
selector = "div.JUa6JJNj7R_Y3i4P8YUX:nth-child(2) > div:nth-child(2) > div:nth-child(#)"

# prepare variables
found_elements = []
found_unique_elements = set()
loaded_index = 0
latest_element = None

# loop through the playlist table rows
for index, element in enumerate(amount_as_int, 1):
    # update the css-selector
    if index % 40 == 0:
        loaded_index = 1
        interaction.send_keys("\ue00f\ue00f").perform() # pagedown x2
        driver.implicitly_wait(30)
    else:
        loaded_index += 1

    selector = selector[:73] + str(loaded_index) + ")"
    print("i, li, e, s: ", index, loaded_index, element, selector)
    
    # get the webelement
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        tempElement = driver.find_element(By.CLASS_NAME, "UpiE7J6vPrJIa59qxts4")
        loadedElement = element.find_element(By.CLASS_NAME, "IjYxRc5luMiDPhKhZVUH UpiE7J6vPrJIa59qxts4")

        if loadedElement is not tempElement:
            print(tempElement, tempElement.text)
            print(loadedElement, loadedElement.text) # child node

        # add element to lists
        found_elements.append(loadedElement)
        found_unique_elements.add(loadedElement)

        # site loads (and unloads) about 23 hits at a time, so we scroll to get more
        # should be run 2 times before loop and then two times for each 20 hits
        # interaction.send_keys("\ue00c").perform() # escape key, escapes ad popup
        # interaction.send_keys("\ue00f\ue00f").perform() # PAGE_DOWN x2

        # interaction.scroll_to_element(element) # only works on chromium

    except:
        print("---------exception occured|")
        driver.minimize_window()
        break


driver.minimize_window()

print(len(found_elements))
print(len(found_unique_elements))

print(found_elements.__getitem__(0).text) # crashes as node is no longer in active view
print(found_elements.pop().text)
print(found_unique_elements.pop().text) # as of 14.03.25, song 14 ?

xset = set()
for x in found_elements:
    xset.add(x)
    print(len(xset))

driver.quit()