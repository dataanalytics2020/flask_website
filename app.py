#utf-8
from flask import Flask, render_template, request, redirect
from datetime import date, timedelta
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from flask_assets import Environment, Bundle
from flask_bootstrap import Bootstrap
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
from dotenv import load_dotenv
load_dotenv()

df  = pd.read_csv(r'csv/2022-12-09_touhou.csv')
heroku_port = int(os.environ.get("PORT", 5000))

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

app = Flask(__name__, static_folder="static")
bootstrap = Bootstrap(app)

#pathがどこにあるか確認
path=os.getcwd()
print(path)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SECRET_KEY'] = os.urandom(24)
# db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect("/top")

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
                on schedule2.店舗名 = maptable2.anaslo_name
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

        folium_map = folium.Map(location=[prefecture_latitude,prefecture_longitude], zoom_start=12)
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
            popup_data = folium.Popup(popup_df,  max_width=1500,show=True,size=(700, 300))

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
        folium_map.get_root().width = "1000px"
        folium_map.get_root().height = "800px"
        
        iframe = folium_map.get_root()._repr_html_()
        
        
        return render_template('schedule_map.html',data=data,jpn_target_day=jpn_target_day,\
                                            user_data=user_data,iframe=iframe,\
                                            zip=zip,\
                                            column_names=map_report_df.columns.values, \
                                            row_data=list(map_report_df.values.tolist()))
    else:
        prefecture_list =['神奈川県','千葉県','埼玉県']
        w_list = ['(月)', '(火)', '(水)', '(木)', '(金)', '(土)', '(日)']
        today = date.today()
        jp_str_day_list = []
        for i in range(0,7):
            day = today + timedelta(days=i)
            jp_str_day = day.strftime('%m').lstrip('0') + '月' + day.strftime('%d').lstrip('0') + '日' + w_list[day.weekday()]
            jp_str_day_list.append(jp_str_day)
        return render_template('top.html',date_list=jp_str_day_list,prefecture_list=prefecture_list)

@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    print('test')
    return render_template('test.html')

@app.route('/recommend/<prefecture>', methods=['GET', 'POST'])
def test2(prefecture):
    print(prefecture)
    tenpo_url_df:pd.DataFrame = pd.read_csv('csv/tenpo_url_flask_web_site.csv')
    group_name_list:list[str] ='''123,BBステーション,SAP,アビバ,グランドホール,ともえ,トワーズ,アスカ,アリーナ,ラ・カータ,DAS,Dステーション,MGM,PIA,やすだ,ウエスタン,エスパス,\
エンジェル,オゼック,オリエンタルパサージュ,オーパス・ワン,カレイド,キコーナ,\
キューデンアネックス,グランパ,コンサートホール,ゴードン,ジャラン,\
ジャンジャンマールゴット,デルパラ,ドキわくランド,ニラク,パラッツォ,\
パーラースーパーセブン,パーラーフィオーレ,ヒノマル,ヒロキ,ビックディッパー,\
ピーアーク,フルハウス,プレゴ,ベガスベガス,マルハン,ミカド,ミリオン,ガイア,\
メッセ,国際センター,UNO,楽園,オーシャン,金時'''.split(',')
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
            target = extract_tokyo_tenpo_url_df.index[(extract_tokyo_tenpo_url_df['店舗名'] == tenpo_name)]
            others_extract_tokyo_tenpo_url_df = others_extract_tokyo_tenpo_url_df.drop(target)
    web_group_name_list.append(list(others_extract_tokyo_tenpo_url_df['店舗名'].unique()))
    sorted_group_name_count_dict['その他'] = len(others_extract_tokyo_tenpo_url_df)
    group_num_list = list(sorted_group_name_count_dict.values())
    display_group_name_list = list(sorted_group_name_count_dict.keys())
    return render_template('test2.html',prefecture=prefecture,zip=zip,web_group_name_list=web_group_name_list,group_num_list=group_num_list,display_group_name_list=display_group_name_list,)

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
 
        ######
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
        groupby_date_kisyubetu_df['平均差枚'] = groupby_date_kisyubetu_df['平均差枚'].astype(str) + '枚'
        groupby_date_kisyubetu_df['合計差枚'] = groupby_date_kisyubetu_df['合計差枚'].astype(str) + '枚'
        groupby_date_kisyubetu_df['合計G数'] = groupby_date_kisyubetu_df['合計G数'].astype(str) + 'G'
        groupby_date_kisyubetu_df['総台数'] = groupby_date_kisyubetu_df['総台数'].astype(str) + '台'

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
        
        
        
        return render_template('target_date_recommend_report.html',data=data,serch_number=serch_number,\
                                            user_data=user_data,\
                                            column_names=concat_df.columns.values, \
                                            row_data=list(concat_df.values.tolist()),\
                                            zip=zip,target_day_list_str=str(target_day_list),\
                                            target_day_list=target_day_list,
                                            output_bubble_chart_df = output_bubble_chart_df,
                                            target_day_list_jp=target_day_list_jp,\
                                            display_day_df_list=display_day_df_list,\
                                            samai_list=str(samai_list),\
                                            gamesuu_list=str(gamesuu_list),\
                                            samai_table = ave_tenpo_df.to_html(justify='justify-all',classes='tb01'),\
                                            groupby_kisyu_table = groupby_kisyubetu_df.to_html(justify='justify-all',classes='tb01',index=False))
    else:
        today = date.today()
        date_list = [today + timedelta(days=day) for day in range(1,9)]
        date_list = [date.strftime("%Y-%m-%d") for date in date_list]
        return render_template('target_date_recommend_schedule.html',date_list=date_list,tenpo_name=tenpo_name)

