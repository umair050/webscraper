import csv
import random
import time
import sys
import requests
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

SEARCH_DICT = []
driver = ""

sheet_flag_1 = 0
sheet_flag_2 = 0
sheet_flag_3 = 0

counter = 0

search_key_words1 = ["local delivery", "subscription", "pre - order", "pre - orders", "pre - ordering",
                     "order cutoff", "membership", "local pickup"]

search_key_words2 = ["local delivery", "subscription", "pre - order", "pre - orders", "pre - ordering",
                     "order cutoff", "membership", "local pickup", "wholesale", "stockist"]

search_key_words3 = ["wholesale", "stockist"]


def get_csv_data():
    filename = "sheet_unique.csv"
    # opening the file using "with"
    # statement
    with open(filename, 'r') as data:
        for line in csv.reader(data):
            # print(line)
            SEARCH_DICT.append(line)
    print(len(SEARCH_DICT))


def initSetup():
    userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    op = webdriver.ChromeOptions()

    op.add_argument("--window-size=1920,1080")
    # op.add_argument('--verbose')
    # op.add_argument('--headless')
    op.add_argument("--window-size=1920,1080")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--start-maximized")
    global driver
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    # webdriver.Chrome(executable_path="chromedriver.exe")
    driver = webdriver.Firefox(executable_path="F:\\Users\\Malik Umair\\PycharmProjects\\WebScrapper\\geckodriver.exe")
    driver.implicitly_wait(10)


def get_filter():
    try:
        global driver
        global sheet_flag_1
        global sheet_flag_2
        global sheet_flag_3
        global counter

        for index, url in enumerate(SEARCH_DICT):
            print(" Current URL : " + str(url[0]))
            counter = index
            try:
                sheet_flag_1 = 0
                sheet_flag_2 = 0
                sheet_flag_3 = 0

                driver.get(url[0])
                filter_data(url[0])

                if BeautifulSoup(driver.page_source, 'html.parser').find("nav"):
                    nav_links = BeautifulSoup(driver.page_source, 'html.parser').find("nav").findChildren("a",
                                                                                                          href=True)
                    for link in nav_links:
                        if sheet_flag_1 == 1 and sheet_flag_2 == 1 and sheet_flag_3 == 1:
                            break
                        print("Flag 1 =" + str(sheet_flag_1))
                        print("Flag 2 =" + str(sheet_flag_2))
                        print("Flag 3 =" + str(sheet_flag_3))
                        link = link['href']
                        print(link)
                        if len(link) == 0:
                            continue
                        if link[0] == "/":
                            link = url[0] + link
                            driver.get(link)
                            # time.sleep(10)
                            filter_data(url[0])
                        elif link[0] == "h":
                            link = link
                            driver.get(link)
                            # time.sleep(10)
                            filter_data(url[0])
                        else:
                            continue
                    print(nav_links)

            except selenium.common.exceptions.TimeoutException:
                continue
            except selenium.common.exceptions.WebDriverException as e:
                print("WebDriverException inside t: ")
                continue

    except selenium.common.exceptions.WebDriverException:
        print("WebDriverException")
        return 0


def filter_data(url):
    try:
        global driver
        global sheet_flag_1
        global sheet_flag_2
        global sheet_flag_3

        # time.sleep(5)
        page_source = BeautifulSoup(driver.page_source, 'html.parser').text.lower()
        if sheet_flag_1 == 0:
            for s in search_key_words1:
                if s in page_source:
                    sheet_flag_1 = 1
                    print("Exist in sheet 1" + s)
                    write_to_csv(url, "sheet1.csv")

        if sheet_flag_2 == 0:
            for s in search_key_words2:
                if s in page_source:
                    sheet_flag_2 = 1
                    print("Exist in sheet 2" + s)
                    write_to_csv(url, "sheet2.csv")

        if sheet_flag_3 == 0:
            for s in search_key_words3:
                if s in page_source:
                    sheet_flag_3 = 1
                    print("Exists in sheet 3" + s)
                    write_to_csv(url, "sheet3.csv")

        # print(page_source)

    except selenium.common.exceptions.WebDriverException:
        print("test")


def write_to_csv(url, filename):
    with open(filename, 'a', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow([url])


get_csv_data()
initSetup()
get_filter()
