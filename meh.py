for indx in range(1, self.num_images_per_category + 1):

    try:
        try:
            main = WebDriverWait(self.driver, 2.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' %
                     (str(indx))))
            )
        except:
            print("Looks like the image element could not be located, moving on.")

        imgurl = self.driver.find_element_by_xpath(
            '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' % (str(indx)))
        imgurl.click()

        time.sleep(self.sleep_amount)
        images = self.driver.find_elements_by_class_name("n3VNCb")
        for image in images:
            print("%d. %s" % (count, image.get_attribute("src")))
            image_urls.append(image.get_attribute("src"))
            count += 1
            break

        self.driver.execute_script("window.scrollTo(0, " + str(indx * 150) + ");")
        time.sleep(self.sleep_amount)
    except Exception as e:
        print(f"{self.message_prefix}Unable to get the link for this photo exception was {e}")
        print(f"{self.message_prefix}Trying to get the link the other way.")
        try:
            try:
                main = WebDriverWait(self.driver, 2.5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' %
                         (str(indx))))
                )
            except:
                print("Looks like the image element could not be located, moving on.")
            imgurl = self.driver.find_element_by_xpath(
                '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img' % (str(indx)))
            src = imgurl.get_attribute("src")
            image_urls.append(src)
            print(f"{self.message_prefix}Successfully found image {indx} at url {src}")
            count += 1
        except Exception as e:
            print(f"Ran into another exception even when trying to get the link the other way.")
            print(f" Exception was {e}. Moving on.")