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
from selenium.webdriver.common.keys import Keys

# Locating and Opening ChromeWebDriver
driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe')

# Maximize Webdriver window size

# Getting relevant start page
driver.get('https://wyo.in/collections/women-printed-funky-t-shirts-online-india')
time.sleep(2)
'''
# Croll to the Bottom
copyright = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "copyright")))
driver.execute_script("return arguments[0].scrollIntoView(true);", copyright)
time.sleep(10)
element = driver.find_element_by_tag_name('html')
element.send_keys(Keys.HOME)
'''
srNo = 1
imgNo = 1

# List to save scraped data
scraped_results = []
pages = driver.find_elements_by_xpath("//ul[@class='pagination']//li")

for page in pages:

    try:
        items = driver.find_elements_by_xpath("//div[@class='image-cell']//a']")

        for item in items:
            try:
                # Clicking an item
                item.send_keys(Keys.CONTROL + Keys.RETURN)
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[1])

                element = driver.find_element_by_xpath("//div[@class='wrapper']")

                try:
                    temp_product_name = element.find_element_by_xpath(
                        "//div[@class='product-title']//h1").text

                    temp_categories = element.find_elements_by_xpath(
                        "//nav[@class = 'breadcrumb']//a")
                    temp_category = temp_categories[1].text

                    temp_discription = element.find_element_by_xpath(
                        "//div[@id='tabs-1']").text

                    temp_image_link = element.find_element_by_xpath(
                        "//img[@id='FeaturedImage-product-template']")

                    temp_sizes = element.find_elements_by_xpath("//select[@id='SingleOptionSelector-0']")
                    temp_sizes_1 = []
                    for temp_size1 in temp_sizes:
                        temp_size = temp_size1.text
                        temp_sizes_1.append(temp_size)

                    temp_sizes_2 = [size.replace('\n', ',') for size in temp_sizes_1]
                    temp_sizes_3 = [size1.replace(' ', '') for size1 in temp_sizes_2]
                    temp_sizes_4 = [size2.replace(',,', ' ') for size2 in temp_sizes_3]
                    temp_sizes_5 = [size2.replace(',', '') for size2 in temp_sizes_4]

                    temp_colors = element.find_elements_by_xpath("//select[@id='SingleOptionSelector-1']")
                    temp_colors_1 = []
                    for temp_colors1 in temp_colors:
                        temp_colors = temp_colors1.text
                        temp_colors_1.append(temp_colors)

                    temp_colors_2 = [color.replace('\n', ',') for color in temp_colors_1]
                    temp_colors_3 = [color.replace(' ', '') for color in temp_colors_2]
                    temp_colors_4 = [color.replace(',,', ' ') for color in temp_colors_3]
                    temp_colors_5 = [color.replace(',', '') for color in temp_colors_4]
                    temp_color = temp_colors_5

                    temp_product_id = " "

                    temp_price = element.find_element_by_xpath("//span[@id='ProductPrice-product-template']").text
                    temp_price = re.sub('[^0-9]', '', temp_price)
                    temp_website_name = "WYO"
                    temp_website_url = driver.current_url

                    product_name = temp_product_name if temp_product_name else None
                    category = temp_category if temp_category else None
                    product_discription = temp_discription if temp_discription else None
                    image_link = temp_image_link.get_attribute("src") if temp_image_link else None
                    product_sizes = temp_sizes_5 if temp_sizes_5 else None
                    product_color = temp_color if temp_color else None
                    product_id = temp_product_id if temp_product_id else None
                    price = temp_price if temp_price else None
                    website_name = temp_website_name if temp_website_name else None
                    website = temp_website_url if temp_website_url else None

                    print(srNo)
                    print(product_name)
                    print(category)
                    print(product_discription)
                    print(image_link)
                    print(product_sizes)
                    print(product_color)
                    print(product_id)
                    print(price)
                    print(website_name)
                    print(website)

                    print("\n")
                    # download the image
                    urllib.request.urlretrieve(image_link, "{0}.png".format(imgNo))

                    imgNo += 1

                    product_details = {
                        'SR.NO': srNo,
                        'Product_Name': product_name,
                        'Category': category,
                        'Product_Discription': product_discription,
                        'Image_link': image_link,
                        'Product_Sizes': product_sizes,
                        'Color': product_color,
                        'Product_ID': product_id,
                        'Price': price,
                        'Website_Name': website_name,
                        'Website': website,
                    }

                    scraped_results.append(product_details)

                    srNo += 1
                    driver.close()
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[0])

                except NoSuchElementException:
                    print("No Element found")
                    driver.close()
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[0])
                    pass

            except NoSuchElementException:
                print("No items found")
                pass

            except StaleElementReferenceException:
                print("No items found")
                pass

            except URLError:
                print("No items found")
                pass
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)
        next_page = driver.find_elements_by_xpath("//ul[@class='pagination']//li//a")
        next_page[-1].click()
        print("\n next page \n")
        time.sleep(2)

    except NoSuchElementException:
        print("Page Not Found")
        pass
    except StaleElementReferenceException:
        print("Page Not Found")
        pass

    except URLError:
        print("Page Not Found")
        pass


if scraped_results:
    print("Writing scraped data to google_scrap2.csv")
    with open('Shop_scrap.csv', 'wb') as csvfile:
        fieldnames = ['SR.NO', 'Product_Name', 'Category', 'Product_Discription', 'Image_link', 'Product_Sizes', 'Product_ID', 'Color', 'Price', 'Website_Name', 'Website', ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for data in scraped_results:
            writer.writerow(data)
