#utf-8
from flask import Flask, render_template, request, redirect 
from flask_mail import Mail
from email.mime.text import MIMEText
import smtplib
from datetime import date, timedelta
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from flask_assets import Environment, Bundle
from flask_bootstrap import Bootstrap
import os
from PIL  import ImageDraw , ImageFont , Image
import unicodedata
import string
from folium import plugins
import branca
import folium
from folium.features import CustomIcon
import mysql
import mysql.connector
import sshtunnel
from sshtunnel import SSHTunnelForwarder
import datetime
import psycopg2
from folium import plugins
import branca
import sympy
from dotenv import load_dotenv
load_dotenv()

df:pd.DataFrame  = pd.read_csv(r'csv/2022-12-09_touhou.csv')
heroku_port:int = int(os.environ.get("PORT", 5000))

def convert_sql_date_to_jp_date(sql_date:datetime.date) -> str:
    sql_str_date = str(sql_date)
    return sql_str_date.split('-')[1].lstrip('0') + '月' + sql_str_date.split('-')[2].lstrip('0') + '日'


def get_area_sql_text(target_area_name='minamikantou'):
    print(target_area_name)
    hokkaidoutouhoku_list = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県']
    kitakantou_list = ['茨城県', '栃木県', '群馬県']
    minamikantou_list = ['埼玉県', '千葉県', '東京都', '神奈川県']
    hokurikukoushinetsu_list = ['新潟県', '富山県', '石川県', '福井県', '長野県', '山梨県']
    toukai_list = ['愛知県', '岐阜県', '静岡県', '三重県']
    kansai_list = ['大阪府', '京都府', '兵庫県', '奈良県', '滋賀県', '和歌山県']
    chugokushikoku_list = ['鳥取県', '島根県', '岡山県', '広島県','徳島県', '香川県', '愛媛県', '高知県']
    kyushu_list = [ '山口県','福岡県', '佐賀県', '長崎県', '大分県', '熊本県', '宮崎県', '鹿児島県','沖縄県']
    prefecture_str_lists = ['hokkaidoutouhoku_list', 'kitakantou_list','minamikantou_list','hokurikukoushinetsu_list','toukai_list','kansai_list','chugokushikoku_list','kyushu_list'] 
    for prefecture_list_name in prefecture_str_lists:
        #print(prefecture_list_name)
        if target_area_name == prefecture_list_name.replace('_list',''):
            print('ok',target_area_name)
            target_area_name_list = eval(prefecture_list_name)
            #print(target_area_name_list)
            break
    area_sql_text = ''
    for prefecture_name in target_area_name_list:
        if len(area_sql_text) == 0:
            area_sql_text += f"都道府県 = '{prefecture_name}'"
        else:
            area_sql_text += f" OR 都道府県 = '{prefecture_name}'"
    #print(area_sql_text)
    return area_sql_text


def get_driver():
    users = os.getenv('HEROKU_PSGR_USER')    # DBにアクセスするユーザー名(適宜変更)
    dbnames = os.getenv('HEROKU_PSGR_DATABASE')   # 接続するデータベース名(適宜変更)
    passwords = os.getenv('HEROKU_PSGR_PASSWORD')  # DBにアクセスするユーザーのパスワード(適宜変更)
    host = os.getenv('HEROKU_PSGR_HOST')     # DBが稼働しているホスト名(適宜変更)
    port = 5432        # DBが稼働しているポート番号(適宜変更)
    # PostgreSQLへ接続
    conn = psycopg2.connect("user=" + users +" dbname=" + dbnames +" password=" + passwords, host=host, port=port)

    # PostgreSQLにデータ登録
    cursor = conn.cursor()
    return cursor

def get_concat_h_multi_resize(im_list, resample=Image.BICUBIC):
    min_height = min(im.height for im in im_list)
    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=resample)
                    for im in im_list]
    total_width = sum(im.width for im in im_list_resize)
    dst = Image.new('RGB', (total_width, min_height))
    pos_x = 0
    for im in im_list_resize:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width
    return dst

