import os
from ssl import Options
import sys
import time
from os.path import exists
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
# from seleniumrequests import Firefox
import pandas as pd

options = Options()
# proxies = ['13.115.164.210:24432', '163.116.131.129:8080', '80.48.119.28:8080', '66.29.154.103:3128', '169.57.1.85:8123', '66.29.154.105:3128', '135.148.2.21:444', '135.148.2.22:444', '8.219.97.248:80', '51.250.80.131:80', '139.99.237.62:80', '47.245.33.104:12345']
# browser = webdriver.Firefox(options=options)

options = webdriver.FirefoxOptions()
options.set_preference('profile', "/Users/test/Library/Application Support/Firefox/Profiles/<name_of_your_profile>")

caps = {
    "os" : "OS X",
    "osVersion" : "Monterey",
    "buildName" : "firefoxprofile- python",
    "sessionName" : "firefoxprofile- python",       
    "browserName" : "Firefox",
}
options.set_capability('bstack:options', caps)

browser = webdriver.Firefox(options=options)
browser.set_page_load_timeout(125)
try:
    url = input("Enter the URL which you want to scrape?")
    if url.strip() == "":
        browser.get('https://www.ltdcommodities.com/browse/all')
        unique_id = 0
        count = 0
    else:
        df = pd.read_csv('data.csv')
        unique_id = df.iloc[-1,1]+1
        count = df.iloc[-1,0]+1 
        browser.get(url)
except Exception as ex:
    print(str(ex))
    sys.exit()

