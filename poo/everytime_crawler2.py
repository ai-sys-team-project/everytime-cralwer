from time import sleep
from urllib.request import Request, urlopen
import requests
import ssl

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
base_url = 'https://everytime.kr/375138'
context = ssl._create_unverified_context()


def crawler():
    driver.get(base_url)
    driver.implicitly_wait(2)

    driver.find_element(By.NAME, 'id').send_keys('sangji9504')
    driver.find_element(By.NAME, 'password').send_keys('shan3585')
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
    driver.implicitly_wait(2)

    # 페이지 로드 대기
    sleep(2)

    # response = urlopen(base_url, context=context, headers={'User-agent':'Mozila/5.0'}) 
    response = Request(base_url, headers={'User-agent':'Mozila/5.0'}) 
    html = urlopen(response).read()

    articles = driver.find_elements(By.CSS_SELECTOR, '.wrap.articles article.list a.article')
    for article in articles:
        href = article.get_attribute('href')
        print('href:', href)

    # soup = BeautifulSoup(html, "html.parser")
    # container_div = soup.find('div', {'id': 'container', 'class': 'article'})
    # if container_div:
    #     wrap_div = container_div.find('div', {'class': 'wrap articles'})
    #     print('wrap_div: ', wrap_div)
    #     articles = container_div.find_all('article', {'class': 'list'})
    #     for article in articles:
    #         a_tag = article.find('a', {'class': 'article'})
    #         if a_tag:
    #             href = a_tag['href']
    #             print('href: ', href)
    #         else:
    #             print('a_tag is None')
    #         sleep(2)
    # else:
    #     print('container_div is None')

crawler()
