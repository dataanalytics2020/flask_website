#utf-8
from flask import Flask, render_template, request, redirect 
from flask_paginate import Pagination, get_page_parameter
from flask_caching import Cache
from flask_mail import Mail
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
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
import numpy as np
import html
load_dotenv()

#df:pd.DataFrame  = pd.read_csv(r'csv/2022-12-09_touhou.csv')
heroku_port:int = int(os.environ.get("PORT", 5000))

w_list = ['(月)', '(火)', '(水)', '(木)', '(金)', '(土)', '(日)']
prefecture_list:list[str] = '''北海道
,青森県,岩手県,宮城県,秋田県,山形県,福島県
,茨城県,栃木県,群馬県
,埼玉県,千葉県,東京都,神奈川県
,新潟県,富山県,石川県,福井県,山梨県,長野県
,岐阜県,静岡県,愛知県,三重県,滋賀県
,京都府,大阪府,兵庫県,奈良県,和歌山県
,鳥取県,島根県,岡山県,広島県
,徳島県,香川県,愛媛県,高知県
,山口県,福岡県,佐賀県,長崎県,熊本県,大分県,宮崎県,鹿児島県,沖縄県'''.replace('\n','').split(',')

prefecture_id_and_name_dict:dict = {}
for prefecture_id,prefecture_name in enumerate(prefecture_list):
    prefecture_id += 1
    prefecture_id_and_name_dict[prefecture_name]= prefecture_id
    
def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

# def convert_sql_date_to_jp_date(sql_date:datetime.date) -> str:
#     sql_str_date = str(sql_date)
#     return sql_str_date.split('-')[1].lstrip('0') + '月' + sql_str_date.split('-')[2].lstrip('0') + '日'
def convert_str_date_to_jp_date_and_weekday(target_date:str) -> str:
    target_date = datetime.datetime.strptime(target_date, '%Y-%m-%d')
    target_date = target_date .strftime('%m').lstrip('0') + '/' + target_date .strftime('%d').lstrip('0')  + w_list[target_date .weekday()]
    return target_date


def convert_sql_date_to_jp_date_and_weekday(sql_date:datetime.date) -> str:
    w_list = ['(月)', '(火)', '(水)', '(木)', '(金)', '(土)', '(日)']
    target_date = sql_date.strftime('%m').lstrip('0') + '/' + sql_date.strftime('%d').lstrip('0')  + w_list[sql_date.weekday()]
    return target_date

def get_sql_target_day_list_str(target_number:int) -> str:
    print('get_sql_target_day_list_str',target_number)
    today = date.today()
    target_day_list = []
    number = 0
    for i in range(3):
        while True:
            compare_day = today - timedelta(days=number)
            #print(compare_day)
            print(str(target_number),str(compare_day)[-1])
            if str(target_number) == str(compare_day)[-1]:
                target_day = today - timedelta(days=number)
                print('取得日',target_day)
                target_day_str = target_day.strftime('%Y-%m-%d')
                target_day_list.append(target_day_str)
                number += 1
                break
            else:
                pass
            number += 1
            #break
    target_day_list_str = str(tuple(target_day_list))
    print('target_day_list_str',target_day_list_str)
    # 引数が9なら → '("2024-01-09", "2023-12-29", "2023-12-19")'
    return target_day_list_str


def create_post_map_iframe(location_name_df,groupby_date_kisyubetu_df):

    try:
        prefecture_latitude = location_name_df.iloc[0]['latitude']
        prefecture_longitude = location_name_df.iloc[0]['longitude']
    except:
        prefecture_latitude = 35.681236
        prefecture_longitude = 139.767125
        
    print('新prefecture_latitude',prefecture_latitude,prefecture_longitude)

    folium_map = folium.Map(location=[prefecture_latitude,prefecture_longitude], zoom_start=10, width="100%", height="100%")
    # 地図表示
    # マーカープロット（ポップアップ設定，色変更，アイコン変更）
    print(location_name_df)
    rank_num = 0
    for i,row in location_name_df.iterrows():
        try:
            print("row",row)
            rank_num += 1
            tenpo_name = row['店舗名']
            print(tenpo_name)
            extract_syuzai_df_1 = groupby_date_kisyubetu_df[groupby_date_kisyubetu_df['店舗名'].str.contains(tenpo_name)]
            #display(extract_syuzai_df_1)
            print(extract_syuzai_df_1)
            #print(syuzai_rank_list)
            longitude = row['longitude']
            latitude = row['latitude']
            #print('latitude,longitude',latitude,longitude)
            # グレースケールの画像データを作成
            im= Image.new("L", (280, 100),color=(0))
            im.putalpha(0)
            im2= Image.new("L", (260, 50),color=(50))
            im2.putalpha(128)
            im3 = Image.open('icon.png')
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype('font/LightNovelPOPv2.otf',19)
            try:
                rank_num:int = int((extract_syuzai_df_1.index[0]/ 3) + 1)
                rank_num_str:str = f'お勧め店舗{rank_num}位'
            except:
                rank_num_str = 'お勧め店舗\n'
            syuzai_name_text = rank_num_str +'\n◆' + tenpo_name
            #print(syuzai_name_text)


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
            popup_df = extract_syuzai_df_1[['日付','差枚合計','平均差枚','平均G数','勝率']]
            #popup_df['イベント日'] = popup_df['イベント日'].apply(convert_sql_date_to_jp_date_and_weekday) 
            popup_df =   popup_df.to_html(escape=False,index=False,justify='center',classes='table table-striped table-hover table-sm')
            popup_df += f'<a href="#{tenpo_name}" target="_parent"> {tenpo_name} ※店舗詳細データに飛びます</a>'
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
                            shadow_anchor = (-4, -4),
                            popup_anchor = (3, 3))).add_to(folium_map)
            #break
        except:
            post_line(f'create_post_map_iframeでエラー発生。{row["prefecture"]} {tenpo_name}の位置情報がありません\n{tenpo_name}')
            pass
    # set the iframe width and height
    plugins.Fullscreen(
                        position="topright",
                        title="拡大する",
                        title_cancel="元に戻す",
                        force_separate_button=True,
                    ).add_to(folium_map)
    folium_map.get_root().width = "500px"
    folium_map.get_root().height = "500px"
    return folium_map.get_root()._repr_html_()

def create_syuzai_map_iframe(report_df:pd.DataFrame,pref_name_en:str):
    report_df = report_df.drop_duplicates(keep='first')
    report_df = report_df.dropna(subset=['latitude'])
    
    #今日より前の日付のデータを削除
    furture_exist_hall_name_list  = list(report_df[report_df['イベント日'] >= datetime.date.today()]['店舗名'].unique())
    print('furture_exist_hall_name_list',furture_exist_hall_name_list)
    #(取材ランク = 'S' OR 取材ランク = 'A')のみ抽出
    map_report_df = report_df[['店舗名','取材名','媒体名']].drop_duplicates(keep='first')
    map_report_df = map_report_df.sort_values(['店舗名','媒体名']).reset_index(drop=True)
    #東京都に設定
    try:
        prefecture_latitude = report_df.iloc[0]['latitude']
        prefecture_longitude = report_df.iloc[0]['longitude']
    except:
        prefecture_latitude = 35.681236
        prefecture_longitude = 139.767125
        
    print('新prefecture_latitude',prefecture_latitude,prefecture_longitude)

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
        #print('latitude,longitude',latitude,longitude)
        if len(extract_syuzai_df_1)==1:
            syuzai_name_text = '◆' + tenpo_name + f'\n {extract_syuzai_df_1["取材名"].values[0]}'
        else:
            syuzai_name_text = '◆' + tenpo_name + f'\n {extract_syuzai_df_1["取材名"].values[0]}、他{len(extract_syuzai_df_1)-1}件'
        #print(syuzai_name_text)
        # グレースケールの画像データを作成
        im= Image.new('RGBA', (260, 100),color=(0))
        im.putalpha(0)
        im2= Image.new('RGBA', (230, 35),color=(0))
        im2.putalpha(128)
        im.paste(im2, (15,48))
        #print(syuzai_name_text)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype('font/LightNovelPOPv2.otf',13)
        draw = ImageDraw.Draw(im)
        draw.multiline_text(
            (130, 50),
            f'{syuzai_name_text}',
            font=font,
            fill='white',
            align='center',
            spacing=0,
            anchor='ma'
        )

        #背景と同サイズの透明な画像を生成
        img_clear = Image.new("RGBA", im.size, (255, 255, 255, 0))
        if tenpo_name in furture_exist_hall_name_list:
            im3 = Image.open('icon.png')
        else:
            im3 = Image.open('icon_gray.png')
        #透明画像の上にペースト
        img_clear.paste(im3, (-10, -10))
        #重ね合わせる
        bg = Image.alpha_composite(im, img_clear)
        bg.save('syuzai_image.png')
        img = 'syuzai_image.png'
        popup_df = extract_syuzai_df_1[['イベント日','店舗名','取材名','媒体名']].sort_values('店舗名')
        furture_popup_df = popup_df[popup_df['イベント日'] >= datetime.date.today()]
        past_popup_df = popup_df[popup_df['イベント日'] < datetime.date.today()]
        furture_popup_df['イベント日'] = furture_popup_df['イベント日'].apply(convert_sql_date_to_jp_date_and_weekday) 
        past_popup_df['イベント日'] = past_popup_df['イベント日'].apply(convert_sql_date_to_jp_date_and_weekday) 
        #popup_df['イベント日'] = popup_df['イベント日'].apply(convert_sql_date_to_jp_date_and_weekday) 
        popup_df = ''
        if len(furture_popup_df) != 0:
            popup_df += '<h4 class="my-2">◆取材予定(※直近一週間分表示中)</h4>\n'
            popup_df += furture_popup_df.to_html(escape=False,index=False,justify='center',classes='display compact nowrap table table-striped table-hover table-sm')
        if len(past_popup_df) != 0:
            popup_df += '<h4 class="my-2">◆過去取材</h4>\n'
            popup_df += past_popup_df.to_html(escape=False,index=False,justify='center',classes='display compact nowrap table table-striped table-hover table-sm')
        popup_df +=f'<a href="/tomorrow_recommend/{pref_name_en}/hall/{tenpo_name}"  target="_parent">{tenpo_name}※店舗詳細ページに飛びます </a>'
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
    folium_map.get_root().height = "500px"
    return folium_map.get_root()._repr_html_()

