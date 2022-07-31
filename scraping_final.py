import os
from ssl import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import pandas as pd

options = Options()
# options.add_argument('--headless')
browser = webdriver.Firefox(options=options)
browser.get('https://www.ltdcommodities.com/browse/all')
data = []
unique_id = 0
count = 0
df=pd.DataFrame()

while True:
    prod_links = []
    current_page = browser.find_element(By.XPATH,'//*[@id="js-pagebread--top-id"]/section/aside/div/p/span[2]').get_attribute('textContent')
    total_page = browser.find_element(By.XPATH,'//*[@id="js-pagebread--top-id"]/section/aside/div/p/span[3]').get_attribute('textContent')
    current_page_url = browser.current_url
    next_page = browser.find_elements(By.CLASS_NAME,'js-pagbrd--next')[0].get_attribute('href')
    seconds = time.time()
    local_time = time.ctime(seconds)
    with open(os.getcwd() + '\logs.txt', 'a') as log:
        log.write(local_time + " \t " + current_page_url + '\n')
    links = browser.find_elements(By.XPATH, './/section/article[@class="prod-artc" and @role="row"]')
    for link in links:
        prod_links.append(link.find_element(By.XPATH, './/a[1]').get_attribute('href'))
    for prod in prod_links:
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
        if prod != None:
            try:
                browser.get(prod)
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
                if "hidden" in option1 and option2 and option3:
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
                elif ("hidden" in option2 and option3):
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
                data=[id, titles, description, category, sku, image, option1_name, option1_value, option2_name, option2_value, quantity, variant_image, price]
            except:
                with open(os.getcwd() + '\errorlogs.txt', 'a') as log:
                    log.write(local_time + '\t:\t' + prod + '\n')
                continue
        data = pd.DataFrame({'ID': pd.Series(id), 'Title': pd.Series(titles), 'Description': pd.Series(description), 'Category': pd.Series(category), 'SKU': pd.Series(sku), 'Images': pd.Series(image), 'Option1 Name': pd.Series(option1_name), 'Option1 Value': pd.Series(option1_value), 'Option2 Name': pd.Series(option2_name), 'Option2 Value': pd.Series(option2_value), 'Quantity': pd.Series(quantity), 'Variant Image': pd.Series(variant_image), 'Price': pd.Series(price)})
        df = df.append(data)
        count += 1
    if(int(current_page) > int(total_page)):
        break
    browser.get(next_page)

df.to_csv(os.getcwd() + '\data.csv', index= False, header=True)   
browser.close()