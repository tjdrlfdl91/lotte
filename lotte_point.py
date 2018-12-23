# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 19:03:33 2018

@author: SKMOON
"""

'''
LP_MASTER

1. Settings
    1.1. Libraries
    1.2. Data
2. EDA & Preprocessing
    2.1. Purchase Data
    2.2. 
3. Data cleaning
4. Making the first Function
'''

""" 1. Settings """

''' 1.1. Libraries '''

cwd = "D:/Downloads/DigitalTrendAnalyzer" #skmoon (PC)
cwd = "C:/Python/git/LPoint" #skmoon (Laptop)
cwd = "C:/Users/yongsuplee/Desktop" #surbi (Laptop)

import os
os.getcwd()
os.chdir(cwd)

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
pd.set_option('float_format', '{:f}'.format)

import matplotlib.pyplot as plt
import re

import winsound
winsound.Beep(500,500)


''' 1.2. Data '''

df01 = pd.read_csv("01_Product.csv")
df02 = pd.read_csv("02_Search1.csv")
df03 = pd.read_csv("03_Search2.csv")
df04 = pd.read_csv("04_Custom.csv")
df05 = pd.read_csv("05_Session.csv")
df06 = pd.read_csv("06_Master.csv")

df01.head()
df02.head()
df03.head()
df04.head()
df05.head()
df06.head()


df01.dtypes
temp01 = df01[['CLNT_ID','SESS_ID','PD_C']]
temp01.head()

df06.head()
temp06 = df06[['PD_C','PD_NM','CLAC2_NM']]
temp06.head()

temp0106 = pd.merge(temp01, temp06, on = 'PD_C', how = 'left')
temp0106.head()

client0106 = temp0106[['CLNT_ID','SESS_ID','PD_C']].groupby(['CLNT_ID','SESS_ID']).count()
client0106 = client0106.reset_index()
client0106 = client0106.rename(columns={"PD_C": "PURCH_TOT"})

client0106.head()

temp0106 = pd.merge(temp0106, client0106, on = ['CLNT_ID','SESS_ID'], how = 'left')
temp0106.head()


df02.dtypes
df02.head()

search02 = df02[['CLNT_ID','SESS_ID','SEARCH_CNT']].groupby(['CLNT_ID','SESS_ID']).sum()['SEARCH_CNT']
search02 = search02.reset_index()
search02 = search02.rename(columns={"SEARCH_CNT": "SEARCH_TOT"})
search02.head()

df02 = pd.merge(df02, search02, on = ['CLNT_ID','SESS_ID'], how = 'left')
df02.head()


final = pd.merge(df02, temp0106, on = ['CLNT_ID','SESS_ID'], how = 'left')

final['SEARCH_POINT'] = final['SEARCH_CNT'] / final['SEARCH_TOT']
final['PURCH_POINT'] = 1 / final['PURCH_TOT']
final['POINT'] = final['SEARCH_POINT'] * final['PURCH_POINT']

final.head()

keyword = final[['KWD_NM', 'CLAC2_NM', 'POINT']].groupby(['KWD_NM', 'CLAC2_NM']).sum()['POINT']
keyword = keyword.reset_index()
keyword = keyword.sort_values(by = ['KWD_NM', 'POINT'], ascending = False)
keyword3 = keyword.sort_values(by = ['KWD_NM', 'POINT'], ascending = False).drop_duplicates('KWD_NM')
keyword3.sort_values(by = ['KWD_NM'], ascending = True)

keyword.head(100)
keyword.tail(100)

keyword2 = final[['KWD_NM', 'CLAC2_NM', 'SEARCH_POINT']].groupby(['KWD_NM']).sum()['SEARCH_POINT']
keyword2.tail()



del temp01, temp06






""" 2. EDA & Preprocessing """

''' 2.1. Purchase Data '''

df01.loc[df01['CLNT_ID'].isnull()==True]
df01.loc[df01['SESS_ID'].isnull()==True]
df01.loc[df01['HITS_SEQ'].isnull()==True]
df01.loc[df01['PD_C'].isnull()==True]
df01.loc[df01['PD_ADD_NM'].isnull()==True]







''' 2.2 Macro Search Data '''

df03.dtypes
df03['SESS_DT'] = df03['SESS_DT'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))



# 검색량 object -> numeric
df03['SEARCH_CNT'] = df03['SEARCH_CNT'].map(lambda row: str(row).replace(',', '')) #천 단위 comma 제거
df03['SEARCH_CNT'] = df03['SEARCH_CNT'].convert_objects(convert_numeric=True)
df03['KWD_NM'].nunique()

# 일자 별 검색량 변화
df03.sort_values(by = ['SEARCH_CNT'], ascending=False).head(20) #전체 검색량 순위
df03.loc[(df03['SEARCH_CNT'] >= 100) & (df03['SEARCH_CNT'] < 150.0)].head(20) #검색량 100개 이상 150개 미만인 검색어
df03.loc[df03['KWD_NM'] == '뉴발란스운동화'].sort_values(by = ['SESS_DT']) #일자별 '뉴발란스 운동화' 검색량 추이

date_raw = df03.loc[df03['KWD_NM'] == '뉴발란스운동화'].sort_values(by = ['SESS_DT'])['SESS_DT']
date_modified = date_raw.apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
count_newbal = df03.loc[df03['KWD_NM'] == '뉴발란스운동화'].sort_values(by = ['SESS_DT'])['SEARCH_CNT']
count_adidas = df03.loc[df03['KWD_NM'] == '아디다스운동화'].sort_values(by = ['SESS_DT'])['SEARCH_CNT']
count_nike = df03.loc[df03['KWD_NM'] == '나이키운동화'].sort_values(by = ['SESS_DT'])['SEARCH_CNT']

plt.plot(date_modified, count_newbal, color = 'gray')
plt.plot(date_modified, count_adidas, color = 'black')
plt.plot(date_modified, count_nike, color = 'orange')
plt.xlabel('Date')
plt.ylabel('Search Counts')
plt.title('Shoes Search Counts')
plt.legend(['NewBal', 'Adidas', 'Nike'])
plt.show() #일자별 운동화 검색량 비교 시각화

# 특정 키워드를 포함한 검색어의 추이도 살펴볼 수 있습니다
search_word = df03.loc[df03['KWD_NM'].str.contains('미세먼지')] #미세먼지 키워드를 포함한 검색어의 검색량 추이
search_word = search_word.groupby('SESS_DT').sum() #일자별로 묶음
len(search_word) #183일 중 158일만 미세먼지에 대해 검색함

search_word = search_word.reset_index()

date = date_raw.reset_index()
date.drop('index', axis = 1, inplace = True) #전체 분석기간

search = pd.merge(date, search_word, on = 'SESS_DT', how = 'outer')
search.fillna(0, inplace = True) #검색량이 없는 날에는 0으로 채움

search['SESS_DT'] = search['SESS_DT'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

plt.plot(search['SESS_DT'], search['SEARCH_CNT'])
plt.xlabel('Date')
plt.ylabel('Search Counts')
plt.title('Fine Dust Search Counts')
plt.legend(['Fine Dust'])
plt.show() #일자별 미세먼지 키워드를 포함한 검색어의 검색량 시각화



# 제품, 대분류, 중분류, 소분류 별 매출액 규모
sales = df01.drop(['PD_ADD_NM', 'PD_BRA_NM'], axis = 1)
sales['REV'] = sales['PD_BUY_AM'] * sales['PD_BUY_CT'] #매출액 계산

sales_by_product = sales.groupby('PD_C').sum()
sales_by_class1 = sales.groupby('CLAC1_NM').sum()
sales_by_class2 = sales.groupby('CLAC2_NM').sum()
sales_by_class3 = sales.groupby('CLAC3_NM').sum()

sales_by_product = sales_by_product.reset_index()
sales_by_product = pd.merge(sales_by_product, df06, on = 'PD_C', how = 'inner')
sales_by_product.sort_values(by = ['REV'], ascending = False).head(20)

sales_by_class1 = sales_by_class1.reset_index()
sales_by_class1.sort_values(by = ['REV'], ascending = False).head(20)

sales_by_class2 = sales_by_class2.reset_index()
sales_by_class2.sort_values(by = ['REV'], ascending = False).head(20)

sales_by_class3 = sales_by_class3.reset_index()
sales_by_class3.sort_values(by = ['REV'], ascending = False).head(20)



### 고객 및 세션 단위 데이터를 합쳐봅시다
df01.head()
df01.dtypes

# object로 돼있는 숫자는 건 int로 바꿔줍니다
df01['PD_BUY_CT'] = df01['PD_BUY_CT'].map(lambda row: str(row).replace(',', ''))
df01['PD_BUY_AM'] = df01['PD_BUY_AM'].map(lambda row: str(row).replace(',', '')) #천 단위 comma 제거
df01['PD_BUY_CT'] = df01['PD_BUY_CT'].convert_objects(convert_numeric=True)
df01['PD_BUY_AM'] = df01['PD_BUY_AM'].convert_objects(convert_numeric=True) #단가 및 구매 수량 숫자로 변횐

### 브랜드 명 수정 중 개 빡침 ㄹㅇ루
df01['PD_BRA_NM'] = df01['PD_BRA_NM'].map(lambda row: row.replace('[', ''))
df01['PD_BRA_NM'] = df01['PD_BRA_NM'].map(lambda row: row.replace(']', '')) #브랜드 이름에 대괄호 삭제

brand_list = df01['PD_BRA_NM'].tolist()
brand_list = list(set(brand_list))

weird = [i for i in brand_list if any(s in i for s in "(")]

for i in weird[:]:
    b = re.sub(r'\(.*?\)', '', i)
    weird.append(b)
    weird.remove(str(i))



# 추가 정보는 cleaning이 불가능할 정도로 지저분해서 우선 빼둡시다
temp01 = df01.drop(['PD_ADD_NM'], axis = 1)
temp01.head()

### 검색어와 구매 데이터를 붙여봅시다
### 구매건수 X 검색건수를 하면 데이터가 쓸 데 없이 커지게 되므로 세션 내 검색어는 한 row로 만들어 줍시다
df02['KWD_CNT'] = df02.KWD_NM.str.cat(df02.SEARCH_CNT.astype(str), sep='/') #검색어/검색횟수 형태로 변환
df02.head()

temp02 = df02.drop(['KWD_NM', 'SEARCH_CNT'], axis = 1)
temp02.head()

temp02a = temp02.groupby(['CLNT_ID', 'SESS_ID'])['KWD_CNT'].apply(lambda x: "{%s}" % ', '.join(x)) #세션마다의 검색어를 묶어주기
temp02a = temp02a.reset_index()
temp02a.head()

temp02b = df02[['CLNT_ID','SESS_ID','SEARCH_CNT']].groupby(['CLNT_ID', 'SESS_ID']).sum()
temp02b = temp02b.reset_index()
temp02b.head()

df05['TOT_SESS_HR_V'] = df05['TOT_SESS_HR_V'].map(lambda row: str(row).replace(',', '')) #천 단위 comma 제거
df05['TOT_SESS_HR_V'] = df05['TOT_SESS_HR_V'].convert_objects(convert_numeric=True)

purchase = pd.merge(temp01, pd.merge(temp02a, temp02b, on = ['CLNT_ID', 'SESS_ID'], how = 'left'), on = ['CLNT_ID', 'SESS_ID'], how = 'left') #구매-검색 결합

purchase = pd.merge(purchase, df04, on = ['CLNT_ID'], how = 'left') #고객 인적사항 결합
purchase = pd.merge(purchase, df05, on = ['CLNT_ID', 'SESS_ID'], how = 'left') #세션 정보 결합
purchase = pd.merge(purchase, df06, on = ['PD_C'], how = 'left') #상품 정보 결합
winsound.Beep(500,500)

del df01, df02, df04, df05, df06
del temp01, temp02, temp02a, temp02b

purchase.to_csv('purchase.csv')

purchase = pd.read_csv("purchase.csv", delimiter = ',' , encoding = 'ISO-8859-1')
purchase.dtypes



### 고객 단위 파생변수를 만들어 봅시다
# 구매 건당 소비액 & 고객 당 구매 건수
purchase['REV'] = purchase['PD_BUY_AM'] * purchase['PD_BUY_CT']
clnt_count = purchase[['CLNT_ID','SESS_ID']].groupby(['CLNT_ID']).count()[['SESS_ID']]
clnt_count = clnt_count.reset_index()
clnt_count = clnt_count.rename(columns={"SESS_ID": "CLNT_N_PURCHASE"})

# 고객 당 페이지뷰, 체류시간, 소비액 합계
clnt_sum = purchase[['CLNT_ID','TOT_PAG_VIEW_CT','TOT_SESS_HR_V','REV']].groupby(['CLNT_ID']).sum()[['TOT_PAG_VIEW_CT','TOT_SESS_HR_V', 'REV']]
clnt_sum = clnt_sum.reset_index()
clnt_sum = clnt_sum.rename(columns={"REV": "CLNT_REV_TOTAL", "TOT_PAG_VIEW_CT": "CLNT_PAG_VIEW_TOTAL", "TOT_SESS_HR_V":"CLNT_SESS_HR_TOTAL"})

# 고객 당 페이지뷰, 체류시간, 소비액 평균
clnt_mean = purchase.groupby(['CLNT_ID']).mean()[['TOT_PAG_VIEW_CT','TOT_SESS_HR_V', 'REV']]
clnt_mean = clnt_mean.reset_index()
clnt_mean = clnt_mean.rename(columns={"REV": "CLNT_REV_AVG", "TOT_PAG_VIEW_CT": "CLNT_PAG_VIEW_AVG", "TOT_SESS_HR_V":"CLNT_SESS_HR_AVG"})

# 고객 당 세션 수, 구매 제품 종류, 브랜드 종류, 접속일 수, 사용 기기 종류, 접속지역 수
clnt_unique = purchase[['CLNT_ID','SESS_ID','PD_C','PD_BRA_NM','SESS_DT','DVC_CTG_NM','CITY_NM']].groupby(['CLNT_ID']).nunique()[['SESS_ID','PD_C','PD_BRA_NM','SESS_DT','DVC_CTG_NM','CITY_NM']]
clnt_unique = clnt_unique.reset_index()
clnt_unique = clnt_unique.rename(columns={"SESS_ID":"N_SESS","PD_C": "N_PRODUCT","PD_BRA_NM":"N_BRAND","SESS_DT": "N_LOGIN_DAY", "DVC_CTG_NM": "N_DEVICE", "CITY_NM":"N_CITY"})

clnt = pd.merge(clnt_count, pd.merge(clnt_sum, pd.merge(clnt_mean, clnt_unique, on = ['CLNT_ID'], how = 'left'), on = ['CLNT_ID'], how = 'left'), on = ['CLNT_ID'], how = 'left')
purchase = pd.merge(purchase, clnt, on = ['CLNT_ID'], how = 'left')

del clnt_count, clnt_sum, clnt_mean, clnt_unique, clnt

# 최초 등장일 & 활동 기간
purchase["SESS_DT"] = purchase["SESS_DT"].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d')) #날짜 형식으로 변환
base_date = pd.to_datetime('2018-10-01')
first_date = purchase[["CLNT_ID", "SESS_DT"]].groupby(["CLNT_ID"]).min() #최초 등장 일자
first_date = first_date.reset_index()
first_date = first_date.rename(columns={"SESS_DT": "FIRST_PURCHASE"})
first_date["ACTIVE_DAYS"] = first_date["FIRST_PURCHASE"].apply(lambda x: pd.Timedelta(base_date - x).days) #기준 일자 - 최초 등장 일자로 활동기간 계산

purchase = pd.merge(purchase, first_date, on = ['CLNT_ID'], how = 'left')

del first_date

# 평균 활동 주기 (활동 기간 / 접속일 수)
purchase["PURCHASE_CYCLE"] = purchase["ACTIVE_DAYS"] / purchase["N_LOGIN_DAY"]



### 세션 단위 파생변수를 만들어 봅시다
# 세션 당 구매 건수 (working)
sess_count = purchase[['CLNT_ID','SESS_ID','PD_C','KWD_CNT']] .groupby(['CLNT_ID','SESS_ID']).count()[['PD_C','KWD_CNT']] 
sess_count = sess_count.reset_index()
sess_count = sess_count.rename(columns={"PD_C": "SESS_N_PURCHASE","KWD_CNT": "SEARCHED_SESS"})
sess_count['SEARCHED_SESS'][sess_count['SEARCHED_SESS'] != 0] = 1 #0을 제외한 수를 1로 변환

# 세션 당 소비액 총합
sess_sum = purchase.groupby(["CLNT_ID", "SESS_ID"]).sum()["REV"]
sess_sum = sess_sum.reset_index()
sess_sum = sess_sum.rename(columns={"REV": "REV_TOTAL"})

# 평균 낼 변수들
sess_mean = purchase.groupby(['CLNT_ID','SESS_ID']).mean()
sess_mean = sess_mean.reset_index()

purchase = pd.merge(purchase, sess_count, on = ['CLNT_ID', 'SESS_ID'], how = 'left')
purchase = pd.merge(purchase, sess_sum, on = ['CLNT_ID', 'SESS_ID'], how = 'left')

del sess_count, sess_sum




### 고객군 분석
client = purchase[['CLNT_ID','CLNT_GENDER','CLNT_AGE','CLNT_N_PURCHASE','CLNT_PAG_VIEW_TOTAL','CLNT_SESS_HR_TOTAL','CLNT_REV_TOTAL','CLNT_PAG_VIEW_AVG','CLNT_SESS_HR_AVG','CLNT_REV_AVG','N_SESS','N_PRODUCT','N_BRAND','N_LOGIN_DAY','N_DEVICE','N_CITY','ACTIVE_DAYS','FIRST_PURCHASE','PURCHASE_CYCLE']]

client['CLNT_GENDER'][client['CLNT_GENDER'] == 'M'] = 1
client['CLNT_GENDER'][client['CLNT_GENDER'] == 'F'] = 0 #남자는 1, 여자는 0

client = client.drop_duplicates()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.xlabel('N_SESS')
plt.ylabel('CLNT_REV_AVG')
ax.scatter(client['N_SESS'],client['CLNT_REV_AVG'], c=client['CLNT_GENDER'] )
plt.show()

client['CLNT_REV_TOTAL'].mean()
client_rich = client.loc[client['CLNT_REV_TOTAL'] > 10000000]
client_normal = client.loc[(client['CLNT_REV_TOTAL'] < 10000000) & (client['CLNT_REV_TOTAL'] > 300000)]
client_poor = client.loc[client['CLNT_REV_TOTAL'] < 300000]

client['CLNT_REV_TOTAL'].sort_values()

pd.options.display.max_columns = None

client.to_csv('client.csv')


### 이하 낙서장

only_purchase = temp01[~temp01.isin(temp02a)].dropna()
only_purchase.head()

df02.sort_values(by = ['SEARCH_CNT'])

df01.sort_values(by=['HITS_SEQ']).head()

temp01 = df01.loc[df01.CLNT_ID == [1738139]].sort_values(by=['SESS_ID', 'HITS_SEQ'])

df02.loc[df02.SESS_ID == [7112876]]
df02.loc[df02.CLNT_ID == [1738139]].sort_values(by=['SESS_ID']) 

df04.loc[df04.CLNT_ID == [1738139]] ## 40대 남성

temp05 = df05.loc[df05.CLNT_ID == [1738139]].sort_values(by=['SESS_SEQ'])

pd.merge(temp01, temp05, on = 'SESS_ID', how = 'inner').sort_values(by=['SESS_SEQ', 'HITS_SEQ'])



df03.loc[df03['SEARCH_CNT'] > 100].head()