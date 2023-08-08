from selenium import webdriver
import time
import pandas as pd
import re
from selenium.webdriver.common.by import By
#from datetime import datetime, date, timedelta
from selenium.webdriver.chrome.options import Options
import requests
import json

from webdriver_manager.chrome import ChromeDriverManager
import mysql
import mysql.connector
import os

import datetime

import psycopg2
import sshtunnel
from sshtunnel import SSHTunnelForwarder


from dotenv import load_dotenv
load_dotenv(".env")


print('ライブラリの読み込み完了')

    
def insert_data_bulk(df,cnx):
    insert_sql = """INSERT INTO schedule (都道府県, イベント日, 曜日, 店舗名, 取材名, 媒体名, 取材ランク,取得時間) values (%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur = cnx.cursor()
    cur.executemany(insert_sql, df.values.tolist())
    print("Insert bulk data")



def removal_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans( '', '',string.punctuation  + '！'+ '　'+ ' '+'・'+'～' + '‐'))
    return text



def post_line_text(message,token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}
    post = requests.post(url ,headers = headers ,params=payload) 

def post_line_text_and_image(message,image_path,token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}
    #imagesフォルダの中のgazo.jpg
    print('image_path',image_path)
    files = {"imageFile":open(image_path,'rb')}
    post = requests.post(url ,headers = headers ,params=payload,files=files) 


def login_scraping_site(area_name):
    options = Options()
    #options.add_argument('--headless')
    options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(ChromeDriverManager(requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE').text).install(),options=options)#ChromeDriverManager().install() 
    browser.implicitly_wait(10)
    url_login = f"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/login_form_mail"
    #admageを開く
    browser.get(url_login)
    browser.implicitly_wait(10)

    # id
    element = browser.find_element(By.NAME,"id")
    element.click()
    element.clear()
    browser.implicitly_wait(10)
    element.send_keys(os.getenv('REPORT_SITE_ID'))

    # pw
    element = browser.find_element(By.NAME,"pass")
    element.click()
    element.clear()
    browser.implicitly_wait(10)
    element.send_keys(os.getenv('REPORT_SITE_PW'))

    browser.implicitly_wait(10)
    element = browser.find_element(By.CLASS_NAME,"box_hole_view_report_input")
    element.click()
    browser.implicitly_wait(10)
    url = f"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/select_area"
    browser.get(url)
    browser.implicitly_wait(10)
    url = f"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/?area={area_name}"
    browser.get(url)
    browser.implicitly_wait(10)
    return browser


furture_syuzai_list_df = pd.DataFrame(index=[], columns=['都道府県','イベント日','店舗名','取材名','媒体名','取材ランク'])
browser = login_scraping_site('kanto')
elements = browser.find_elements(By.CLASS_NAME,"mgn_serch_list_bottom")
i = 0
while True:
    browser.find_element(By.CLASS_NAME,"head_change_main").click()
    browser.implicitly_wait(10)
    if 'プレミアム会員登録' == browser.find_element(By.CLASS_NAME,"menu_child").text:
        browser = login_scraping_site('kanto')
    else:
        pass
    try:
        elements = browser.find_elements(By.CLASS_NAME,"mgn_serch_list_bottom")
        baitai_name = elements[i].text.split(' ')[0]
        baitai_name = baitai_name.replace('パチマガスロマガじゃ…','パチマガスロマガ').replace('パチンコ店長のホール…','パチンコ店長のホール攻略')

        if  ('県' in baitai_name) or ('府' in baitai_name) or ('東京都' in baitai_name) or ('北海道' in baitai_name):
            print('県がついているためパスを処理しました',baitai_name)
            i += 1
            continue

        print(baitai_name)
        elements[i].click()
        # if 'ホールナビ' in baitai_name:
        #     print(baitai_name)
        #     break
        num = 0
        while True:
            for syuzai_tenpo_data in browser.find_elements(By.CLASS_NAME,"osbox"):
                tenpo_name = syuzai_tenpo_data.find_element(By.CLASS_NAME,"oslh2").text.replace('\n', '').replace(' ', '').replace('　', '')
                #print(tenpo_name.text)
                syuzai_date = syuzai_tenpo_data.find_element(By.CLASS_NAME,"oslmd").text
                rank_and_syuzai_name = syuzai_tenpo_data.find_element(By.CLASS_NAME,"list_event_name").text
                syuzai_rank = rank_and_syuzai_name.split('\n')[0]
                syuzai_name = rank_and_syuzai_name.split('\n')[1]
                prefectures = syuzai_tenpo_data.find_elements(By.CLASS_NAME,"oslha")[0].text
                #print(baitai_name,syuzai_date ,syuzai_rank,syuzai_name,prefectures)#prefectures
                record = pd.Series([prefectures,syuzai_date, tenpo_name,syuzai_name,baitai_name,syuzai_rank], index=furture_syuzai_list_df.columns)
                record_df =  pd.DataFrame(record)
                furture_syuzai_list_df = pd.concat([furture_syuzai_list_df,record_df.T])
                #print(record)
                #break
                browser.implicitly_wait(10)
            if num >6:
                break
            elif browser.find_element(By.CLASS_NAME,'navi_1_next').text == '次へ':
                browser.find_element(By.CLASS_NAME,'navi_1_next').click()
                num += 1
                print('num',num)
            else:
                break
        i += 1
        # time.sleep(1)
        #break
        #break
    except Exception as e:
        print('エラー理由',e)
        break
    # if i > 5:
    #     break

pattern = '東京都|北海道|(京都|大阪)府|.{2,3}県'
# 都道府県を抽出する
furture_syuzai_list_df = furture_syuzai_list_df[furture_syuzai_list_df['都道府県'] != '']
# furture_syuzai_list_df['都道府県']=furture_syuzai_list_df['都道府県'].apply(lambda x:re.match(pattern,x).group())
prefectures_list = []
for adress in furture_syuzai_list_df['都道府県']:
    adress = adress.split(']')[-1]
    try:
        #print(re.match(pattern,adress).group())
        prefectures_list.append(re.match(pattern,adress).group())
    except:
        prefectures_list.append('情報なし')
furture_syuzai_list_df['都道府県'] = prefectures_list
furture_syuzai_list_df_1 = furture_syuzai_list_df
furture_syuzai_list_df_1 = pd.concat([furture_syuzai_list_df_1, furture_syuzai_list_df_1['イベント日'].str.split('(', expand=True)], axis=1).drop('イベント日', axis=1)
furture_syuzai_list_df_1.rename(columns={0: 'イベント日', 1: '曜日'}, inplace=True)
furture_syuzai_list_df_1['曜日'] = furture_syuzai_list_df_1['曜日'].map(lambda x:x.replace(')',''))
furture_syuzai_list_df_1['イベント日'] = pd.to_datetime(furture_syuzai_list_df_1['イベント日'])
furture_syuzai_list_df_1 = furture_syuzai_list_df_1 [['都道府県','イベント日','曜日',	'店舗名','取材名','媒体名','取材ランク']]
furture_syuzai_list_df_1

browser.quit()


server = sshtunnel.SSHTunnelForwarder((os.getenv('SSH_USERNAME'), 10022), 
    ssh_username="pachislot777", 
    ssh_private_key_password='akasaka2', 
    ssh_pkey="akasaka2.key", 
    remote_bind_address=("mysql8055.xserver.jp", 3306 )) 
# SSH接続確認


# 現在時刻
today = datetime.datetime.now()
print(today)
#[結果] 2021-08-23 07:12:20.806648
# 1日後
today_str:str = today.strftime('%Y-%m-%d')
eight_days_after:str = (today + datetime.timedelta(days=8)).strftime('%Y-%m-%d')
yesterday:str = (today + datetime.timedelta(days=-2)).strftime('%Y-%m-%d')
#### Create dataframe from resultant table ####

server.start()

print(f"local bind port: {server.local_bind_port}")
# データベース接続
cnx = mysql.connector.connect(
    host="localhost", 
    port=server.local_bind_port, 
    user=os.getenv('WORDPRESS_DB_ID'), 
    password=os.getenv('DB_PASSWORD'), 
    database=os.getenv('WORDPRESS_DB_NAME'), 
    charset='utf8',
    use_pure=True
    )

# 接続確認
print(f"sql connection status: {cnx.is_connected()}")
cursor = cnx.cursor()

prefectures ="("
prefecture_list = ['東京都','千葉県','埼玉県','神奈川県','茨城県','群馬県','栃木県']
for i,text in enumerate(prefecture_list):
    if i == (len(prefecture_list) -1 ):
        prefectures += f"'{text}'"
    else:
        prefectures += f"'{text}',"
prefectures += ')'
print(prefectures)

concat_df = furture_syuzai_list_df_1
concat_df['イベント日'] = concat_df['イベント日'].astype(str)   
concat_df = concat_df[~concat_df.duplicated(keep=False)]
concat_df['取得時間'] = today_str
concat_df['取得時間'] = concat_df['取得時間'].astype(str)   
concat_df

#UPSERTするために現在のデータを削除
sql = f"""
        DELETE
        FROM schedule
        WHERE イベント日 BETWEEN '{today_str}' AND '{eight_days_after}'
        AND  都道府県 in {prefectures}
        """
print(sql)
cursor.execute(sql)
cnx.commit()

insert_data_bulk(concat_df ,cnx)
cnx.commit()
server.stop()
post_line_text(f'{len(concat_df)}件のxサーバーへの関東の取材予定追加おわり',os.getenv('LINE_TOKEN'))
print(f'{len(concat_df)}件の関東の取材予定追加おわり')

## Postgresへのデータ登録

def insert_data_bulk(df,cnx):
    insert_sql = """INSERT INTO schedule (id,都道府県, イベント日, 曜日, 店舗名, 取材名, 媒体名, 取材ランク,取得時間) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur = cnx.cursor()
    cur.executemany(insert_sql, df.values.tolist())
    print("Insert bulk data")

