# Coded By SanojC

# Importing necessary packages
import urllib.request
from urllib.error import URLError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import re
import unicodecsv as csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Locating and Opening ChromeWebDrive
driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe')

# Maximize Webdriver window size
urls = ["https://www.amazon.in/s/ref=lp_1968511031_nr_p_72_0?fst=as%3Aoff&rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1953602031%2Cn%3A11400137031%2Cn%3A15330094031%2Cn%3A1968511031%2Cp_72%3A1318476031&bbn=1968511031&ie=UTF8&qid=1551524738&rnid=1318475031&lo=apparel"]
# Getting relevant start page
for url in urls:
    try:
        driver.get(url)
        time.sleep(2)
        srNo = 1
        imgNo = 1

        page = 1

        print("Creating Amazon.csv")
        with open('Amazon.csv', 'ab') as csvfile:
            fieldnames = ['SR.NO', 'Product_Name', 'Category', 'Product_Discription', 'Image_link', 'Product_Sizes',
                          'Product_ID', 'Color', 'Price', 'Website_Name', 'Website', ]

        while page <= 10:
            scraped_results = []
            try:
                items = driver.find_elements_by_xpath("//div[@class='a-section a-spacing-none a-spacing-top-small']//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2']//a")
                len_items = len(items)
                print("{} Items found".format(len_items))
                time.sleep(10)
                for item in items:
                    # Clicking an item
                    item.click()
                    # Take a break and Keep Low Profile :P
                    time.sleep(2)

                    driver.switch_to.window(driver.window_handles[1])

                    time.sleep(10)

                    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='dp']")))
                    try:
                        temp_product_name = element.find_element_by_xpath(
                            "//span[@id='productTitle']").text
                        try:
                            temp_categories = element.find_elements_by_xpath("//ul[@class='a-unordered-list a-horizontal "
                                                                             "a-size-small']//li//a[@class='a-link-normal "
                                                                             "a-color-tertiary']")

                            temp_category = temp_categories[-1].text

                        except IndexError:

                            temp_categories = element.find_elements_by_xpath("//ul[@class='a-unordered-list a-horizontal "
                                                                             "a-size-small']//li//a[@class='a-link-normal']")

                            temp_category = temp_categories[-1].text

                        temp_discription = element.find_element_by_xpath(
                            "//ul[@class='a-unordered-list a-vertical a-spacing-none']").text

                        temp_image_link = element.find_element_by_xpath(
                            "//div[@id='imgTagWrapperId']//img[@id='landingImage']")

                        temp_sizes = element.find_elements_by_xpath(
                            "//span[@class='a-dropdown-container']//select[@name='dropdown_selected_size_name']//option")
                        temp_sizes_1 = []
                        for temp_size in temp_sizes[1:]:
                            temp_sizes_1.append(temp_size.text)

                        temp_sizes_2 = [size.replace('\n', '') for size in temp_sizes_1]
                        temp_sizes_3 = [size1.replace(' ', '') for size1 in temp_sizes_2]

                        try:
                            temp_color = element.find_element_by_xpath(
                                "//div[@id='variation_color_name']//span[@class='selection']").text
                        except NoSuchElementException:
                            temp_color = ""

                        temp_product_ids = element.find_elements_by_xpath("//div[@class='content']//ul//li")
                        dic = {}
                        for id1 in temp_product_ids:
                            detail = id1.text
                            detail = detail.replace(':', '')
                            key, value = detail.split(' ', 1)
                            dic.update({key: value})
                        temp_product_id1 = dic.get('ASIN')
                        try:
                            temp_product_id = "ASIN: "+temp_product_id1
                        except TypeError:
                            temp_product_id = temp_product_id1

                        try:
                            temp_price = element.find_element_by_xpath(
                                "//td[@class='a-span12']//span[@id='priceblock_ourprice']").text
                            # temp_price = re.sub('[^0-9]', '', temp_price)
                        except NoSuchElementException:
                            temp_price = element.find_element_by_xpath(
                                "//td[@class='a-span12']//span[@id='priceblock_saleprice']").text

                        temp_website_name = "Amazon"

                        temp_website_url = driver.current_url

                        product_name = temp_product_name if temp_product_name else None
                        category = temp_category if temp_category else None
                        product_discription = temp_discription if temp_discription else None
                        image_link = temp_image_link.get_attribute("src") if temp_image_link else None
                        product_sizes = temp_sizes_3 if temp_sizes_3 else None
                        color = temp_color if temp_color else None
                        product_id = temp_product_id if temp_product_id else None
                        price = temp_price if temp_price else None
                        website_name = temp_website_name if temp_website_name else None
                        website = temp_website_url if temp_website_url else None

                        urllib.request.urlretrieve(image_link, "{0}.png".format(imgNo))

                        print(srNo)
                        print(product_name)
                        print(category)
                        print(product_discription)
                        print(image_link)
                        print(product_sizes)
                        print(color)
                        print(product_id)
                        print(price)
                        print(website_name)
                        print(website)

                        print("\n")
                        product_details = {
                            'SR.NO': srNo,
                            'Product_Name': product_name,
                            'Category': category,
                            'Product_Discription': product_discription,
                            'Image_link': image_link,
                            'Product_Sizes': product_sizes,
                            'Color': color,
                            'Product_ID': product_id,
                            'Price': price,
                            'Website_Name': website_name,
                            'Website': website,
                        }
                        scraped_results.append(product_details)

                        srNo += 1
                        imgNo += 1

                        driver.close()
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[0])

                    except NoSuchElementException:
                        print("No Element Found")
                        driver.close()
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[0])
                        pass
                if scraped_results:
                    print("Writing scraped data to Amazon.csv")
                    with open('Amazon.csv', 'ab') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                        writer.writeheader()
                        for data in scraped_results:
                            writer.writerow(data)

                time.sleep(10)
                print("Moving to Next Page")
                next_page = driver.find_element_by_xpath("//ul[@class='a-pagination']//li[@class='a-last']//a")
                next_page.click()
                time.sleep(10)
                page += 1

            except NoSuchElementException:
                break
    except NoSuchElementException:
        pass