def create_media_map_iframe(report_df:pd.DataFrame,pref_name_jp:str,past_diffcoins_df:pd.DataFrame=None):
    print('pref_name_jp',pref_name_jp)
    try:
        pref_name_en = prefecture_df[prefecture_df['pref_name'] == pref_name_jp]['pref_name_en'].values[0]
    except:
        pref_name_en = prefecture_df[prefecture_df['area_name_jp'] == pref_name_jp]['area_name_en'].values[0]
        
    furture_exist_hall_name_list  = list(report_df[report_df['イベント日'] >= datetime.date.today()]['店舗名'].unique())
    print('furture_exist_hall_name_list',furture_exist_hall_name_list)
    report_df = report_df.dropna(subset=['latitude'])
    report_df.drop_duplicates(keep='first',inplace=True)
    print('report_df',report_df)
    #(取材ランク = 'S' OR 取材ランク = 'A')のみ抽出
    print('report_df',report_df)
    map_report_df = report_df[['店舗名','取材名','媒体名']]
    map_report_df = map_report_df.sort_values(['店舗名','媒体名']).reset_index(drop=True)
    map_report_df.drop_duplicates(keep='first',inplace=True)
    print('map_report_df',map_report_df)

    try:
        prefecture_latitude = report_df.iloc[0]['latitude']
        prefecture_longitude = report_df.iloc[0]['longitude']
    except:
        prefecture_latitude = 35.681236
        prefecture_longitude = 139.767125
    folium_map = folium.Map(location=[prefecture_latitude,prefecture_longitude], zoom_start=10, width="100%", height="100%")
    # 地図表示
    # マーカープロット（ポップアップ設定，色変更，アイコン変更）
    #print(report_df)
    for tenpo_name in report_df['店舗名'].unique():
        #print(tenpo_name)
        extract_syuzai_df_1 = report_df[report_df['店舗名'] == tenpo_name]
        extract_syuzai_df_1.drop_duplicates(keep='first',inplace=True)
        #display(extract_syuzai_df_1)
        #print(extract_syuzai_df_1)
        syuzai_rank_list = list(extract_syuzai_df_1['取材ランク'].unique())
        #print(syuzai_rank_list)
        longitude = extract_syuzai_df_1.iloc[0]['longitude']
        latitude = extract_syuzai_df_1.iloc[0]['latitude']
        #print('latitude,longitude',latitude,longitude)
        # グレースケールの画像データを作成
        if len(extract_syuzai_df_1)==1:
            syuzai_name_text = '◆' + tenpo_name + f'\n {extract_syuzai_df_1["取材名"].values[0]}'
        else:
            syuzai_name_text = '◆' + tenpo_name + f'\n {extract_syuzai_df_1["取材名"].values[0]}、他{len(extract_syuzai_df_1)-1}件'

        # グレースケールの画像データを作成
        im= Image.new('RGBA', (260, 100),color=(0))
        im.putalpha(0)
        im2= Image.new('RGBA', (230, 35),color=(0))
        im2.putalpha(128)
        im.paste(im2, (15,48))
        #print(syuzai_name_text)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype('font/LightNovelPOPv2.otf',13)
        draw = ImageDraw.Draw(im)
        draw.multiline_text(
            (130, 50),
            f'{syuzai_name_text}',
            font=font,
            fill='white',
            align='center',
            spacing=0,
            anchor='ma'
        )

        #背景と同サイズの透明な画像を生成
        img_clear = Image.new("RGBA", im.size, (255, 255, 255, 0))
        if tenpo_name in furture_exist_hall_name_list:
            im3 = Image.open('icon.png')
        else:
            im3 = Image.open('icon_gray.png')
        #透明画像の上にペースト
        img_clear.paste(im3, (-10, -10))
        #重ね合わせる
        bg = Image.alpha_composite(im, img_clear)
        bg.save('syuzai_image.png')
        img = 'syuzai_image.png'
        popup_df = extract_syuzai_df_1[['イベント日','店舗名','取材名','媒体名']].sort_values('店舗名')#.reset_index(drop=True).T
        popup_df.drop_duplicates(keep='first',inplace=True)
        popup_df['イベント日'] = popup_df['イベント日'].apply(convert_sql_date_to_jp_date_and_weekday) 
        popup_df = popup_df.to_html(escape=False,index=False,justify='center',classes='table-striped table-sm')
        if past_diffcoins_df is not None:
            extract_past_diffcoins_df = past_diffcoins_df[past_diffcoins_df['店舗名'] == tenpo_name]
            extract_past_diffcoins_df.drop_duplicates(keep='first',inplace=True)
            popup_df += extract_past_diffcoins_df.to_html(escape=False,index=False,justify='center',classes='table-striped table-sm')

        popup_df +=f'<a href="/tomorrow_recommend/{pref_name_en}/hall/{tenpo_name}"  target="_parent">{tenpo_name}※店舗詳細ページに飛びます </a>'
        popup_df +='''<a class="leaflet-popup-close-button" role="button" aria-label="Close popup" href="#close">
        <span aria-hidden="true">✖</span>
</a>'''
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
    folium_map.get_root().height = "500px"
    return folium_map.get_root()._repr_html_()

def create_hall_map_iframe(extract_hall_name_df,zoom_size=10):
    longitude = extract_hall_name_df.iloc[0]['longitude']
    latitude = extract_hall_name_df.iloc[0]['latitude']
    folium_map = folium.Map(location=[latitude,longitude], zoom_start=zoom_size, width="100%", height="100%")
    tenpo_name = list(extract_hall_name_df['店舗名'].unique())[0]
    # グレースケールの画像データを作成
    im= Image.new("L", (280, 100),color=(0))
    im.putalpha(0)
    im2= Image.new("L", (260, 50),color=(50))
    im2.putalpha(128)
    im3 = Image.open('icon.png')
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('font/LightNovelPOPv2.otf',19)
    syuzai_name_text = '◆' + tenpo_name 

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
    folium.Marker(location=[latitude ,longitude],
        tiles='https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',
        attr='国土地理院',
        icon = CustomIcon(
                    icon_image = img,
                    icon_size = (280, 100),
                    icon_anchor = (0, 0),
                    #shadow_image = shadow_img, # 影効果（今回は使用せず コメントアウト
                    #shadow_size = (30, 30),
                    shadow_anchor = (-4, -40),
                    popup_anchor = (3, 3))).add_to(folium_map)
    # set the iframe width and height
    plugins.Fullscreen(
                        position="topright",
                        title="拡大する",
                        title_cancel="元に戻す",
                        force_separate_button=True,
                    ).add_to(folium_map)
    folium_map.get_root().width = "500px"
    folium_map.get_root().height = "500px"
    return folium_map.get_root()._repr_html_()

def get_area_prefecture_list(target_area_name):
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
            print(target_area_name_list)
            break
    return target_area_name_list

def get_prefecture_area_list(prefecture_name):
    print(prefecture_name)
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
        target_area_name_list = eval(prefecture_list_name)
        if prefecture_name in target_area_name_list:
            print('ok',prefecture_list_name)
            area_name = prefecture_list_name.replace('_list','')
            if area_name == 'hokkaidoutouhoku':
                area_name_jp = '北海道・東北'
                area_name_url = 'hokkaidoutouhoku'
            elif area_name == 'kitakantou':
                area_name_jp = '北関東'
                area_name_url = 'kitakantou'
            elif area_name == 'minamikantou':
                area_name_jp = '南関東'
                area_name_url = 'minamikantou'
            elif area_name == 'hokurikukoushinetsu':
                area_name_jp = '北陸・甲信越'
                area_name_url = 'hokurikukoushinetsu'
            elif area_name == 'toukai':
                area_name_jp = '東海'
                area_name_url = 'toukai'
            elif area_name == 'kansai':
                area_name_jp = '関西'
                area_name_url = 'kansai'
            elif area_name == 'chugokushikoku':
                area_name_jp = '中国・四国'
                area_name_url = 'chugokushikoku'
            elif area_name == 'kyushu':
                area_name_jp = '九州・沖縄'
                area_name_url = 'kyushu'
            else:
                area_name_jp = '情報なし'
            break
    return area_name_jp,area_name_url

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
    global conn
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

def convert_date(date):
    date:str = str(date).split('-')
    date = date[1].lstrip('0') + '/' + date[2].lstrip('0')
    return date

def post_line(message):
    url = "https://notify-api.line.me/api/notify"
    token = os.environ['LINE_TOKEN']
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}
    post = requests.post(url ,headers = headers ,params=payload)

def generate_past_data_n_day_sql_text(n_day:int,today:datetime.date) -> str:
    target_day = today + datetime.timedelta(days=n_day)
    target_day_str = target_day.strftime('%Y-%m-%d')
    sql_date_text = ''
    for i in range(39):
        belong_day = today - datetime.timedelta(days= i)
        belong_day_str = belong_day.strftime('%Y-%m-%d')
        ##print(belong_day_str[-2:])
        if belong_day_str[-1] == target_day_str[-1]:
            if belong_day_str[-2:] == '31':
                continue
            day_str = belong_day.strftime('%m月%d日').lstrip('0')
            belong_day_str
            sql_date_text += f"'{belong_day_str}'" + ',' 
    sql_date_text = sql_date_text.rstrip(',')
    print(sql_date_text)
    return sql_date_text
area_name_and_str_jp_area_name_dict = {'hokkaidoutouhoku':'北海道・東北', 'kitakantou':'北関東','minamikantou':'南関東','hokurikukoushinetsu':'北陸・甲信越','toukai':'東海','kansai':'関西','chugokushikoku':'中国・四国','kyushu':'九州・山口'}

