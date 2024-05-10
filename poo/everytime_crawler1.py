from time import sleep
from bs4 import BeautifulSoup as bs

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import random
import pandas as pd

path_driver = ChromeDriverManager().install()
driver = webdriver.Chrome(service=Service(path_driver), options=option) # 크롬 드라이버 객체 생성

option = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
option.add_argument("start-maximized") # 전체화면
option.add_experimental_option('detach', True) # 브라우저 바로 닫힘 방지
option.add_experimental_option("excludeSwitches", ["enable-logging"]) # 불필요한 메세지 제거


driver.implicity_wait(30) # 브라우저에서 사용되는 엘리먼트를 찾을 수 있을 때까지 기다림