@app.route('/target-date-analytics', methods=['GET', 'POST'])
def target_date_analytics():
    from datetime import date, timedelta
    if request.method == 'POST':
        user_data = request.form
        print(user_data)
        print(user_data['tenpo-name'],user_data['n-times'],user_data['target-date'])
        target_day_list = []
        number = 0
        today = date.today()
        target_number:int = str(user_data['target-date'][-1])
        for i in range(int(user_data['n-times'])):
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

        with ThreadPoolExecutor(3) as executor:
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

        concat_df = pd.concat(concat_df_list,axis=0)
        for column_name in ['合成確率','BB確率','RB確率','台番号','ART確率']:
            try:
                concat_df = concat_df.drop([column_name],axis=1)
            except:
                pass
        
        concat_df = concat_df.groupby(['日付','機種名']).mean().sort_values('差枚',ascending=False)#機種毎に集計
        for column_name in ['差枚','G数','BB','RB','ART']:
            try:
                concat_df[column_name] = concat_df[column_name].astype(int)
            except:
                pass

        concat_df = concat_df.reset_index()
        
        print('concat_df',concat_df, flush=True)
        kisyubetu_master_df = concat_df.groupby(['機種名']).sum()
        kisyubetu_master_df['総台数'] = concat_df.groupby(['機種名']).size()
        kisyubetu_master_df = kisyubetu_master_df.reset_index(drop=False).reset_index().rename(columns={'index': '機種順位','ゲーム数': 'G数'})
        kisyubetu_master_df['機種順位'] = kisyubetu_master_df['機種順位'] + 1
        kisyubetu_master_df[['機種順位','機種名','総台数','G数','差枚']]
        kisyubetu_win_daissuu_list = []
        kisyubetu_master_df_list = []
        for kisyu_name in kisyubetu_master_df['機種名']:
            kisyu_df = concat_df.query('機種名 == @kisyu_name')
            kisyubetu_master_df_list.append(kisyu_df)
            kisyu_win_daisuu = len(kisyu_df[kisyu_df['差枚'] > 0])
            kisyubetu_win_daissuu_list.append(kisyu_win_daisuu)
        kisyubetu_master_df['勝率'] = kisyubetu_win_daissuu_list
        kisyubetu_master_df['勝率'] = kisyubetu_master_df['勝率'].astype(str)
        kisyubetu_master_df['総台数'] = kisyubetu_master_df['総台数'].astype(int)
        kisyubetu_master_df['平均G数'] = kisyubetu_master_df['G数'] / kisyubetu_master_df['総台数']
        kisyubetu_master_df['平均G数'] = kisyubetu_master_df['平均G数'].astype(int)
        kisyubetu_master_df = kisyubetu_master_df[kisyubetu_master_df['総台数'] >= 2 ]
        kisyubetu_master_df['差枚'] = kisyubetu_master_df['差枚'].astype(int)
        kisyubetu_master_df['平均差枚'] = kisyubetu_master_df['差枚'] / kisyubetu_master_df['総台数']
        kisyubetu_master_df['平均差枚'] = kisyubetu_master_df['平均差枚'].astype(int) 
        kisyubetu_master_df['総台数'] = kisyubetu_master_df['総台数'].astype(str) 
        kisyubetu_master_df['勝率'] = kisyubetu_master_df['勝率'] + '/' + kisyubetu_master_df['総台数']
        kisyubetu_master_df['勝率'] = kisyubetu_master_df['勝率'].map(lambda x : '(' + x + '台) ' + str(round(int(x.split('/')[0])/int(x.split('/')[1])*100,1))  + '%')
        kisyubetu_master_df = kisyubetu_master_df[['機種順位','機種名','勝率','平均G数','平均差枚','差枚','G数','総台数']]
        kisyubetu_master_df = kisyubetu_master_df.sort_values('平均差枚',ascending=False)
        kisyubetu_master_df['機種順位'] = list(range(1,len(kisyubetu_master_df)+1)) + '位'
        kisyubetu_master_df['機種平均出率'] =(((kisyubetu_master_df['G数'] * 3) + kisyubetu_master_df['差枚']) / (kisyubetu_master_df['G数'] * 3) )*100
        kisyubetu_master_df['機種平均出率'] = kisyubetu_master_df['機種平均出率'].map(lambda x : round(x,1))
        kisyubetu_master_df['機種平均出率'] = kisyubetu_master_df['機種平均出率'].astype(str) + '%'
        kisyubetu_master_df = kisyubetu_master_df.rename(columns={'機種順位':'お勧め順位','G数': '合計G数','差枚': '合計差枚'})
        kisyubetu_master_df

        target_day_list_jp = []
        for day in target_day_list:
            day = day.split('-')[1] + '/' + day.split('-')[2] 
            target_day_list_jp.append(day)
        target_day_list_jp.reverse
        
        
        return render_template('values.html',
                                            user_data=user_data,\
                                            column_names=concat_df_1.columns.values, \
                                            row_data=list(concat_df_1.values.tolist()),\
                                            zip=zip,target_day_list=str(target_day_list),
                                            target_day_list_jp=str(target_day_list_jp))
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=int(os.environ.get('PORT', 5000)))
