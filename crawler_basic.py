""" 
새내기 게시판: https://everytime.kr/375132 - 상지
성균맛집: 257902 - 윤지
브로리에게 물어봐: 402030 - 경철
동아리, 학회: 418760 - 재은
인사캠 자유게시판: 370444 - 상지
정보게시판: 375130 - 태웅

아이디 seinundzeit1
비밀번호 s9hkfm$w 
"""
import datetime
from datetime import datetime
from time import sleep
import ssl
import csv
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import selenium.common.exceptions  # selenium 모듈 임포트

from webdriver_manager.chrome import ChromeDriverManager

ID = 'seinundzeit1'
PWD = 's9hkfm$w'

BOARD_NUMBER = '370444' # 인사캠 자유 게시판
BASE_URL = f'https://everytime.kr/{BOARD_NUMBER}'

PAGE_FROM = 101 #  # 101, 1001
PAGE_TO = 300

BREAK_DATE = '23/05/08'
TODAY = datetime.today().strftime('%m/%d')

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
context = ssl._create_unverified_context()            


# def save_articles_to_xlsx(articles):
#     df = pd.DataFrame(articles)
#     df.to_excel(f'{BOARD_NUMBER}_{PAGE_FROM}-{PAGE_TO}.xlsx', index=False)

def save_articles_to_xlsx(articles_data, file_name):
    df = pd.DataFrame(articles_data)
    df.to_excel(file_name, index=False)

def extract_comments(div_comments):
    comments = []
    articles = div_comments.find_elements(By.CSS_SELECTOR, 'div.comments article') 
    for article in articles:
        comment_text = article.find_element(By.CSS_SELECTOR, 'p.large').text.strip()
        likes_element = article.find_element(By.CSS_SELECTOR, 'li.vote.commentvote')
        likes = likes_element.text.strip()
        if likes == '':
            likes = 0
        else:
            likes = int(likes)
        comments.append({'comment': comment_text, 'likes': likes})
    if len(comments) == 0:
        comments = None
    return comments




def crawler(base_url=BASE_URL, id=ID, pwd=PWD, break_date=BREAK_DATE, today=TODAY, page_from=PAGE_FROM, page_to=PAGE_TO):
    start_time = datetime.now()
    print('Start time: ', start_time)
    print('Break date: ', BREAK_DATE )

    driver.get(base_url)
    driver.implicitly_wait(2)

    driver.find_element(By.NAME, 'id').send_keys(id)
    driver.find_element(By.NAME, 'password').send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
    driver.implicitly_wait(2)

    sleep(2) # 페이지 로드 대기

    articles_data = []  
    hrefs = []
    times = []
    title = ''
    contents = ''
    comments = []
    likes, scrapes = 0, 0
    
    try:
        for page_num in range(page_from, page_to+1): # 101, 1001 # 새내기: 1 ~ 1840까지가 1년치 
            page_url = f"{base_url}/p/{page_num}"
            driver.get(page_url)
            driver.implicitly_wait(3)
            sleep(2)

            articles = driver.find_elements(By.CSS_SELECTOR, '.wrap.articles article.list')

            time_elements = driver.find_elements(By.CSS_SELECTOR, 'div.info time.small')
            print('time_elements: ', time_elements[0].text.split(' ')[0])
            if time_elements[0].text.split(' ')[0] == break_date:
                break
            else: 
                pass

            for article in articles:
                time_element = article.find_element(By.CSS_SELECTOR, 'div.info time.small')
                date = time_element.text.split(' ')[0]
                
                if '/' not in date:
                    date = today
                if date == break_date:
                    break

                times.append(date)

                href = article.find_element(By.CSS_SELECTOR, 'a.article').get_attribute('href')
                hrefs.append(href)


        for href in hrefs:
            driver.get(href)
            sleep(2)

            try: 
                time_element = driver.find_element(By.XPATH, '//time[@class="large"]')
                date = time_element.text.split(' ')[0]

                if date == break_date:
                    break
                
                if '/' not in date:
                    date = today

                title = driver.find_element(By.CSS_SELECTOR, 'h2.large').text
                contents = driver.find_element(By.CSS_SELECTOR, 'a.article p.large').text

                likes = int(driver.find_element(By.CSS_SELECTOR, 'li.vote').text)
                scrapes = int(driver.find_element(By.CSS_SELECTOR, 'li.scrap').text) 
                comments = extract_comments(driver.find_element(By.CSS_SELECTOR, 'div.comments'))
                
                article = { 
                    'date': date,
                    'title': title,
                    'contents': contents,
                    'likes': likes,
                    'scrapes': scrapes,
                    'comments': comments
                }
                articles_data.append(article)
            
            except selenium.common.exceptions.NoSuchElementException as e:
                print(f"Error finding element: {e}")
                # save_articles_to_xlsx(articles_data)
                save_articles_to_xlsx(articles_data, f'{BOARD_NUMBER}_until_error.xlsx')
                break
        
    except selenium.common.exceptions.NoSuchElementException as e:
        print(f"Error finding element: {e}")
        # save_articles_to_xlsx(articles_data)
        save_articles_to_xlsx(articles_data, f'{BOARD_NUMBER}_until_error.xlsx')

    driver.quit()

    # save_articles_to_xlsx(articles_data)
    save_articles_to_xlsx(articles_data, f'{BOARD_NUMBER}_{PAGE_FROM}-{PAGE_TO}.xlsx')

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print('End time: ',end_time)
    print(f"Crawling completed in {elapsed_time.total_seconds()} seconds.")



crawler()