from selenium import webdriver
import unicodedata
import time
import pandas as pd
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import json
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import mysql
import mysql.connector
import os
import datetime
import psycopg2
from dotenv import load_dotenv
load_dotenv(".env")
print('ライブラリの読み込み完了')
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
    from selenium.webdriver.chrome.service import Service
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
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
#['hokkaido','tohoku','kanto','chubu','kansai','chugoku','sikoku','kyushu']
for area_name in ['hokkaido','tohoku','kanto','chubu','kansai','chugoku','sikoku','kyushu']:
    #try:
    browser = login_scraping_site(area_name)
    elements = browser.find_elements(By.CLASS_NAME,"mgn_serch_list_bottom")
    i = 0
    while True:
        browser.find_element(By.CLASS_NAME,"head_change_main").click()
        browser.implicitly_wait(10)
        if 'プレミアム会員登録' == browser.find_element(By.CLASS_NAME,"menu_child").text:
            browser = login_scraping_site(area_name)
        else:
            pass
        try:
            elements = browser.find_elements(By.CLASS_NAME,"mgn_serch_list_bottom")
            baitai_name = elements[i].text.split(' ')[0]
            baitai_name = baitai_name.replace('パチマガスロマガじゃ…','パチマガスロマガ').replace('パチンコ店長のホール…','パチンコ店長のホール攻略').replace('よっしー社長プロデュ…','よっしー社長プロデュース')

            if  ('県' in baitai_name) or ('府' in baitai_name) or ('東京都' in baitai_name) or ('北海道' in baitai_name):
                print('県がついているためパスを処理しました',baitai_name)
                i += 1
                continue

            print(baitai_name)
            elements[i].click()
            # if 'ホールナビ' in baitai_name:
            #     print(baitai_name)
            #     break
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
                if browser.find_element(By.CLASS_NAME,'navi_1_next').text == '次へ':
                    browser.find_element(By.CLASS_NAME,'navi_1_next').click()
                else:
                    break
            i += 1
            # time.sleep(1)
            #break
            #break
        except Exception as e:
            print('エラー理由',e)
            break
        # if i > 13:
        #break

    browser.quit()

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
# 現在時刻
today = datetime.datetime.now()
print(today)
#[結果] 2021-08-23 07:12:20.806648
# 1日後
today_str:str = today.strftime('%Y-%m-%d')
eight_days_after:str = (today + datetime.timedelta(days=8)).strftime('%Y-%m-%d')
yesterday:str = (today + datetime.timedelta(days=-2)).strftime('%Y-%m-%d')
    #### Create dataframe from resultant table ####
# except Exception as e:
#     post_line_text(f'取材予定エラー\n{e}',os.getenv('LINE_TOKEN'))

users = os.getenv('HEROKU_PSGR_USER')    # DBにアクセスするユーザー名(適宜変更)
dbnames = os.getenv('HEROKU_PSGR_DATABASE')   # 接続するデータベース名(適宜変更)
passwords = os.getenv('HEROKU_PSGR_PASSWORD')  # DBにアクセスするユーザーのパスワード(適宜変更)
host = os.getenv('HEROKU_PSGR_HOST')     # DBが稼働しているホスト名(適宜変更)
port = 5432        # DBが稼働しているポート番号(適宜変更)

# PostgreSQLへ接続
conn = psycopg2.connect("user=" + users +" dbname=" + dbnames +" password=" + passwords, host=host, port=port)

# PostgreSQLにデータ登録
cursor = conn.cursor()
sql = f"""
        SELECT *
        FROM pledge
        """
print(sql)
cursor.execute(sql)
#cols = [col[0] for col in cursor.description]
sql_syuzai_report_all_df = pd.DataFrame(cursor.fetchall(),columns = ['id','syuzai_name','media_name','pledge_text','created_at'])
sql_syuzai_report_all_df
insert_pledge_df = furture_syuzai_list_df_1[['取材名','媒体名']]
insert_pledge_df = insert_pledge_df.drop_duplicates()
#insert_pledge_df = insert_pledge_df[insert_pledge_df['媒体名'] != 'ホールナビ']
insert_pledge_df['pledge_text'] = None
insert_pledge_df = insert_pledge_df.reset_index(drop=True)
insert_pledge_df.rename(columns={'取材名':'syuzai_name','媒体名':'media_name'},inplace=True)
count = 0
concat_pledge_df = pd.DataFrame(index=[], columns=[])
increment_id = max(list(sql_syuzai_report_all_df['id']))
print(increment_id)
text = ''
for i,row in insert_pledge_df.iterrows():
    dicision_df = sql_syuzai_report_all_df[sql_syuzai_report_all_df['syuzai_name'] == row['syuzai_name']]
    #display(dicision_df)
    increment_id += 1
    if len(dicision_df) == 0:
        count += 1
        print('追加',row['syuzai_name'],row['media_name'],None)
        text += f'\n{row["syuzai_name"]}-{row["media_name"]} '
        cursor.execute("INSERT INTO pledge VALUES (%s, %s,%s, %s, %s)", (increment_id ,row['syuzai_name'],row['media_name'],row['pledge_text'],datetime.datetime.now()))
        conn.commit()
    else:
        #print('追加なし')
        pass
text = f'{area_name} {count}件のpostgresへの公約レコードの追加が終了しました。'
post_line_text(text,os.getenv('LINE_TOKEN'))


