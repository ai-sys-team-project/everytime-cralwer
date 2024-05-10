from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 네이버 로그인 정보
naver_id = "네이버 아이디"
naver_pw = "네이버 비밀번호"

# WebDriver 설정
driver = webdriver.Chrome()

# 네이버 로그인 페이지로 이동
driver.get("https://nid.naver.com/nidlogin.login")
time.sleep(2)

# 아이디와 비밀번호 입력 후 로그인
driver.find_element(By.CSS_SELECTOR, "#id").send_keys(naver_id)
driver.find_element(By.CSS_SELECTOR, "#pw").send_keys(naver_pw)
# driver.find_element(By.CSS_SELECTOR, ".btn_global").click()
driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
time.sleep(2)

# 네이버 프로필 페이지로 이동
driver.get("https://nid.naver.com/user2/help/myInfo.nhn?menu=myinfo")
time.sleep(2)

# 프로필 정보 가져오기
nickname = driver.find_element(By.CSS_SELECTOR, ".useid").text
email = driver.find_element(By.CSS_SELECTOR, ".useemail").text

# DataFrame 생성
profile_data = {
    "Nickname": [nickname],
    "Email": [email],
}
df = pd.DataFrame(profile_data)

# CSV 파일로 저장
df.to_csv("naver_profile.csv", index=False)

# WebDriver 종료
driver.quit()
