from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import sys
from hanja import translate

def start_program():
    chrome_options = Options()
    chrome_options.add_experimental_option('detach',True) #실행 후 자동 종료 방지

    driver = webdriver.Chrome(options=chrome_options)
    #driver.implicitly_wait(10) #페이지 로딩 완료까지 3초 대기 #모든 코드에 적용되며, 페이지 로딩이 설정 시간 이전에 끝나면 다음코드를 수행한다. 의도한대로 동작하지 않는듯함
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.google.com")
# 검색창에 고서번역 플랫폼의 '간편 번역' 입력
    #inputBox = driver.find_element(By.CSS_SELECTOR, '#APjFqb')
    inputBox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#APjFqb')))
    inputBox.send_keys('https://aigoseo.or.kr/home/simple/translation.do')
    inputBox.send_keys(Keys.ENTER)

    # 접속(검색이 완료되기 전에 접속 시도 방지를 위해 try catch)
    aigoseoURLSelector = '#rso > div:nth-child(1) > div > div > div > div.kb0PBd.cvP2Ce.A9Y9g.jGGQ5e > div > div > span > a > div > div > div > div.byrV5b > cite'
    #aigoseoURL = driver.find_element(By.CSS_SELECTOR, aigoseoURLSelector)
    aigoseoURL = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, aigoseoURLSelector)))
    aigoseoURL.click()


    # 사진이 가려 textarea사용 못하는 상황 -> class속성 값을 강제로 바꿔서 textarea활성화
    imgSelector = '#drop_zone > div > div.simple_img.pd10.hide'
    #img = driver.find_element(By.CSS_SELECTOR, imgSelector)
    img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, imgSelector)))
    driver.execute_script("arguments[0].setAttribute('class', 'simple_img pd10')", img)
    return driver

def translate_with_selenium(driver, sentences):
    transText_list = []
    wait = WebDriverWait(driver, 10)
    #textarea에 번역할 값 전달하고 번역 버튼 클릭
    textareaSelector = '#text_zone'
    textArea = driver.find_element(By.CSS_SELECTOR, textareaSelector)
    print(sentences)
    for text in sentences:
        print(text)
        textArea.send_keys(text)
        #transBtn = driver.find_element(By.CSS_SELECTOR, '#autoTranslation')
        transBtn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#autoTranslation')))
        transBtn.click()
        while True:
            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                print("번역 가능 용량을 초과하여 재시도합니다.")
                alert = driver.switch_to.alert
                alert.dismiss() 
                transBtn.click() 
            except:
                break

        #번역된 결과를 가지고 오기- 클립보드 복사 클릭
        clipboard = driver.find_element(By.CSS_SELECTOR, '#textClipboard') 
        clipboard.click()
        alert = driver.switch_to.alert
        alert.dismiss()

        # 클립보드의 내용 가져오기
        clipboard_content = pyperclip.paste()
        translation_start_index = clipboard_content.find("- 번역문")
        translation_text = clipboard_content[translation_start_index+6:].strip() # - 번역문 이후부터 "번역된 내용만" 추출
        textArea.clear() #문자열 비우기 (다음 문자열 대비)
        transText_list.append(translation_text)
    return transText_list


def translate_with_hanjaLibrary(text):
    translation = translate(text, 'substitution')
    return translation

if __name__ == "__main__":
    driver = start_program()
    #translate_with_selenium(driver)
