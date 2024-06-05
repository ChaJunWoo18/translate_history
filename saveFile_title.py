import pandas as pd
import xml.etree.ElementTree as ET
import translate_module_copy

# XML 파일을 읽어와 ElementTree 객체 생성
tree = ET.parse('JoseonDynastyAnnals/2nd_waa_101.xml')
root = tree.getroot()

data=[]

for level4 in root.findall('.//level4'):
    level4_elem_mainT = level4.find('.//mainTitle')
    if level4_elem_mainT is not None:
        main_title_date = level4_elem_mainT.text.strip()
        main_title_date = translate_module_copy.translate_with_hanjaLibrary(main_title_date)

    level5_elem = level4.find('.//level5')
    if level5_elem is not None:
        main_title = level5_elem.find('.//mainTitle').text.strip()

    data.append({'mainDate': main_title_date, 'mainTitle': main_title})
    
df = pd.DataFrame(data)
df.to_csv('./result/title_trans.csv', index=False, encoding='utf-8-sig')
print('Data has been saved to output.csv')