config = {
    "DEBUG": False,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
app.config.from_mapping(config)
cache = Cache(app)

#都道府県テーブルの読み込み
prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
area_str_list = ['hokkaidoutouhoku', 'kitakantou','minamikantou','hokurikukoushinetsu','toukai','kansai','chugokushikoku','kyushu']

@app.route('/', methods=['GET'])
@cache.cached(timeout=300)
def get_top():
    data = {}
    data['prefecture_list'] = prefecture_list
    today = datetime.datetime.utcnow().today()
    print('today',today)
    jp_str_day_list = []
    for i in range(0,7):
        day = today + timedelta(days=i)
        jp_str_day = day.strftime('%m').lstrip('0') + '月' + day.strftime('%d').lstrip('0') + '日' + w_list[day.weekday()]
        jp_str_day_list.append(jp_str_day)
    data['jp_str_day_list'] = jp_str_day_list
    tomorrow:date = today + timedelta(days=1)
    #today = datetime.datetime.utcnow().today()
    target_n_day_str = tomorrow.strftime('%Y-%m-%d')[-1]
    print('target_n_day_str',target_n_day_str)
    datetime64_tomorrow = np.datetime64(tomorrow)
    print(tomorrow)
    tommorow_jp_str_day = tomorrow.strftime('%m').lstrip('0') + '月' + tomorrow.strftime('%d').lstrip('0') + '日' + w_list[tomorrow.weekday()]
    print(tommorow_jp_str_day)
    data['tommorow_jp_str_day'] =  tommorow_jp_str_day
    data['prefecture_id_and_name_dict'] = prefecture_id_and_name_dict
    report_df = pd.read_csv('csv/kanto_top_location_df.csv', parse_dates=['イベント日'])
    try:
        report_row_1 = str(report_df[:1]["イベント日"].values[0]).split('T')[0]
        print(report_row_1)
    except:
        report_row_1 = 'NONE'
    compare_date:str = tomorrow.strftime('%Y-%m-%d')#-%d
    if str(report_row_1) == str(compare_date):
        print('今日のデータは取得済み'+report_row_1+"と"+compare_date)
        post_line('今日のデータは取得済み'+report_row_1+"と"+compare_date)
        post_line('report_df' + str(report_row_1))
    else:
        post_line('今日のデータは未取得'+report_row_1+"と"+compare_date)
        area_sql_text = get_area_sql_text('minamikantou')
        cursor = get_driver()
        sql = f'''SELECT イベント日,都道府県,店舗名,取材名,取材ランク,媒体名,latitude,longitude
                FROM schedule as schedule2
                left join halldata as halldata2
                on schedule2.店舗名 = halldata2.hall_name
                WHERE イベント日 > current_date
                AND イベント日 <= current_date + 1
                AND 媒体名 != 'ホールナビ'
                AND 取材名 LIKE '%{target_n_day_str}のつく日%'
                AND 都道府県 = '東京都'
                ORDER BY イベント日,都道府県,店舗名,媒体名,取材名 desc;'''#AND (取材ランク = 'S' OR 取材ランク = 'A')
        print(sql)
        cursor.execute(sql)
        cols = [col[0] for col in cursor.description]
        print('cols',cols)
        report_df =  pd.DataFrame(cursor.fetchall(),columns = cols )
        report_df = report_df.loc[:,~report_df.columns.duplicated()]
        print(report_df)
        sql_hall_name_text = ''
        for hall_name_text in list(report_df['店舗名'].unique()):
            sql_hall_name_text += f"'{hall_name_text}'" + ','
        sql_hall_name_text = sql_hall_name_text.rstrip(',')
        sql_date_text = get_sql_target_day_list_str(int(target_n_day_str))
        print('sql_date_text',sql_date_text)
        if report_df.empty:
            post_line('empty error'+report_row_1+"と"+compare_date)
            sql_hall_name_text = "'マルハン池袋店'"
        sql = f"""SELECT date,hall_name,sum_diffcoins,ave_diffcoins,ave_game,win_rate
               FROM groupby_date_hall_diffcoins
               WHERE date in {sql_date_text}
               AND hall_name in  ({sql_hall_name_text})"""
        print('sql',sql)
        cursor.execute(sql)
        print("sql_hall_name_text",sql_hall_name_text)
        cols = [col.name for col in cursor.description]
        past_diffconis_df = pd.DataFrame(cursor.fetchall(),columns=cols)
        past_diffconis_df['date'] = past_diffconis_df['date'].apply(convert_sql_date_to_jp_date_and_weekday)
        past_diffconis_df.rename(columns={'date':'日付','hall_name':'店舗名','sum_diffcoins':'総差枚','ave_diffcoins':'平均差枚','ave_game':'平均G数','win_rate':'勝率'},inplace=True)
        past_diffconis_df['平均差枚'] = past_diffconis_df['平均差枚'].astype(str) + '枚'
        past_diffconis_df['総差枚'] = past_diffconis_df['総差枚'].map(lambda x: round(x,-2)).astype(str) + '枚'
        past_diffconis_df['平均G数'] = past_diffconis_df['平均G数'].astype(str) + 'G'
        post_line('report_df'+str(report_row_1))
        report_df.to_csv('csv/kanto_top_location_df.csv',index=False)
        past_diffconis_df.to_csv('csv/tokyo_past_diffconis_df.csv',index=False)

    all_kanto_display_df = report_df = report_df.drop_duplicates(keep='first')
    if str(report_row_1) != str(compare_date):
        post_line('今日のデータはマップ未取得'+report_row_1+"と"+compare_date)
        report_df['イベント日'] = pd.to_datetime(report_df['イベント日'])
        latitude_isnull_df = report_df[report_df['latitude'].isnull()]
        message = ''
        if len(latitude_isnull_df) > 0:
            for isnull_hall_name in latitude_isnull_df['店舗名'].unique():
                message += f'{isnull_hall_name}の緯度経度が取得できていません。\n'
            post_line(message)
        report_df = report_df.dropna(subset=['latitude'])
        tomorrow_report_df = report_df
        #(取材ランク = 'S' OR 取材ランク = 'A')のみ抽出
        #report_df =  report_df[report_df['取材ランク'].isin(['S','A'])]
        #print('report_df_2',report_df)
        map_report_df = report_df#[report_df['イベント日'] == datetime64_tomorrow ]
        tomorrow_report_df = report_df
        #print('map_report_df',map_report_df)
        map_report_df = map_report_df[['店舗名','取材名','媒体名']].drop_duplicates(keep='first')
        map_report_df = map_report_df.sort_values(['店舗名','媒体名']).reset_index(drop=True)

        #東京都に設定
        prefecture_latitude = 35.68944
        prefecture_longitude = 139.69167

        folium_map = folium.Map(location=[prefecture_latitude,prefecture_longitude], zoom_start=10, width="100%", height="100%")
        # 地図表示
        # マーカープロット（ポップアップ設定，色変更，アイコン変更）
        print('map_report_df',map_report_df)
        print('past_diffconis_df',past_diffconis_df.columns)
        for tenpo_name in map_report_df['店舗名'].unique():
            #print(tenpo_name)
            extract_syuzai_df_1 = tomorrow_report_df[tomorrow_report_df['店舗名'] == tenpo_name]
            #extract_syuzai_df_1 = extract_syuzai_df_1[extract_syuzai_df_1['イベント日'] == datetime64_tomorrow ]
            extract_syuzai_df_1.drop_duplicates(keep='first',inplace=True)
            #display(extract_syuzai_df_1)
            #print('extract_syuzai_df_1',extract_syuzai_df_1)
            #syuzai_rank_list = list(extract_syuzai_df_1['取材ランク'].unique())
            #print(syuzai_rank_list)
            try:
                longitude = extract_syuzai_df_1.iloc[0]['longitude']
                latitude = extract_syuzai_df_1.iloc[0]['latitude']
                #print('latitude,longitude',latitude,longitude)
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
                popup_df = extract_syuzai_df_1[['イベント日','店舗名','媒体名','取材名']].sort_values('店舗名')#.reset_index(drop=True)#.T
                popup_df['イベント日'] = popup_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
                popup_df_html = popup_df.to_html(escape=False,index=False,table_id="mystyle",justify='center',classes='table table-striped table-hover table-sm')
                extract_hall_df = past_diffconis_df[past_diffconis_df['店舗名'] == tenpo_name]
                if len(extract_hall_df) == 0:
                    continue
                popup_df_html += extract_hall_df.to_html(escape=False,index=False,table_id="mystyle",justify='center',classes='table table-striped table-hover table-sm')
                popup_df_html +=f'<a href="/tomorrow_recommend/tokyo/hall/{tenpo_name}"  target="_parent">{tenpo_name}※店舗詳細ページに飛びます </a>'
                popup_data = folium.Popup(popup_df_html,  max_width=1500,show=False,size=(700, 300))

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

            except:
                print(tenpo_name,'の緯度経度が取得できていません。')
                pass
            
        plugins.Fullscreen(
                position="topright",
                title="拡大する",
                title_cancel="元に戻す",
                force_separate_button=True,
            ).add_to(folium_map)
        folium_map.get_root().width = "500px"
        folium_map.get_root().height = "500px"
        map_test_html = folium_map.get_root()._repr_html_()
        #data['iframe'] = folium_map.get_root()._repr_html_()
        top_map_html = folium_map.get_root().render()
        #top_map.html = html.unescape(map_ top_html)
        with open('templates/top_map.html', mode='w', encoding='utf-8') as f:
            f.write(top_map_html)
    else:
        print('今日のデータは取得済み'+report_row_1+"と"+compare_date)
        post_line('今日のデータはマップ取得済み'+report_row_1+"と"+compare_date)
        #pass
        with open('templates/top_map.html', mode='r', encoding='utf-8') as f:
            top_map_html = f.read()

    prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
    data['pref_name_en'] = pref_name_en = 'tokyo'
    data['pref_name_jp'] = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['pref_name'].values[0]
    #print('pref_name_en',pref_name_en)  
    #print('data',data) 
    # アクセス情報の設定
    SITE_URL = os.getenv('WORDPRESS_PACHISLO7_URL')
    API_URL = f"{SITE_URL}/wp-json/wp/v2/"
    AUTH_USER = os.getenv('WORDPRESS_PACHISLO7_ID')
    AUTH_PASS = os.getenv('WORDPRESS_PACHISLO7_PW')

    #下書き状態の記事を取得
    #画像は取得するがurl以外は取得しない
    post_slug = f'tokyo_{compare_date}'
    label = f'posts?slug={post_slug}&status=draft&_embed'
    url = f"{API_URL}{label}"
    # すべてのアイテムを取得
    #print(url)
    res = requests.get(url, auth=(AUTH_USER, AUTH_PASS)).json()
    #print(res)
    thumbnail_url = res[0]['_embedded']['wp:featuredmedia'][0]['source_url']
    #print('thumbnail_url',thumbnail_url)
    data['thumbnail_url'] = thumbnail_url
    parameter_id = res[0]['id']
    data['post_slug'] = post_slug
    data['target_date_md'] = 'tokyo_' + post_slug.split('_')[1].split('-')[1] + post_slug.split('_')[1].split('-')[2]
    #print('parameter_id',parameter_id)
    write_html = res[0]['content']['rendered'].split('ここまで')[-1]
    content = res[0]['content']['rendered'].split('ここまで')[0]
    data['title'] = res[0]['title']['rendered']
    dfs = pd.read_html(content)
    #print('dfs',dfs)
    data['write_html'] = write_html
    
    #data['tag_df'] = tag_df.to_html(justify='justify-all',classes='tb01')
    dfs = pd.read_html(content)
    groupby_date_kisyubetu_df = dfs[0]
    location_name_df = dfs[1]
    recommend_hall_name_list = list(location_name_df['店舗名'].unique())
    data['recommend_hall_name_list'] = recommend_hall_name_list
    
    display_report_df = all_kanto_display_df[['イベント日','都道府県','店舗名','媒体名','取材名']].sort_values(['イベント日','都道府県','店舗名','媒体名','取材名'],ascending=[True,False,True,True,False],inplace=False).reset_index(drop=True)
    #print(display_report_df)
    display_report_df = display_report_df.drop_duplicates(keep='first')
    display_report_df['イベント日'] = pd.to_datetime(display_report_df['イベント日'])
    display_report_df['イベント日'] = display_report_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    display_report_df.rename(columns={'イベント日':'日','都道府県':'県'},inplace=True)
    #display_report_df.sort_values(['イベント日','都道府県','店舗名','媒体名','取材名'],ascending=[True,False,True,True,False],inplace=True)
    data['display_report_df_column_names'] = display_report_df.columns.values
    data['display_report_df'] = display_report_df
    data['display_report_df_row_data'] = list(display_report_df.values.tolist())
    data['area_name'] = 'minamikantou'
    data['area_name_jp'] = area_name_and_str_jp_area_name_dict['minamikantou']
    return render_template('top.html',data=data,zip=zip)

@app.route("/show_iframe")
def show_iframe():
    return render_template("top_map.html")

@app.route('/', methods=['POST'])
def post_top():
    user_data = request.form
    today = datetime.date.today()
    print('user_data',user_data)
    prefecture_id = int(user_data['pref_id'])
    print('prefecture_id',prefecture_id,type(prefecture_id))
    prefecture = get_key_from_value(prefecture_id_and_name_dict, prefecture_id)
    print(prefecture)
    area_name_jp,area_name = get_prefecture_area_list(prefecture)
    print(area_name_jp,area_name)
    data = {}
    data['prefecture_name'] = prefecture
    data['area_name_jp'] = area_name_jp
    data['area_name'] = area_name
    print('dataは',data)
    target_month =  int(f"{user_data['target_day'].split('月')[0]}")
    print(target_month,type(target_month))
    #target_monthを2桁にする
    target_month =  f'{target_month:02}' 
    target_day = int(user_data['target_day'].split('月')[1].split('日')[0])
    target_day_str = str(target_day)[-1]
    target_day  = f'{target_day:02}'
    target_date = str(today.year) + '-' + target_month  + '-' + target_day
    data['tommorow_jp_str_day'] = target_month.lstrip('0') + '月' + target_day.lstrip('0') + '日'
    #print(prefecture,target_day)
    #イベント日,店舗名,取材名,媒体名,アナスロ店舗名
    cursor = get_driver()
    print('prefectureは',prefecture)
    cursor.execute(f'''SELECT *
                FROM schedule as schedule2
                left join halldata as halldata2
                on schedule2.店舗名 = halldata2.hall_name
                WHERE イベント日 = '{target_date}'
                AND 媒体名 != 'ホールナビ'
                AND 都道府県 = '{prefecture}'
                ORDER BY イベント日,都道府県 desc;''')
    cols = [col.name for col in cursor.description]
    extract_prefecture_name_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    extract_prefecture_name_df.drop_duplicates(keep='first',inplace=True)
    #差枚テーブルの取得
    sql_hall_name_text = ''
    for hall_name_text in list(extract_prefecture_name_df['店舗名'].unique()):
        sql_hall_name_text += f"'{hall_name_text}'" + ','
    sql_hall_name_text = sql_hall_name_text.rstrip(',')
    #sql_date_text = generate_past_data_n_day_sql_text(1,today)
    target_number:int = int(target_day_str)
    diffcoins_sql_date_str = get_sql_target_day_list_str(target_number)
    print('diffcoins_sql_date_str',diffcoins_sql_date_str)
    print()
    sql=f"""SELECT date,hall_name,sum_diffcoins,ave_diffcoins,ave_game,win_rate
            FROM groupby_date_hall_diffcoins
            WHERE date in {diffcoins_sql_date_str}
            AND hall_name in  ({sql_hall_name_text})
            ORDER BY date DESC"""
    print(sql)
    cursor.execute(sql)
    print("sql_hall_name_text",sql_hall_name_text)
    cols = [col.name for col in cursor.description]
    past_diffconis_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    past_diffconis_df['date'] = past_diffconis_df['date'].apply(convert_sql_date_to_jp_date_and_weekday)
    past_diffconis_df.rename(columns={'date':'日付','hall_name':'店舗名','sum_diffcoins':'総差枚','ave_diffcoins':'平均差枚','ave_game':'平均G数','win_rate':'勝率'},inplace=True)
    past_diffconis_df['平均差枚'] = past_diffconis_df['平均差枚'].astype(str) + '枚'
    past_diffconis_df['総差枚'] = past_diffconis_df['総差枚'].map(lambda x: round(x,-2)).astype(str) + '枚'
    past_diffconis_df['平均G数'] = past_diffconis_df['平均G数'].astype(str) + 'G'
    print('past_diffconis_df',past_diffconis_df)
    table_df = extract_prefecture_name_df[['イベント日','店舗名','媒体名','取材名']]
    table_df['イベント日'] = table_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    table_df = table_df.sort_values(['イベント日','店舗名','媒体名','取材名'],ascending=[True,True,True,True],inplace=False).reset_index(drop=True)
    table_df.rename(columns={'イベント日':'日'},inplace=True)
    table_df.drop_duplicates(keep='first',inplace=True)
    #print(table_df)
    prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
    data['pref_name_jp'] = prefecture_name
    data['pref_name_en'] = pref_name_en = prefecture_df[prefecture_df['pref_name'] == prefecture]['pref_name_en'].values[0]
    #print('data',data) 
    # アクセス情報の設定
    SITE_URL = os.getenv('WORDPRESS_PACHISLO7_URL')
    API_URL = f"{SITE_URL}/wp-json/wp/v2/"
    AUTH_USER = os.getenv('WORDPRESS_PACHISLO7_ID')
    AUTH_PASS = os.getenv('WORDPRESS_PACHISLO7_PW')

    #下書き状態の記事を取得
    #画像は取得するがurl以外は取得しない
    print('pref_name_en',pref_name_en) 
    post_slug = f'{pref_name_en}_{target_date}'
    label = f'posts?slug={post_slug}&status=draft&_embed'
    url = f"{API_URL}{label}"
    # すべてのアイテムを取得
    print(data)
    print('url',url)
    
    res = requests.get(url, auth=(AUTH_USER, AUTH_PASS)).json()
    #print('res',res)
    thumbnail_url = res[0]['_embedded']['wp:featuredmedia'][0]['source_url']
    #print('thumbnail_url',thumbnail_url)
    data['thumbnail_url'] = thumbnail_url
    parameter_id = res[0]['id']
    data['post_slug'] = post_slug
    print('pref_name_en',pref_name_en)
    print('post_slug',post_slug)
    data['target_date_md'] = post_slug
    #print('parameter_id',parameter_id)
    
    data['iframe'] = create_media_map_iframe(extract_prefecture_name_df,area_name='minamikantou',past_diffcoins_df=past_diffconis_df)
    data['extract_prefecture_name_df'] = table_df
    data['extract_prefecture_name_df_column_names'] = table_df.columns.values
    data['extract_prefecture_name_df_row_data'] = list(table_df.values.tolist())
    return render_template('tomorrow_recommend_area_prefecture_prefecturename.html',data=data,zip=zip)

@app.route("/post_heatmap", methods=['POST'])
def post_heatmap():
    data = {}
    target_date_text = request.form["target-date"]
    print(type(target_date_list))
    hall_name = request.form["hall-name"]
    target_date_list = target_date_text.replace('/','-').split(', ')
    target_date_list
    data['target_date_list'] = target_date_list
    data['hall_name'] = hall_name

    return render_template('test_post.html',data=data)



@app.route('/heatmap', methods=['POST'])#<prefecture>/<tenpo_name>
def heatmap_test():#prefecture,tenpo_name
    from datetime import date, timedelta
    data = {}
    tenpo_name = request.form["hall-name"]
    data['tenpo_name'] = tenpo_name
    target_day_list = request.form["target-date"].replace('/','-').split(', ')
    target_day_list.reverse()
    print(target_day_list)
    concat_df_list = []
    urls = []
    for serch_date in target_day_list:
        search_url = url = f"https://ana-slo.com/{serch_date}-{tenpo_name}-data/"
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
    concat_df = pre_concat_df =pd.concat(concat_df_list,axis=0)
    print(concat_df.head())
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
    print(horizon_concat_df.head())
    horizon_concat_df_html = re.sub(' target', '" id="target', horizon_concat_df.to_html(classes='target',index=False))
    return render_template('test.html',horizon_concat_df = horizon_concat_df_html,\
                                        zip=zip,\
                                        heatmap_column_names=horizon_concat_df.columns.values, \
                                        heatmap_row_data=list(horizon_concat_df.values.tolist()) )

@app.route('/recommend', methods=['GET', 'POST'])
def select_recommend_area():
    return render_template('target_date_recommend_top.html')

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

@app.route('/target_date_recommend_report', methods=['POST'])
def target_date_recommend_report():
    from datetime import date, timedelta
    user_data = {}
    tenpo_name = request.form["hall-name"]
    user_data['tenpo-name'] = tenpo_name
    target_day_list = request.form["target-date"].replace('/','-').split(', ')
    serch_number:int = len(target_day_list)
    print(target_day_list)
    concat_df_list = []
    urls = []
    for serch_date in target_day_list:
        search_url = url = f"https://ana-slo.com/{serch_date}-{tenpo_name}-data/"
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
                df['機種名'] = df['機種名'].map(lambda x: x \
                    .replace('[前編]始まりの物語/[後編]永遠の物語','') \
                    .replace('劇場版','') \
                    .replace('解き放たれし','') \
                    .replace('もっと！',''))
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
        groupby_date_df['機種名'] = groupby_date_df['台番号'] + '番_' + groupby_date_df['機種名']
        groupby_date_df = groupby_date_df.drop(['台番号'],axis=1)
        column_date_name:str = groupby_date_df['日付'].loc[0].split('-')[1].lstrip('0') + '/' + groupby_date_df['日付'].loc[0].split('-')[2].lstrip('0')
        groupby_date_df = groupby_date_df.drop(['日付'],axis=1)
        groupby_date_df = groupby_date_df.rename(columns={'機種名':column_date_name+'_台番号_機種名','G数':column_date_name+'_G数','差枚':column_date_name + '_差枚'})
        #display(groupby_date_df)
        groupby_date_df.reset_index(drop=True,inplace=True)
        horizon_concat_list.append(groupby_date_df)

    horizon_concat_df = pd.concat(horizon_concat_list,axis=1)
    horizon_concat_df_html = re.sub(' target', '" id="target', horizon_concat_df.to_html(classes='compact nowrap',index=False))

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
    concat_df = groupby_date_kisyubetu_df
    print('concat_df',concat_df)
    display_day_df_list = []
    
    for target_day in target_day_list:
        #target_day = target_day.split('-')[1].lstrip('0') + '/' + target_day.split('-')[2].lstrip('0') 
        print('target_day',target_day)
        extract_groupby_day_df = groupby_date_kisyubetu_df[groupby_date_kisyubetu_df['日付'] == target_day]
        print(extract_groupby_day_df)
        extract_groupby_day_df['日付'] = extract_groupby_day_df['日付'].map(convert_date)
        extract_groupby_day_df = extract_groupby_day_df.to_html(justify='justify-all',classes='display compact nowrap',index=False)
        display_day_df_list.append(extract_groupby_day_df)
    print(concat_df)
    concat_df['日付'] = concat_df['日付'].map(convert_date)
    bubble_chart_color_dict = {'purple':'rgb(255,0,255)','red':'rgb(255,0,0)','green':'rgb(0,128,0)','lime':'rgb(0,255,0)','yellow':'rgb(255,255,0)',\
'blue':'rgb(0,0,255)','aqua':'rgb(0,255,255)','gray':'rgb(128,128,128)','white':'rgb(192,192,192)','black':'rgb(0,0,0)'}
    bubble_chart_color_list = list(bubble_chart_color_dict.values())
    output_bubble_chart_df = output_bubble_chart_df[:10]
    output_bubble_chart_df['順位'] = ['1位','2位','3位','4位','5位','6位','7位','8位','9位','10位']
    output_bubble_chart_df['機種名'] = output_bubble_chart_df['順位'] +' ' + output_bubble_chart_df['機種名']
    output_bubble_chart_df['color'] = bubble_chart_color_list
    return render_template('target_date_recommend_report.html',bubble_chart_division_calc_num = bubble_chart_division_calc_num,\
                                        serch_number=serch_number,\
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
                                        samai_table = ave_tenpo_df.to_html(justify='justify-all'),\
                                        groupby_kisyu_table = groupby_kisyubetu_df.to_html(justify='justify-all',classes='display compact nowrap',index=False),\
                                        heatmap_column_names=horizon_concat_df.columns.values, \
                                        heatmap_row_data=list(horizon_concat_df.values.tolist()) )


@app.route("/form", methods=['GET','POST'])
def form():
    if request.method == "POST":
        accoun_mail = os.getenv('GMAIL_ACCOUNT')
        password = os.getenv('GMAIL_PASSWORD')
        second_password = os.getenv('GMAIL_SECOND_PASSWORD')
        name =  request.form.get('name')
        if name == '':
            name = '名無し'
        from_email = request.form.get('email')
        if from_email == '':
            from_email = accoun_mail
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

@app.route("/tomorrow_recommend/<area_name>/prefecture/<pref_name_en>", methods=['GET','POST']) 
def tomorrow_recommend_area_prefecture_prefecturename(area_name,pref_name_en):
    pref_name_df = pd.read_csv('csv/pref_lat_lon.csv')
    data = {}
    data['pref_name_jp'] = pref_name_jp = pref_name_df[pref_name_df['pref_name_en'] == pref_name_en]['pref_name'].values[0]
    today = datetime.date.today()
    try:
        req = request.args
        target_date = req.get("target_date")
    except:
        target_date = None
        
    if target_date == None:
        #?user_id=1
        print('target_date',target_date)
        target_date:date = today + timedelta(days=1)
        target_date_str = target_date.strftime('%Y-%m-%d')
        target_date_jp_str_day = target_date.strftime('%m').lstrip('0') + '月' + target_date.strftime('%d').lstrip('0') + '日' + w_list[target_date.weekday()]
        print(target_date_jp_str_day)
            #data['area_name_jp'] = area_name_and_str_jp_area_name_dict[area_name]
        cursor = get_driver()
        #area_sql_text = get_area_sql_text(area_name)
        #首都圏のイベントの媒体別の予約数を集計
        print('pref_name_en',pref_name_en)
        cursor.execute(f'''SELECT *
                        FROM schedule as schedule2
                        left join halldata as halldata2
                        on schedule2.店舗名 = halldata2.hall_name
                        WHERE イベント日 >= current_date
                        AND イベント日 < current_date + 7
                        AND 媒体名 != 'ホールナビ'
                        AND 都道府県 = '{pref_name_jp}'
                        ORDER BY イベント日,都道府県,媒体名 desc;''')

    else:
        target_date_str = target_date
        target_date = datetime.datetime.strptime(target_date, '%Y-%m-%d')
        target_date_jp_str_day = target_date.strftime('%m').lstrip('0') + '月' + target_date.strftime('%d').lstrip('0') + '日' + w_list[target_date.weekday()]
        print(target_date_jp_str_day)
            #data['area_name_jp'] = area_name_and_str_jp_area_name_dict[area_name]
        cursor = get_driver()
        #area_sql_text = get_area_sql_text(area_name)
        #首都圏のイベントの媒体別の予約数を集計
        print('pref_name_en',pref_name_en)
        cursor.execute(f'''SELECT *
                        FROM schedule as schedule2
                        left join halldata as halldata2
                        on schedule2.店舗名 = halldata2.hall_name
                        WHERE イベント日 >= current_date
                        AND イベント日 < current_date + 7
                        AND 媒体名 != 'ホールナビ'
                        AND 都道府県 = '{pref_name_jp}'
                        AND イベント日 = '{target_date_str}'
                        ORDER BY イベント日,都道府県,媒体名 desc;''')
        
    data['pref_name_en'] = pref_name_en 
    data['target_date_str'] = target_date_str
    data['target_jp_str_day'] =  target_date_jp_str_day
    date_list = [today + timedelta(days=day) for day in range(0,6)]
    date_list = [date.strftime("%Y-%m-%d") for date in date_list]
    data['area_name_jp'] = area_name_and_str_jp_area_name_dict[area_name]
    data['date_list'] = date_list
    data['area_name'] = area_name


    cols = [col.name for col in cursor.description]
    extract_prefecture_name_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    extract_prefecture_name_df.drop_duplicates(keep='first',inplace=True)
    table_df = extract_prefecture_name_df[['イベント日','店舗名','媒体名','取材名']]
    table_df.sort_values(['イベント日','店舗名','媒体名','取材名'],ascending=[True,True,True,True],inplace=True)
    table_df['イベント日'] = table_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    table_df.rename(columns={'イベント日':'日'},inplace=True)
    table_df.drop_duplicates(keep='first',inplace=True)
    print('extract_prefecture_name_df',extract_prefecture_name_df)
    data['iframe'] = create_media_map_iframe(extract_prefecture_name_df,pref_name_jp)
    data['extract_prefecture_name_df'] = table_df
    data['extract_prefecture_name_df_column_names'] = table_df.columns.values
    data['extract_prefecture_name_df_row_data'] = list(table_df.values.tolist())
    
     
    #print('data',data) 
    # アクセス情報の設定
    SITE_URL = os.getenv('WORDPRESS_PACHISLO7_URL')
    API_URL = f"{SITE_URL}/wp-json/wp/v2/"
    AUTH_USER = os.getenv('WORDPRESS_PACHISLO7_ID')
    AUTH_PASS = os.getenv('WORDPRESS_PACHISLO7_PW')

    #下書き状態の記事を取得
    #画像は取得するがurl以外は取得しない
    print('pref_name_en',pref_name_en) 
    post_slug = f'{pref_name_en}_{target_date_str}'
    label = f'posts?slug={post_slug}&status=draft&_embed'
    url = f"{API_URL}{label}"
    # すべてのアイテムを取得
    #print(data)
    print('url',url)

    #記事がどれくらい見られてるかリアルタイムで把握するためのライン通知
    #post_line(f'明日の{post_slug}の記事が見られました。')

    res = requests.get(url, auth=(AUTH_USER, AUTH_PASS)).json()
    #print('res',res)
    thumbnail_url = res[0]['_embedded']['wp:featuredmedia'][0]['source_url']
    #print('thumbnail_url',thumbnail_url)
    data['thumbnail_url'] = thumbnail_url
    parameter_id = res[0]['id']
    data['post_slug'] = post_slug
    print('pref_name_en',pref_name_en)
    print('post_slug',post_slug)
    data['target_date_md'] = post_slug
    #print('parameter_id',parameter_id)
    write_html = res[0]['content']['rendered'].split('ここまで')[-1]
    content = res[0]['content']['rendered'].split('ここまで')[0]
    data['title'] = res[0]['title']['rendered'].replace('TOP10','')
    dfs = pd.read_html(content)
    #print('dfs',dfs)
    data['write_html'] = write_html
    #data['tag_df'] = tag_df.to_html(justify='justify-all',classes='tb01')
    dfs = pd.read_html(content)
    groupby_date_kisyubetu_df = dfs[0]
    location_name_df = dfs[1]
    recommend_hall_name_list = list(location_name_df['店舗名'].unique())
    data['recommend_hall_name_list'] = recommend_hall_name_list
    return render_template('tomorrow_recommend_area_prefecture_prefecturename.html',data=data,zip=zip)

@app.route("/tomorrow_recommend/<pref_name_en>/syuzai/<syuzai_name>")
def tomorrow_recommend_area_syuzai_syuzainame(pref_name_en,syuzai_name):
    data = {}
    if pref_name_en in area_str_list:
        area_name = pref_name_en
        data['pref_name_en'] = pref_name_en
        data['pref_name_jp'] = pref_name_jp = prefecture_df[prefecture_df['area_name_en'] == area_name]['area_name_jp'].values[0]
        print('pref_name_jp',pref_name_jp)
        cursor = get_driver()
        area_sql_text = get_area_sql_text(area_name)
        print('area_sql_text',area_sql_text)
        #首都圏のイベントの媒体別の予約数を集計
        cursor.execute(f'''SELECT 都道府県, イベント日,店舗名, 取材名,媒体名,取材ランク,longitude, latitude, pledge_text,no_pledge_visit_count 
                FROM schedule as schedule2
                left join halldata as halldata2
                on schedule2.店舗名 = halldata2.hall_name
                left join pledge as pledge
                on schedule2.取材名 = pledge.syuzai_name
                WHERE イベント日 >= current_date - 31
                AND イベント日 < current_date + 7
                AND 媒体名 != 'ホールナビ'
                AND 取材名 = '{syuzai_name}'
                AND  ({area_sql_text})
                ORDER BY イベント日,都道府県,媒体名 desc;''')
    else:
        data['pref_name_en'] = pref_name_en
        data['pref_name_jp'] = pref_name_jp = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['pref_name'].values[0]
        cursor = get_driver()
        #首都圏のイベントの媒体別の予約数を集計
        cursor.execute(f'''SELECT 都道府県, イベント日,店舗名, 取材名,媒体名,取材ランク,longitude, latitude, pledge_text,no_pledge_visit_count 
                FROM schedule as schedule2
                left join halldata as halldata2
                on schedule2.店舗名 = halldata2.hall_name
                left join pledge as pledge
                on schedule2.取材名 = pledge.syuzai_name
                WHERE イベント日 >= current_date - 31
                AND イベント日 < current_date + 7
                AND 媒体名 != 'ホールナビ'
                AND 取材名 = '{syuzai_name}'
                AND 都道府県 = '{pref_name_jp}'
                ORDER BY イベント日,都道府県,媒体名 desc;''')
    cols = [col.name for col in cursor.description]
    extract_syuzai_name_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    print('extract_syuzai_name_df',extract_syuzai_name_df,extract_syuzai_name_df.shape)
    extract_syuzai_name_df.drop_duplicates(keep='first',inplace=True)
    future_extract_syuzai_name_df = extract_syuzai_name_df[extract_syuzai_name_df['イベント日'] >= datetime.date.today() ]
    past_extract_syuzai_name_df = extract_syuzai_name_df[extract_syuzai_name_df['イベント日'] < datetime.date.today() ]
    pledge_text = extract_syuzai_name_df.iloc[0]['pledge_text']
    media_name = extract_syuzai_name_df.iloc[0]['媒体名']
    # no_pledge_visit_count = int(extract_syuzai_name_df.iloc[0]['no_pledge_visit_count'])
    data['media_name'] = media_name
    data['syuzai_name'] = syuzai_name
    # if (pledge_text == '') or (pledge_text == None):
    #     pledge_text = '未調査'
    #     no_pledge_visit_count += 1
    #     #post_line(f'未調査の取材名があります。{area_name} {media_name} {syuzai_name} {no_pledge_visit_count}回')
    #     sql = f'''UPDATE pledge SET  no_pledge_visit_count = {no_pledge_visit_count} WHERE syuzai_name = '{syuzai_name}';'''
    #     cursor.execute(sql)
    #     conn.commit()
    if (pledge_text == '') or (pledge_text == None):
        pledge_text = '未調査'
    data['pledge_text'] = pledge_text
    future_extract_syuzai_name_df.sort_values(['イベント日','都道府県','媒体名'],ascending=[False,True,True],inplace=True)
    past_extract_syuzai_name_df.sort_values(['イベント日','都道府県','媒体名'],ascending=[False,True,True],inplace=True)
    future_extract_syuzai_name_df = future_extract_syuzai_name_df[['イベント日','都道府県','店舗名','媒体名']]
    past_extract_syuzai_name_df = past_extract_syuzai_name_df[['イベント日','都道府県','店舗名','媒体名']]
    try:
        future_extract_syuzai_name_df['イベント日'] = future_extract_syuzai_name_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    except:
        pass
    try:
        past_extract_syuzai_name_df['イベント日'] = past_extract_syuzai_name_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    except:
        pass
    future_extract_syuzai_name_df.rename(columns={'イベント日':'日'},inplace=True)
    future_extract_syuzai_name_df.drop_duplicates(keep='first',inplace=True)
    past_extract_syuzai_name_df.rename(columns={'イベント日':'日'},inplace=True)
    past_extract_syuzai_name_df.drop_duplicates(keep='first',inplace=True)
    data['past_extract_syuzai_name_df'] = past_extract_syuzai_name_df
    data['past_extract_syuzai_name_df_column_names'] = past_extract_syuzai_name_df.columns.values
    data['past_extract_syuzai_name_df_row_data'] = list(past_extract_syuzai_name_df.values.tolist())
    data['future_extract_syuzai_name_df'] = future_extract_syuzai_name_df
    data['future_extract_syuzai_name_df_column_names'] = future_extract_syuzai_name_df.columns.values
    data['future_extract_syuzai_name_df_row_data'] = list(future_extract_syuzai_name_df.values.tolist())
    extract_syuzai_name_df.sort_values(['イベント日','都道府県','媒体名'],ascending=[False,True,True],inplace=True)
    table_df = extract_syuzai_name_df[['イベント日','都道府県','店舗名','媒体名']]
    table_df['イベント日'] = table_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    table_df.rename(columns={'イベント日':'日'},inplace=True)
    table_df.drop_duplicates(keep='first',inplace=True)
    data['iframe'] = create_syuzai_map_iframe(extract_syuzai_name_df,pref_name_jp)
    data['extract_syuzai_name_df'] = table_df
    data['extract_syuzai_name_df_column_names'] = table_df.columns.values
    data['extract_syuzai_name_df_row_data'] = list(table_df.values.tolist())
    return render_template('tomorrow_recommend_area_syuzai_syuzainame.html',data=data,zip=zip)

@app.route("/tomorrow_recommend/<pref_name_en>/hall/<hall_name>")
def tomorrow_recommend_area_hall_hallname(pref_name_en,hall_name):
    data = {}
    data['pref_name_en'] =  pref_name_en
    try:
        data['pref_name_jp'] = pref_name_jp = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['pref_name'].values[0]
    except:
        data['pref_name_jp'] = pref_name_jp = prefecture_df[prefecture_df['area_name_en'] == pref_name_en]['area_name_jp'].values[0]
    data['hall_name'] = hall_name
    cursor = get_driver()
    cursor.execute(f'''SELECT  都道府県, イベント日, 曜日, 店舗名, 取材名, 媒体名, 取材ランク, 取得時間 , halldata2.id , hall_name, prefecture_name, hall_url, dmm_url, pworld_url, line_url, twitter_url,  address, longitude, latitude, anaslo_name
            FROM schedule as schedule2
            left join halldata as halldata2
            on schedule2.店舗名 = halldata2.hall_name
            WHERE (店舗名 = '{hall_name}') or (hall_name = '{hall_name}')
            AND イベント日 >= current_date - 31
            AND イベント日 < current_date + 7
            AND 媒体名 != 'ホールナビ'
            ORDER BY イベント日,都道府県,媒体名 ASC;''')
    cols = [col.name for col in cursor.description]
    extract_hall_name_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    print('extract_hall_name_df.columns',extract_hall_name_df.columns)

    for column_name in ['twitter_url','pworld_url','dmm_url','line_url','id','address']:
        try:
            data[column_name] = extract_hall_name_df.iloc[0].T[column_name]
        except:
            data[column_name] = ''
    data['iframe'] = create_hall_map_iframe(extract_hall_name_df,zoom_size=10)
    future_extract_hall_name_df = extract_hall_name_df[extract_hall_name_df['イベント日'] >= datetime.date.today() ]
    past_extract_hall_name_df = extract_hall_name_df[extract_hall_name_df['イベント日'] < datetime.date.today() ]
    data['iframe'] = create_hall_map_iframe(extract_hall_name_df,zoom_size=10)
    future_extract_hall_name_df.sort_values(['イベント日','都道府県','媒体名'],ascending=[False,True,True],inplace=True)
    past_extract_hall_name_df.sort_values(['イベント日','都道府県','媒体名'],ascending=[False,True,True],inplace=True)
    future_extract_hall_name_df = future_extract_hall_name_df[['イベント日','都道府県','媒体名','取材名']]
    past_extract_hall_name_df = past_extract_hall_name_df[['イベント日','都道府県','媒体名','取材名']]
    try:
        future_extract_hall_name_df['イベント日'] = future_extract_hall_name_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    except:
        pass
    try:
        past_extract_hall_name_df['イベント日'] = past_extract_hall_name_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    except:
        pass
    future_extract_hall_name_df.rename(columns={'イベント日':'日'},inplace=True)
    future_extract_hall_name_df.drop_duplicates(keep='first',inplace=True)
    past_extract_hall_name_df.rename(columns={'イベント日':'日'},inplace=True)
    past_extract_hall_name_df.drop_duplicates(keep='first',inplace=True)
    data['past_extract_hall_name_df'] = past_extract_hall_name_df
    data['past_extract_hall_name_df_column_names'] = past_extract_hall_name_df.columns.values
    data['past_extract_hall_name_df_row_data'] = list(past_extract_hall_name_df.values.tolist())
    data['future_extract_hall_name_df'] = future_extract_hall_name_df
    data['future_extract_hall_name_df_column_names'] = future_extract_hall_name_df.columns.values
    data['future_extract_hall_name_df_row_data'] = list(future_extract_hall_name_df.values.tolist())
    return render_template('tomorrow_recommend_area_hall_hallname.html',data=data,zip=zip)

@app.route("/tomorrow_recommend/<pref_name_en>/media/<media_name>")
def tomorrow_recommend_area_media_medianame(pref_name_en,media_name):
    prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
    data = {}
    if pref_name_en in area_str_list:
        area_name = pref_name_en
        data['pref_name_en'] = pref_name_en
        data['pref_name_jp'] = pref_name_jp = prefecture_df[prefecture_df['area_name_en'] == area_name]['area_name_jp'].values[0]
        print('pref_name_jp',pref_name_jp)
        cursor = get_driver()
        area_sql_text = get_area_sql_text(area_name)
        print('area_sql_text',area_sql_text)
        today = date.today()
        date_list = [today + timedelta(days=day) for day in range(0,6)]
        date_list = [date.strftime("%Y-%m-%d") for date in date_list]
        data['date_list'] = date_list
        data['media_name'] = media_name
        cursor = get_driver()
        #首都圏のイベントの媒体別の予約数を集計
        print('media_name',media_name)
        cursor.execute(f'''SELECT *
                    FROM schedule as schedule2
                    left join halldata as halldata2
                    on schedule2.店舗名 = halldata2.hall_name
                    WHERE イベント日 >= current_date - 31
                    AND イベント日 < current_date + 7
                    AND 媒体名 = '{media_name}'
                    AND  ({area_sql_text})
                    ORDER BY イベント日,都道府県,媒体名 desc;''')
    else:
        data['pref_name_en'] = pref_name_en
        data['pref_name_jp'] = pref_name_jp = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['pref_name'].values[0]
        data['area_name_jp'] = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['area_name_jp'].values[0]
        data['area_name_en'] = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['area_name_en'].values[0]
        today = date.today()
        date_list = [today + timedelta(days=day) for day in range(0,6)]
        date_list = [date.strftime("%Y-%m-%d") for date in date_list]
        data['date_list'] = date_list
        data['media_name'] = media_name
        cursor = get_driver()
        #首都圏のイベントの媒体別の予約数を集計
        print('media_name',media_name)
        print('pref_name_en',pref_name_en)
        cursor.execute(f'''SELECT *
                    FROM schedule as schedule2
                    left join halldata as halldata2
                    on schedule2.店舗名 = halldata2.hall_name
                    WHERE イベント日 >= current_date - 31
                    AND イベント日 < current_date + 7
                    AND 媒体名 = '{media_name}'
                    AND 都道府県 = '{pref_name_jp}'
                    ORDER BY イベント日,都道府県,媒体名 desc;''')
    cols = [col.name for col in cursor.description]
    extract_media_name_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    extract_media_name_df.drop_duplicates(keep='first',inplace=True)
    extract_media_name_df = extract_media_name_df.sort_values(['イベント日','都道府県','店舗名','取材名'],ascending=[False,True,True,True],inplace=False).reset_index(drop=True)
    print('extract_media_name_df',extract_media_name_df)
    create_media_map_iframe_df = extract_media_name_df
    extract_media_name_df = extract_media_name_df[['イベント日','店舗名','取材名']]
    future_extract_media_name_df = extract_media_name_df[extract_media_name_df['イベント日'] >= datetime.date.today() ]
    past_extract_media_name_df = extract_media_name_df[extract_media_name_df['イベント日'] < datetime.date.today() ]
    future_extract_media_name_df = future_extract_media_name_df[['イベント日','店舗名','取材名']]
    future_extract_media_name_df['イベント日'] = future_extract_media_name_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    past_extract_media_name_df['イベント日'] = past_extract_media_name_df['イベント日'].map(convert_sql_date_to_jp_date_and_weekday)
    future_extract_media_name_df.rename(columns={'イベント日':'日'},inplace=True)
    future_extract_media_name_df.drop_duplicates(keep='first',inplace=True)
    print(future_extract_media_name_df)
    data['iframe'] = create_media_map_iframe(create_media_map_iframe_df,pref_name_jp)
    data['extract_media_name_df'] = future_extract_media_name_df
    data['extract_media_name_df_column_names'] = future_extract_media_name_df.columns.values
    data['extract_media_name_df_row_data'] = list(future_extract_media_name_df.values.tolist())
    data['past_extract_media_name_df'] = past_extract_media_name_df
    data['past_extract_media_name_df_column_names'] = past_extract_media_name_df.columns.values
    data['past_extract_media_name_df_row_data'] = list(past_extract_media_name_df.values.tolist())
    return render_template('tomorrow_recommend_pref_media_medianame.html',data=data,zip=zip)



@app.route("/tomorrow-recommend/<area_name>/", methods=['GET'])
@cache.cached(timeout=300)
def tomorrow_recommend_area(area_name):
    area_sql_text = get_area_sql_text(area_name)
    sql = f'''SELECT COUNT(媒体名), 媒体名
    FROM schedule
    WHERE イベント日 >= current_date
    AND イベント日 <= current_date + 6
    AND 媒体名 != 'ホールナビ'
    AND 媒体名 != '旧イベ'
    AND ({area_sql_text})
    GROUP BY 媒体名
    ORDER BY COUNT(媒体名) desc;'''

    data = {}
    today = date.today()
    date_list = [today + timedelta(days=day) for day in range(0,9)]
    date_list = [date.strftime("%Y-%m-%d") for date in date_list]
    data['date_list'] = date_list
    data['area_name'] = area_name
    data['area_name_jp'] = area_name_and_str_jp_area_name_dict[area_name]
    data['prefecture_name_list'] = get_area_prefecture_list(area_name)

    cursor = get_driver()
    #首都圏のイベントの媒体別の予約数を集計
    cursor.execute(sql)
    cols = [col.name for col in cursor.description]
    groupby_media_name_count_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    #重複行を削除する
    groupby_media_name_count_df.drop_duplicates(keep='first',inplace=True)
    print('groupby_media_name_count_df:',groupby_media_name_count_df)
    groupby_media_name_count_df.rename(columns={'count': '取材数'},inplace=True)
    data['groupby_media_name_count_df'] = groupby_media_name_count_df
    data['groupby_media_name_count_df_column_names'] = groupby_media_name_count_df.columns.values
    data['groupby_media_name_count_df_row_data'] = list(groupby_media_name_count_df.values.tolist())
    print('data',data)
    cursor = get_driver()
    cursor.execute(f'''SELECT COUNT(店舗名),都道府県, 店舗名
            FROM schedule as schedule2
            left join halldata as halldata2
            on schedule2.店舗名 = halldata2.hall_name
            WHERE イベント日 >= current_date
            AND イベント日 <= current_date + 7
            AND 媒体名 != 'ホールナビ'
            AND 媒体名 != '旧イベ'
            AND ({area_sql_text})
            GROUP BY 店舗名,都道府県
            ORDER BY COUNT(店舗名) desc;''')
    cols = [col.name for col in cursor.description]
    groupby_hall_name_count_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    #重複行を削除する
    print(groupby_hall_name_count_df)
    groupby_hall_name_count_df.drop_duplicates(keep='first',inplace=True)
    print('groupby_hall_name_count_df:',groupby_hall_name_count_df)
    groupby_hall_name_count_df.rename(columns={'count': '取材数'},inplace=True)
    data['groupby_hall_name_count_df'] = groupby_hall_name_count_df
    data['groupby_hall_name_count_df_column_names'] = groupby_hall_name_count_df.columns.values
    data['groupby_hall_name_count_df_row_data'] = list(groupby_hall_name_count_df.values.tolist())
    return render_template('tomorrow_recommend_area.html',data=data,zip=zip)

class DateForm(FlaskForm):
    inputdate = DateField('', format='%Y/%m/%d')
    submit = SubmitField('検索')
@app.route("/tomorrow-recommend/<pref_name_en>/", methods=['POST'])
def tomorrow_recommend_area_post(pref_name_en):
    form = DateForm()
    prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
    data = {}
    data['pref_id'] = prefecture_id  = prefecture_df[prefecture_df['pref_name'] == '沖縄県'].index[0]
    data['pref_name_en'] = pref_name_en = prefecture_df.iloc[int(data['pref_id'])-1]['pref_name_en']
    data['pref_name_jp'] = pref_name_jp = prefecture_df.iloc[int(data['pref_id'])-1]['pref_name']
    data['area_name_jp'] = prefecture_df.iloc[int(data['pref_id'])-1]['area_name_jp']
    data['area_name_en'] = prefecture_df.iloc[int(data['pref_id'])-1]['area_name_en']
    data = request.form
    print('dataは',data)
    print('form.inputdate.data',form.inputdate.data)
    target_date_jp:str = data['date']
    target_date = data['date'].split(' (')[0].replace('年','-').replace('月','-').replace('日','')
    print('target_date',target_date)
    data = {}
    data['target_date_jp'] = target_date_jp
    data['area_name'] = area_name
    data['target_date'] = target_date
    data['area_name_jp'] = area_name_and_str_jp_area_name_dict[area_name]
    area_sql_text = get_area_sql_text(area_name)
    cursor = get_driver()
    #首都圏のイベントの媒体別の予約数を集計
    cursor.execute(f'''SELECT *
                FROM schedule as schedule2
                left join halldata as halldata2
                on schedule2.店舗名 = halldata2.hall_name
                WHERE イベント日 >= current_date
                    AND イベント日 < current_date + 7
                    AND 媒体名 != 'ホールナビ'
                    AND イベント日 = '{target_date}'
                    AND ({area_sql_text})
                    ORDER BY イベント日,都道府県,媒体名 desc;''')
    cols = [col.name for col in cursor.description]
    extract_target_date_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    extract_target_date_df.drop_duplicates(keep='first',inplace=True)
    table_df = extract_target_date_df[['都道府県','店舗名','媒体名','取材名']]
    table_df.sort_values(['都道府県','店舗名','媒体名','取材名'],ascending=[True,True,True,True],inplace=True)
    table_df.drop_duplicates(keep='first',inplace=True)
    data['iframe'] = create_syuzai_map_iframe(extract_target_date_df,area_name)
    data['extract_target_date_df'] = table_df
    data['extract_target_date_df_column_names'] = table_df.columns.values
    data['extract_target_date_df_row_data'] = list(table_df.values.tolist())
    return render_template('tomorrow_recommend_area_date.html',data=data,zip=zip)


@app.route("/tomorrow-recommend/<area_name>/<date>-data")
@cache.cached(timeout=300)
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

@app.route("/serch-recommend-prefecture-day", methods=['GET','POST'])
def serch_recommend_prefecture_day():
    if request.method == 'GET':
        prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
        data = {}
        date_list = []
        day_str_list = []
        prefecture_name_en_and_name_dict = dict(zip(prefecture_df['pref_name_en'],prefecture_df['pref_name']))
        print('prefecture_name_en_and_name_dict',prefecture_name_en_and_name_dict)
        data['prefecture_name_en_and_name_dict'] = prefecture_name_en_and_name_dict
        today = datetime.date.today()
        prefecture_name = '東京都'
        pref_name_en = 'tokyo'
        #target_day =  today + datetime.timedelta(days=target_day_number)
        target_day_str = today.strftime('%Y-%m-%d')
        #曜日のリスト
        print(target_day_str[-1])
        #Nの付く日
        display_date_list_dict = {}
        tag_dict = {}
        for i in range(0,9):
            #print(i)
            target_day = today + datetime.timedelta(days=i)
            belong_day_str = target_day.strftime('%Y-%m-%d')
            target_day_str_jp = target_day.strftime('%m/').lstrip('0')  +target_day.strftime('%d').lstrip('0') +  w_list[target_day.weekday()]
            target_day_str_number:str = belong_day_str[-1] + 'の付く日'
            display_date_list_dict[target_day_str_jp] = target_day_str_number
            display_list_str = target_day_str_jp + ' ' + target_day_str_number
            tag_dict[display_list_str] = belong_day_str
        print(tag_dict)
        data['tag_dict'] = tag_dict
        return render_template('serch-recommend-prefecture-day.html',data=data,enumerate=enumerate)
    else:
        pass
    
@app.route("/prefecture/<pref_name_en>", methods=['GET','POST'])
def select_page_prefecture(pref_name_en):
    prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
    #index番号で取り出す
    data = {}
    if pref_name_en in area_str_list:
        data['area_name_en'] = pref_name_en
        data['area_name_jp'] = prefecture_df[prefecture_df['area_name_en'] == pref_name_en]['area_name_jp'].values[0]
        data['pref_name_en_list'] = pref_name_en_list = list(prefecture_df[prefecture_df['area_name_en'] == pref_name_en]['pref_name_en'])
        data['pref_name_jp_list'] =pref_name_jp_list = list(prefecture_df[prefecture_df['area_name_en'] == pref_name_en]['pref_name'])
        #pref_name_jp_listとpref_name_en_listを辞書型に変換
        data['pref_name_jp_and_en_dict'] = dict(zip(pref_name_jp_list,pref_name_en_list))
        return render_template('select_page_area_to_prefecture.html',data=data,zip=zip,enumerate=enumerate)


    data['pref_name_en'] = pref_name_en
    data['pref_name_jp'] = pref_name_jp = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['pref_name'].values[0]
    data['area_name_jp'] = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['area_name_jp'].values[0]
    data['area_name_en'] = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['area_name_en'].values[0]
    print('pref_name_en',pref_name_en,pref_name_jp)  
    print('data',data) 

    date_list = []
    day_str_list = []
    today = datetime.date.today()
    #target_day =  today + datetime.timedelta(days=target_day_number)
    target_day_str = today.strftime('%Y-%m-%d')
    #曜日のリスト
    print(target_day_str[-1])
    #Nの付く日
    display_date_list_dict = {}
    tag_dict = {}
    for i in range(-1,7):
        #print(i)
        target_day = today + datetime.timedelta(days=i)
        belong_day_str = target_day.strftime('%Y-%m-%d')
        target_day_str_jp = target_day.strftime('%m/').lstrip('0')  +target_day.strftime('%d').lstrip('0') +  w_list[target_day.weekday()]
        target_day_str_number:str = belong_day_str[-1] + 'の付く日'
        display_date_list_dict[target_day_str_jp] = target_day_str_number
        display_list_str = target_day_str_jp + ' ' + target_day_str_number
        tag_dict[display_list_str] = belong_day_str
    print(tag_dict)
    
    data['tag_dict'] = tag_dict
    sql = f'''SELECT COUNT(媒体名), 媒体名
    FROM schedule
    WHERE イベント日 >= current_date 
    AND イベント日 <= current_date + 7
    AND 媒体名 != 'ホールナビ'
    AND 都道府県 = '{pref_name_jp}'
    GROUP BY 媒体名
    ORDER BY COUNT(媒体名) desc;'''

    today = date.today()
    date_list = [today + timedelta(days=day) for day in range(0,9)]
    date_list = [date.strftime("%Y-%m-%d") for date in date_list]
    data['date_list'] = date_list


    cursor = get_driver()
    #首都圏のイベントの媒体別の予約数を集計
    print('sql1',sql)
    cursor.execute(sql)
    cols = [col.name for col in cursor.description]
    groupby_media_name_count_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    #重複行を削除する
    groupby_media_name_count_df.drop_duplicates(keep='first',inplace=True)
    print('groupby_media_name_count_df:',groupby_media_name_count_df)
    groupby_media_name_count_df.rename(columns={'count': '取材数'},inplace=True)
    data['groupby_media_name_count_df'] = groupby_media_name_count_df
    data['groupby_media_name_count_df_column_names'] = groupby_media_name_count_df.columns.values
    data['groupby_media_name_count_df_row_data'] = list(groupby_media_name_count_df.values.tolist())
    print('data',data)
    #cursor = get_driver()
    sql2 = f'''SELECT COUNT(店舗名),都道府県, 店舗名
            FROM schedule as schedule2
            left join halldata as halldata2
            on schedule2.店舗名 = halldata2.hall_name
            WHERE イベント日 >= current_date - 4
            AND イベント日 <= current_date + 7
            AND 媒体名 != 'ホールナビ'
            AND 都道府県 = '{pref_name_jp}'
            GROUP BY 店舗名,都道府県
            ORDER BY COUNT(店舗名) desc;'''
    print('sql2',sql2)
    cursor.execute(sql2)
    cols = [col.name for col in cursor.description]
    groupby_hall_name_count_df = pd.DataFrame(cursor.fetchall(),columns=cols)
    #重複行を削除する
    print(groupby_hall_name_count_df)
    groupby_hall_name_count_df.drop_duplicates(keep='first',inplace=True)
    print('groupby_hall_name_count_df:',groupby_hall_name_count_df)
    groupby_hall_name_count_df.rename(columns={'count': '取材数'},inplace=True)
    data['groupby_hall_name_count_df'] = groupby_hall_name_count_df[['取材数','店舗名']]
    groupby_hall_name_count_df = groupby_hall_name_count_df[['取材数','店舗名']]
    data['groupby_hall_name_count_df_column_names'] = groupby_hall_name_count_df.columns.values
    data['groupby_hall_name_count_df_row_data'] = list(groupby_hall_name_count_df.values.tolist())
    return render_template('select_page_prefecture.html',data=data,enumerate=enumerate,zip=zip)



@app.route("/prefecture_post_detail", methods=['GET','POST'])
def prefecture_post_detail():
    if request.method == 'POST':
        prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
        #index番号で取り出す

        #北海道が選択された場合 wordpressのタグのidは72
        data = {}
        data['target_day'] = target_day = request.form.get('target_day')
        data['pref_name_en'] = pref_name_en = request.form.get('pref_name_en')
        data['pref_name_jp'] = pref_name_jp = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['pref_name'].values[0]
        data['area_name_jp'] = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['area_name_jp'].values[0]
        data['area_name_en'] = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['area_name_en'].values[0]
        print('pref_name_en',pref_name_en,pref_name_jp)  
        print('pref_name_en',pref_name_en)  
        print('data',data) 
        # アクセス情報の設定
        SITE_URL = os.getenv('WORDPRESS_PACHISLO7_URL')
        API_URL = f"{SITE_URL}/wp-json/wp/v2/"
        AUTH_USER = os.getenv('WORDPRESS_PACHISLO7_ID')
        AUTH_PASS = os.getenv('WORDPRESS_PACHISLO7_PW')

        #下書き状態の記事を取得
        #画像は取得するがurl以外は取得しない
        label = f'posts?slug={pref_name_en}_{target_day}&status=draft&_embed'
        url = f"{API_URL}{label}"
        # すべてのアイテムを取得
        print(url)
        res = requests.get(url, auth=(AUTH_USER, AUTH_PASS)).json()
        #print(res)
        thumbnail_url = res[0]['_embedded']['wp:featuredmedia'][0]['source_url']
        print('thumbnail_url',thumbnail_url)
        data['thumbnail_url'] = thumbnail_url
        parameter_id = res[0]['id']
        print('parameter_id',parameter_id)
        write_html = res[0]['content']['rendered'].split('ここまで')[-1]
        content = res[0]['content']['rendered'].split('ここまで')[0]
        data['title'] = res[0]['title']['rendered']
        dfs = pd.read_html(content)
        #print('dfs',dfs)
        data['write_html'] = write_html
        #data['tag_df'] = tag_df.to_html(justify='justify-all',classes='tb01')
        dfs = pd.read_html(content)
        groupby_date_kisyubetu_df = dfs[0]
        location_name_df = dfs[1]
        print('location_name_df',location_name_df)
        data['iframe'] = create_post_map_iframe(location_name_df,groupby_date_kisyubetu_df)
        return render_template('prefecture_post_detail.html',data=data,enumerate=enumerate)
    else:
        pass

#post_prefecture_list.html
@app.route("/post_prefecture_list/<pref_name_en>", methods=['GET'])
def post_prefecture_list(pref_name_en):
    data = {}
    data['pref_name_en'] = pref_name_en
    prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
    #index番号で取り出す
    data['pref_name_jp'] = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['pref_name'].values[0]
    #北海道が選択された場合 wordpressのタグのidは72
    prefecture_tag_id:int = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en].index[0] + 72
    print('pref_name_en',pref_name_en)  
    print('data',data) 
    # アクセス情報の設定
    SITE_URL = os.getenv('WORDPRESS_PACHISLO7_URL')
    API_URL = f"{SITE_URL}/wp-json/wp/v2/"
    AUTH_USER = os.getenv('WORDPRESS_PACHISLO7_ID')
    AUTH_PASS = os.getenv('WORDPRESS_PACHISLO7_PW')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    label = f'posts?_embed&tags={str(prefecture_tag_id)}+&status=draft&page={page}'
    url = f"{API_URL}{label}"
    # すべてのアイテムを取得
    print(url)
    items = requests.get(url, auth=(AUTH_USER, AUTH_PASS)).json()
    #jsonから取得したデータをページネーションで表示する
    print('len(items)',len(items))
    print('page',page)
    target_day = datetime.date(2023, 11, 29)
    today = datetime.date.today()
    diff = today - target_day
    print(diff.days,type(diff.days))
    total_page = diff.days//10 + 1
    pagination = Pagination(page=page, total=total_page,  per_page=1, css_framework='bootstrap4')
    return render_template('post_prefecture_list.html',items=items,data=data,enumerate=enumerate,pagination=pagination)

