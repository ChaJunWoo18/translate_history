#merge파일
#date_title_content와 trans 병합 및 수정
#하나씩 처리
import os
import re
import fnmatch
import pandas as pd
import xml.etree.ElementTree as ET
import translate_module_copy

def split_text(text):
    sentences = []
    sentence = ""
    quote_count = 0

    for char in text:
        sentence += char
        if char == '"':
            quote_count += 1
        if char == '。' and quote_count % 2 == 0:
            sentences.append(sentence)
            sentence = ""
            quote_count = 0

    if sentence:
        sentences.append(sentence)

    return sentences

def extract_text(text):
    # <index> 태그 안의 값은 쌍따옴표로 감싸고, 나머지 값은 그대로 가져오도록 정규 표현식을 설정
    processed_text = re.sub(r'<index[^>]*>(.*?)</index>', r'"\1"', text)
    return processed_text

dir_list = ['JoseonDynastyAnnals','gojong']
originalData_DIR= dir_list[0]

###파일 목록 전처리
originalData_list = os.listdir(originalData_DIR)
originalData_list_ecp = []# 000.xml로 끝나는 파일과 history.dtd제거
for filename in originalData_list:
    if fnmatch.fnmatch(filename, "2nd_*") and not fnmatch.fnmatch(filename, "*_000.xml" and "*_200.xml"):
        originalData_list_ecp.append(filename)

data=[]

###selenium을 통한 ai 번역준비
driver = translate_module_copy.start_program()

for file in originalData_list_ecp:
    tree = ET.parse(originalData_DIR+'/'+file)
    root = tree.getroot()

    textContent =[]
    
    for level4 in root.findall('.//level4'):
        level4_elem_mainT = level4.find('.//mainTitle')
        main_title_date = level4_elem_mainT.text.strip()
        main_title_date = translate_module_copy.translate_with_hanjaLibrary(main_title_date)

        if main_title_date[:4] != '정조 8':
            print(main_title_date[:4],'PASS')
            break
        
        fname = f'./result/{main_title_date}.csv'
        print(main_title_date)
        if main_title_date != '정조 8년 8월 24일':
            continue
        #이미 존재하는 파일이면 번역 X
        if os.path.exists(fname):
            print(fname,'은 이미 존재합니다...다음 파일 검색')
            continue

        level5_elem = level4.findall('.//level5')

        for el in level5_elem:
            main_title = el.find('.//mainTitle').text.strip()
            
            paragraphs = el.findall('.//paragraph')
            for paragraph in paragraphs:
                text = ''.join(paragraph.itertext())
                text = extract_text(text)
                sentences = split_text(text.replace("○","")) # text 문장으로 쪼개기
                
                translate_module_copy.translate_with_selenium(driver,sentences, fname, main_title)
            

driver.quit()



