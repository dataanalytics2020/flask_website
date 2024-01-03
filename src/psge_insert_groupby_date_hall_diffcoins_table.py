import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import unicodedata
import string
import requests
import mysql.connector
import os

from sshtunnel import SSHTunnelForwarder
import pymysql as db

import sshtunnel
import psycopg2

from dotenv import load_dotenv
load_dotenv(".env")

import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

users = os.getenv('HEROKU_PSGR_USER')    # DBにアクセスするユーザー名(適宜変更)
dbnames = os.getenv('HEROKU_PSGR_DATABASE')   # 接続するデータベース名(適宜変更)
passwords = os.getenv('HEROKU_PSGR_PASSWORD')  # DBにアクセスするユーザーのパスワード(適宜変更)
host = os.getenv('HEROKU_PSGR_HOST')     # DBが稼働しているホスト名(適宜変更)
port = 5432        # DBが稼働しているポート番号(適宜変更)

# PostgreSQLへ接続
conn = psycopg2.connect("user=" + users +" dbname=" + dbnames +" password=" + passwords, host=host, port=port)
#自動コミットモードにする

conn.autocommit = True
conn.autocommit
# カーソルを取得する
cursor = conn.cursor()

# PostgreSQLにデータ登録
def get_driver():
    users = os.getenv('HEROKU_PSGR_USER')    # DBにアクセスするユーザー名(適宜変更)
    dbnames = os.getenv('HEROKU_PSGR_DATABASE')   # 接続するデータベース名(適宜変更)
    passwords = os.getenv('HEROKU_PSGR_PASSWORD')  # DBにアクセスするユーザーのパスワード(適宜変更)
    host = os.getenv('HEROKU_PSGR_HOST')     # DBが稼働しているホスト名(適宜変更)
    port = 5432        # DBが稼働しているポート番号(適宜変更)
    # PostgreSQLへ接続
    conn = psycopg2.connect("user=" + users +" dbname=" + dbnames +" password=" + passwords, host=host, port=port)
    conn.autocommit = True
    conn.autocommit
    # PostgreSQLにデータ登録
    cursor = conn.cursor()
    return cursor
print('get_driver()')

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


def delete_data(cnx,day):
    cursor = cnx.cursor()
    target_days_ago = datetime.date.today() - datetime.timedelta(days=day)
    target_days_ago_str = target_days_ago.strftime('%Y-%m-%d')
    target_days_ago_str
    sql = f"DELETE FROM {os.getenv('WORDPRESS_DB_TABLE')} WHERE 日付 < '{target_days_ago_str} 00:00:00';"
    cursor.execute(sql)
    cnx.commit()

def insert_data_bulk(ichiran_all_tennpo_df,conn):
    insert_sql = f"""INSERT INTO groupby_date_hall_diffcoins (date, prefecture, hall_name, url_hall_name, sum_diffcoins, ave_diffcoins, ave_game, win_rate) values (%s,%s,%s,%s,%s,%s,%s,%s)"""
    print(ichiran_all_tennpo_df.values.tolist())
    cur = conn.cursor()
    cur.executemany(insert_sql, ichiran_all_tennpo_df.values.tolist())
    print("Insert bulk data")
    conn.commit()


prefecture_df = pd.read_csv(r'csv\pref_lat_lon.csv')


cursor = get_driver()
sql = f'''SELECT date,prefecture
            FROM groupby_date_hall_diffcoins '''#AND (取材ランク = 'S' OR 取材ランク = 'A')
print(sql)
cursor.execute(sql)
result = cursor.fetchall()
report_df = pd.DataFrame(result, columns=['イベント日','都道府県'])
report_df = report_df.astype(str)
date_list = list(report_df['イベント日'].unique())
prefecture_list = list(report_df['都道府県'].unique())
report_df_1  = report_df.drop_duplicates(subset=['イベント日','都道府県'],keep='first')
report_df_1["date_prefecture"] = report_df_1["イベント日"] + "_" +report_df_1["都道府県"]
date_prefecture_list = list(report_df_1['date_prefecture'])
print(date_prefecture_list)


