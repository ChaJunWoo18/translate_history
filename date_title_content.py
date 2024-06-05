import pandas as pd
import xml.etree.ElementTree as ET
from tabulate import tabulate
# XML 파일을 읽어와 ElementTree 객체 생성
tree = ET.parse('JoseonDynastyAnnals/2nd_waa_101.xml')
root = tree.getroot()

data=[]
textContent =[]
# 필요한 부분을 찾아서 텍스트를 출력
for level4 in root.findall('.//level4'):
    level4_elem_mainT = level4.find('.//mainTitle')
    if level4_elem_mainT is not None:
        main_title_date = level4_elem_mainT.text.strip()
    else:
        main_title_date = "No main title available"
    level5_elem = level4.find('.//level5')
    if level5_elem is not None:
        main_title = level5_elem.find('.//mainTitle').text.strip()
        paragraphs = level5_elem.findall('.//paragraph')
        for paragraph in paragraphs:
            text = ''.join(paragraph.itertext())
            if text:
                textContent.append({'text':text})
    else:
        main_title = "No main title available"

    data.append({'mainDate': main_title_date, 'mainTitle': main_title})
    
df = pd.DataFrame(data) #목차?
df2 = pd.DataFrame(textContent) #내용
# 목차와 내용은 index가 같음

#print(tabulate(df, headers="keys", tablefmt="pretty")) #예쁘게 출력
print(df2.head(15))