@app.route("/post_prefecture/<post_slug>", methods=['GET','POST'])
def post_prefecture(post_slug):
    if request.method == 'GET':
        prefecture_df = pd.read_csv('csv/pref_lat_lon.csv')
        data = {}
        data['pref_name_en'] = pref_name_en = post_slug.split('_')[0]
        data['pref_name_jp'] = prefecture_df[prefecture_df['pref_name_en'] == pref_name_en]['pref_name'].values[0]
        print('pref_name_en',pref_name_en)  
        print('data',data) 
        # アクセス情報の設定
        SITE_URL = os.getenv('WORDPRESS_PACHISLO7_URL')
        API_URL = f"{SITE_URL}/wp-json/wp/v2/"
        AUTH_USER = os.getenv('WORDPRESS_PACHISLO7_ID')
        AUTH_PASS = os.getenv('WORDPRESS_PACHISLO7_PW')

        #下書き状態の記事を取得
        #画像は取得するがurl以外は取得しない
        label = f'posts?slug={post_slug}&status=draft&_embed'
        url = f"{API_URL}{label}"
        # すべてのアイテムを取得
        print(url)

        #都道府県別日別の記事がどれくらい見られてるかLINEで通知する
        #post_line(f'{post_slug}の記事が都道府県別一覧経由で見られています。')

        res = requests.get(url, auth=(AUTH_USER, AUTH_PASS)).json()
        #print(res)
        thumbnail_url = res[0]['_embedded']['wp:featuredmedia'][0]['source_url']
        print('thumbnail_url',thumbnail_url)
        data['thumbnail_url'] = thumbnail_url
        parameter_id = res[0]['id']
        print('parameter_id',parameter_id)
        write_html = res[0]['content']['rendered'].split('ここまで')[-1]
        content = res[0]['content']['rendered'].split('ここまで')[0]
        data['title'] = res[0]['title']['rendered']
        dfs = pd.read_html(content)
        #print('dfs',dfs)
        data['write_html'] = write_html
        #data['tag_df'] = tag_df.to_html(justify='justify-all',classes='tb01')
        dfs = pd.read_html(content)
        groupby_date_kisyubetu_df = dfs[0]
        location_name_df = dfs[1]
        print('location_name_df',location_name_df)
        data['iframe'] = create_post_map_iframe(location_name_df,groupby_date_kisyubetu_df)
        return render_template('prefecture_post_detail.html',data=data,enumerate=enumerate)

