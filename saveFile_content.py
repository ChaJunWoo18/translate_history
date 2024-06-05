import pandas as pd
import xml.etree.ElementTree as ET
from tabulate import tabulate
# XML 파일을 읽어와 ElementTree 객체 생성
tree = ET.parse('JoseonDynastyAnnals/2nd_waa_101.xml')
root = tree.getroot()

textContent =[]
# 필요한 부분을 찾아서 텍스트를 출력
for level5 in root.findall('.//level5'):
    paragraphs = level5.findall('.//paragraph')
    for paragraph in paragraphs:
        text = ''.join(paragraph.itertext())
        if text:
            textContent.append({'text': text})

df = pd.DataFrame(textContent) 

df.to_csv('./result/content.csv', index=False, encoding='utf-8-sig')
print('Data has been saved to output.csv')