def get_concat_v_multi_resize(im_list, resample=Image.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample)
                    for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = Image.new('RGB', (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst

def convert_date(date):
    date:str = str(date).split('-')
    date = date[1].lstrip('0') + '/' + date[2].lstrip('0')
    return date

#テーブルタイプの画像出力
def create_df_cell_image(_df,image_name):
    global create_df_cell_image_path
    width_concat_lists = []
    font = ImageFont.truetype('font/MochiyPopOne-OTF-ExtraBold.otf', 18)
    df_columns_list = list(_df.columns)
    for column_number in range(len(_df.columns)):
        height_concat_lists = []
        #print(column_number)
        print(df_columns_list[column_number])
        if df_columns_list[column_number] == '機種名':
            cell_width = 380
        elif df_columns_list[column_number] == '店舗名':
            cell_width = 300
        elif df_columns_list[column_number] == '店舗平均差枚':
            cell_width = 150
        elif df_columns_list[column_number] == '店舗平均G数':
            cell_width = 150
        elif df_columns_list[column_number] == '勝率':
            cell_width = 200
        elif df_columns_list[column_number] == 'データ':
            cell_width = 200
        else:
            cell_width = 100
        cell_height = 40
        im = Image.new('RGB', (cell_width, cell_height), (139, 0, 206))  # イメージオブジェクトの生成(黒のベタ画像)
        draw = ImageDraw.Draw(im)  # Drawオブジェクトを生成  
        # フォントの指定(メイリオ48pt)
        draw.multiline_text((cell_width/2, 20), df_columns_list[column_number], fill=(255,255,255), font=font, align ="center",anchor="mm") # 文字の描画
        w, h = im.size
        draw.rectangle((0, 0, w-1, h-1), outline = (255,255,255))
        height_concat_lists.append(im)
        for index_number ,(i,record) in enumerate(_df.iterrows()):
            if (index_number + 1 ) %  2 != 0:
                im = Image.new('RGB', (cell_width, cell_height), (255, 255, 255))  # イメージオブジェクトの生成(黒のベタ画像)
            else:
                im = Image.new('RGB', (cell_width, cell_height), (202, 168, 255))  # イメージオブジェクトの生成(黒のベタ画像)
            draw = ImageDraw.Draw(im)  # Drawオブジェクトを生成  
            
            draw.multiline_text((cell_width/2,10), f'{record[column_number]}', fill=(0,0,0), font=font,anchor="ma") 
            w, h = im.size
            
            if df_columns_list[column_number] == '店舗平均差枚':
                samai = record[column_number]
                if samai > 0:
                    samai_bunbo = 400
                    samai_percet = samai / samai_bunbo
                    draw.rectangle([(30, 0), (30+ samai_percet * 100, 40)], fill=(124, 233, 255))
                else :
                    samai_bunbo = 500
                    samai_percet = samai / samai_bunbo
                    draw.rectangle([(30, 0),  (30+ samai_percet * 100, 40)], fill=(255, 0,0))
                draw.rectangle([(29, 0), (30, 40)], fill=(255, 255, 255)) 
                
            if df_columns_list[column_number] == '差枚' :
                samai = record[column_number]
                if samai > 0:
                    samai_bunbo = 50000
                    samai_percet = samai / samai_bunbo
                    draw.rectangle([(30, 0), (30+ samai_percet * 100, 40)], fill=(124, 233, 255))
                else :
                    samai_bunbo = 50000
                    samai_percet = samai / samai_bunbo
                    draw.rectangle([(30, 0),  (30+ samai_percet * 50, 40)], fill=(255, 0,0))
                draw.rectangle([(29, 0), (30, 40)], fill=(255, 255, 255))  
                
            if df_columns_list[column_number] == 'G数' or df_columns_list[column_number] == 'ゲーム数' or df_columns_list[column_number] == '店舗平均G数':
                gamesuu = record[column_number]
                samai_bunbo = 6000
                samai_percet = gamesuu / samai_bunbo
                #print(samai_percet)
                draw.rectangle([(0, 0), (samai_percet * 100, 40)], fill=(0, 255, 206))

            if df_columns_list[column_number] ==  'BB' or df_columns_list[column_number] ==  'RB' or df_columns_list[column_number] ==  'ART' :
                atari_kaisuu = record[column_number]
                bunbo = 35
                percet = atari_kaisuu / bunbo
                #print(percet)
                draw.rectangle([(0, 0), (percet * 100, 40)], fill=(255, 193, 133))
                
            if df_columns_list[column_number] ==  '総台数'  :
                atari_kaisuu = int(record[column_number])
                bunbo = 20
                percet = atari_kaisuu / bunbo
                #print(percet)
                draw.rectangle([(0, 0), (percet * 100, 40)], fill=(255, 193, 133))
            if df_columns_list[column_number] ==  '台数'  :
                atari_kaisuu = int(record[column_number])
                bunbo = 500
                percet = atari_kaisuu / bunbo
                #print(percet)
                draw.rectangle([(0, 0), (percet * 100, 40)], fill=(255, 193, 133))
                
            if df_columns_list[column_number] ==  '勝率'  :
                atari_kaisuu = float(record[column_number].split(')')[1].replace('%','').replace(' ',''))
                #print(atari_kaisuu)
                draw.rectangle([(0, 0), ((atari_kaisuu/100)*200, 40)], fill=(251, 244, 0))
            
            else:
                pass
                
            draw.multiline_text((cell_width/2,10), f'{record[column_number]}', fill=(0,0,0), font=font,anchor="ma")
            draw.rectangle((0, 0, w-1, h-1), outline = (0,0,0))
            height_concat_lists.append(im)
            
        #break
        concat_image_path  = rf"image/temp_image/complted_cell_{column_number}.png"
        get_concat_v_multi_resize(height_concat_lists).save(concat_image_path)
        concat_im = Image.open(concat_image_path)
        width_concat_lists.append(concat_im)
    create_df_cell_image_path = rf"image/temp_image/temp_complted_df_image_cell_{image_name}.png"
    get_concat_h_multi_resize(width_concat_lists).save(create_df_cell_image_path)
    return create_df_cell_image_path

area_name_and_str_jp_area_name_dict = {'hokkaidoutouhoku':'北海道・東北', 'kitakantou':'北関東','minamikantou':'南関東','hokurikukoushinetsu':'北陸・甲信越','toukai':'東海','kansai':'関西','chugokushikoku':'中国・四国','kyushu':'九州・山口'}

app = Flask(__name__, static_folder="static")
bootstrap = Bootstrap(app)

#pathがどこにあるか確認
path=os.getcwd()
print(path)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SECRET_KEY'] = os.urandom(24)
# db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def root():
    return redirect("/top")

@app.route('/heatmap', methods=['GET', 'POST'])#<prefecture>/<tenpo_name>
def heatmap_test():#prefecture,tenpo_name
    from datetime import date, timedelta
    if request.method == 'POST':
        target_day_list = []
        number = 0
        today = date.today()
        target_number:int = '7'
        serch_number:int = 3
        tenpo_name = 'マルハン亀有店'
        for i in range(serch_number):
            while True:
                #print(str(date.today() - timedelta(days=number))[-1])
                if target_number == str(today - timedelta(days=number))[-1]:
                    target_day = today - timedelta(days=number)
                    print('取得日',target_day)
                    target_day_str = target_day.strftime('%Y-%m-%d')
                    target_day_list.append(target_day_str)
                    number += 1
                    break
                else: 
                    pass
                number += 1
        target_day_list.reverse()
        print(target_day_list)
        concat_df_list = []
        urls = []
        for serch_date in target_day_list:
            search_url = url = f"https://ana-slo.com/{serch_date}-マルハン亀有店-data/"
            urls.append(search_url)

        with ThreadPoolExecutor(serch_number) as executor:
            results = list(executor.map(requests.get, urls))
        print(results)

        concat_df_list = []
        for search_response,target_day in zip(results, target_day_list):
            soup = BeautifulSoup(search_response.text, "lxml")
            elem = soup.select('#all_data_block')
            dfs = pd.read_html(str(elem))
            for df in dfs:
                if '機種名' in list(df.columns):
                    tmp_df = df
                    #tmp_df['店舗名'] = user_data['tenpo-name']
                    tmp_df['日付'] = target_day
                    #tmp_df['機種名'] = tmp_df['機種名'].map(removal_text)
                    break
            concat_df_list.append(df)

        concat_df = pre_concat_df =pd.concat(concat_df_list,axis=0)
        for column_name in ['合成確率','BB確率','RB確率','ART確率','BB','RB','ART']:
            try:
                concat_df = concat_df.drop([column_name],axis=1)
            except:
                pass

        horizon_concat_list =[]
        for groupby_date_df in concat_df_list:
            for column_name in ['合成確率','BB確率','RB確率','ART確率','BB','RB','ART']:
                try:
                    groupby_date_df = groupby_date_df.drop([column_name],axis=1)
                except:
                    pass
            groupby_date_df['台番号'] = groupby_date_df['台番号'].astype(int)
            groupby_date_df.sort_values(['台番号'],inplace=True)
            groupby_date_df['台番号'] = groupby_date_df['台番号'].astype(str)
            groupby_date_df['機種名'] = groupby_date_df['台番号'] + '_' + groupby_date_df['機種名']
            groupby_date_df = groupby_date_df.drop(['台番号'],axis=1)
            column_date_name:str = groupby_date_df['日付'].loc[0].split('-')[1].lstrip('0') + '/' + groupby_date_df['日付'].loc[0].split('-')[2].lstrip('0')
            groupby_date_df = groupby_date_df.drop(['日付'],axis=1)
            groupby_date_df = groupby_date_df.rename(columns={'機種名':column_date_name+'_台番号_機種名','G数':column_date_name+'_G数','差枚':column_date_name + '_差枚'})
            #display(groupby_date_df)
            groupby_date_df.reset_index(drop=True,inplace=True)
            horizon_concat_list.append(groupby_date_df)
            

        horizon_concat_df = pd.concat(horizon_concat_list,axis=1)
        horizon_concat_df_html = re.sub(' target', '" id="target', horizon_concat_df.to_html(classes='target',index=False))
        return render_template('test.html',horizon_concat_df = horizon_concat_df_html,\
                                            zip=zip,\
                                            heatmap_column_names=horizon_concat_df.columns.values, \
                                            heatmap_row_data=list(horizon_concat_df.values.tolist()) )
    else:
        today = date.today()
        date_list = [today + timedelta(days=day) for day in range(1,9)]
        date_list = [date.strftime("%Y-%m-%d") for date in date_list]
        return render_template('target_date_recommend_schedule.html',date_list=date_list,tenpo_name=tenpo_name)

@app.route('/top', methods=['GET', 'POST'])
def top():
    if request.method == 'POST':
        user_data = request.form
        today = datetime.date.today()
        print('user_data',user_data)
        data = {}
        prefecture = user_data['prefecture']
        target_day = str(today.year) + '-' + user_data['target_day'].split('月')[0] + '-' + user_data['target_day'].split('月')[1].split('日')[0]
        jpn_target_day = target_day.split('-')[1].lstrip('0') + '月' + target_day.split('-')[2].lstrip('0') + '日'
        print(prefecture,target_day)
        
        #イベント日,店舗名,取材名,媒体名,アナスロ店舗名
        cursor = get_driver()
        sql = f"""SELECT イベント日,店舗名,取材名,媒体名,店舗名,latitude,longitude,取材ランク
                FROM schedule as schedule2
                left join maptable as maptable2
                on schedule2.店舗名 = maptable2.hallnavi_name
                where schedule2.都道府県 = '{prefecture}' and schedule2.イベント日 IN ('{target_day}') and schedule2.媒体名 != 'ホールナビ' 
                """
        print(sql)
        cursor.execute(sql)
        cols = [col[0] for col in cursor.description]
        print('cols',cols)
        report_df =  pd.DataFrame(cursor.fetchall(),columns = cols )
        report_df = report_df.loc[:,~report_df.columns.duplicated()]
        report_df = report_df.drop_duplicates(keep='first')
        report_df =report_df.dropna(subset=['latitude'])
        map_report_df = report_df[['店舗名','取材名','媒体名']].drop_duplicates(keep='first')
        map_report_df = map_report_df.sort_values(['店舗名','媒体名']).reset_index(drop=True)

        if prefecture == '神奈川県':
            prefecture_latitude = 35.44778
            prefecture_longitude = 139.64250
        elif prefecture == '東京都':
            prefecture_latitude = 35.68944
            prefecture_longitude = 139.69167
        elif prefecture == '千葉県':
            prefecture_latitude = 35.60472
            prefecture_longitude = 140.12333
        elif prefecture == '埼玉県':
            prefecture_latitude = 35.85694
            prefecture_longitude = 139.64889
        elif prefecture == '茨城県':
            prefecture_latitude = 36.34139
            prefecture_longitude = 140.44667
        else:
            pass

        folium_map = folium.Map(location=[prefecture_latitude,prefecture_longitude], zoom_start=12, width="100%", height="100%")
        # 地図表示
        # マーカープロット（ポップアップ設定，色変更，アイコン変更）
        print(report_df)
        for tenpo_name in report_df['店舗名'].unique():
            print(tenpo_name)
            extract_syuzai_df_1 = report_df[report_df['店舗名'] == tenpo_name]
            #display(extract_syuzai_df_1)
            print(extract_syuzai_df_1)
            syuzai_rank_list = list(extract_syuzai_df_1['取材ランク'].unique())
            #print(syuzai_rank_list)
            longitude = extract_syuzai_df_1.iloc[0]['longitude']
            latitude = extract_syuzai_df_1.iloc[0]['latitude']
            print('latitude,longitude',latitude,longitude)
            # グレースケールの画像データを作成
            im= Image.new("L", (280, 100),color=(0))
            im.putalpha(0)
            im2= Image.new("L", (260, 50),color=(50))
            im2.putalpha(128)
            im3 = Image.open('icon.png')
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype('font/LightNovelPOPv2.otf',19)
            if len(extract_syuzai_df_1)==1:
                syuzai_name_text = '◆' + tenpo_name + f'\n {extract_syuzai_df_1["取材名"].values[0]}'
            else:
                syuzai_name_text = '◆' + tenpo_name + f'\n {extract_syuzai_df_1["取材名"].values[0]}、他{len(extract_syuzai_df_1)-1}件'
            #print(syuzai_name_text)
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype('font/LightNovelPOPv2.otf',19)

            # 画像を表示
            im.paste(im3, (-15,-14))
            im.paste(im2, (25,48))
            draw.multiline_text(
                (150, 50),
                f'{syuzai_name_text}',
                font=font,
                fill='white',
                align='center',
                spacing=0,
                anchor='ma'
            )

            im.save('syuzai_image.png', quality=95)
            img = 'syuzai_image.png'
            popup_df = extract_syuzai_df_1[['店舗名','取材名','媒体名']].sort_values('店舗名').reset_index(drop=True).T
            popup_df = popup_df.to_html(escape=False)
            popup_data = folium.Popup(popup_df,  max_width=1500,show=False,size=(700, 300))

            folium.Marker(location=[latitude ,longitude],
                tiles='https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
                attr='国土地理院',
                popup=popup_data,
                icon = CustomIcon(
                            icon_image = img,
                            icon_size = (280, 100),
                            icon_anchor = (0, 0),
                            #shadow_image = shadow_img, # 影効果（今回は使用せず コメントアウト
                            #shadow_size = (30, 30),
                            shadow_anchor = (-4, -40),
                            popup_anchor = (3, 3))).add_to(folium_map)
            #break
        
        # set the iframe width and height
        plugins.Fullscreen(
                            position="topright",
                            title="拡大する",
                            title_cancel="元に戻す",
                            force_separate_button=True,
                        ).add_to(folium_map)
        folium_map.get_root().width = "500px"
        folium_map.get_root().height = "600px"
        
        iframe = folium_map.get_root()._repr_html_()
 
        return render_template('schedule_map.html',data=data,jpn_target_day=jpn_target_day,\
                                            user_data=user_data,iframe=iframe,\
                                            zip=zip,\
                                            column_names=map_report_df.columns.values, \
                                            row_data=list(map_report_df.values.tolist()))
    else:
        data = {}
        
        data['prefecture_list'] =['北海道','青森県','岩手県','宮城県','秋田県','山形県',\
                                '福島県','茨城県','栃木県','群馬県','埼玉県','千葉県',\
                                '東京都','神奈川県','新潟県','富山県','石川県','福井県',\
                                '山梨県','長野県','岐阜県','静岡県','愛知県','三重県',\
                                '滋賀県','京都府','大阪府','兵庫県','奈良県',\
                                '和歌山県','鳥取県','島根県','岡山県','広島県',\
                                '山口県','徳島県','香川県','愛媛県','高知県',\
                                '福岡県','佐賀県','長崎県','熊本県','大分県',\
                                '宮崎県','鹿児島県','沖縄県']
        data['kanto_prefecture_list'] = ['東京都','神奈川県','千葉県','埼玉県']
        w_list = ['(月)', '(火)', '(水)', '(木)', '(金)', '(土)', '(日)']
        today = date.today()
        jp_str_day_list = []
        for i in range(0,7):
            day = today + timedelta(days=i)
            jp_str_day = day.strftime('%m').lstrip('0') + '月' + day.strftime('%d').lstrip('0') + '日' + w_list[day.weekday()]
            jp_str_day_list.append(jp_str_day)
        data['jp_str_day_list'] = jp_str_day_list
        area_sql_text = get_area_sql_text('minamikantou')
        cursor = get_driver()
        sql = f'''SELECT イベント日,都道府県,店舗名,取材名,取材ランク,媒体名,latitude,longitude
                FROM schedule as schedule2
                left join maptable as maptable2
                on schedule2.店舗名 = maptable2.hallnavi_name
                WHERE イベント日 > CURRENT_DATE
                AND イベント日 <= CURRENT_DATE + 1
                AND 媒体名 != 'ホールナビ'
                AND ({area_sql_text})
                ORDER BY イベント日,都道府県,店舗名,媒体名,取材名 desc;'''#AND (取材ランク = 'S' OR 取材ランク = 'A')
        print(sql)
        cursor.execute(sql)
        cols = [col[0] for col in cursor.description]
        print('cols',cols)
        report_df =  pd.DataFrame(cursor.fetchall(),columns = cols )
        report_df = report_df.loc[:,~report_df.columns.duplicated()]
        all_kanto_display_df = report_df = report_df.drop_duplicates(keep='first')
        report_df = report_df.dropna(subset=['latitude'])
        #(取材ランク = 'S' OR 取材ランク = 'A')のみ抽出
        report_df = report_df[report_df['取材ランク'].isin(['S','A'])]
        map_report_df = report_df[['店舗名','取材名','媒体名']].drop_duplicates(keep='first')
        map_report_df = map_report_df.sort_values(['店舗名','媒体名']).reset_index(drop=True)
        #東京都に設定
        prefecture_latitude = 35.68944
        prefecture_longitude = 139.69167
        
        folium_map = folium.Map(location=[prefecture_latitude,prefecture_longitude], zoom_start=10, width="100%", height="100%")
        # 地図表示
        # マーカープロット（ポップアップ設定，色変更，アイコン変更）
        print(report_df)
        for tenpo_name in report_df['店舗名'].unique():
            print(tenpo_name)
            extract_syuzai_df_1 = report_df[report_df['店舗名'] == tenpo_name]
            #display(extract_syuzai_df_1)
            print(extract_syuzai_df_1)
            syuzai_rank_list = list(extract_syuzai_df_1['取材ランク'].unique())
            #print(syuzai_rank_list)
            longitude = extract_syuzai_df_1.iloc[0]['longitude']
            latitude = extract_syuzai_df_1.iloc[0]['latitude']
            print('latitude,longitude',latitude,longitude)
            # グレースケールの画像データを作成
            im= Image.new("L", (280, 100),color=(0))
            im.putalpha(0)
            im2= Image.new("L", (260, 50),color=(50))
            im2.putalpha(128)
            im3 = Image.open('icon.png')
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype('font/LightNovelPOPv2.otf',19)
            if len(extract_syuzai_df_1)==1:
                syuzai_name_text = '◆' + tenpo_name + f'\n {extract_syuzai_df_1["取材名"].values[0]}'
            else:
                syuzai_name_text = '◆' + tenpo_name + f'\n {extract_syuzai_df_1["取材名"].values[0]}、他{len(extract_syuzai_df_1)-1}件'
            #print(syuzai_name_text)
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype('font/LightNovelPOPv2.otf',19)

            # 画像を表示
            im.paste(im3, (-15,-14))
            im.paste(im2, (25,48))
            draw.multiline_text(
                (150, 50),
                f'{syuzai_name_text}',
                font=font,
                fill='white',
                align='center',
                spacing=0,
                anchor='ma'
            )

            im.save('syuzai_image.png', quality=95)
            img = 'syuzai_image.png'
            popup_df = extract_syuzai_df_1[['店舗名','取材名','媒体名']].sort_values('店舗名').reset_index(drop=True).T
            popup_df = popup_df.to_html(escape=False)
            popup_data = folium.Popup(popup_df,  max_width=1500,show=False,size=(700, 300))

            folium.Marker(location=[latitude ,longitude],
                tiles='https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
                attr='国土地理院',
                popup=popup_data,
                icon = CustomIcon(
                            icon_image = img,
                            icon_size = (280, 100),
                            icon_anchor = (0, 0),
                            #shadow_image = shadow_img, # 影効果（今回は使用せず コメントアウト
                            #shadow_size = (30, 30),
                            shadow_anchor = (-4, -40),
                            popup_anchor = (3, 3))).add_to(folium_map)
            #break
        
        # set the iframe width and height
        plugins.Fullscreen(
                            position="topright",
                            title="拡大する",
                            title_cancel="元に戻す",
                            force_separate_button=True,
                        ).add_to(folium_map)
        folium_map.get_root().width = "500px"
        folium_map.get_root().height = "600px"
        
        data['iframe'] = folium_map.get_root()._repr_html_()
        display_report_df = all_kanto_display_df[['イベント日','都道府県','店舗名','媒体名','取材名']].sort_values(['イベント日','都道府県','店舗名','媒体名','取材名'],ascending=[True,False,True,True,False]).reset_index(drop=True)
        display_report_df = display_report_df.drop_duplicates(keep='first')
        display_report_df['イベント日'] = display_report_df['イベント日'].map(convert_sql_date_to_jp_date)
        data['display_report_df_column_names'] = display_report_df.columns.values
        data['display_report_df'] = display_report_df
        data['display_report_df_row_data'] = list(display_report_df.values.tolist())
        data['area_name'] = 'minamikantou'
        data['area_name_jp'] = area_name_and_str_jp_area_name_dict['minamikantou']
        return render_template('top.html',data=data,zip=zip)


@app.route('/recommend/<prefecture>', methods=['GET', 'POST'])
def select_tenpo_name(prefecture):
    print(prefecture)
    tenpo_url_df:pd.DataFrame = pd.read_csv('csv/tenpo_url_flask_web_site.csv')
    group_name_list:list[str] ='''123,BBステーション,SAP,アビバ,グランドホール,ともえ,トワーズ,アスカ,アリーナ,ラ・カータ,DAS,Dステーション,MGM,PIA,やすだ,ウエスタン,エスパス,\
エンジェル,オゼック,オリエンタルパサージュ,オーパス・ワン,カレイド,キコーナ,\
キューデンアネックス,グランパ,コンサートホール,ゴードン,ジャラン,\
ジャンジャンマールゴット,デルパラ,ドキわくランド,ニラク,パラッツォ,\
パーラースーパーセブン,パーラーフィオーレ,ヒノマル,ヒロキ,ビックディッパー,\
ピーアーク,フルハウス,プレゴ,ベガスベガス,マルハン,ミカド,ミリオン,ガイア,\
メッセ,国際センター,UNO,楽園,オーシャン,金時,ヴィーナス,メトロ,アムディ,アミューズ,PLAZA,ダイナム,\
SKIP,ザシティ/ベルシティ,ジアス,ジャパンニューアルファ,プレスト,東横フェスタ,グランドオータ,エランドール,\
ジャムフレンドクラブ,スカイプラザ,第一プラザ,チャレンジャー'''.split(',')
    others_extract_tokyo_tenpo_url_df = extract_tokyo_tenpo_url_df = tenpo_url_df[tenpo_url_df['都道府県'] == prefecture]
    extract_tokyo_tenpo_url_df = extract_tokyo_tenpo_url_df.sort_values('店舗名')

    group_name_count_dict:dict[str] = {}
    web_group_name_list:list[str] = []
    for group_name in group_name_list:
        extract_groupname_df = extract_tokyo_tenpo_url_df[extract_tokyo_tenpo_url_df['店舗名'].str.contains(group_name)]
        #display(extract_groupname_df)
        group_name_count_dict[group_name] = len(extract_groupname_df)
        #break
        #print(group_name)
        tmp_list = []
        #print(group_name)
        for tenpo_name in extract_groupname_df['店舗名']:
            tmp_list.append(tenpo_name)
            target = extract_tokyo_tenpo_url_df.index[(extract_tokyo_tenpo_url_df['店舗名'] == tenpo_name)]
        web_group_name_list.append(tmp_list)


    sorted_group_name_count_dict = sorted(group_name_count_dict.items(), key = lambda fruit : fruit[1])
    #print(type(sorted_group_name_count_dict))
    sorted_group_name_count_dict.reverse()
    sorted_group_name_count_dict = dict(sorted_group_name_count_dict)
    sorted_group_name_count_dict

    group_name_count_dict:dict[str] = {}
    web_group_name_list:list[str] = []
    for group_name in sorted_group_name_count_dict:
        extract_groupname_df = extract_tokyo_tenpo_url_df[extract_tokyo_tenpo_url_df['店舗名'].str.contains(group_name)]
        #display(extract_groupname_df)
        group_name_count_dict[group_name] = len(extract_groupname_df)
        #break
        #print(group_name)
        tmp_list = []
        #print(group_name)
        for tenpo_name in extract_groupname_df['店舗名']:
            tmp_list.append(tenpo_name)
            target = extract_tokyo_tenpo_url_df.index[(extract_tokyo_tenpo_url_df['店舗名'] == tenpo_name)]
        web_group_name_list.append(tmp_list)

    
    others_extract_tokyo_tenpo_url_df = extract_tokyo_tenpo_url_df 
    for group_name in sorted_group_name_count_dict:
        extract_groupname_df = extract_tokyo_tenpo_url_df[extract_tokyo_tenpo_url_df['店舗名'].str.contains(group_name)]
        for tenpo_name in extract_groupname_df['店舗名']:
            try:
                target = extract_tokyo_tenpo_url_df.index[(extract_tokyo_tenpo_url_df['店舗名'] == tenpo_name)]
                others_extract_tokyo_tenpo_url_df = others_extract_tokyo_tenpo_url_df.drop(target)
            except Exception as e:
                print('error',tenpo_name,e)
                pass
    web_group_name_list.append(list(others_extract_tokyo_tenpo_url_df['店舗名'].unique()))
    sorted_group_name_count_dict['その他'] = len(others_extract_tokyo_tenpo_url_df)
    group_num_list = list(sorted_group_name_count_dict.values())
    display_group_name_list = list(sorted_group_name_count_dict.keys())
    return render_template('select_prefecture.html',prefecture=prefecture,zip=zip,web_group_name_list=web_group_name_list,group_num_list=group_num_list,display_group_name_list=display_group_name_list,)

@app.route('/<prefecture>/<tenpo_name>', methods=['GET', 'POST'])
def clicked_tenpo_name(prefecture,tenpo_name):
    from datetime import date, timedelta
    if request.method == 'POST':
        user_data = request.form
        print(user_data)
        data = {}
        
        print(user_data['tenpo-name'],user_data['recommend-day'])
        target_day_list = []
        number = 0
        today = date.today()
        target_number:int = str(user_data['recommend-day'][-1])
        data['target_number'] = target_number
        serch_number:int = int(user_data['n-times'])
        for i in range(serch_number):
            while True:
                #print(str(date.today() - timedelta(days=number))[-1])
                if target_number == str(today - timedelta(days=number))[-1]:
                    target_day = today - timedelta(days=number)
                    print('取得日',target_day)
                    target_day_str = target_day.strftime('%Y-%m-%d')
                    target_day_list.append(target_day_str)
                    number += 1
                    break
                else: 
                    pass
                number += 1
        target_day_list.reverse()
        print(target_day_list)
        concat_df_list = []
        urls = []
        for serch_date in target_day_list:
            search_url = url = f"https://ana-slo.com/{serch_date}-{user_data['tenpo-name']}-data/"
            urls.append(search_url)

        with ThreadPoolExecutor(serch_number) as executor:
            results = list(executor.map(requests.get, urls))
        print(results)

        concat_df_list = []
        for search_response,target_day in zip(results, target_day_list):
            soup = BeautifulSoup(search_response.text, "lxml")
            elem = soup.select('#all_data_block')
            dfs = pd.read_html(str(elem))
            for df in dfs:
                if '機種名' in list(df.columns):
                    tmp_df = df
                    #tmp_df['店舗名'] = user_data['tenpo-name']
                    tmp_df['日付'] = target_day
                    #tmp_df['機種名'] = tmp_df['機種名'].map(removal_text)
                    break
            concat_df_list.append(df)

        concat_df = pre_concat_df =pd.concat(concat_df_list,axis=0)
        for column_name in ['合成確率','BB確率','RB確率','台番号','ART確率','BB','RB','ART']:
            try:
                concat_df = concat_df.drop([column_name],axis=1)
            except:
                pass
 
        ######3列同時比較用のデータフレーム作成
        
        horizon_concat_list =[]
        for groupby_date_df in concat_df_list:
            for column_name in ['合成確率','BB確率','RB確率','ART確率','BB','RB','ART']:
                try:
                    groupby_date_df = groupby_date_df.drop([column_name],axis=1)
                except:
                    pass
            groupby_date_df['台番号'] = groupby_date_df['台番号'].astype(int)
            groupby_date_df.sort_values(['台番号'],inplace=True)
            groupby_date_df['台番号'] = groupby_date_df['台番号'].astype(str)
            groupby_date_df['機種名'] = groupby_date_df['台番号'] + '_' + groupby_date_df['機種名']
            groupby_date_df = groupby_date_df.drop(['台番号'],axis=1)
            column_date_name:str = groupby_date_df['日付'].loc[0].split('-')[1].lstrip('0') + '/' + groupby_date_df['日付'].loc[0].split('-')[2].lstrip('0')
            groupby_date_df = groupby_date_df.drop(['日付'],axis=1)
            groupby_date_df = groupby_date_df.rename(columns={'機種名':column_date_name+'_台番号_機種名','G数':column_date_name+'_G数','差枚':column_date_name + '_差枚'})
            #display(groupby_date_df)
            groupby_date_df.reset_index(drop=True,inplace=True)
            horizon_concat_list.append(groupby_date_df)

        horizon_concat_df = pd.concat(horizon_concat_list,axis=1)
        horizon_concat_df_html = re.sub(' target', '" id="target', horizon_concat_df.to_html(classes='target',index=False))


        groupby_date_kisyubetu_df = pre_concat_df.groupby(['日付','機種名']).sum()
        groupby_date_kisyubetu_df['総台数'] = pre_concat_df.groupby(['日付','機種名']).size()
        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df.reset_index(drop=False).reset_index().rename(columns={'index': '機種順位','ゲーム数': 'G数'})
        groupby_date_kisyubetu_df[['日付','機種名','機種名','総台数','G数','差枚']]
        kisyubetu_win_daissuu_list = []
        groupby_date_kisyubetu_df_list = []
        for kisyu_name,day in zip(groupby_date_kisyubetu_df['機種名'],groupby_date_kisyubetu_df['日付']):
            kisyu_df = pre_concat_df.query('機種名 == @kisyu_name & 日付 == @day')
            groupby_date_kisyubetu_df_list.append(kisyu_df)
            kisyu_win_daisuu = len(kisyu_df[kisyu_df['差枚'] > 0])
            kisyubetu_win_daissuu_list.append(kisyu_win_daisuu)
        groupby_date_kisyubetu_df['勝率'] = kisyubetu_win_daissuu_list
        groupby_date_kisyubetu_df['勝率'] = groupby_date_kisyubetu_df['勝率'].astype(str)
        groupby_date_kisyubetu_df['総台数'] = groupby_date_kisyubetu_df['総台数'].astype(int)
        groupby_date_kisyubetu_df['平均G数'] = groupby_date_kisyubetu_df['G数'] / groupby_date_kisyubetu_df['総台数']
        groupby_date_kisyubetu_df['平均G数'] = groupby_date_kisyubetu_df['平均G数'].astype(int)
        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df[groupby_date_kisyubetu_df['総台数'] >= 2 ]
        groupby_date_kisyubetu_df['差枚'] = groupby_date_kisyubetu_df['差枚'].astype(int)
        groupby_date_kisyubetu_df['平均差枚'] = groupby_date_kisyubetu_df['差枚'] / groupby_date_kisyubetu_df['総台数']
        groupby_date_kisyubetu_df['平均差枚'] = groupby_date_kisyubetu_df['平均差枚'].astype(int)
        groupby_date_kisyubetu_df['総台数'] = groupby_date_kisyubetu_df['総台数'].astype(str)
        groupby_date_kisyubetu_df['勝率'] = groupby_date_kisyubetu_df['勝率'] + '/' + groupby_date_kisyubetu_df['総台数']
        groupby_date_kisyubetu_df['勝率'] = groupby_date_kisyubetu_df['勝率'].map(lambda x : '(' + x + '台) ' + str(round(int(x.split('/')[0])/int(x.split('/')[1])*100,1))  + '%')
        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df[['日付','機種順位','機種名','勝率','平均G数','平均差枚','差枚','G数','総台数']]
        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df.sort_values('平均差枚',ascending=False)
        groupby_date_kisyubetu_df['機種平均出率'] =(((groupby_date_kisyubetu_df['G数'] * 3) + groupby_date_kisyubetu_df['差枚']) / (groupby_date_kisyubetu_df['G数'] * 3) )*100
        groupby_date_kisyubetu_df['機種平均出率'] = groupby_date_kisyubetu_df['機種平均出率'].map(lambda x : round(x,1))
        groupby_date_kisyubetu_df['機種平均出率'] = groupby_date_kisyubetu_df['機種平均出率'].astype(str) + '%'
        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df.rename(columns={'G数': '合計G数','差枚': '合計差枚'})
        groupby_date_kisyubetu_df = groupby_date_kisyubetu_df[['日付','機種名','勝率','機種平均出率','平均G数','平均差枚','合計差枚','合計G数','総台数']]
        groupby_date_kisyubetu_df['平均G数'] = groupby_date_kisyubetu_df['平均G数'].astype(str) + 'G'
        bubble_chart_samai_division_list = list(groupby_date_kisyubetu_df['合計差枚'][:10])
        groupby_date_kisyubetu_df['平均差枚'] = groupby_date_kisyubetu_df['平均差枚'].astype(str) + '枚'
        groupby_date_kisyubetu_df['合計差枚'] = groupby_date_kisyubetu_df['合計差枚'].astype(str) + '枚'
        groupby_date_kisyubetu_df['合計G数'] = groupby_date_kisyubetu_df['合計G数'].astype(str) + 'G'
        groupby_date_kisyubetu_df['総台数'] = groupby_date_kisyubetu_df['総台数'].astype(str) + '台'

        
        #バブルチャートの大きさが相対的な値になるように調整
        bubble_chart_division_top10_samai_ave = sum(bubble_chart_samai_division_list) / len(bubble_chart_samai_division_list)
        bubble_chart_division_top10_samai_ave = int(bubble_chart_division_top10_samai_ave)
        #xを変数xとして定義
        print(bubble_chart_division_top10_samai_ave)
        x = sympy.Symbol('x')
        expr =   x*bubble_chart_division_top10_samai_ave - 10
        print(sympy.solve(expr)[0])
        calc_str = str(sympy.solve(expr)[0])
        bubble_chart_division_calc_num = int(calc_str.split("/")[0]) / int(calc_str.split("/")[1])
        print(bubble_chart_division_calc_num)
        
        ########
        concat_df =  concat_df.groupby(['日付','機種名']).mean().sort_values('差枚',ascending=False)#機種毎に集計
        for column_name in ['差枚','G数','BB','RB','ART']:
            try:
                concat_df[column_name] = concat_df[column_name].astype(int)
            except:
                pass

        concat_df = concat_df.reset_index()
        groupby_samai_game_mean_df = concat_df.drop(['機種名'],axis=1)
        groupby_samai_game_mean_df = groupby_samai_game_mean_df.groupby('日付').mean()
        groupby_samai_game_mean_df.reset_index(inplace=True)
        groupby_samai_game_mean_df['差枚'] = groupby_samai_game_mean_df['差枚'].astype(int)
        groupby_samai_game_mean_df['G数'] = groupby_samai_game_mean_df['G数'].astype(int)
        groupby_samai_game_mean_df['差枚'] = groupby_samai_game_mean_df['差枚'].astype(str)
        groupby_samai_game_mean_df['G数'] = groupby_samai_game_mean_df['G数'].astype(str)
        samai_list:str = str(groupby_samai_game_mean_df['差枚'].tolist())
        print('samai_list',samai_list)
        gamesuu_list:str = str(groupby_samai_game_mean_df['G数'].tolist())
        concat_df = concat_df.rename(columns={'差枚': '平均差枚', 'G数': '平均G数'})

        record = [groupby_samai_game_mean_df['差枚'].tolist(),groupby_samai_game_mean_df['G数'].tolist()]
        print(record)
        
        target_day_list_jp = []
        for day in target_day_list:
            day = day.split('-')[1].lstrip('0') + '月' + day.split('-')[2].lstrip('0') + '日'
            target_day_list_jp.append(day)

        
        ave_tenpo_df = pd.DataFrame(record, columns=target_day_list_jp,index=['平均差枚','平均G数'])
        ave_tenpo_df[0:1]  =  ave_tenpo_df[0:1]  + '枚'
        ave_tenpo_df[1:2]  =  ave_tenpo_df[1:2]  + 'G'  
        groupby_kisyubetu_df = pre_concat_df.groupby(['機種名']).sum()
        groupby_kisyubetu_df['総台数'] = pre_concat_df.groupby(['機種名']).size()
        groupby_kisyubetu_df = groupby_kisyubetu_df.reset_index(drop=False).reset_index().rename(columns={'index': '機種順位','ゲーム数': 'G数'})
        groupby_kisyubetu_df[['機種名','総台数','G数','差枚']]
        kisyubetu_win_daissuu_list = []
        groupby_kisyubetu_df_list = []
        for kisyu_name in groupby_kisyubetu_df['機種名']:
            kisyu_df = pre_concat_df.query('機種名 == @kisyu_name')
            groupby_kisyubetu_df_list.append(kisyu_df)
            kisyu_win_daisuu = len(kisyu_df[kisyu_df['差枚'] > 0])
            kisyubetu_win_daissuu_list.append(kisyu_win_daisuu)
        groupby_kisyubetu_df['勝率'] = kisyubetu_win_daissuu_list
        groupby_kisyubetu_df['勝率'] = groupby_kisyubetu_df['勝率'].astype(str)
        groupby_kisyubetu_df['総台数'] = groupby_kisyubetu_df['総台数'].astype(int)
        groupby_kisyubetu_df['平均G数'] = groupby_kisyubetu_df['G数'] / groupby_kisyubetu_df['総台数']
        groupby_kisyubetu_df['平均G数'] = groupby_kisyubetu_df['平均G数'].astype(int)
        groupby_kisyubetu_df = groupby_kisyubetu_df[groupby_kisyubetu_df['総台数'] >= 2 ]
        groupby_kisyubetu_df['差枚'] = groupby_kisyubetu_df['差枚'].astype(int)
        groupby_kisyubetu_df['平均差枚'] = groupby_kisyubetu_df['差枚'] / groupby_kisyubetu_df['総台数']
        groupby_kisyubetu_df['平均差枚'] = groupby_kisyubetu_df['平均差枚'].astype(int)
        groupby_kisyubetu_df['総台数'] = groupby_kisyubetu_df['総台数'].astype(str)
        groupby_kisyubetu_df['勝率'] = groupby_kisyubetu_df['勝率'] + '/' + groupby_kisyubetu_df['総台数']
        groupby_kisyubetu_df['勝率'] = groupby_kisyubetu_df['勝率'].map(lambda x : '(' + x + '台) ' + str(round(int(x.split('/')[0])/int(x.split('/')[1])*100,1))  + '%')
        groupby_kisyubetu_df = groupby_kisyubetu_df[['機種順位','機種名','勝率','平均G数','平均差枚','差枚','G数','総台数']]
        groupby_kisyubetu_df = groupby_kisyubetu_df.sort_values('平均差枚',ascending=False)
        groupby_kisyubetu_df['機種平均出率'] =(((groupby_kisyubetu_df['G数'] * 3) + groupby_kisyubetu_df['差枚']) / (groupby_kisyubetu_df['G数'] * 3) )*100
        groupby_kisyubetu_df['機種平均出率'] = groupby_kisyubetu_df['機種平均出率'].map(lambda x : round(x,1))
        groupby_kisyubetu_df['機種平均出率'] = groupby_kisyubetu_df['機種平均出率'].astype(str) + '%'
        groupby_kisyubetu_df = groupby_kisyubetu_df.rename(columns={'G数': '合計G数','差枚': '合計差枚'})
        groupby_kisyubetu_df = groupby_kisyubetu_df[['機種順位','機種名','勝率','機種平均出率','平均G数','平均差枚','合計差枚','合計G数','総台数']]
        output_bubble_chart_df = groupby_kisyubetu_df[['機種名','平均差枚','平均G数','合計差枚','総台数']]
        output_bubble_chart_df['総台数'] = output_bubble_chart_df['総台数'].astype(int)
        output_bubble_chart_df = output_bubble_chart_df[output_bubble_chart_df['総台数'] > serch_number]
        groupby_kisyubetu_df['平均G数'] = groupby_kisyubetu_df['平均G数'].astype(str) + 'G'
        groupby_kisyubetu_df['平均差枚'] = groupby_kisyubetu_df['平均差枚'].astype(str) + '枚'
        groupby_kisyubetu_df['合計差枚'] = groupby_kisyubetu_df['合計差枚'].astype(str) + '枚'
        groupby_kisyubetu_df['合計G数'] = groupby_kisyubetu_df['合計G数'].astype(str) + 'G'
        groupby_kisyubetu_df['総台数'] = groupby_kisyubetu_df['総台数'].astype(int)
        groupby_kisyubetu_df= groupby_kisyubetu_df[groupby_kisyubetu_df['総台数'] > serch_number]
        groupby_kisyubetu_df['総台数'] = groupby_kisyubetu_df['総台数'].astype(str) + '台'
        groupby_kisyubetu_df = groupby_kisyubetu_df.reset_index(drop=False).reset_index().rename(columns={'index': '機種順位'})
        groupby_kisyubetu_df['お勧め順位'] = list(range(1,len(groupby_kisyubetu_df)+1))
        groupby_kisyubetu_df['お勧め順位'] = groupby_kisyubetu_df['お勧め順位'].astype(str) + '位'
        groupby_kisyubetu_df = groupby_kisyubetu_df[['お勧め順位','機種名','勝率','機種平均出率','平均G数','平均差枚','合計差枚','合計G数','総台数']]
        # groupby_kisyubetu_df = groupby_kisyubetu_df.rename(columns={'機種順位': 'お勧め順位'})
        groupby_kisyubetu_df = groupby_kisyubetu_df[:10]
        concat_df = groupby_date_kisyubetu_df[:30]
        print('concat_df',concat_df)
        display_day_df_list = []
        
        for target_day in target_day_list:
            #target_day = target_day.split('-')[1].lstrip('0') + '/' + target_day.split('-')[2].lstrip('0') 
            print('target_day',target_day)
            extract_groupby_day_df = groupby_date_kisyubetu_df[groupby_date_kisyubetu_df['日付'] == target_day]
            print(extract_groupby_day_df)
            extract_groupby_day_df['日付'] = extract_groupby_day_df['日付'].map(convert_date)
            extract_groupby_day_df = extract_groupby_day_df.to_html(justify='justify-all',index=False)
            display_day_df_list.append(extract_groupby_day_df)
        print(concat_df)
        concat_df['日付'] = concat_df['日付'].map(convert_date)
        bubble_chart_color_dict = {'purple':'rgb(255,0,255)','red':'rgb(255,0,0)','green':'rgb(0,128,0)','lime':'rgb(0,255,0)','yellow':'rgb(255,255,0)',\
    'blue':'rgb(0,0,255)','aqua':'rgb(0,255,255)','gray':'rgb(128,128,128)','white':'rgb(192,192,192)','black':'rgb(0,0,0)'}
        bubble_chart_color_list = list(bubble_chart_color_dict .values())
        output_bubble_chart_df = output_bubble_chart_df[:10]
        output_bubble_chart_df['順位'] = ['1位','2位','3位','4位','5位','6位','7位','8位','9位','10位']
        output_bubble_chart_df['機種名'] = output_bubble_chart_df['順位'] +' ' + output_bubble_chart_df['機種名']
        output_bubble_chart_df['color'] = bubble_chart_color_list
        return render_template('target_date_recommend_report.html',bubble_chart_division_calc_num = bubble_chart_division_calc_num,\
                                            data=data,serch_number=serch_number,\
                                            user_data=user_data,\
                                            column_names=concat_df.columns.values, \
                                            row_data=list(concat_df.values.tolist()),\
                                            zip=zip,int=int,target_day_list_str=str(target_day_list),\
                                            target_day_list=target_day_list,
                                            output_bubble_chart_df = output_bubble_chart_df,
                                            target_day_list_jp=target_day_list_jp,\
                                            display_day_df_list=display_day_df_list,\
                                            samai_list=str(samai_list),\
                                            gamesuu_list=str(gamesuu_list),\
                                            samai_table = ave_tenpo_df.to_html(justify='justify-all',classes='tb01'),\
                                            groupby_kisyu_table = groupby_kisyubetu_df.to_html(justify='justify-all',classes='tb01',index=False),\
                                            heatmap_column_names=horizon_concat_df.columns.values, \
                                            heatmap_row_data=list(horizon_concat_df.values.tolist()) )
    else:
        today = date.today()
        date_list = [today + timedelta(days=day) for day in range(0,9)]
        date_list = [date.strftime("%Y-%m-%d") for date in date_list]
        return render_template('target_date_recommend_schedule.html',date_list=date_list,tenpo_name=tenpo_name)


@app.route("/form", methods=['GET','POST'])
def form():
    if request.method == "POST":
        accoun_mail = os.getenv('GMAIL_ACCOUNT')
        password = os.getenv('GMAIL_PASSWORD')
        second_password = os.getenv('GMAIL_SECOND_PASSWORD')
        
        name =  request.form.get('name')
        from_email = request.form.get('email')
        category = request.form.get('category')
        about = request.form.get('about')
        subject = category + ':'+ name  + 'お問い合わせ'
        bodytext = "名前：" + name + "\n" + "メールアドレス：" + from_email + "\n問い合わせ内容："  +  about

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(accoun_mail, second_password)

        msg = MIMEText(bodytext)
        msg['subject'] = subject
        print('from_email',from_email)
        msg['From'] = from_email
        msg['To'] = accoun_mail

        server.send_message(msg)
        server.close()
        return render_template('send.html', success=True)
    return render_template("form.html")

@app.route("/send")
def send():
    return render_template('send.html')


@app.route("/tomorrow-recommend/")
def tomorrow_recommend():
    return render_template('tomorrow_recommend.html')


@app.route("/tomorrow_recommend/<area_name>/syuzai/<syuzai_name>")
def tomorrow_recommend_area_syuzai_syuzainame(area_name,syuzai_name):
    data = {}
    data['area_name'] = area_name
    data['syuzai_name'] = syuzai_name
    data['area_name_jp'] = area_name_and_str_jp_area_name_dict[area_name]
    if area_name == 'minamikantou':
        data['area_name_jp'] = '南関東'

    area_sql_text = get_area_sql_text(area_name)
    cursor = get_driver()
    #首都圏のイベントの媒体別の予約数を集計
    cursor.execute(f'''SELECT イベント日,都道府県,店舗名,媒体名,取材名
                FROM schedule
                WHERE イベント日 >= current_date
                    AND イベント日 < current_date + 7
                    AND 媒体名 != 'ホールナビ'
                    AND 取材名 = '{syuzai_name}'
                    AND ({area_sql_text})
                    ORDER BY イベント日,都道府県 desc;''')
    cols = [col.name for col in cursor.description]
    extract_syuzai_name_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    data['extract_syuzai_name_df'] = extract_syuzai_name_df
    data['extract_syuzai_name_df_column_names'] = extract_syuzai_name_df.columns.values
    data['extract_syuzai_name_df_row_data'] = list(extract_syuzai_name_df.values.tolist())
    return render_template('tomorrow_recommend_area_syuzai_syuzainame.html',data=data,zip=zip)


@app.route("/tomorrow_recommend/<area_name>/hall/<hall_name>")
def tomorrow_recommend_area_hall_hallname(area_name,hall_name):
    data = {}
    data['area_name'] = area_name
    data['hall_name'] = hall_name
    data['area_name_jp'] = area_name_and_str_jp_area_name_dict[area_name]
    area_sql_text = get_area_sql_text(area_name)
    cursor = get_driver()
    #首都圏のイベントの媒体別の予約数を集計
    cursor.execute(f'''SELECT イベント日,都道府県,店舗名,媒体名,取材名
                FROM schedule
                WHERE イベント日 >= current_date
                    AND イベント日 < current_date + 7
                    AND 媒体名 != 'ホールナビ'
                    AND 店舗名 = '{hall_name}'
                    AND ({area_sql_text})
                    ORDER BY イベント日,都道府県 desc;''')
    cols = [col.name for col in cursor.description]
    extract_hall_name_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    data['extract_hall_name_df'] = extract_hall_name_df
    data['extract_hall_name_df_column_names'] = extract_hall_name_df.columns.values
    data['extract_hall_name_df_row_data'] = list(extract_hall_name_df.values.tolist())
    return render_template('tomorrow_recommend_area_hall_hallname.html',data=data,zip=zip)


@app.route("/tomorrow_recommend/<area_name>/media/<media_name>")
def tomorrow_recommend_area_media_medianame(area_name,media_name):
    data = {}
    today = date.today()
    date_list = [today + timedelta(days=day) for day in range(0,6)]
    date_list = [date.strftime("%Y-%m-%d") for date in date_list]
    data['date_list'] = date_list
    data['area_name'] = area_name
    data['media_name'] = media_name
    data['area_name_jp'] = area_name_and_str_jp_area_name_dict[area_name]
    cursor = get_driver()
    area_sql_text = get_area_sql_text(area_name)
    #首都圏のイベントの媒体別の予約数を集計
    cursor.execute(f'''SELECT イベント日,都道府県,店舗名,取材名
                FROM schedule
                WHERE イベント日 >= current_date
                    AND イベント日 < current_date + 7
                    AND 媒体名 != 'ホールナビ'
                    AND 媒体名 = '{media_name}'
                    AND ({area_sql_text})
                    ORDER BY イベント日,都道府県 desc;''')
    cols = [col.name for col in cursor.description]
    extract_media_name_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    data['extract_media_name_df'] = extract_media_name_df
    data['extract_media_name_df_column_names'] = extract_media_name_df.columns.values
    data['extract_media_name_df_row_data'] = list(extract_media_name_df.values.tolist())
    return render_template('tomorrow_recommend_area_media_medianame.html',data=data,zip=zip)

@app.route("/tomorrow-recommend/<area_name>/")
def tomorrow_recommend_area(area_name):
    data = {}
    today = date.today()
    date_list = [today + timedelta(days=day) for day in range(0,9)]
    date_list = [date.strftime("%Y-%m-%d") for date in date_list]
    data['area_name_jp'] = area_name_and_str_jp_area_name_dict[area_name]
    data['date_list'] = date_list
    data['area_name'] = area_name

    area_sql_text = get_area_sql_text(area_name)
    cursor = get_driver()
    #首都圏のイベントの媒体別の予約数を集計
    cursor.execute(f'''SELECT COUNT(媒体名), 媒体名
               FROM schedule
               WHERE イベント日 >= current_date
                AND イベント日 <= current_date + 6
                AND 媒体名 != 'ホールナビ'
                AND ({area_sql_text})
                GROUP BY 媒体名
                ORDER BY COUNT(媒体名) desc;''')
    cols = [col.name for col in cursor.description]
    groupby_media_name_count_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    groupby_media_name_count_df.rename(columns={'count': '取材数'},inplace=True)
    data['groupby_media_name_count_df'] = groupby_media_name_count_df
    data['groupby_media_name_count_df_column_names'] = groupby_media_name_count_df.columns.values
    data['groupby_media_name_count_df_row_data'] = list(groupby_media_name_count_df.values.tolist())
    
    
    return render_template('tomorrow_recommend_area.html',data=data,zip=zip)
#           /tomorrow_recommend/minamikanto/media/BASHtv-data



@app.route("/tomorrow-recommend/<area_name>/<date>-data")
def tomorrow_recommend_area_date(area_name,date):
    data = {}
    data['area_name'] = area_name
    data['date'] = date
    print(date)
    date_jp = date.split('-')[1].lstrip('0') + '月' + date.split('-')[2].lstrip('0') + '日'
    print(date_jp)
    data['date_jp'] = date_jp
    if area_name == 'kanto':
        data['area_name_jp'] = '関東'
    return render_template('tomorrow_recommend_area_date.html',data=data)


@app.route("/privacy_policy")
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route("/sitemap.xml")
def sitemap():
    return app.send_static_file("sitemap.xml")

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=int(os.environ.get('PORT', 5000)))
