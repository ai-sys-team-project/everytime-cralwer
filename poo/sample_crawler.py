from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

import random
import csv
import pandas as pd

option = webdriver.ChromeOptions()
option.add_argument("start-maximized")
option.add_experimental_option('detach', True) # 브라우저 바로 닫힘 방지
option.add_experimental_option("excludeSwitches", ["enable-logging"]) # 불필요한 메세지 제거
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/539.26 (KHTML, like Gecko) Chrome/69.0.3026.130 Safari/539.26") # user-agent
option.add_argument("--disable-blink-features") # 브라우저 기능 비활성화
option.add_argument("--disable-blink-features=AutomationControlled") # 브라우저 자동화 기능 비활성화
link_list = []
title_list = []
sentence_list = []
date_list = []
user_list = []
comments_user_1_list = []
comments_sen_1_list = []
comments_user_2_list = []
comments_sen_2_list = []

def get_post_comment(driver, zz, page_number, site):
    driver.implicitly_wait(30)
    random_time = random.uniform(15, 25)
    sleep(random_time)
    html = driver.page_source
    soup = bs(html,'html.parser')
    body = soup.select('article a.article')
    for i in body:
        id_date = i.select('div.profile')
        titles = i.select('h2.large')
        sentences = i.select('p.large')
        for j in  id_date:
            user = j.select_one('h3.large').text
            date = j.select_one('time.large').text
        for k in  titles:
            title = k.text
        for l in  sentences:
            sentence = l.text
    body2 = soup.select('div.comments')
    driver.implicitly_wait(30)
    for i in body2:
        comments_1=i.select('article.parent')
        comments_2=i.select('article.child')
        if comments_1 == []:
            link_list.append(site)
            title_list.append(title)
            sentence_list.append(sentence)
            date_list.append(date)
            user_list.append(user)
            comments_user_1_list.append(None)
            comments_sen_1_list.append(None)
            comments_user_2_list.append(None)
            comments_sen_2_list.append(None)
        for j in comments_1:
            comments_user_1=j.select_one('h3.medium').text
            comments_sen_1=j.select_one('p.large').text
            link_list.append(site)
            title_list.append(title)
            sentence_list.append(sentence)
            date_list.append(date)
            user_list.append(user)
            comments_user_1_list.append(comments_user_1)
            comments_sen_1_list.append(comments_sen_1)
            comments_user_2_list.append(None)
            comments_sen_2_list.append(None)
        for k in comments_2:
            comments_user_2=k.select_one('h3.medium').text
            comments_sen_2=k.select_one('p.large').text
            link_list.append(site)
            title_list.append(title)
            sentence_list.append(sentence)
            date_list.append(date)
            user_list.append(user)
            comments_user_1_list.append(None)
            comments_sen_1_list.append(None)
            comments_user_2_list.append(comments_user_2)
            comments_sen_2_list.append(comments_sen_2)
    result = {'id':user_list,'posting time':date_list,'post title':title_list,'post text':sentence_list,
         'comments id':comments_user_1_list,'comments':comments_sen_1_list,
         'vs_comments id':comments_user_2_list,'vs_comments':comments_sen_2_list}
    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in result.items()]))
    df.to_excel(f'every_time_Result_{page_number:05}p_{zz:05}.xlsx', index=False)
    print(f'{page_number}페이지의 {zz}번째까지 엑셀 저장완료')
def login(driver):
    login_url = "https://everytime.kr/503023"

    ID_ = '' 
    PWD_ = ''
    
    driver.get(login_url)
    sleep(10)
    driver.find_element(By.CSS_SELECTOR, '#container > form > p:nth-child(1) > input').send_keys(ID_)
    driver.find_element(By.CSS_SELECTOR, '#container > form > p:nth-child(2) > input').send_keys(PWD_)

def scroll_down(driver, before_h=0):
    while True:
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
        random_time = random.uniform(1, 3)
        sleep(random_time)
        after_h = driver.execute_script('return window.scrollY')
        if before_h == after_h:
            break
        before_h = after_h
    # 동일한 클래스 이름을 가진 모든 요소 찾기
    element_count = len(driver.find_elements(By.CSS_SELECTOR, list_title_a_selector))
    return element_count
def list_move_in_page(driver, element_count, list_title_a_selector, page_number, before_h=0):
    # 각 요소를 반복하며 클릭
    for i in range(element_count):
        # 매 반복마다 요소 목록을 다시 가져오기
        _ = scroll_down(driver, before_h)
        elements = driver.find_elements(By.CSS_SELECTOR, list_title_a_selector)
        href = elements[i].get_attribute('href')
        driver.get(href)
        driver.implicitly_wait(10)
        sleep(10)
        get_post_comment(driver, i, page_number, site=href)
        random_time = random.uniform(17, 27)
        sleep(random_time)
        # 이전 페이지로 돌아가기
        driver.back()
        driver.implicitly_wait(10)
        print(f'{page_number}페이지의 {i}/{element_count}번째 요소 클릭 완료')
        random_time = random.uniform(10, 20)
        sleep(random_time)
def navigate_and_click_posts(base_url, list_title_a_selector, button_selector, start_page, login_required=False):
    path_driver = ChromeDriverManager().install()
    # print(path_driver)
    driver = webdriver.Chrome(service=Service(path_driver), options=option)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    """
    })
    if login_required:
        login(driver)
        sleep(30)
    try:
        page_number = start_page
        while True:
            print(f'Navigating page {page_number}')
            url = base_url.format(page=page_number)
            driver.get(url)
            driver.implicitly_wait(10)
            before_h = driver.execute_script('return window.scrollY') #최초 스크롤 높이 가져오기
            element_count = scroll_down(driver, before_h)
            list_move_in_page(driver, element_count, list_title_a_selector, page_number, before_h=before_h)
            try:
                # "다음" 링크
                next_link = driver.find_element(By.CSS_SELECTOR, button_selector)
                # "다음" 링크의 href 속성 값
                next_page_url = next_link.get_attribute('href')
                # "다음" 페이지로 이동합니다.
                driver.get(next_page_url)
            except NoSuchElementException:
                # "다음" 링크가 없으면, 마지막 페이지에 도달한 것으로 간주하고 반복을 중지
                print(f'Last page reached: {page_number}')
                break
            page_number += 1  # 페이지 번호를 증가
    finally:
        # WebDri3ver 인스턴스를 종료하여 브라우저 창을 닫음
        driver.quit()