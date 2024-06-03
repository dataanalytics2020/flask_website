
import time
import pandas as pd
import re

import requests
import json
import mysql
import mysql.connector
import os

import datetime
import unicodedata

from github import Github
# Authentication is defined via github.Auth
from github import Auth
import os
import json
import requests
import traceback
from bs4 import BeautifulSoup
import urllib.parse
import traceback
import psycopg2
import psycopg2.extras as extras
from dotenv import load_dotenv
load_dotenv(".env")

def scraping_hall_data_to_record_df(url) -> pd.DataFrame:
    r = requests.get(url)
    # print(r.content)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.content.decode("utf-8", "ignore"), "html.parser") #追加
    hall_name = soup.find(class_='box_hole_view_hole_name').text
    table_elem = soup.find(class_='hole_base')
    hall_df = pd.read_html(str(table_elem))[0]
    dmm_url = pworld_url = googlemap_url = twitter_url = line_url = google_serch_url = None
    for table_link in table_elem.find_all('a'):
        print(table_link.get('href'))
        href = table_link.get('href')
        print(href)
        if 'dmm' in href:
            dmm_url = href
            print(dmm_url)
        elif 'p-world' in href:
            pworld_url = href
            print(pworld_url)
        elif 'maps' in href:
            googlemap_url = href
            print(googlemap_url)
        elif 'twitter' in href:
            twitter_url = href
            print(twitter_url)
        elif 'lin' in href:
            line_url = href
            print(line_url)
        elif 'google.co.jp/search' in href:
            google_serch_url = href
            print(google_serch_url)
        else:
            print('error', href)
            pass
    
    # テーブル内の各データ取得
    
    #最寄り駅
    try:
        nearest_station = hall_df[hall_df[0] == '最寄駅'].iloc[0, 1]
        print(nearest_station)
    except Exception as e:
        print(e)
        nearest_station = None
    #住所
    try:
        address = hall_df[hall_df[0] == '住所'].iloc[0, 1]
        print(address)
    except Exception as e:
        print(e)
        address = None
    #都道府県
    try:
        #都道府県のみ
        matches = re.match('東京都|北海道|(?:京都|大阪)府|.{2,3}県' , address)
        print(matches.group()) 
        prefecture_name = matches.group()
        print(prefecture_name)
    except Exception as e:
        print(e)
        prefecture_name = None
    #電話番号
    try:
        tel_number = hall_df[hall_df[0] == '電話'].iloc[0, 1]
    except Exception as e:
        print(e)
        tel_number  = None
    # パチンコ台数
    try:
        pachinko_num = hall_df[hall_df[0] == 'パチンコ台数'].iloc[0, 1]
    except Exception as e:
        print(e)
        pachinko_num = None

    # スロット台数
    try:
        slot_num = hall_df[hall_df[0] == 'スロット台数'].iloc[0, 1]
    except Exception as e:
        print(e)
        slot_num = None
    # 入場方法
    try:
        entrance_method = hall_df[hall_df[0] == '入場方法'].iloc[0, 1]
    except Exception as e:
        print(e)
        entrance_method = None
    # 台移動
    try:
        machine_move = hall_df[hall_df[0] == '台移動'].iloc[0, 1]
    except Exception as e:
        print(e)
        machine_move = None
    # 出玉共有
    try:
        dedama_share = hall_df[hall_df[0] == '出玉共有'].iloc[0, 1]
    except Exception as e:
        print(e)
        dedama_share = None
    # 駐車場
    try:
        car_parking = hall_df[hall_df[0] == '駐車場'].iloc[0, 1]
    except Exception as e:
        print(e)
        car_parking = None
    # 駐輪場
    try:
        bicycle_parking = hall_df[hall_df[0] == '駐輪場'].iloc[0, 1]
    except Exception as e:
        print(e)
        bicycle_parking = None
    # 携帯充電
    try:
        mobile_charging = hall_df[hall_df[0] == '携帯充電'].iloc[0, 1]
    except Exception as e:
        print(e)
        mobile_charging = None

    # 出玉情報
    try:
        dedama_info = hall_df[hall_df[0] == '出玉情報'].iloc[0, 1]
    except Exception as e:
        print(e)
        dedama_info = None
    # 行き方補足
    try:
        access_info = hall_df[hall_df[0] == '行き方補足'].iloc[0, 1]
    except Exception as e:
        print(e)
        access_info = None

    columns = ['hall_name','prefecture_name','hall_url','dmm_url',\
            'pworld_url','line_url','twitter_url',\
            'nearest_station','address','pachinko_num','slot_num',\
            'entrance_method','machine_move','dedama_share',
            'car_parking','mobile_charging',\
            'dedama_info','access_info']
    record_df = pd.DataFrame([[hall_name,prefecture_name,url,dmm_url,\
                        pworld_url,line_url,twitter_url,\
                        nearest_station,address,pachinko_num,slot_num,\
                        entrance_method,machine_move,dedama_share,\
                        car_parking,mobile_charging,\
                        dedama_info,access_info]], columns=columns)
    record_df = record_df
    return address , record_df

