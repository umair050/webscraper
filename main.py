import csv
import random
import time
import sys
import requests
import selenium
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
# req_proxy = RequestProxy()
# proxies = req_proxy.get_proxy_list()

BASE_URL = "https://www.google.com"
SEARCH_DICT = []
driver = ""
ALL_URL_250 = []
PER_QUERY = 0
PER_QUERY_LIMIT = 250
PROXIES = []


def initSetup():
    userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    op = webdriver.ChromeOptions()

    op.add_argument("--window-size=1920,1080")
    op.add_argument('--verbose')

    op.add_argument("--window-size=1920,1080")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--start-maximized")
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    # driver.get("http://ipinfo.io")
    driver.get(BASE_URL)
    time.sleep(4)


def getCSVDATA():
    filename = "sheet.csv"
    # opening the file using "with"
    # statement
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            # print(line)
            SEARCH_DICT.append(line)
    print(SEARCH_DICT)


def startSearching():
    for x in SEARCH_DICT:
        # print(x)
        search_key = x['Segment'] + " :" + x['State']
        # search(search_key)
        #
        # search_key_words = ["Local delivery", "Subscription", "Pre - order", "Pre - orders", "Pre - ordering",
        #                     "Order cutoff", "Membership", "Local pickup", "Wholesale", "Stockist"]
        search_key_words = ["Local delivery", "Subscription", "Pre - order", "Pre - orders", "Pre - ordering",
                            "Order cutoff"]

        for y in search_key_words:
            search_key = x['Segment'] + " " + y + " :" + x['State']
            search(search_key)


def search(search_key):
    print("Search 1")
    global PER_QUERY
    PER_QUERY = 0
    global driver

    print(search_key)

    try:
        driver.find_element_by_name("q").clear()
        driver.find_element_by_name("q").send_keys(search_key)
        driver.find_element_by_tag_name("form").submit()
        global SEARCH_1_URL_250
        get_all_cite_tags()
        next_url = driver.find_element_by_id("pnnext")
        while next_url and PER_QUERY <= 250:
            next_page_url = next_url.get_attribute("href")
            print(next_page_url)

            driver.get(next_url.get_attribute("href"))
            get_all_cite_tags()
            next_url = driver.find_element_by_id("pnnext")
        print(ALL_URL_250)


    except selenium.common.exceptions.InvalidElementStateException:
        print("Invalid state exception")
        search(search_key)
    except NoSuchElementException:
        print("No element found in the single url")


def get_all_cite_tags():
    time.sleep(random.randint(1, 5))
    cite_tags = driver.find_elements_by_tag_name("cite")
    print(cite_tags)
    for tag in cite_tags:
        print(tag)
        print(tag.text)
        search_url = tag.text.split("›")[0].strip()
        if search_url not in ALL_URL_250 and (search_url != ""):
            ALL_URL_250.append(search_url)
            # open the file in the write mode
            filename = "search.csv"
            with open(filename, 'a+', newline='') as f:
                # create the csv writer
                writer = csv.writer(f)

                # write a row to the csv file
                writer.writerow([search_url])
            global PER_QUERY
            PER_QUERY = PER_QUERY + 1
            if PER_QUERY >= PER_QUERY_LIMIT:
                break


initSetup()
getCSVDATA()
startSearching()