@app.route("/news/<post_slug>", methods=['GET','POST'])
def news_detail(post_slug):
    if request.method == 'GET':
        data = {}
        # アクセス情報の設定
        SITE_URL = os.getenv('WORDPRESS_PACHISLO7_URL')
        API_URL = f"{SITE_URL}/wp-json/wp/v2/"
        AUTH_USER = os.getenv('WORDPRESS_PACHISLO7_ID')
        AUTH_PASS = os.getenv('WORDPRESS_PACHISLO7_PW')

        #下書き状態の記事を取得
        label = f'posts?slug={post_slug}&status=draft&_embed'
        url = f"{API_URL}{label}"
        print(url)
        res = requests.get(url, auth=(AUTH_USER, AUTH_PASS)).json()
        data['date'] = res[0]['slug'].split('_')[1]
        data['content'] = res[0]['content']['rendered']
        data['title'] = res[0]['title']['rendered']
        return render_template('news_post_detail.html',data=data,enumerate=enumerate)

@app.route("/select_hallname", methods=['GET','POST'])
def select_hallname():
    if request.method == 'GET':
        data = {}
        select_hall_df = pd.read_csv('csv/ana_prefecture_hallname_city_name_df.csv')
        data['select_hall_df'] = select_hall_df
        data['select_hall_df_column_names'] = select_hall_df.columns.values
        data['select_hall_df_row_data'] = list(select_hall_df.values.tolist())
        return render_template('select_hallname.html',data=data,zip=zip)

@app.route("/target_hallname/<hall_name>", methods=['GET'])
def target_hallname(hall_name):
    today = date.today()
    date_list = [today + timedelta(days=day) for day in range(0,9)]
    date_list = [date.strftime("%Y-%m-%d") for date in date_list]
    return render_template('target_date_recommend_schedule.html',date_list=date_list,hall_name=hall_name)

@app.route("/privacy_policy")
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/sitemap.xml")
def sitemap():
    return app.send_static_file("sitemap.xml")

@app.route("/robots.txt")
def robots():
    return app.send_static_file("robots.txt")

@app.route("/ads.txt")
def ads():
    return app.send_static_file("ads.txt")

@app.route("/test", methods=['GET','POST'])
def test():
    data = {}
    data['hall_name'] = 'ホール名'
    return render_template('test_templete.html',data=data)

@app.route("/test2", methods=['GET','POST'])
def post_test():
    data = {}
    prefecture_id_and_name_dict = {}
    for i, prefecture_name in enumerate(prefecture_list):
        i = i + 1
        prefecture_id_and_name_dict[i] = prefecture_name
    data['prefecture_id_and_name_dict'] = prefecture_id_and_name_dict
    return render_template('test2.html',data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False, port=int(os.environ.get('PORT', 5000)))
