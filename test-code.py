import random
from re import UNICODE
from django.db import connection
from twocaptcha import TwoCaptcha
from django.shortcuts import render
from background_task import background
# Create your views here.
from urllib.parse import urlparse
from urllib.parse import parse_qs
from celery import shared_task
import os
import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
from background_task import background
import requests
from product.models import Scrap as ProductScrap
# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
144
200
56

# req_proxy = RequestProxy()
# proxies = req_proxy.get_proxy_list()
# https://github.com/2captcha/2captcha-python

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


LOGIN_URL = "https://www.ebay-kleinanzeigen.de/m-einloggen.html?targetUrl=/anzeigen/stadt/berlin/"
USERNAME = "3006evita+22@gmail.com"
PASSWORD = "M2iB2QYL3d"
driver = ""
BASE_URL = "https://www.ebay-kleinanzeigen.de"

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="cats_bot"
# )
# cursor = db.cursor(dictionary=True)


def initSetup():
    userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    op = webdriver.ChromeOptions()
    op.add_argument("start-maximized")
    op.add_argument("disable-infobars")
    op.add_argument('--no-sandbox')
    op.add_argument('--headless')
    op.add_argument("--disable-extensions")
    op.add_argument('--disable-blink-features=AutomationControlled')
    op.add_argument('headless')
    op.add_argument('user-agent={user_agent}')
    # op.add_argument("--window-size=1200,720")
    op.add_argument('--lang=en_US')

    # self.chrome_options = webdriver.ChromeOptions()
    op.add_argument("--window-size=1920,1080")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--start-maximized")
    # op.add_argument('--headless')

    op.add_argument('--verbose')
    op.add_argument('--disable-gpu')
    op.add_argument('--disable-dev-shm-usage')
    # op.add_argument('--no-sandbox')
    op.add_argument('--ignore-certificate-errors')
    # self.browser = webdriver.Chrome(options=self.chrome_options)

    proxy_url = 'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&country=DE'
    r = requests.get(proxy_url)
    r_dictionary = r.json()
    # print(r_dictionary['data'][0])
    proxies = r_dictionary['data']

    print("******************** Proxy **************************")
    print(len(proxies))
    n = random.randint(0, len(proxies) - 1)
    PROXY = proxies[n]['ip']
    print("******************** Random Number **************************")
    print(n)
    print("******************** Proxy IP **************************")
    print(PROXY)
    # PROXY = '59.120.147.82'
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
        "autodetect": False

    }

    global driver
    # driver = webdriver.Chrome(options=op)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    driver.get(BASE_URL)
    time.sleep(4)
    # driver.find_element_by_id("gdpr-banner-accept").click()


def user_login():
    # global driver
    # user_register()
    driver.get(LOGIN_URL)
    # driver.get('https://www.ebay-kleinanzeigen.de/m-benutzer-anmeldung.html')
    print("User Login Visiting.....")
    # print(LOGIN_URL)
    time.sleep(20)
    api_key = '96e332842138a896549d12e3df4e1df3'
    solver = TwoCaptcha(api_key)
    print(solver)
    code = ''
    try:
        result = solver.recaptcha(
            sitekey='6LfwuyUTAAAAAOAmoS0fdqijC2PbbdH4kjq62Y1b',
            url=LOGIN_URL,
            version='v2',
            score=0.1
        )
        print("API RESPONSE =====>", result)

    except Exception as e:
        print("Exception ======> ")
        sys.exit(e)

    else:
        code = str(result['code'])
        # driver.get('https://www.ebay-kleinanzeigen.de/m-benutzer-anmeldung.html')
        time.sleep(10)
        # driver.find_element_by_id("gdpr-banner-accept").click()
        html2 = driver.execute_script(
            "return document.getElementById('g-recaptcha-response').innerHTML = '" + code + "';")
        print("API STATUS RE-CAPTCHA ====>", html2)

        # print()
        # driver.find_element_by_id("gdpr-banner-accept").click()
        # print(driver.page_source)
        driver.find_element_by_id("login-email").send_keys(USERNAME)
        driver.find_element_by_id("login-password").send_keys(PASSWORD)
        time.sleep(10)
        driver.find_element_by_id("login-submit").click()