line_token = os.getenv('LINE_TOKEN')


prefecture_list = list(prefecture_df['pref_name'])
print(prefecture_list)
for prefecture in prefecture_list[12:13]:
    print('prefecture',prefecture)
    prefecture_url = urllib.parse.quote(prefecture)
    url = f'https://{os.getenv("SCRAPING_DOMAIN")}/%e3%83%9b%e3%83%bc%e3%83%ab%e3%83%87%e3%83%bc%e3%82%bf/{prefecture_url}'
    res = requests.get(url)#class="hall-list-table"
    soup = BeautifulSoup(res.text, 'lxml')
    table_elem = soup.find('div',class_='hall-list-table')
    time.sleep(1)
    tenpo_url_name_list = []
    tenpo_url_name_dict = {}
    for table_row in table_elem.find_all('div',class_='table-row'):
        try:
            hall_name = table_row.find('div',class_='table-data-cell').a.text
            url = table_row.find('div',class_='table-data-cell').a.get("href")
            print(hall_name,url)
            tenpo_url_name = urllib.parse.unquote(url).split('/')[-2].replace('-データ一覧','')
            tenpo_url_name_list.append(tenpo_url_name)
            tenpo_url_name_dict[tenpo_url_name] = hall_name
        except:
            pass
    i = 0
    #break
    ichiran_all_tennpo_df = pd.DataFrame(columns=[],index=[])
    #post_line_text(f'{len(tenpo_url_name_list)}店舗取得数',line_area_token[prefecture])


