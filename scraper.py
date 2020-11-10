from selenium import webdriver
from bs4 import BeautifulSoup 

driver = webdriver.Chrome(executable_path='/home/aphrx/Code/tv_sale_scraper/chromedriver')
driver.get("https://www.bestbuy.ca/en-ca/collection/tvs-on-sale/79094?icmp=home_offers_tvsonsale")

def load_full_page():
    while True:
        try:     
            driver.find_element_by_class_name("loadMore_3AoXT").click()
        except:
            if check_end_of_page():
                break

def check_end_of_page():
    try:
        driver.find_element_by_class_name("endOfList_b04RG")
    except:
        return False
    return True

def find_all_tv():
    tvs = driver.find_elements_by_class_name('x-productListItem')
    tv_info = []
    for tv in tvs:
        try:
            name = tv.find_element_by_class_name('productItemName_3IZ3c').text
            url = tv.find_element_by_class_name('link_3hcyN').get_attribute('href')

            tv_info.append([name, url])
        except:
            print("No name")
    print(len(tv_info))

load_full_page()
find_all_tv()