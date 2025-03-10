import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get("https://open.spotify.com/playlist/6RAdTOh6toX0KHSxjoqG1z")

driver.implicitly_wait(30)

amount_of_songs = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[5]/div/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/div/div[2]/span[1]').text
print(amount_of_songs)

amount_as_int = int(amount_of_songs.split()[0])
print(amount_as_int, 'is', type(amount_as_int))

driver.implicitly_wait(30)

for element in range(amount_as_int):
    found_elements = driver.find_element(By.CLASS_NAME, 'IjYxRc5luMiDPhKhZVUH UpiE7J6vPrJIa59qxts4')

print(len(found_elements))