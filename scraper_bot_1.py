from selenium import webdriver
import urllib.request
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

PATH = "C:\\Program Files (unsecure)\\Chromedrivers\\87.0.4280.88\\chromedriver.exe"

driver = webdriver.Chrome(executable_path=PATH)

query = input("What do you want to search for?: ")
X_PATH_ROOT = "/html/body/div[@class='T1diZc KWE8qe']/c-wiz[@class='P3Xfjc SSPGKf BIdYQ FA7L0b zE3eif']/" \
              "div[@class='mJxzWe']/div[@class='OcgH4b']/div/div/div[@class='tmS4cc']/div[@class='gBPM8']/div[" \
              "@id='islrg']" \
              "/div[@class='islrc']"

driver.get(f"https://www.google.com/"
           f"search?q={query}&safe=active&source=lnms&tbm=isch&sa=X&ved=2ahUKEwis84SC5eLtAhWDup4KHTMNDFIQ_"
           f"AUoAXoECBIQAw&biw=1707&bih=850&dpr=2.25")


def return_image_element_from_page(image_index):
    new_x_path = X_PATH_ROOT + f"/div[@data-ri='{image_index}']/a[@class='wXeWr islib nfEiy mM5pbd']/" \
                               f"div[@class='bRMDJf islir']/img[@class='rg_i Q4LuWd']"
    return driver.find_element_by_xpath(new_x_path)


def return_image_element_x_path(image_index):
    new_x_path = X_PATH_ROOT + f"/div[@data-ri='{image_index}']/a[@class='wXeWr islib nfEiy mM5pbd']/" \
                               f"div[@class='bRMDJf islir']/img[@class='rg_i Q4LuWd']"
    return new_x_path


def get_image_src(img_element):
    src = img_element.get_attribute('src')
    if src is None:
        print('Sorry, It looks like "src" was equal to none.')

    return src


def scroll_down(scroll_amount):
    driver.execute_script(f"window.scrollBy(0,{scroll_amount})")


def url_to_jpg(i, url, file_path, image_base_name):
    file_name = f'{image_base_name}-{i}.jpg'
    full_path = f'{file_path}{file_name}'
    urllib.request.urlretrieve(url, full_path)

    print(f'Successfully saved image {file_name}')

    return None


def scrape_page(num_images):

    for i in range(num_images):
        img = return_image_element_from_page(image_index=i)
        img_src = img.get_attribute('src')
        print(f"On image {i + 1} with source {img_src}")
        try:
            url_to_jpg(i=i + 1, url=img_src, file_path='CatImages/', image_base_name=query)
        except TypeError:
            print("Frick this thing, I ran into that type error again.")
            scroll_down(1000)

            #driver.execute_script("window.open('https://www.google.com/', '_blank')")
            #driver.switch_to.window(driver.window_handles[-1])

            #driver.get(f'https://www.google.com/'
                       #f'search?q={query}&safe=active&source=lnms&tbm=isch&sa=X&ved=2ahUKEwis84SC5eLtAhWDup4KHTMNDFIQ_'
                       #f'AUoAXoECBIQAw&biw=1707&bih=850&dpr=2.25')

            #try:
                #main = WebDriverWait(driver, 10).until(
                    #EC.presence_of_element_located((By.XPATH, return_image_element_x_path(image_index=i)))
                #)

            #except:
                #driver.quit()

            img = return_image_element_from_page(image_index=i)
            print(f'Found image element {img}')
            img_src = get_image_src(img)
            #print(img_src)
            # url_to_jpg(i=i + 1, url=img_src, file_path='CatImages/', image_base_name=query)


if __name__ == '__main__':
    scrape_page(22)