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

# prepare css-selector
selector = "div.JUa6JJNj7R_Y3i4P8YUX:nth-child(2) > div:nth-child(2) > div:nth-child(#)"

# prepare lists
found_elements = []
found_unique_elements = set()

# get rid of popups to be able to send keys
driver.maximize_window()
driver.implicitly_wait(30)

interaction.move_to_element(driver.find_element(By.CSS_SELECTOR, "#onetrust-consent-sdk"))

cookie_btn = driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
interaction.move_to_element(cookie_btn).perform() # navigate to element tillad cookies 
interaction.click(cookie_btn).perform()

interaction.send_keys("\ue00c").perform() # escape key, escapes ad popup

# return focus to main window to pass keypresses
an_element = driver.find_element(By.CSS_SELECTOR, ".main-view-container__scroll-node > div:nth-child(1)")
interaction.context_click(an_element).perform()

# prepare playlist view for scraping
interaction.send_keys("\ue00f\ue00f").perform() # pagedown x2

loaded_index = 0

# loop through the playlist table rows
for index, element in enumerate(amount_as_int, 1):
    # update the css-selector
    if index > 39:
        loaded_index = 1
    else:
        loaded_index += 1

    selector = selector[:73] + str(loaded_index) + ")"
    print("i, li, e, s: ", index, loaded_index, element, selector)
    
    # get the webelement
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        # element = driver.find_element(By.CLASS_NAME, 'j2s64Lz8y6VzBLB_V9Gm') # the button "play song by artist" class name
    
        # add element to lists
        found_elements.append(element)
        found_unique_elements.add(element)

        # site loads (and unloads) about 20 hits at a time, so we scroll to get more
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

# for webelement in found_elements:
#     webelement = webelement.get_attribute('aria-label')

# print(found_elements[0])

driver.quit()