concat_df = furture_syuzai_list_df_1
concat_df['イベント日'] = concat_df['イベント日'].astype(str)   
concat_df = concat_df[~concat_df.duplicated(keep=False)]
concat_df['取得時間'] = today_str
concat_df['取得時間'] = concat_df['取得時間'].astype(str)   

concat_df['id'] = 0
cols = concat_df.columns.tolist()
cols = cols[-1:] + cols[:-1]
concat_df = concat_df[cols] 
concat_df

users = os.getenv('HEROKU_PSGR_USER')    # DBにアクセスするユーザー名(適宜変更)
dbnames = os.getenv('HEROKU_PSGR_DATABASE')   # 接続するデータベース名(適宜変更)
passwords = os.getenv('HEROKU_PSGR_PASSWORD')  # DBにアクセスするユーザーのパスワード(適宜変更)
host = os.getenv('HEROKU_PSGR_HOST')     # DBが稼働しているホスト名(適宜変更)
port = 5432        # DBが稼働しているポート番号(適宜変更)

# PostgreSQLへ接続
conn = psycopg2.connect("user=" + users +" dbname=" + dbnames +" password=" + passwords, host=host, port=port)

# PostgreSQLにデータ登録
cursor = conn.cursor()

#UPSERTするために現在のデータを削除
sql = f"""
        DELETE
        FROM schedule
        WHERE イベント日 BETWEEN '{today_str}' AND '{eight_days_after}'
        AND  都道府県 in {prefectures}
        """
print(sql)
cursor.execute(sql)
conn.commit()

insert_data_bulk(concat_df ,conn)
conn.commit()
post_line_text(f'{len(concat_df)}件のpostgresへの関東の取材予定追加おわり',os.getenv('LINE_TOKEN'))
print(f'{len(concat_df)}件の関東の取材予定追加おわり')