for prefecture in prefecture_list[12:13]:
    try:
        prefecture_url = urllib.parse.quote(prefecture)
        url = f'https://{os.getenv("SCRAPING_DOMAIN")}/%e3%83%9b%e3%83%bc%e3%83%ab%e3%83%87%e3%83%bc%e3%82%bf/{prefecture_url}'
        res = requests.get(url)#class="hall-list-table"
        soup = BeautifulSoup(res.text, 'lxml')

        table_elem = soup.find('div',class_='hall-list-table')
        time.sleep(1)
        tenpo_url_name_list = []
        tenpo_url_name_dict = {}
        for table_row in table_elem.find_all('div',class_='table-row'):
            try:
                hall_name = table_row.find('div',class_='table-data-cell').a.text
                url = table_row.find('div',class_='table-data-cell').a.get("href")
                #print(hall_name,url)
                tenpo_url_name = urllib.parse.unquote(url).split('/')[-2].replace('-データ一覧','')
                tenpo_url_name_list.append(tenpo_url_name)
                tenpo_url_name_dict[tenpo_url_name] = hall_name
            except:
                pass
        i = 0
        #break
        count = 0
        error_count = 0
        post_line_text(f'{prefecture} {len(tenpo_url_name_list)}店舗取得数',line_token)
        for day_num in reversed(range(1,25)):
            ichiran_all_tennpo_df = pd.DataFrame(columns=[],index=[])
        #tenpo_ichiran_df['ホール名']
            try:
                target_day = datetime.date.today() + datetime.timedelta(days=-day_num)
                target_day_str = target_day.strftime('%Y-%m-%d')
                target_date_prefecture_str = target_day_str + '_' + prefecture
                target_date_prefecture_str
                if target_date_prefecture_str in date_prefecture_list:
                    continue
                # if i> 2:
                #     break
                for i, tenpo_name in enumerate(tenpo_url_name_list):
                    try:
                        print(i,tenpo_name,target_day.strftime('%Y-%m-%d'))
                        url = f'https://{os.getenv("SCRAPING_DOMAIN")}/{target_day.strftime("%Y-%m-%d")}-{tenpo_name}'
                        res = requests.get(url)
                        soup = BeautifulSoup(res.text, 'html.parser')
                        try:
                            hall_name = soup.title.text.split(' ')[1]
                        except:
                            hall_name = soup.title.text
                        table = soup.find(id = "all_data_table")
                        dfs =pd.read_html(str(table))
                        #display(tenpo_df)
                        #time.sleep(1)
                        for df in  dfs:
                            try:
                                if '機種名' in list(df.columns):
                                    df['date'] = target_day.strftime('%Y-%m-%d')
                                    df['hall_name'] = hall_name
                                    #print(tenpo_name)

                                    df['prefecture'] = prefecture
                                    gruopby_diff_coins_df = df.groupby(['hall_name','date']).sum().reset_index()
                                    gruopby_diff_coins_df = gruopby_diff_coins_df
                                    gruopby_diff_coins_df['hall_name'] = hall_name
                                    gruopby_diff_coins_df['prefecture'] = prefecture
                                    gruopby_diff_coins_df['url_hall_name'] = tenpo_name
                                    gruopby_diff_coins_df['勝利台数'] = len(df[df['差枚'] > 0])
                                    gruopby_diff_coins_df['勝利台数'] = gruopby_diff_coins_df['勝利台数'].astype(str)
                                    gruopby_diff_coins_df['総台数'] = df.groupby(['hall_name','date']).size().reset_index()[0]
                                    gruopby_diff_coins_df['平均差枚'] = gruopby_diff_coins_df['差枚'] / gruopby_diff_coins_df['総台数']
                                    gruopby_diff_coins_df['平均G数'] = gruopby_diff_coins_df['G数'] / gruopby_diff_coins_df['総台数']
                                    gruopby_diff_coins_df['総台数'] = gruopby_diff_coins_df['総台数'].astype(str)
                                    gruopby_diff_coins_df['勝率'] = gruopby_diff_coins_df['勝利台数'] + '/' + gruopby_diff_coins_df['総台数']
                                    gruopby_diff_coins_df['勝率'] = gruopby_diff_coins_df['勝率'].map(lambda x : '(' + x + '台)' + str(round(int(x.split('/')[0])/int(x.split('/')[1])*100,1))  + '%')
                                    gruopby_diff_coins_df = gruopby_diff_coins_df.fillna(0)
                                    gruopby_diff_coins_df = gruopby_diff_coins_df.astype({'平均差枚':int,'平均G数':int})
                                    gruopby_diff_coins_df = gruopby_diff_coins_df.sort_values('date',ascending=False)
                                    gruopby_diff_coins_df = gruopby_diff_coins_df.reset_index(drop=True)
                                    gruopby_diff_coins_df = gruopby_diff_coins_df[['date','prefecture','hall_name','url_hall_name','差枚','平均差枚','平均G数','勝率']]
                                    gruopby_diff_coins_df.columns = ['date','prefecture','hall_name','url_hall_name','sum_diffcoins','ave_diffcoins','ave_game','win_rate']
                                    ichiran_all_tennpo_df =  pd.concat([ichiran_all_tennpo_df, gruopby_diff_coins_df])
                                    print('成功',i,tenpo_name)
                                    #display(ichiran_all_tennpo_df)
                                    break
                                else:
                                    print('見つかりませんでした',i,tenpo_name)
                                count += 1
                                time.sleep(1)
                            except Exception as e:
                                print(tenpo_name,e)
                                error_count += 1
                                #time.sleep(1)
                                continue
                        #break
                        
                    except Exception as e:
                        print(tenpo_name,e)
                        continue
                #break
                ichiran_all_tennpo_df = ichiran_all_tennpo_df.fillna('')
                cursor = get_driver()
                post_line_text(f'{prefecture} {target_day_str} insert開始',line_token)
                insert_data_bulk(ichiran_all_tennpo_df ,conn)
                post_line_text(f'{prefecture} {target_day_str}insert終了',line_token)
            except Exception as e:
                print(tenpo_name,e)
                continue
        
        #print(ichiran_all_tennpo_df.iloc[:5])
        # SSH 接続 踏み台接続
        #break

    except Exception as e:
        print(e)
        break
        #post_line_text(f'{prefecture}MYSQL追加処理でエラーが発生しました',line_token)
        #continue


#ichiran_all_tennpo_df.to_csv('csv/tokyo_psgr_insert_df.csv',index=False)


