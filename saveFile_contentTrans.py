#merge파일
#date_title_content와 trans 병합 및 수정
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

originalData_DIR= 'JoseonDynastyAnnals'

###파일 목록 전처리
originalData_list = os.listdir(originalData_DIR)
originalData_list_ecp = []# 000.xml로 끝나느 파일과 history.dtd제거
for filename in originalData_list:
    if fnmatch.fnmatch(filename, "2nd_*") and not fnmatch.fnmatch(filename, "*_000.xml" and "*_200.xml"):
        originalData_list_ecp.append(filename)

### Dataframe 저장용
title_df = []
content_df = []

###selenium을 통한 ai 번역준비
driver = translate_module_copy.start_program()

for file in originalData_list_ecp:
    tree = ET.parse(originalData_DIR+'/'+file)
    root = tree.getroot()

    textContent =[]
    # 필요한 부분을 찾기
    for level5 in root.findall('.//level5'):
        paragraphs = level5.findall('.//paragraph')
        for paragraph in paragraphs:
            text = ''.join(paragraph.itertext())
            text = extract_text(text)
            sentences = split_text(text.replace("○","")) # text 문장으로 쪼개기
            translated_cleaned_text = translate_module_copy.translate_with_selenium(driver,sentences)
            textContent.append({'text':translated_cleaned_text})    
            
driver.quit()

df=pd.DataFrame(textContent)
df.to_csv('./result/content_trans.csv', index=False, encoding='utf-8-sig')
print('Data has been saved to output.csv')