# PostgreSQLにデータ登録
def heroku_psgr_get_cursor():
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
    return conn

def rds_mysql_get_cursor():
    # MySQLに接続
    conn = mysql.connector.connect(
        host=os.environ.get("AWS_SLOMAP_RDS_HOST"),
        user=os.environ.get("AWS_SLOMAP_RDS_USER"),
        password=os.environ.get("AWS_SLOMAP_RDS_PASSWORD"),
        database=os.environ.get("AWS_SLOMAP_RDS_DATABASE"),
    )
    return conn
# カーソルを取得
rds_mysql_conn = rds_mysql_get_cursor()
rds_mysql_cursor = rds_mysql_conn.cursor()

heroku_psgr_conn = heroku_psgr_get_cursor()
heroku_psgr_cursor = heroku_psgr_conn.cursor()

def post_line_text(message,token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}
    post = requests.post(url ,headers = headers ,params=payload) 
    
    
def insert_data_bulk(table_name,df,conn):
    sql = str(tuple(df.columns)).replace("'","") + ' values (' +  (len(df.columns) * '%s,').rstrip(',') + ')'
    print(sql)
    insert_sql = f"""INSERT INTO {table_name} {sql} """
    print(insert_sql)
    #print(df.values.tolist())
    cur = conn.cursor()
    cur.executemany(insert_sql, df.values.tolist())
    conn.commit()
    cur.close()
    print("success Insert bulk data")
    
def insert_data_bulk_psgr(table_name,df,conn):
    sql = str(tuple(df.columns)).replace("'","") + 'values %s'
    print(sql)
    tuples = [tuple(x) for x in df.to_numpy()]
    print(tuples)
    insert_sql = f"""INSERT INTO {table_name} {sql} """
    print(insert_sql)
    #print(df.values.tolist())
    cur = conn.cursor()
    insert_sql = f"""INSERT INTO {table_name} {sql} """
    print(insert_sql)
    extras.execute_values(cur,insert_sql , tuples)
    conn.commit()
    cur.close()
    print("success Insert bulk data")
    


# def delete_data(conn,day):
#     rds_mysql_cursor = conn.cursor()
#     target_days_ago = datetime.date.today() - datetime.timedelta(days=day)
#     target_days_ago_str = target_days_ago.strftime('%Y-%m-%d')
#     target_days_ago_str
#     sql = f"DELETE FROM {os.getenv('WORDPRESS_DB_TABLE')} WHERE 日付 < '{target_days_ago_str} 00:00:00';"
#     rds_mysql_cursor.execute(sql)
#     conn.commit()
    
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
    
prefecture_df = pd.read_csv(r'csv\pref_lat_lon.csv')
prefecture_list = list(prefecture_df['pref_name'])
prefecture_list[10:14]
line_token = os.getenv('WORK_LINE_TOKEN')

heroku_psgr_conn = heroku_psgr_get_cursor()
heroku_psgr_cursor = heroku_psgr_conn.cursor()
heroku_psgr_cursor.execute('''SELECT *
               FROM halldata ''')
