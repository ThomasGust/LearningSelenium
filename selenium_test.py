from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PATH = "C:\\Program Files (unsecure)\\Chromedrivers\\87.0.4280.88\\chromedriver.exe"

driver = webdriver.Chrome(executable_path=PATH)

driver.get("https://www.google.com/")

search_bar = driver.find_element_by_name("q")

search_bar.send_keys("Dog")
search_bar.send_keys(Keys.RETURN)
