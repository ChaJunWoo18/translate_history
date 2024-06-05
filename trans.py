from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip

chrome_options = Options()
chrome_options.add_experimental_option('detach',True) #실행 후 자동 종료 방지

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3) #페이지 로딩 완료까지 3초 대기
driver.get(url='https://google.com')

#검색창에 고서번역 플랫폼의 '간편 번역' 입력
inputBox = driver.find_element(By.CSS_SELECTOR, '#APjFqb')
inputBox.send_keys('https://aigoseo.or.kr/home/simple/translation.do')
inputBox.send_keys(Keys.ENTER)
driver.implicitly_wait(3) #페이지 로딩 완료까지 3초 대기

#접속(검색이 완료되기 전에 접속 시도 방지를 위해 try catch)
aigoseoURLSelector = '#rso > div:nth-child(1) > div > div > div > div.kb0PBd.cvP2Ce.A9Y9g.jGGQ5e > div > div > span > a > div > div > div > div.byrV5b > cite'
try:
    aigoseoURL = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, aigoseoURLSelector))
    )
    aigoseoURL = driver.find_element(By.CSS_SELECTOR, aigoseoURLSelector)
    aigoseoURL.click()
except:
    print("요소를 찾을 수 없습니다.")

driver.implicitly_wait(3) #페이지 로딩 완료까지 3초 대기
#사진이 가려 textarea사용 못하는 상황 -> class속성 값을 강제로 바꿔서 textarea활성화
imgSelector = '#drop_zone > div > div.simple_img.pd10.hide'
try:
    aigoseoURL = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, imgSelector))
    )
    img = driver.find_element(By.CSS_SELECTOR, imgSelector)
    driver.execute_script("arguments[0].setAttribute('class', 'simple_img pd10')", img)
except:
    print("요소를 찾을 수 없습니다.")

def  translate_with_selenium():
    driver.implicitly_wait(3) #페이지 로딩 완료까지 3초 대기
    #textarea에 번역할 값 전달하고 번역 버튼 클릭
    textareaSelector = '#text_zone'
    textArea = driver.find_element(By.CSS_SELECTOR, textareaSelector)
    textArea.send_keys('○丙申/十七日丙申, 太祖卽位于壽昌宮。 先是, 是月十二日辛卯, 恭讓將幸太祖第, 置酒與之同盟, 儀仗已列。')
    transBtn = driver.find_element(By.CSS_SELECTOR, '#autoTranslation')
    transBtn.click()

    #번역된 결과를 가지고 오기- 클립보드 복사 클릭
    clipboard = driver.find_element(By.CSS_SELECTOR, '#textClipboard') 
    clipboard.click()
    alert = driver.switch_to.alert
    alert.dismiss()

    # 클립보드의 내용 가져오기
    clipboard_content = pyperclip.paste()
    print(clipboard_content)

#time.sleep(15) # 실행이 완료되면 스스로 종료하기때문에 결과를 확인할 수 있도록 대기(11번 라인으로 종료방지)
#driver.quit() #자동종료됨


# source = driver.page_source
# print(source)
# soup = BeautifulSoup(source, 'html.parser')  # textarea에 원문, 번역문이 포함되지않아 해당 방법 사용불가
# print(soup)


