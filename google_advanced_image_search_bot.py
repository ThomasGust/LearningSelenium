from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "C:\\Program Files (unsecure)\\Chromedrivers\\87.0.4280.88\\chromedriver.exe"

driver = webdriver.Chrome(executable_path=PATH)

driver.get("https://www.google.com/advanced_search?hl=en&fg=1")


def do_advanced_image_search(query="Dog", usage_rights="Default"):
    query_bar = driver.find_element_by_id("xX4UFf")
    query_bar.send_keys(query)

    usage_rights_bar = driver.find_element_by_id("as_rights_button")
    usage_rights_bar.send_keys(Keys.LEFT)

    driver.find_element_by_xpath("")


if __name__ == "__main__":
    do_advanced_image_search(query="Dog")
