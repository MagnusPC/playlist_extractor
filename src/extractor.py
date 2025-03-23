from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox()
interaction = ActionChains(driver)

driver.get("https://open.spotify.com/playlist/6RAdTOh6toX0KHSxjoqG1z")

driver.implicitly_wait(30)

# prepare loop count
number_of_songs = driver.find_element(By.CSS_SELECTOR, 'span.w1TBi3o5CTM7zW1EB3Bm:nth-child(1)').text # the number of songs in playlist header
print("||", number_of_songs)

# convert str with char to int
count_as_int = int(number_of_songs.split()[0])
print("||", count_as_int, 'is', type(count_as_int))

# get rid of popups to be able to send keys
driver.implicitly_wait(30)

interaction.move_to_element(driver.find_element(By.CSS_SELECTOR, "#onetrust-consent-sdk"))

cookie_btn = driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
interaction.move_to_element(cookie_btn).perform() # navigate to element tillad cookies 
interaction.click(cookie_btn).perform()

interaction.send_keys(Keys.ESCAPE).perform() # escape key, escapes ad popup

# navigate to the start of the list
element_to_click = driver.find_element(By.CSS_SELECTOR, "div.JUa6JJNj7R_Y3i4P8YUX:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4)")
# click date added column (prevents clicking the album url when clicking center of component)
interaction.click(element_to_click).perform()

# prepare variables
found_elements = []
found_unique_elements = set()
inc_idx = 0
end_reached = False

# prepare node selector
selector = "div.JUa6JJNj7R_Y3i4P8YUX:nth-child(2) > div:nth-child(2) > div:nth-child(1)"
init_element = driver.find_element(By.CSS_SELECTOR, selector)
starting_rowidx = int(init_element.get_attribute("aria-rowindex"))
print("|| starting_rowidx:", starting_rowidx, type(starting_rowidx))

# start collecting row elements
while not end_reached:
    # try: TODO uncomment
    # find the current element
    element = driver.find_element(By.CSS_SELECTOR, selector)

    # if element is temporary (only "UpiE7J6vPrJIa59qxts4") wait 

    # parent element of row indexes: div.JUa6JJNj7R_Y3i4P8YUX:nth-child(2) > div:nth-child(2)
    #   get first (or all) elements of parent element, set the aria-rowindex as starting point for extracting row elements
    #   maybe, get aria-rowindex of last element of parent element, when loop/findelement reaches that number, update again?
    
    found_rowidx = int(element.get_attribute("aria-rowindex"))
    print("|| found index:", found_rowidx, type(found_rowidx))

    if found_rowidx >= starting_rowidx: #TODO add check to prevent found index from spilling over the max loaded elements
        # increase the element selectors last node index
        inc_idx += 1
        selector = selector[:73] + str(inc_idx) + ")"
        
        # focus next element
        interaction.send_keys(Keys.DOWN).perform()
    else:
        print("!NB found index is not greater than or equal to starting index\n=", found_rowidx >= starting_rowidx)

    # add to list
    found_elements.append(element)
    found_unique_elements.add(element)

    # if child element is not of class IjYxRc5luMiDPhKhZVUH UpiE7J6vPrJIa59qxts4 (JgERXNoqNav5zOHiZGfG) break
    # if element is of class qnYVzttodnzg9WdrVQ1p break
    print("|| increasing index, starting_rowindex:", inc_idx, starting_rowidx, "\n||")
    print(element.text)
    print("||\n||", selector)
    print("|| printing new line...\n")

    # exit loop
    if found_rowidx > count_as_int:
        end_reached = True

    # except: TODO uncomment
    #     # print("exception occured")
    #     break

print(len(found_elements), len(found_unique_elements)) 

driver.minimize_window