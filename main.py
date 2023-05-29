import logging
import math
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_properties(driver, url):
    result = []
    driver.get(url)
    # search_field = driver.find_element(By.ID, 'searchLocation')
    # search_field.send_keys('Watermead, Buckinghamshire')
    #
    # # Click the search button
    # search_button = driver.find_element(By.ID, 'search')
    # search_button.click()
    # time.sleep(2)
    # search_button = driver.find_element(By.CLASS_NAME, 'touchsearch-primarybutton')
    # search_button.click()
    url = driver.current_url
    cards = driver.find_elements(By.CLASS_NAME, 'propertyCard')
    for each in cards:
        result.append(get_property_links(each))
    count = 0
    try:
        count = int(driver.find_element(By.CLASS_NAME, "searchHeader-resultCount").text)
    except Exception:
        logging.info("Single Page.")

    count = math.ceil(count / 24)
    for i in range(1, 3):
        print(i)
        driver.get(url + f"&index={str(i * 24)}")
        time.sleep(1)
        cards = driver.find_elements(By.CLASS_NAME, 'propertyCard')
        for each in cards:
            result.append(get_property_links(each))
    return result


def get_property_links(property):
    try:
        # print(prop.text)
        sale_link = property.find_element(By.CLASS_NAME, 'propertyCard-link')
        rent_link = property.find_element(By.CLASS_NAME, 'propertyCard-priceValue')
        if sale_link and rent_link:
            return (sale_link.get_attribute('href'), rent_link.text)
        return None
    except Exception as e:
        logging.exception(e)
        return None


def main():
    webdriver_service = Service('path_to_your_chromedriver')
    driver = webdriver.Chrome(service=webdriver_service)

    sale_url = 'https://www.rightmove.co.uk/property-for-sale.html'
    rent_url = 'https://www.rightmove.co.uk/property-to-rent.html'
    sale_url = 'https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E1498&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false'
    rent_url = 'https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E1498&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare='

    sale_properties = get_properties(driver, sale_url)
    # rent_properties = get_properties(driver, rent_url)
    rent_properties = []

    #sale_links = get_property_links(sale_properties)
    # rent_links = get_property_links(rent_properties)
    rent_links = []

    # Properties listed both for sale and rent
    # both_links = set(sale_links).intersection(set(rent_links))

    for links in sale_properties:
        print(f'Sale link: {links}')

    driver.quit()


if __name__ == "__main__":
    main()
