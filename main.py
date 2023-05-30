import logging
import math
import time

from fuzzywuzzy import fuzz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

def string_similarity(str1, str2):
    ratio = fuzz.ratio(str1.lower(), str2.lower())
    return ratio >= 80


def get_properties(driver, url, type):
    result = []
    driver.get(url)
    search_field = driver.find_element(By.ID, 'searchLocation')
    search_field.send_keys('York')

    search_button = driver.find_element(By.ID, 'search')
    search_button.click()
    search_button = driver.find_element(By.CLASS_NAME, 'touchsearch-primarybutton')
    search_button.click()
    url = driver.current_url
    cards = driver.find_elements(By.CLASS_NAME, 'propertyCard')
    for each in cards:
        result.append(get_property_links(each, type))
    count = 0
    try:
        count = int(driver.find_element(By.CLASS_NAME, "searchHeader-resultCount").text)
    except Exception:
        logging.info("Single Page.")

    count = math.ceil(count / 24)
    for i in range(1, 2):
        driver.get(url + f"&index={str(i * 24)}")
        time.sleep(1)
        cards = driver.find_elements(By.CLASS_NAME, 'propertyCard')
        for each in cards:
            result.append(get_property_links(each, type))
    return result


def get_property_links(property, type):
    try:

        sale_link = property.find_element(By.CLASS_NAME, 'propertyCard-link')
        title = property.find_element(By.CLASS_NAME, 'propertyCard-address')
        try:
            beds = property.find_element(By.CLASS_NAME, 'property-information')
            beds = beds.find_elements(By.CLASS_NAME, 'text')
            beds = int(beds[1].text)
        except Exception as e:
            beds = 0

        rent_link = property.find_element(By.CLASS_NAME, 'propertyCard-priceValue')

        if sale_link and rent_link:
            return type, title.text, beds, sale_link.get_attribute('href'), rent_link.text
        return None
    except Exception as e:
        logging.exception(e)
        return None


def main():
    webdriver_service = Service('path_to_your_chromedriver')
    driver = webdriver.Chrome(service=webdriver_service)

    sale_url = 'https://www.rightmove.co.uk/property-for-sale.html'
    rent_url = 'https://www.rightmove.co.uk/property-to-rent.html'

    sale_properties = get_properties(driver, sale_url, "Sale")
    rent_properties = get_properties(driver, rent_url, "Rent")
    data = {"Title": [], "Beds": [], "Price": [], "Sale Link": [], "Rent Link": []}
    for sale in sale_properties:
        for each in rent_properties:
            if sale[2] == each[2] and string_similarity(sale[1], each[1]):
                data["Title"].append(sale[1])
                data["Beds"].append(sale[2])
                data["Price"].append(sale[4])
                data["Sale Link"].append(sale[3])
                data["Rent Link"].append(each[4])
    print(sale_properties)
    print(rent_properties)
    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=False)
    driver.quit()


if __name__ == "__main__":
    main()
