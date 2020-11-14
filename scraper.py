from selenium import webdriver
from bs4 import BeautifulSoup 
from re import sub
from decimal import Decimal

import collections


driver = webdriver.Chrome(executable_path='/home/aphrx/Code/tv_sale_scraper/chromedriver')
driver.get("https://www.bestbuy.ca/en-ca/collection/tvs-on-sale/79094?icmp=home_offers_tvsonsale")

best_price = {}
best_discount = {}
tv_info = []

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
    for tv in tvs:
        try:
            name = tv.find_element_by_class_name('productItemName_3IZ3c').text
            url = tv.find_element_by_class_name('link_3hcyN').get_attribute('href')
            price = Decimal(sub(r'[^\d.]', '',tv.find_element_by_class_name('price_FHDfG').text))
            save = Decimal(sub(r'[^\d.]', '',tv.find_element_by_class_name('productSaving_3YmNX').text.split(" ")[1]))
            discount = 0
            discount = (save/price) * 100
            size = 0
            name_split = name.split()
            for n in name_split:
                if ('\"' in n) or ('”' in n)  or ('\'' in n) or ('-Inch' in n) or ('IN' in n and n[:2].isdigit()):
                    size = n[:2]
                    break
                elif(('IN' in n) or ('INCH' in n) or ('inch' in n) or ('Inch' in n) or ('in.' in n)):
                    if name_split[name_split.index(n)-1][:2].isdigit():
                        size = name_split[name_split.index(n)-1][:2]
                        break

            tv_info.append([name, size, url, price, save, discount])
            
        except:
            print("No info")

def parse_tv_info():
    for tv in tv_info:
        print("%-90s %-5s %-10s %-10s %-10s" % (tv[0].split('(')[0].split('-')[0], tv[1], tv[3], tv[4], tv[5]))

        if best_price.get(tv[1]) is None:
            best_price[str(tv[1])] = tv
        else:
            if best_price.get(tv[1])[3] > tv[3]:
                best_price[str(tv[1])] = tv

        if best_discount.get(tv[1]) is None:
            best_discount[str(tv[1])] = tv
        else:
            if best_discount.get(tv[1])[5] < tv[5]:
                best_discount[str(tv[1])] = tv
    
def print_output():
    print("\nCheapest TV's")
    for i, j in best_price.items():
        print("%-5s %-10s %-100s" % (i, "$" + str(j[3]), j[0]))

    print("\nMost Discounted TV's")
    for i, j in best_discount.items():
        print("%-5s %-10s %-10s %-100s" % (i, "$" + str(j[3]), str(round(j[5], 2)) + "%", j[0]))

load_full_page()
find_all_tv()
parse_tv_info()
print_output()

driver.close()