def user_register():
    api_key = '96e332842138a896549d12e3df4e1df3'
    solver = TwoCaptcha(api_key)
    code = ''
    try:
        result = solver.recaptcha(
            sitekey='6LcZlE0UAAAAAFQKM6e6WA2XynMyr6WFd5z1l1Nr',
            url='https://www.ebay-kleinanzeigen.de/m-benutzer-anmeldung.html',
            version='v2',
            score=0.1
        )

    except Exception as e:
        sys.exit(e)

    else:
        code = str(result['code'])
        driver.get('https://www.ebay-kleinanzeigen.de/m-benutzer-anmeldung.html')
        time.sleep(10)
        driver.find_element_by_id("gdpr-banner-accept").click()
        html2 = driver.execute_script(
            "return document.getElementById('g-recaptcha-response').innerHTML = '" + code + "';")
        print(html2)
        time.sleep(2)
        driver.find_element_by_id("registration-email").send_keys(USERNAME)
        driver.find_element_by_id("registration-password").send_keys(PASSWORD)
        driver.find_element_by_id(
            "registration-password-confirmation").send_keys(PASSWORD)
        driver.find_element_by_id("marketing-optin").click()
        driver.find_element_by_id("registration-submit").click()


def get_products():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products where status=3")
    rows = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in rows:
        insertObject.append(dict(zip(columnNames, record)))
    return insertObject


def get_messages(status):
    cursor = connection.cursor()
    sql_query = "SELECT * FROM messages where type = " + str(status)
    print(sql_query)
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in rows:
        insertObject.append(dict(zip(columnNames, record)))
    return insertObject


# @background(queue="send-messages")
@shared_task
def send_messages():
    initSetup()
    user_login()
    global driver
    products = get_products()
    # print(products)
    # exit()
    offer_messages = get_messages(0)
    request_messages = get_messages(1)
    offer_count = 0
    request_count = 0
    print(offer_messages)
    # exit(1)
    # print(data[0])

    for product in products:
        print(product['url'])
        print(" URL ==>", product)
        driver.get(str(product['url']))
        time.sleep(5)
        product_type = product['type']
        # user_id = product['user_id']
        # print("Product Type ==>", product_type)
        # print("Product Type ==>", type(product_type))
        # print("Request Count ==>", request_count)
        # print("Offer Count ==>", offer_count)

        if int(product_type) == 1:
            message = request_messages[request_count]['message']
            print("Message ==> ", message)
            request_count = request_count + 1
            send_message(str(message))
            if request_count == len(request_messages):
                request_count = 0
        elif int(product_type) == 0:
            message = offer_messages[offer_count]['message']
            print("Message ==> ", message)
            offer_count = offer_count + 1
            send_message(str(message))

            if offer_count == len(offer_messages):
                offer_count = 0

        # cursor = connection.cursor()
        # cursor.execute("UPDATE  products set status=5 where id =". product['id'])
        # print(send_message)
        # driver.find_element_by_id("viewad-contact-button").click()
        # driver.find_element_by_name("message").send_keys(str(send_message))
        # driver.find_element_by_class_name("viewad-contact-submit").click()


def send_message(message):
    # time.sleep()
    print("=============== MESSAGE=====================")
    # print(user_id)
    print(message)
    # if user_id == '64453079':
    # model = driver.find_element_by_class_name("mfp-close")
    # if model:
    #     model.click()
    driver.find_element_by_id("viewad-contact-button").click()
    driver.find_element_by_name("message").send_keys(str(message))
    time.sleep(3)
    driver.find_element_by_class_name("viewad-contact-submit").click()


# @background(queue="scrap-ads")
@shared_task
def scrap_ads(url):
    initSetup()
    # url = "https://www.ebay-kleinanzeigen.de/s-tierbetreuung-training/berlin/c133l3331"
    # cats_url = "https://www.ebay-kleinanzeigen.de/s-katzen/c136"
    # dogs_url = "https://www.ebay-kleinanzeigen.de/s-hunde/c134"
    # small_animal_offers_url = "https://www.ebay-kleinanzeigen.de/s-kleintiere/anzeige:angebote/c132"
    # small_animal_wanted_url = "https://www.ebay-kleinanzeigen.de/s-kleintiere/anzeige:gesuche/c132"
    getPaginationLinks(url)
    # visit_page(cats_url)
    # visit_page(dogs_url)
    # visit_page(small_animal_offers_url)
    # visit_page(small_animal_wanted_url)
    driver.close()