while True:
    prod_links = []
    current_page = browser.find_element(By.XPATH,'//*[@id="js-pagebread--top-id"]/section/aside/div/p/span[2]').get_attribute('textContent')
    total_page = browser.find_element(By.XPATH,'//*[@id="js-pagebread--top-id"]/section/aside/div/p/span[3]').get_attribute('textContent')
    current_page_url = browser.current_url
    next_page = browser.find_elements(By.CLASS_NAME,'js-pagbrd--next')[0].get_attribute('href')
    seconds = time.time()
    local_time = time.ctime(seconds)
    with open(os.getcwd() + r'\logs.txt', 'a') as log:
        log.write(local_time + " \t " + current_page_url + '\n')
    links = browser.find_elements(By.XPATH, './/section/article[@class="prod-artc" and @role="row"]')
    for link in links:
        try:
            prod_links.append(link.find_element(By.XPATH, './/a[1]').get_attribute('href'))
        except:
            pass
    for prod in prod_links:
        try:
            df=pd.DataFrame()
            data = []
            titles = []
            category = []
            image = ""
            option1_name = []
            option1_value = []
            option2_name = []
            option2_value = []
            variant_image = []
            description = []
            id = []
            price = []
            sku = []
            quantity = []
            name = []
            counter = []
            if prod != None:
                try:
                    browser.get(prod)
                except Exception as ex:
                    with open(os.getcwd() + '\\urllogs.txt', 'a') as log:
                        log.write(prod + '\n' + local_time + '\n' + '__________________________________________' + '\n' + str(ex) + '\n__________________________________________' + '\n')
                    continue
                if (browser.page_source.__contains__("Decline Offer")):
                    print("Found")
                    browser.find_element(By.XPATH, ' //*[ contains (text(), "Decline Offer" ) ]').click()
                images = browser.find_elements(By.CSS_SELECTOR,'.thumb-nav > a > img')
                print("Counter : " + str(count))
                for img in images:
                    image = image + "|" + img.get_attribute('src')
                raw_description = browser.find_element(By.CLASS_NAME, "sku-pers__instruct--2").get_property("innerHTML")
                raw_description = raw_description.replace('<a tabindex="0" onkeydown="if(event.keyCode == 13) this.click();" class="exp-clp-det__lnk">View Product Specifications</a> <aside class="exp-clp-det__dsc">', '')
                description.append(raw_description)
                try:
                    category.append(browser.find_element(By.CSS_SELECTOR, '.js-fm--navigation > p > a:nth-child(3)').text)
                except:
                    pass
                # Product page variants
                option1 = browser.find_element(By.ID, 'js-dropdown-0--id').get_attribute('class')
                option2 = browser.find_element(By.ID, 'js-dropdown_1--id').get_attribute('class')
                option3 = browser.find_element(By.ID, 'js-dropdown_2--id').get_attribute('class')
                if "hidden" in option1 and "hidden" in option2 and "hidden" in option3:
                    counter.append(count)
                    titles.append(browser.find_element(By.TAG_NAME,'h1').get_attribute("textContent"))
                    price.append(browser.find_element(By.CLASS_NAME,'sku-desc__price').text)
                    Variant_SKU = browser.find_element(By.CLASS_NAME, 'sku-desc__except--pin').get_attribute('textContent')
                    sku.append(str((Variant_SKU.strip().split(' '))[1]))
                    stock = browser.find_element(By.CLASS_NAME, "sku-desc__except--instock").get_property("innerHTML")
                    if stock == "In stock":
                        quantity.append("10")
                    else:
                        quantity.append("0")
                    unique_id += 1
                    id.append(unique_id)
                elif ("hidden" in option2 and "hidden" in option3):
                    Variants = browser.find_elements(By.XPATH, '//*[@id="js-dropdown-0--id"]//*[@class="prod__text--item"]')
                    # variant_count = 0
                    for variant in Variants:
                        if ("hidden" not in option1):
                            dropdown = browser.find_element(By.CLASS_NAME, 'drop-surface__init--closed')
                            browser.execute_script("arguments[0].click();", dropdown)
                            browser.execute_script("arguments[0].click();", variant)
                            option1_name.append(browser.find_element(By.XPATH, '//*[@id="js-dropdown-0--id"]/nav/p[1]').text)
                            option1_value.append(variant.get_attribute('textContent'))
                            variant_image.append(browser.find_element(By.XPATH, '//*[@class="l-HeroZoom-Cntr"]/a').get_property("href"))
                        titles.append(browser.find_element(By.TAG_NAME,'h1').get_attribute("textContent"))
                        counter.append(count)
                        price.append(browser.find_element(By.CLASS_NAME,'sku-desc__price').text)
                        Variant_SKU = browser.find_element(By.CLASS_NAME, 'sku-desc__except--pin').get_attribute('textContent')
                        sku.append(str((Variant_SKU.strip().split(' '))[1]))
                        stock = browser.find_element(By.CLASS_NAME, "sku-desc__except--instock").get_property("innerHTML")
                        if stock == "In stock":
                            quantity.append("10")
                        else:
                            quantity.append("0")
                        unique_id += 1
                        id.append(unique_id)
                else:
                    Variants_1 = browser.find_elements(By.XPATH, '//*[@id="js-dropdown_1--id"]//*[@class="prod__text--item"]')
                    variant_count = 0
                    for variant_1 in Variants_1:
                        Variants_2 = browser.find_elements(By.XPATH, '//*[@id="js-dropdown_2--id"]//*[@class="prod__text--item"]')
                        dropdown_1 = browser.find_element(By.CLASS_NAME, 'drop-surface__init--closed')
                        browser.execute_script("arguments[0].click();", dropdown_1)
                        browser.execute_script("arguments[0].click();", variant_1)
                        for variant_2 in Variants_2:
                            dropdown_2 = browser.find_element(By.CLASS_NAME, 'drop-surface__init--closed')
                            browser.execute_script("arguments[0].click();", dropdown_2)
                            browser.execute_script("arguments[0].click();", variant_2)
                            option1_name.append(browser.find_element(By.XPATH, '//*[@id="js-dropdown_1--id"]/nav/p[1]').text)
                            option1_value.append(variant_1.get_attribute('textContent'))
                            option2_name.append(browser.find_element(By.XPATH, '//*[@id="js-dropdown_2--id"]/nav/p[1]').text)
                            option2_value.append(variant_2.get_attribute('textContent'))
                            counter.append(count)
                            titles.append(browser.find_element(By.TAG_NAME,'h1').get_attribute("textContent"))
                            variant_image.append(browser.find_element(By.XPATH, '//*[@class="l-HeroZoom-Cntr"]/a').get_property("href"))
                            price.append(browser.find_element(By.CLASS_NAME,'sku-desc__price').text)
                            Variant_SKU = browser.find_element(By.CLASS_NAME, 'sku-desc__except--pin').get_attribute('textContent')
                            sku.append(str((Variant_SKU.strip().split(' '))[1]))
                            stock = browser.find_element(By.CLASS_NAME, "sku-desc__except--instock").get_property("innerHTML")
                            if stock == "In stock":
                                quantity.append("10")
                            else:
                                quantity.append("0")
                            unique_id += 1
                            id.append(unique_id)
                data=[counter, id, titles, description, category, sku, image, option1_name, option1_value, option2_name, option2_value, quantity, variant_image, price]
            data = pd.DataFrame({'Count': pd.Series(counter), 'ID': pd.Series(id), 'Title': pd.Series(titles), 'Description': pd.Series(description), 'Category': pd.Series(category), 'SKU': pd.Series(sku), 'Images': pd.Series(image), 'Option 1 Name': pd.Series(option1_name), 'Option 1 Value': pd.Series(option1_value), 'Option 2 Name': pd.Series(option2_name), 'Option 2 Value': pd.Series(option2_value), 'Stock': pd.Series(quantity), 'Variant Images': pd.Series(variant_image), 'Orignal Pirce': pd.Series(price)})
            df = df.append(data)
            if(exists("./data.csv")):
                df.to_csv(os.getcwd() + r'\data.csv', mode='a', index= False, header= False)
            else:
                df.to_csv(os.getcwd() + r'\data.csv', mode='a', index= False, header= True)
            count += 1
        except Exception as ex:
            with open(os.getcwd() + '\\errorlogs.txt', 'a') as log:
                log.write(prod + '\n' + '__________________________________________' + '\n' + str(ex) + '\n__________________________________________' + '\n')
            continue
    if(int(current_page) == int(total_page)):
        break
    try:
        browser.get(next_page)
    except Exception as ex:
        with open(os.getcwd() + '\\urllogs.txt', 'a') as log:
            log.write(prod + '\n' + local_time + '\n' + '__________________________________________' + '\n' + str(ex) + '\n__________________________________________' + '\n')

browser.close()