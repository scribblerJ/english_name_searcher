import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import json


# # 1) 데이터 수집
# # 1-0) 필요 변수 세팅
# options = webdriver.ChromeOptions()     # 셀레니움 옵션 설정
# options.add_experimental_option(        # 오류 코드 출력 방지
#     'excludeSwitches', ['enable-logging'])
# options.add_argument('headless')        # 셀레니움 창 안보이게 하기
# driver = webdriver.Chrome(              # 옵션 적용한 채로 크롬 드라이버 생성
#     options=options)
# df = pd.DataFrame(                      # 빈 데이터 프레임 생성
#     columns= ['name','meaning','gender'])

# for ascii in tqdm(range(97, 123)):      # 아스키코드를 활용해 이니셜 기준 반복
#     initial = chr(ascii)
#     for page in range(1,100):           # 패이지 기준 반복 (페이지 당 10개, 최대 100페이지)
#         # 1-1) 페이지 별 접속
#         url = f'https://babynames.net/all/starts-with/{initial}?page={page}'
#         driver.get(url)
#         rows = [i for i in driver.find_element(By.ID, ':0.nr').find_elements(By.TAG_NAME, 'li') if i.get_attribute('innerHTML') != '']
#         # 1-2) 해당 페이지에서 이름이 더이상 나오지 않으면 다음 이니셜로 넘어가기
#         if len(rows) == 0:
#             break
#         # 1-3) 필요 데이터 수집 및 저장
#         for row in rows:
#             new_data = {
#                 'name': [row.find_element(By.CLASS_NAME, 'result-name').text],
#                 'meaning': [row.find_element(By.CLASS_NAME, 'result-desc').text],
#                 'gender': [row.find_element(By.CLASS_NAME, 'result-gender').get_attribute('class').split(' ')[1]]
#             }
#             new_df = pd.DataFrame(new_data)
#             df = pd.concat([df,new_df])
#     df.to_csv('./new_data.csv',index=False) # 혹시 모르니까 이니셜 하나 끝나면 파일에 저장

# 2) 데이터 전처리
df = pd.read_csv('./new_data.csv')

# # 2-1) 성별(gender) 데이터 one-hot-encoding 방식으로 변경
# df['gender_m'] = df['gender'].apply(        # 남성적 이름인지 여부
#     lambda x: x =='boy' or x=='boygirl')
# df['gender_f'] = df['gender'].apply(        # 여성적 이름인지 여부
#     lambda x: x =='girl' or x=='boygirl')

# 2-2) 한국어 뜻 추가 (with pypapago)
# https://blockdmask.tistory.com/540
# import googletrans
# import numpy as np
# translator = googletrans.Translator()

# def translate_to_korean(english_text):
#     if english_text == ''or english_text == ' ' or english_text == None or type(english_text) == list:
#         return ''
#     else:
#         try:
#             return translator.translate(english_text,src='en', dest='ko').text
#         except:
#             df.to_csv('./new_data.csv',index=False) # 혹시 모르니까 이니셜 하나 끝나면 파일에 저장
#             time.sleep(600)
#             return translator.translate(english_text,src='en', dest='ko').text


# while len(df[df['korean_meaning'].isna()]) != 0:
#     tempt_df= df[df['korean_meaning'].isna()].head(500)
#     for idx, row in tqdm(tempt_df.iterrows(), total=tempt_df.shape[0]):
#         result = ', '.join([translate_to_korean(j) for j in list(np.array([j.split(',') for j in row['meaning'].split('or')]).flatten())])
#         df.loc[idx,'korean_meaning'] = result
#     df.to_csv('./new_data.csv',index=False) # 혹시 모르니까 이니셜 하나 끝나면 파일에 저장
#     time.sleep(60)
        
    


# 2-3) 동명의 유명인 추가
# def search_celebrity(name):
#     # https://api-ninjas.com/api/celebrity
#     api_key = 'QNBvf44GLJYEKTrTqXgwqw==TEZQrdfcI8ujLV2X'
#     api_url = 'https://api.api-ninjas.com/v1/celebrity?name={}'.format(name)
#     response = requests.get(api_url, headers={'X-Api-Key': api_key})
#     if response.status_code == requests.codes.ok:
#         json_obj = json.loads(response.text)
#         return json_obj[0] if len(json_obj) > 1 else json_obj
            
#     else:
#         print("Error:", response.status_code, response.text)

# df['celebrity'] =  df[
#     'name'].apply(lambda x: search_celebrity(x))
# df.to_csv('./new_data.csv',index=False) # 혹시 모르니까 이니셜 하나 끝나면 파일에 저장


print(df.head(10))







# male_names = []
# female_names = []


# for i in range(97, 123):
#     lower_class= chr(i)
#     upper_class= chr(i-32)
#     with open(f'./english_names/male/{lower_class}.txt', 'r') as f:
#         # male_names.append([upper_class+j for j in f.read().strip().split(upper_class)[1:]])
#         male_names.extend([upper_class+j for j in f.read().strip().split(upper_class)[1:]])
#     with open(f'./english_names/female/{lower_class}.txt', 'r') as f:
#         # female_names.append([upper_class+j for j in f.read().strip().split(upper_class)[1:]])
#         female_names.extend([upper_class+j for j in f.read().strip().split(upper_class)[1:]])
# df1 = pd.read_csv('./data.csv')
# df2 =pd.DataFrame({
#         'name':[i for i in male_names], 
#         'impression':['' for i in range(len(male_names))],
#         'meaning':['' for i in range(len(male_names))],
#         'gender':['m' for i in range(len(male_names))]
#     })
# df3 =pd.DataFrame({
#         'name':[i for i in female_names], 
#         'impression':['' for i in range(len(female_names))],
#         'meaning':['' for i in range(len(female_names))],
#         'gender':['f' for i in range(len(female_names))]
#     })
# df = pd.concat([df1,df2,df3], ignore_index=True)
# df.to_csv('./data.csv',index=False)









# http://www.erumy.com/nameclub/EnglishNameSearch.aspx
# http://m.suksuk.co.kr/momboard/eng_name.php?page=1&table=ABA_005

# url ='http://m.suksuk.com/momboard/eng_name.php?page={}&table=ABA_005'
# df = pd.DataFrame(columns=['name', 'impression', 'meaning', 'gender'])
# for page in range(1,181):
#     req = requests.get(url.format(page))
#     html = req.text
#     soup = BeautifulSoup(html, 'html.parser')
#     rows = soup.findAll('tr')[1:]
#     for row in rows:
#         cells = row.findAll('td')
#         df = df.append(
#             {
#                 'name' : cells[0].span.get_text(),
#                 'impression' : cells[1].get_text(),
#                 'meaning' : cells[2].get_text(),
#                 'gender' :    cells[0].span.get('class')
#             }        
#             ,ignore_index=True
#         )
# df.to_csv('./data.csv',index=False)

# df = pd.read_csv('./data.csv')