def scrap_single_add(ad_url):
    print("*****************Visiting Single Add****************************")
    print(ad_url)
    time.sleep(10)
    # ad_url = 'https://www.ebay-kleinanzeigen.de/s-anzeige/heilige-birma-kitten-reinrassig/1865706739-136-1761'
    # global driver
    driver.get(ad_url)
    # soup = BeautifutrylSoup(driver.page_source, 'html.parser')
    time.sleep(25)

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # print(soup).encode('utf-8')
        counter = 0
        title_tag_html = soup.find(
            "h1", {"id": "viewad-title"})

        while not title_tag_html:
            print(
                "Content not found for single add wait for 10 more sec to load the content")
            # print("Loading......", ad_url)
            time.sleep(10)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            title_tag_html = soup.find("h1", {"id": "viewad-title"})
            counter = counter + 1
            # for 3 minute maximum wait
            # 24*10 = 240 sec | 240/60 = 4 minutes
            if counter == 6:
                break

        title_tag_html = soup.find(
            "h1", {"id": "viewad-title"})
        # print(title_tag_html[0].encode("utf-8"))
        # exit(1)
        title_tag = ''
        description_tag = ''
        user_id = 0

        if title_tag_html:
            title_tag = title_tag_html.getText()

        description_tag_html = soup.find_all(
            "p", {"id": "viewad-description-text"})
        if len(description_tag_html) > 0:
            description_tag = description_tag_html[0].getText()

        user_id_link = soup.find(
            "a", {"class": "user-profile-vip-badge"})
        if hasattr(user_id_link, 'attrs'):
            url = user_id_link.attrs['href']
            parsed_url = urlparse(url)
            user_id = parse_qs(parsed_url.query)['userId'][0]

        print(user_id)

        print("********************** User Id ************")
        print(user_id)
        # exit(1)
        # if title_tag:
        #     ad_title = title_tag.text
        # if description_tag:
        #     ad_description = description_tag.text

        # print("Title :", title_tag)
        # print("Description : ", description_tag)
        # if user_id != 0:
        # save_add_db(ad_url, title_tag, description_tag, user_id)
        save_add_db(ad_url, title_tag, description_tag, user_id)
    except NoSuchElementException:
        print("No element found in the single url")


def save_add_db(ad_url, ad_title, ad_description, user_id):
    meta = [ad_title, ad_description, ad_url, user_id]
    # print(meta)
    # query = "INSERT INTO products(name,description, url) " \
    #         "VALUES(%s,%s,%s)"
    # cursor.execute(query, meta)
    # db.commit()
    p = ProductScrap(name=ad_title, description=ad_description,
                     url=ad_url, user_id=user_id)
    p.save()


def getPaginationLinks(page_url):
    all_page_urls = []
    all_page_urls.append(page_url)
    next_url = getNextUrl(page_url)
    count = 0
    while(next_url):
        all_page_urls.append(next_url)
        count = count + 1
        if count > 10:
            break
        next_url = getNextUrl(next_url)

    print("All Paginated Urls ==> ", all_page_urls)
    for item in all_page_urls:
        print(" Visitig  Page: ", item)
        visit_page(item)


def getNextUrl(url):
    # next_url = ''
    try:
        driver.get(url)
        time.sleep(25)
        next_url = driver.find_element_by_class_name(
            "pagination-next").get_attribute("href")

        print("New Next URL  =>", next_url)
        if next_url:
            return next_url
        # return False
    except NoSuchElementException:
        return False


def visit_page(ad_url):
    # global driver
    driver.get(ad_url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.findAll("li", {"class": "lazyload-item"})
    if len(items) == 0:
        print("Loading......", ad_url)
        driver.get(ad_url)

    counter = 0
    while len(items) == 0:
        print("Content not found wait for 10 more sec to load the content")
        print("Loading......", ad_url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.findAll("li", {"class": "lazyload-item"})
        counter = counter + 1
        # for 3 minute maximum wait
        # 24*10 = 240 sec | 240/60 = 4 minutes
        if counter == 6:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.findAll("li", {"class": "lazyload-item"})

    print("All Itmems ===> ", len(items))
    for item in items:
        add_url = item.article.attrs['data-href']
        scrap_single_add(BASE_URL + add_url)

    return True


# user_login()
# scrap_ads()

# url, title, description = scrap_single_add("https://www.ebay-kleinanzeigen.de/s-anzeige/typvolle-lion-lop-haesin-minilop-zwerg-widder-mini-lop/1815446714-132-2673")
#
# save_add_db(url, title, description)

# user_register()

#
#
# driver.get("https://www.ebay-kleinanzeigen.de/s-anzeige/berghaus-atlas-ii/1811569380-76-15355")
# time.sleep(5)
# driver.find_element_by_id("viewad-contact-button").click()
# driver.find_element_by_name("message").send_keys("hello")
# driver.find_element_by_class_name("viewad-contact-submit").click()

Never Give up 

