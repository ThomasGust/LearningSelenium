from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "C:\\Program Files (unsecure)\\Chromedrivers\\87.0.4280.88\\chromedriver.exe"

driver = webdriver.Chrome(executable_path=PATH)

driver.get("https://www.google.com/search?q=Dog&safe=active&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiHuYachODtAhUCvZ4KHTlFCvEQ_AUoAXoECBEQAw&biw=1707&bih=850")

X_PATH_ROOT = "/html/body/div[@class='T1diZc KWE8qe']/c-wiz[@class='P3Xfjc SSPGKf BIdYQ FA7L0b zE3eif']/" \
         "div[@class='mJxzWe']/div[@class='OcgH4b']/div/div/div[@class='tmS4cc']/div[@class='gBPM8']/div[@id='islrg']" \
         "/div[@class='islrc']"

body = driver.find_element_by_xpath(xpath=X_PATH_ROOT)
