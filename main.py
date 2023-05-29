from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_properties(driver, url):
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
    # print(driver.current_url)
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # response = requests.get(driver.current_url, headers=headers)
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')
    cards = driver.find_elements(By.CLASS_NAME, 'propertyCard')
    # property_list = soup.find_all('div', class_='propertyCard')
    return cards


def get_property_links(property_list):
    results = []
    for prop in property_list:

        # print(prop.text)
        sale_link = prop.find_element(By.CLASS_NAME, 'propertyCard-link')
        rent_link = prop.find_element(By.CLASS_NAME, 'propertyCard-priceValue')
        if sale_link and rent_link:
            results.append(sale_link.get_attribute('href'))
    return results


def main():
    webdriver_service = Service('path_to_your_chromedriver')
    driver = webdriver.Chrome(service=webdriver_service)

    sale_url = 'https://www.rightmove.co.uk/property-for-sale.html'
    rent_url = 'https://www.rightmove.co.uk/property-to-rent.html'
    sale_url = 'https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94610&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false'
    rent_url = 'https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E94610&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare='

    sale_properties = get_properties(driver, sale_url)
    # rent_properties = get_properties(driver, rent_url)
    rent_properties = []

    sale_links = get_property_links(sale_properties)
    # rent_links = get_property_links(rent_properties)
    rent_links = []

    # Properties listed both for sale and rent
    #both_links = set(sale_links).intersection(set(rent_links))

    for links in sale_links:
        print(f'Sale link: {links}')

    driver.quit()


if __name__ == "__main__":
    main()