cols = [col[0] for col in heroku_psgr_cursor.description]
halldata_df = pd.DataFrame(heroku_psgr_cursor.fetchall(),columns=cols)
halldata_df

heroku_psgr_conn = heroku_psgr_get_cursor()
heroku_psgr_cursor = heroku_psgr_conn.cursor()
sql = f'''SELECT date,prefecture
            FROM groupby_date_hall_diffcoins '''
print(sql)
heroku_psgr_cursor.execute(sql)
result = heroku_psgr_cursor.fetchall()
report_df = pd.DataFrame(result, columns=['イベント日','都道府県'])
report_df = report_df.astype(str)
date_list = list(report_df['イベント日'].unique())
prefecture_list = list(report_df['都道府県'].unique())
report_df_1  = report_df.drop_duplicates(subset=['イベント日','都道府県'],keep='first')
report_df_1["date_prefecture"] = report_df_1["イベント日"] + "_" +report_df_1["都道府県"]
date_prefecture_list = list(report_df_1['date_prefecture'])
print(date_prefecture_list)


#print(prefecture_list)

today = datetime.date.today()
error_hall_count = 0
now = datetime.datetime.now()
post_line_text(f'308行目 {now}rdsインサート用スクレイピング開始',line_token)
issue_comment_text = '座標系の問題で取得できなかった店舗一覧\n'

