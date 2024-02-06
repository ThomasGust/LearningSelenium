from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import os
import requests
import urllib.request


class ImageDatasetScraperBase(object):
    """
    I ought to make this better, it is still failing to download at least half of the images.
    """

    def __init__(self, webdriver_path, search_key, image_path, num_images_per_category, headless=True,
                 sleep_amounts=None):
        if sleep_amounts is None:
            sleep_amounts = [0.5, 0.5]
        self.message_prefix = 'Image Dataset Scraper: '
        self.headless = headless
        self.sleep_amount_1, self.sleep_amount_2 = sleep_amounts
        self.search_key = search_key
        self.image_path = os.path.join(image_path, search_key)

        if type(webdriver_path) != str:
            raise TypeError(f'{self.message_prefix}Value for variable \'webdriver_path\' should be a string.'
                            f'Received value: {webdriver_path}, of type: {type(webdriver_path)}')
        if type(image_path) != str:
            raise TypeError(f'{self.message_prefix}Value for variable \'image_path\' should be a string.'
                            f'Received value: {image_path}, of type: {type(image_path)}')
        if not os.path.exists(self.image_path):
            print(f'{self.message_prefix}Image path looks like it does not yet exist, creating new folder.')
            os.mkdir(self.image_path)

        self.webdriver_path = webdriver_path

        self.driver = webdriver.Chrome(executable_path=self.webdriver_path)
        self.url = f"https://www.google.com/" \
                   f"search?q={self.search_key}&safe=active&source=lnms&tbm=isch&sa=X&ved=2ahUKEwis84SC5eLtAhWDup4KHTMNDFIQ_" \
                   f"AUoAXoECBIQAw&biw=1707&bih=850&dpr=2.25"
        self.num_images_per_category = num_images_per_category

        options = Options()
        if self.headless:
            options.add_argument('--headless')
        try:
            self.driver = webdriver.Chrome(self.webdriver_path, options=options)
            self.driver.get(self.url)
        except:
            print(
                "[-] Please update the chromedriver.exe in the webdriver folder according to your chrome "
                "version:https://chromedriver.chromium.org/downloads")

    def scrape_urls(self):
        print(f"{self.message_prefix}Scraping for image link... Please wait.")
        image_urls = []
        count = 1
        count_1 = 1
        while count_1 <= self.num_images_per_category:
            try:
                try:
                    main = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' %
                             (str(count))))
                    )
                except:
                    print("Looks like the image element could not be located, moving on.")

                imgurl = self.driver.find_element_by_xpath(
                    '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' % (str(count)))
                imgurl.click()

                time.sleep(self.sleep_amount_1)
                images = self.driver.find_elements_by_class_name("n3VNCb")
                for image in images:
                    print("%d. %s" % (count_1, image.get_attribute("src")))
                    image_urls.append(image.get_attribute("src"))
                    count_1 += 1
                    count += 1
                    break

                self.driver.execute_script("window.scrollTo(0, " + str(count * 150) + ");")
                time.sleep(self.sleep_amount_2)
            except Exception as e:
                print(f"{self.message_prefix}Unable to get the link for this photo exception was {e}")
                print(f"{self.message_prefix}Trying to get the link the other way.")
                try:
                    try:
                        main = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' %
                                 (str(count))))
                        )
                    except:
                        print("Looks like the image element could not be located, moving on.")
                    imgurl = self.driver.find_element_by_xpath(
                        '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' % (str(count)))
                    src = imgurl.get_attribute("src")
                    if src is not None:
                        image_urls.append(src)
                        print(f"{self.message_prefix}Successfully found image {count_1} at url {src}")
                        count_1 += 1
                        count += 1
                    else:
                        print("Huh, something went wrong with this image.")
                        count += 1
                except Exception as e:
                    print(f"Ran into another exception even when trying to get the link the other way.")
                    print(f" Exception was {e}. Moving on.")
                    count += 1

        self.driver.close()

        return image_urls

    def save_image_urls(self, image_urls):
        for i, image_url in enumerate(image_urls):
            print(f'Attempting to save image {i} from url {image_url}')
            try:
                file_name = f'{self.search_key}_{i}.jpg'
                image_path = os.path.join(self.image_path, file_name)
                print(f"Requesting image {i} from url {image_url}.")
                image = requests.get(image_url)

                if image.status_code == 200:
                    with open(image_path, "wb") as f:
                        f.write(image.content)
                else:
                    print(f"Oh no! Request for image {i} did not have the right status code! Status code was"
                          f" {image.status_code}")
            except Exception as e:
                print(f'{self.message_prefix}Oops, looks like I caught an exception while trying to save image {i} from'
                      f' url {image_url}!')
                print(f"Exception was {e}")
                print(f"Trying to save image {i} using urllib 'urlretrieve' function now.")
                try:
                    file_name = f'{self.search_key}_{i + 1}.jpg'
                    image_path = os.path.join(self.image_path, file_name)
                    print(f"Requesting image {i} from url {image_url} with urllib.")
                    urllib.request.urlretrieve(url=image_url, filename=image_path)
                    print(f"Got image from url with urllib.")
                except Exception as e:
                    print(f"Was not able to save image even with urllib, exception was {e}")


class ImageDatasetScraper(object):
    def __init__(self, webdriver_path, search_keys, image_path, num_images_per_category, headless=True,
                 sleep_amount=None):
        self.webdriver_path = webdriver_path
        self.search_keys = search_keys
        self.image_path = image_path
        self.num_image_per_category = num_images_per_category
        self.headless = headless
        self.sleep_amount = sleep_amount

    def do_scrape(self):
        for search_key in self.search_keys:
            base = ImageDatasetScraperBase(webdriver_path=self.webdriver_path, search_key=search_key,
                                           image_path=self.image_path,
                                           num_images_per_category=self.num_image_per_category, headless=self.headless,
                                           sleep_amounts=self.sleep_amount)
            image_urls = base.scrape_urls()

            base.save_image_urls(image_urls=image_urls)


if __name__ == '__main__':
    scraper = ImageDatasetScraper(webdriver_path="C:\\Program Files (unsecure)\\Chromedrivers\\87.0.4280.88"
                                                 "\\chromedriver.exe", image_path="Images\\DatasetTwo",
                                  search_keys=["Beaver", "Dolphin", "Whale", "Otter", "Seal",
                                               "Aquarium Fish", "Manta Ray", "Flatfish", "Shark", "Trout",
                                               "Orchid", "Sunflower", "Roses", "Tulip", "Poppies",
                                               "Bottle", "Bowl", "Can", "Cup", "Plate"],
                                  num_images_per_category=200,
                                  headless=True, sleep_amount=[0.15, 0.2, 0.2])
    scraper.do_scrape()