prefecture_df = pd.read_csv(r'csv\pref_lat_lon.csv')
prefecture_list = list(prefecture_df['pref_name'])
for prefecture in prefecture_list[10:14]:#reversed([12:13]
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
        
        for day_num in reversed(range(1,2)):
        #tenpo_ichiran_df['ホール名']
            try:
                target_day = today  + datetime.timedelta(days=-day_num)
                target_day_str = target_day.strftime('%Y-%m-%d')
                target_date_prefecture_str = target_day_str + '_' + prefecture
                target_date_prefecture_str
                if target_date_prefecture_str in date_prefecture_list:
                    continue
                # if i> 2:
                #     break
                print(i,prefecture,target_day.strftime('%Y-%m-%d'),"スクレイピング開始")
                str_target_day = target_day.strftime('%Y-%m-%d')
                post_line_text(f"352行目 {now} \n{i} \n{prefecture} \n{str_target_day} \nrdsインサート用スクレイピング開始",line_token)
                insert_count = 0
                for i, tenpo_name in enumerate(tenpo_url_name_list):#[75:90]
                    try:
                        ichiran_all_tennpo_df = pd.DataFrame(columns=[],index=[])
                        concat_df = pd.DataFrame(columns=[],index=[])
                        # if i > 5:
                        #     break
                        print(i,tenpo_name,target_day.strftime('%Y-%m-%d'))
                        url = f'https://{os.getenv("SCRAPING_DOMAIN")}/{target_day.strftime("%Y-%m-%d")}-{tenpo_name}'
                        res = requests.get(url)
                        soup = BeautifulSoup(res.text, 'html.parser')
                        try:
                            hall_name = soup.title.text.split(' ')[1].replace('周年','').replace("'",'').replace('年一','').rstrip(' ')
                        except:
                            hall_name = soup.title.text.replace('周年','').replace("'",'').replace('年一','').rstrip(' ')
                        table = soup.find(id = "all_data_table")
                        try:
                            dfs =pd.read_html(str(table))
                        except:
                            print('テーブルがないのでコンティニュー',tenpo_name)
                            continue

                        #display(tenpo_df)
                        #time.sleep(1)
                        for df in  dfs:
                            if '機種名' in list(df.columns):
                                break
                    
                        df['date'] = target_day.strftime('%Y-%m-%d')
                        hall_name_text = ''
                        for t in soup.h1.text.split(' ')[1:-1]:
                            hall_name_text += t 

                        df['hall_name'] = hall_name_text.replace('周年','').replace("'",'').replace('年一','').rstrip(' ')
                        #print(tenpo_name)

                        df['prefecture'] = prefecture
                        extract_halldata_row = halldata_df[halldata_df['anaslo_name'] == hall_name_text]
                        if len(extract_halldata_row) == 0:
                            extract_halldata_row = halldata_df[halldata_df['anaslo_name'] == hall_name]
                        if len(extract_halldata_row) == 0:
                            pass
                        try:
                            hall_id = extract_halldata_row['id'].values[0]
                            hallnavi_name = extract_halldata_row['hall_name'].values[0]
                        except:
                            try:
                                try:
                                    extract_halldata_row = halldata_df[halldata_df['hall_name'] == hall_name_text]
                                    hall_id = extract_halldata_row['id'].values[-1]
                                    hallnavi_name = extract_halldata_row['hall_name'].values[-1]
                                    update_sql = f"""UPDATE halldata SET anaslo_name = '{hall_name_text}' WHERE hall_name = '{hall_name_text}';"""
                                    heroku_psgr_conn = heroku_psgr_get_cursor()
                                    heroku_psgr_cursor = heroku_psgr_conn.cursor()      
                                    heroku_psgr_cursor.execute(update_sql)
                                    heroku_psgr_conn.commit()
                                    issue_comment_text += f'hall_nameカラムと一致 update_sql 実行済み{prefecture} {hallnavi_name} {target_day.strftime("%Y-%m-%d")} \n'
                                    print('hall_nameカラムと一致 update_sql 実行済み',i,{hallnavi_name})
                                except:
                                    extract_halldata_row = halldata_df[halldata_df['hall_name'] == hall_name_text+'店']
                                    hall_id = extract_halldata_row['id'].values[-1]
                                    hallnavi_name = extract_halldata_row['hall_name'].values[-1]
                                    update_sql = f"""UPDATE halldata SET anaslo_name = '{hall_name_text}店' WHERE hall_name = '{hall_name_text}店';"""
                                    heroku_psgr_conn = heroku_psgr_get_cursor()
                                    heroku_psgr_cursor = heroku_psgr_conn.cursor()  
                                    heroku_psgr_cursor.execute(update_sql)
                                    heroku_psgr_conn.commit()
                                    issue_comment_text += f'hall_name+店でカラムと一致 update_sql 実行済み{prefecture} {hallnavi_name} {target_day.strftime("%Y-%m-%d")} \n'
                                    print('hall_nameカラムと一致 update_sql 実行済み',i,{hallnavi_name})
                                #issue_comment_text += f'hall_nameカラムと一致 {prefecture} {tenpo_name} {target_day.strftime("%Y-%m-%d")} \n'

                            except Exception as e:
                                error_text = traceback.format_exc()
                                post_line_text(f' 425行目  {hall_name} {e} {now} {prefecture} {hall_name_text} {target_day.strftime("%Y-%m-%d")} {error_text}',line_token)
                                print('何かしらのエラー',e,i,tenpo_name)
                                print(f'{prefecture} {tenpo_name} {target_day.strftime("%Y-%m-%d")} \n')
                                issue_comment_text += f'変換テーブルに合致なし {e} {prefecture} {tenpo_name} {target_day.strftime("%Y-%m-%d")} \n'
                                hall_id = 0
                                hallnavi_name = ''
                                error_hall_count += 1
                                try:
                                    serch_url = f"https://www.google.com/search?q=ホールナビ  {hall_name_text} 店舗情報&hl=ja&source=hp/"
                                    print(serch_url)
                                    #print('データ取得中...30秒ほど時間がかかります。')
                                    res = requests.get(serch_url)
                                    soup  = BeautifulSoup(res.text, 'html.parser')
                                    #'MjjYud'クラスの中のテキストを取得
                                    # Googleのページ解析を行う
                                    url_text = soup.select('div.kCrYT > a')[0].get('href')
                                    from urllib.parse import unquote
                                    url_text = unquote(url_text).split('&')[0].replace('/url?q=', '')
                                    print(url_text)

                                    tenpo_adress , scraping_hall_data_df = scraping_hall_data_to_record_df(url_text)
                                    print(tenpo_adress)
                                    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
                                    s_quote = urllib.parse.quote(tenpo_adress)
                                    response = requests.get(makeUrl + s_quote)
                                    url = makeUrl + s_quote
                                    res = requests.get(url)
                                    json_str = res.text.split('">')[-1].split('</pre>')[0]
                                    json_data = json.dumps(json_str)
                                    json_data = json.loads(json_data)
                                    json_data_to_python_value = json.loads(json_data)
                                    print(json_data_to_python_value)
                                    print(json_data_to_python_value[0]["geometry"]["coordinates"])# [経度,緯度]
                                    longtitude = json_data_to_python_value[0]["geometry"]["coordinates"][0]
                                    latitude = json_data_to_python_value[0]["geometry"]["coordinates"][1]
                                    scraping_hall_data_df['anaslo_name'] = hall_name_text
                                    scraping_hall_data_df['longitude'] = longtitude
                                    scraping_hall_data_df['latitude'] = latitude
                                    scraping_hall_data_df['bicycle_parking'] = ''
                                    heroku_psgr_conn = heroku_psgr_get_cursor()
                                    heroku_psgr_cursor = heroku_psgr_conn.cursor()
                                    table_name = 'halldata'
                                    insert_data_bulk_psgr(table_name,scraping_hall_data_df,heroku_psgr_conn)
                                    post_line_text(f'466行目 {now} {prefecture} {hall_name_text} {target_day.strftime("%Y-%m-%d")} ホールナビサイトから座標取得成功 DB登録完了',line_token)
                                except Exception as e:
                                    print('halldataのインサートのエラー',e,i,tenpo_name)
                                    error_text= traceback.format_exc()  
                                    print(f'{prefecture} {tenpo_name} {target_day.strftime("%Y-%m-%d")} \n')
                                    issue_comment_text += f'halldataのインサートのエラー {e} {prefecture} {tenpo_name} {target_day.strftime("%Y-%m-%d")} \n'
                                    post_line_text(f' 471行目 {now} {prefecture} {hall_name_text} {target_day.strftime("%Y-%m-%d")} ホールナビサイトから座標取得失敗 {error_text}',line_token)

                        df['hall_id'] = hall_id
                        df['hallnavi_name'] = hallnavi_name
                        if (hall_id == '') or (hallnavi_name == 0):
                            post_line_text(f' 477行目 hall_id {hall_id}です {hall_name_text} {now} {prefecture}  {target_day.strftime("%Y-%m-%d")} ',line_token)
                        for colmun_name in ['G数','差枚','BB','RB','ART','合成確率','BB確率','RB確率','ART確率']:
                            try:
                                exist_column = df[colmun_name][0]
                                #print('exist_column',exist_column)
                            except:
                                if '確率' in colmun_name:
                                    df[colmun_name] = '-'
                                else:
                                    df[colmun_name] = 0
                                print('カラムエラー',colmun_name,hall_name_text)
                        df = df[['機種名', '台番号', 'G数', '差枚', 'BB', 'RB', 'ART', '合成確率', 'BB確率', 'RB確率', 'ART確率','date', 'hall_name', 'prefecture', 'hall_id', 'hallnavi_name']]
                        concat_df = pd.concat([concat_df, df],axis=0,ignore_index=True)
                        gruopby_diff_coins_df = df.groupby(['hall_name','date']).sum().reset_index()
                        gruopby_diff_coins_df = gruopby_diff_coins_df
                        gruopby_diff_coins_df['hall_name'] = hall_name
                        gruopby_diff_coins_df['hallnavi_name'] = hallnavi_name
                        gruopby_diff_coins_df['hall_id'] = hall_id
                        gruopby_diff_coins_df['prefecture'] = prefecture
                        gruopby_diff_coins_df['url_hall_name'] = tenpo_name
                        gruopby_diff_coins_df['win_machine_count'] = len(df[df['差枚'] > 0])
                        gruopby_diff_coins_df['win_machine_count'] = gruopby_diff_coins_df['win_machine_count'].astype(str)
                        gruopby_diff_coins_df['sum_machine_count'] = df.groupby(['hall_name','date']).size().reset_index()[0]
                        gruopby_diff_coins_df['ave_diff_coins'] = gruopby_diff_coins_df['差枚'] / gruopby_diff_coins_df['sum_machine_count']
                        gruopby_diff_coins_df['ave_game_count'] = gruopby_diff_coins_df['G数'] / gruopby_diff_coins_df['sum_machine_count']
                        gruopby_diff_coins_df['sum_machine_count'] = gruopby_diff_coins_df['sum_machine_count'].astype(str)
                        gruopby_diff_coins_df['win_rate'] = gruopby_diff_coins_df['win_machine_count'] + '/' + gruopby_diff_coins_df['sum_machine_count']
                        gruopby_diff_coins_df['win_rate'] = gruopby_diff_coins_df['win_rate'].map(lambda x : '(' + x + '台)' + str(round(int(x.split('/')[0])/int(x.split('/')[1])*100,1))  + '%')
                        gruopby_diff_coins_df = gruopby_diff_coins_df.fillna(0)
                        gruopby_diff_coins_df = gruopby_diff_coins_df.astype({'ave_diff_coins':int,'ave_game_count':int})
                        gruopby_diff_coins_df = gruopby_diff_coins_df.sort_values('date',ascending=False)
                        gruopby_diff_coins_df = gruopby_diff_coins_df.reset_index(drop=True)
                        gruopby_diff_coins_df = gruopby_diff_coins_df[['date','prefecture','hall_id','hall_name','hallnavi_name','url_hall_name','差枚','ave_diff_coins','ave_game_count','win_rate']]
                        gruopby_diff_coins_df.columns = ['date','prefecture','hall_id','hall_name','hallnavi_name','url_hall_name','sum_diffcoins','ave_diffcoins','ave_game','win_rate']
                        ichiran_all_tennpo_df =  pd.concat([ichiran_all_tennpo_df, gruopby_diff_coins_df],axis=0,ignore_index=True)
                        print('成功',prefecture,i,tenpo_name)
                        #break
                        #ichiran_all_tennpo_df.to_csv('csv/tokyo_psgr_insert_df.csv',index=False)
                        concat_df.rename(columns={'機種名':'machine_name',
                                                                            '台番号':'machine_num',
                                                                            'G数':'game_count',
                                                                            '差枚':'diff_coins',
                                                                            'BB':'bb_count',
                                                                            'RB':'rb_count',
                                                                            'ART':'art_count',
                                                                            '合成確率':'sum_win_rate',
                                                                            'BB確率':'bb_win_rate',
                                                                            'RB確率':'rb_win_rate',
                                                                            'ART確率':'art_win_rate'},inplace=True)
                        concat_df = concat_df.fillna({'bb_count':0,'rb_count':0,'art_count':0,'sum_win_rate':'','bb_win_rate':'','rb_win_rate':'','art_win_rate':''})

                        ichiran_all_tennpo_df.reset_index(drop=True,inplace=True)
                        groupby_date_hall_diffcoins_df = ichiran_all_tennpo_df
                        groupby_date_hall_diffcoins_df
                        table_name = 'groupby_date_hall_diffcoins'
                        #rds_mysql_conn = rds_mysql_get_cursor()
                        #insert_data_bulk(table_name,groupby_date_hall_diffcoins_df,rds_mysql_conn)
                        heroku_psgr_conn = heroku_psgr_get_cursor()
                        insert_data_bulk_psgr(table_name,groupby_date_hall_diffcoins_df,heroku_psgr_conn)
                        #daily_record用のデータフレーム作成
                        daily_record_df = concat_df.reset_index(inplace=False,drop=False)
                        daily_record_df=daily_record_df.rename(columns={'index':'id'})
                        daily_record_df = daily_record_df[['hall_id','date', 'hall_name','hallnavi_name' , 'prefecture',
                                'machine_name', 'machine_num', 'game_count', 'diff_coins',
                            'bb_count', 'rb_count', 'art_count', 'sum_win_rate', 'bb_win_rate',
                            'rb_win_rate', 'art_win_rate' ]]
                        groupby_date_machine_number_diffcoins_df = daily_record_df
                        groupby_date_machine_number_diffcoins_df
                        #rds_mysql_conn = rds_mysql_get_cursor()
                        table_name = 'groupby_date_machine_number_diffcoins'
                        #insert_data_bulk(table_name,groupby_date_machine_number_diffcoins_df,rds_mysql_conn)
                        heroku_psgr_conn = heroku_psgr_get_cursor()
                        #insert_data_bulk_psgr(table_name,groupby_date_machine_number_diffcoins_df,heroku_psgr_conn)

                        concat_groupby_date_kisyubetu_df = pd.DataFrame(columns=[],index=[])
                        try:
                            extract_hall_status_df= concat_df[concat_df['hall_name'] == hall_name]
                        except:
                            extract_hall_status_df= concat_df[concat_df['hall_name'] == hall_name_text]
                        #display(extract_hall_status_df)
                        groupby_date_kisyubetu_df = extract_hall_status_df.groupby(['date','machine_name']).sum()
                        groupby_date_kisyubetu_df['sum_machine_count'] = extract_hall_status_df.groupby(['date','machine_name']).size()
                        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df.reset_index(drop=False).reset_index().rename(columns={'index': 'ranking'})
                        groupby_date_kisyubetu_df[['date','machine_name','sum_machine_count','game_count','diff_coins']]
                        groupby_date_kisyubetu_df['hall_name'] = hall_name
                        kisyubetu_win_daissuu_list = []
                        groupby_date_kisyubetu_df_list = []
                        for kisyu_name,day in zip(groupby_date_kisyubetu_df['machine_name'],groupby_date_kisyubetu_df['date']):
                            kisyu_df = extract_hall_status_df.query('machine_name == @kisyu_name & date == @day')
                            groupby_date_kisyubetu_df_list.append(kisyu_df)
                            kisyu_win_daisuu = len(kisyu_df[kisyu_df['diff_coins'] > 0])
                            kisyubetu_win_daissuu_list.append(kisyu_win_daisuu)
                        groupby_date_kisyubetu_df['win_rate'] = kisyubetu_win_daissuu_list
                        groupby_date_kisyubetu_df['win_machine_count'] = kisyubetu_win_daissuu_list
                        groupby_date_kisyubetu_df['win_rate'] = groupby_date_kisyubetu_df['win_rate'].astype(str)
                        groupby_date_kisyubetu_df['sum_machine_count'] = groupby_date_kisyubetu_df['sum_machine_count'].astype(int)
                        groupby_date_kisyubetu_df['ave_game_count'] = groupby_date_kisyubetu_df['game_count'] / groupby_date_kisyubetu_df['sum_machine_count']
                        groupby_date_kisyubetu_df['ave_game_count'] = groupby_date_kisyubetu_df['ave_game_count'].astype(int)
                        #groupby_date_kisyubetu_df = groupby_date_kisyubetu_df[groupby_date_kisyubetu_df['sum_machine_count'] >= 2 ]
                        groupby_date_kisyubetu_df['diff_coins'] = groupby_date_kisyubetu_df['diff_coins'].astype(int)
                        groupby_date_kisyubetu_df['ave_diff_coins'] = groupby_date_kisyubetu_df['diff_coins'] / groupby_date_kisyubetu_df['sum_machine_count']
                        groupby_date_kisyubetu_df['ave_diff_coins'] = groupby_date_kisyubetu_df['ave_diff_coins'].astype(int)
                        groupby_date_kisyubetu_df['sum_machine_count'] = groupby_date_kisyubetu_df['sum_machine_count'].astype(str)
                        groupby_date_kisyubetu_df['win_rate'] = groupby_date_kisyubetu_df['win_rate'] + '/' + groupby_date_kisyubetu_df['sum_machine_count']
                        groupby_date_kisyubetu_df['win_rate'] = groupby_date_kisyubetu_df['win_rate'].map(lambda x : '(' + x + '台) ' + str(round(int(x.split('/')[0])/int(x.split('/')[1])*100,1))  + '%')
                        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df[['date','ranking','machine_name','win_rate','ave_game_count','ave_diff_coins','diff_coins','game_count','win_machine_count','sum_machine_count']]
                        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df.sort_values('ave_diff_coins',ascending=False)
                        groupby_date_kisyubetu_df['machine_ave_rate'] =(((groupby_date_kisyubetu_df['game_count'] * 3) + groupby_date_kisyubetu_df['diff_coins']) / (groupby_date_kisyubetu_df['game_count'] * 3) )*100
                        groupby_date_kisyubetu_df['machine_ave_rate'] = groupby_date_kisyubetu_df['machine_ave_rate'].map(lambda x : round(x,1))
                        groupby_date_kisyubetu_df['machine_ave_rate'] = groupby_date_kisyubetu_df['machine_ave_rate'].fillna(0)
                        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df.rename(columns={'game_count': 'sum_game_count','diff_coins': 'sum_diff_coins'})
                        groupby_date_kisyubetu_df['hall_name'] = hall_name
                        groupby_date_kisyubetu_df['hall_id'] = hall_id
                        groupby_date_kisyubetu_df['hallnavi_name'] = hallnavi_name
                        groupby_date_kisyubetu_df['prefecture_name'] = prefecture
                        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df[['hall_id','hall_name','hallnavi_name','prefecture_name','date','machine_name','win_rate','machine_ave_rate','ave_game_count','ave_diff_coins','sum_game_count','sum_diff_coins','win_machine_count','sum_machine_count']]
                        groupby_date_kisyubetu_df.reset_index(drop=True,inplace=True)
                        groupby_date_machine_diffcoins_df = groupby_date_kisyubetu_df
                        groupby_date_machine_diffcoins_df['machine_ave_rate'] = groupby_date_machine_diffcoins_df['machine_ave_rate'].astype(str)
                        groupby_date_machine_diffcoins_df.replace('-inf', '0',inplace=True)
                        groupby_date_machine_diffcoins_df.replace('inf', '0',inplace=True)
                        groupby_date_machine_diffcoins_df['machine_ave_rate'] = groupby_date_machine_diffcoins_df['machine_ave_rate'].astype(float)
                        #rds_mysql_conn = rds_mysql_get_cursor()
                        table_name = 'groupby_date_machine_diffcoins'
                        #insert_data_bulk(table_name,groupby_date_machine_diffcoins_df,rds_mysql_conn)

                        heroku_psgr_conn = heroku_psgr_get_cursor()
                        insert_data_bulk_psgr(table_name,groupby_date_machine_diffcoins_df,heroku_psgr_conn)
                        insert_count += 1
                        #break
                    except Exception as e:
                        error_text = traceback.format_exc()
                        print(tenpo_name,error_text)
                        post_line_text(f' 610行目 {hall_name} {hall_name_text} {e} {prefecture} {target_day}\n{error_text}',line_token)
                        error_count += 1
                        #break
                        #time.sleep(1)
                        continue
                #
                post_line_text(f' 616行目 \n{prefecture} \n{target_day}\n{insert_count}/{len(tenpo_url_name_list)}件RDS用HEROKU用インサート完了',line_token)
                #post_line_text(f'{prefecture} {target_day}\n{insert_count}件HEROKU用インサート完了',line_token)
                #break
                
            except Exception as e:
                print(tenpo_name,e)
                post_line_text(f' 622行目 {prefecture} {target_day}\nスクレイピングエラー\n{traceback.format_exc()}',line_token)
                continue
        #break
    except Exception as e:
        print(e)
        error_text = traceback.format_exc()
        post_line_text(f'628行目 {prefecture} RDS追加処理でエラーが発生しました。\n{error_text}',line_token)
        continue
        #break
        #
        #continue

# ユーザ名、パスワードによるインスタンス生成
GITHUB_PERSONAL_ACCESS_TOKENS = os.environ.get('GITHUB_PERSONAL_ACCESS_TOKENS')
# using an access token
auth = Auth.Token(GITHUB_PERSONAL_ACCESS_TOKENS)
g = Github(auth=auth)
issue_comment_text += 'created_at ' + str(datetime.datetime.now()) + '\n'
if error_hall_count != 0:
    repo = g.get_repo("dataanalytics2020/nuxt3_fastapi_aws")
    issue = repo.get_issue(number=6)
    issue.create_comment(issue_comment_text)
    
post_line_text(f'645行目 rdsインサート用スクレイピング終了',line_token)