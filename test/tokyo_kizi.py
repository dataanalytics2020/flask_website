#東京都 オススメ店舗リスト
#WINDOWS用
from selenium import webdriver
import time
import os
import pandas as pd
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
import urllib
from bs4 import BeautifulSoup
import re
import pyperclip
import csv
import codecs
import requests
import urllib.request as req
import openpyxl
import glob
from sklearn.datasets import  load_iris
import json
import requests
import time
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import datetime
#from datetime import datetime, date, timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import chart_studio.plotly as py
import plotly.graph_objs as go
print('ライブラリ読み込み完了')
if os.name == 'nt':
    font_path = r"C:\Windows\Fonts\ラノベPOP.otf"
    read_image_jpg = r"C:\Users\81801\Desktop\twitter_anarytics_bot\recommend_syuzai_report\board_image.jpg"
    SERVICE_ACCOUT_FILE = r"C:\Users\81801\Desktop\twitter_anarytics_bot\twitteranalytics-jsonsercretkey.json"
    #save_image_jpg = f"C:\\Users\\81801\\Desktop\\twitter_anarytics_bot\\recommend_syuzai_report\\{todouhuken}_syuzai_reoort_{tomorrow_str}.jpg"
    executable_path_str = r"C:\Users\81801\Desktop\事務プログラム作業用\請求書処理\chromedriver.exe"
    #image_path = r"C:\Users\81801\Desktop\twitter_anarytics_bot\recommend_syuzai_report\board_image.jpg" #win
    
elif os.name == 'posix':
    SERVICE_ACCOUT_FILE = '/Users/macbook/Desktop/python/共通config/twitteranalytics-jsonsercretkey.json'
    #read_image_jpg = f"/Users/macbook/Desktop/{todouhuken}_ika_board.jpg"
    font_path = "/Users/macbook/Library/Fonts/ラノベPOP.otf"
    #save_image_jpg = f'/Users/macbook/Desktop/python/slot/recommend_syuzai_report/{todouhuken}_syuzai_reoort_{tomorrow_str}.jpg'
    executable_path_str = '/Users/macbook/Desktop/python/共通config/chromedriver'
    #image_path = f"/Users/macbook/Desktop/{todouhuken}_ika_board.jpg" #mac

    
#平均差枚用

#nのつく日
#ここからスタート
import datetime
date_list = []
day_str_list= []

today = datetime.date.today () 
tomorrow = today + datetime.timedelta(days=2)
tomorrow_str = tomorrow.strftime('%Y-%m-%d')
today_year_month = today.strftime('%Y/%m')
tomorrow_str_tweet = tomorrow.strftime('%m月%d日')
print(tomorrow_str[-1])
target_day_number = tomorrow_str[-1]

for i in range(39):
    belong_day = today - datetime.timedelta(days= i)
    belong_day_str = belong_day.strftime('%Y-%m-%d')
    
    ##print(belong_day_str[-2:])
    if belong_day_str[-1] == tomorrow_str[-1]:
        if belong_day_str[-2:] == '31':
            continue
        day_str = belong_day.strftime('%m月%d日').lstrip('0')
        date_list.append(belong_day_str)
        day_str_list.append(day_str)
date_str = ''
for date in day_str_list[:3]:
    date_str += date + ' '

date_list_lists = date_list[:3]

date_str_list = []
date_str_list.append(date_str)
print(date_list_lists)
print(date_str)
print(date_str_list)

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo


# Set URL, ID, Password
WORDPRESS_ID = "tsc953u"
WORDPRESS_PW = "6tjc5306"
WORDPRESS_URL = "https://slotana777.com/xmlrpc.php"
wp = Client(WORDPRESS_URL, WORDPRESS_ID, WORDPRESS_PW)
#py.image.save_as(fig, 'my_plot.png')/Users/macbook/Desktop/board_image.jpg




def context_change_tenpo_name(df_temp,tenpo_name,day):
    #⬇️列のデータをインデックスに指定する
    global df
    df_temp.columns = ['データ', tenpo_name]
    #⬇️余計な文字の除く
    df_temp = df_temp[df_temp['データ'] != 'パチンコ版']
    df_temp[tenpo_name] = df_temp[tenpo_name].str.replace('+','').str.replace('枚','').str.replace('G','').str.replace(',','')
    df1 = df_temp.append({'データ': '日付', tenpo_name: day}, ignore_index=True)
    if df1.loc[3, 'データ'] != '平均G数':
            df1 = df1.append({'データ': '平均G数', tenpo_name: 0}, ignore_index=True)
    df = df1
    
    # for i in range(len(df1)):
    #     if df1.loc[i, 'データ'] == '勝率':
    #         df = df1.drop(i) 
    return df

def add_text_to_image(img, text, font_path, font_size, font_color, height, width, max_length=740):
    position = (width, height)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
#     if draw.textsize(text, font=font)[0] > max_length:
#         while draw.textsize(text + '…', font=font)[0] > max_length:
#             text = text[:-1]
#         text = text + '…'
    draw.text(position, text, font_color, font=font)
    return img

from fractions import Fraction
def 台数計算(x):
    pattern = "(.*)/(.*)"
    z = re.search(pattern, x)
    x = z.group(1)
    y = z.group(2)
    y_1 = str(y) + '台' 
    return y_1

def 台数(x):
    pattern = "(.*)/(.*)"
    z = re.search(pattern, x)
    x = z.group(1)
    y = z.group(2)
    y_1 = int(y) 
    return y_1


def 全体勝率計算(x):
    pattern = "(.*)/(.*)"
    d = re.search(pattern, x)
    x = int(d.group(1))
    y = int(d.group(2))
    全体勝率 = 100 * x / y
    全体勝率 = str(int(全体勝率)) + '%'
    return 全体勝率

def 出率計算(x):
    ave_game = int(x.平均G数)
    number_of_units = int(x.台数)
    sousamai = int(x.総差枚)
    sum_game = ave_game * number_of_units
    in_maisuu = 3 * sum_game
    sum_ave_game = (sousamai + in_maisuu ) / in_maisuu * 100
    sum_ave_game = '{:.1f}'.format(sum_ave_game)
    sum_ave_game = str(sum_ave_game) + '%'

    return sum_ave_game

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                        (img_height - crop_height) // 2,
                        (img_width + crop_width) // 2,
                        (img_height + crop_height) // 2))



#昨日の日付を取得
# today = datetime.today()
# print('本日',datetime.strftime(today, '%Y-%m-%d'))
# tomorrow = today + timedelta(days=1)
# #str_yesterday = str(datetime.strftime(yesterday, '%Y年%m月%d日'))
# #yesterday = str(datetime.strftime(yesterday, '%Y-%m-%d'))
# str_tomorrow = str(datetime.strftime(tomorrow, '%Y年%m月%d日'))
# print('明日の日付',tomorrow)
# #print(str_month_ago_list)

# #先月、先々月,セン先々月
# tomorrow = today + timedelta(days=1)
# #str_yesterday = str(datetime.strftime(yesterday, '%Y年%m月%d日'))
# #yesterday = str(datetime.strftime(yesterday, '%Y-%m-%d'))
# str_tomorrow = str(datetime.strftime(tomorrow, '%Y年%m月%d日'))
# print('明日の日付',tomorrow)
# #print(str_month_ago_list)

# #先月、先々月,セン先々月
# month_ago_list = [tomorrow - relativedelta(months=i) for i in list(range(1,3))]
# str_month_ago_list = [datetime.strftime(month_ago, '%Y-%m-%d') for month_ago in  month_ago_list]

#def tomorrow_reccomend_tenpo_choice_image_create(date_list,date_str_list,date_str):

from datetime import datetime, date, timedelta
image_number = 1
#for date_list,date_str in zip(date_list_lists,date_str_list):
kiji_texts =[]
links = []
urls = []
days =[]
tenpo_names = []
tenpo_url_dict = {}
df_lists = []
for str_day in date_list_lists:
    print(str_day)
    #大阪　https://min-repo.com/category/%E5%A4%A7%E9%98%AA%E5%BA%9C/
    url = f'https://min-repo.com/category/%E6%9D%B1%E4%BA%AC%E9%83%BD/page/1/?report_date={str_day}'
    #取材日データと機種データを取得する関数
    #取材日データと機種データを取得する関数
    response = req.urlopen(url) #データを取得
    soup = BeautifulSoup(response, 'html.parser')
    page_list = soup.find_all(class_='pages')
    page_list_len = soup.find_all(class_='pages')
    time.sleep(1)
    for page in page_list:
        page_text = page.text.replace(' ','')
    if len(page_list_len)==0:
        page_last = 1
    elif int(page_text[-1]) >= 2:
        page_last = int(page_text[-1])
    else:
        pass
    print(page_last)
    print('ページ数',page_last)

    for i in list(range(1, 1+page_last)):
        url = f'https://min-repo.com/category/%E6%9D%B1%E4%BA%AC%E9%83%BD/page/{i}/?report_date={str_day}'
        response = req.urlopen(url) #データを取得
        soup = BeautifulSoup(response, 'html.parser')
        kiji_lists = soup.find_all(class_='ichiran_title')
        #time.sleep(0.5)
        kiji =''
        for kiji in kiji_lists:
            text = kiji.text.replace('\n','')
            kiji_texts.append(text)

        for kiji_list in kiji_lists:
            r = kiji_list.find('a')
            temp = kiji_list.text
            try:
                tenpo_name = temp[6:]
                tenpo_name = tenpo_name.replace(')','').replace('(','').replace('店','').replace('本','本店').replace('本店館','本館').replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                print(tenpo_name)
                day = '2021/' + str(temp[:5]).replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                print(day)
                day = datetime.strptime(day, '%Y/%m/%d')
                print(day)
                day_str  = day.strftime('%Y-%m-%d')
                print(day_str)
            except:
                tenpo_name = temp[12:]
                tenpo_name = tenpo_name.replace(')','').replace('(','').replace('店','').replace('本','本店').replace('本店館','本館').replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                print(tenpo_name)
                day = '2020/' + str(temp[5:10]).replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                print(day)
                day = datetime.strptime(day, '%Y/%m/%d')
                print(day)
                day_str  = day.strftime('%Y-%m-%d')

            url = r.get('href')
            print(tenpo_name)
            print(url)
            days.append(day_str)
            urls.append(url)
            print(len(urls))
            tenpo_names.append(tenpo_name)
            tenpo_url_dict[tenpo_name]=url

for url ,tenpo_name ,str_day in zip(urls,tenpo_names,days):
    df_temp = pd.read_html(url)[0]
    context_change_tenpo_name(df_temp,tenpo_name,str_day)
    time.sleep(1)
    #df1 = df_kisyu_list.rename(columns={tenpo_name: tenpo_name})
    print(df)
    df_lists.append(df)


df_concat = pd.concat(df_lists,axis=1)
df=df_concat.drop('データ', axis=1)
df = df.T
try:
    df.columns = ['イベ状況','総差枚','平均差枚','平均G数','勝率','換金率・口コミ','過去の結果','集計対象','集計対象2','日付']
except:
    df.columns = ['イベ状況','総差枚','平均差枚','平均G数','勝率','換金率・口コミ','過去の結果','集計対象','日付']
#df=df.reindex(['状況','総差枚','平均差枚','NAN','平均G数','換金率・口コミ','過去の結果','集計対象','日付'])
df = df.drop('換金率・口コミ',axis=1)
df = df.drop('過去の結果', axis=1)
df = df.drop('集計対象',axis=1)
try:
    df = df.drop('集計対象2',axis=1)
except:
    pass
#df = df.drop('状況',axis=1)
#df = df.drop('NaN',axis=1)
df = df.dropna()
df = df[~df['日付'].isin([0])]
df['平均差枚'] = pd.to_numeric(df['平均差枚'], downcast='integer')
df['平均G数'] = pd.to_numeric(df['平均G数'], downcast='integer')
df = df.sort_values('平均差枚',axis=0,ascending=False)
df_r = df.reset_index()
df_r = df_r[~df_r['イベ状況'].str.contains('-')]
df_r = df_r[~df_r['イベ状況'].str.contains('曜日')]
df = df_r

#pd.set_option('print.max_rows', None)
# ①②をその日取材がある店舗分だけ繰り返す。
df_s = df.sort_values(['index', '日付'])
print(df_s)
df_sum = df.groupby('index').sum()
# 
df_sum = df_sum.sort_values(['平均差枚'], ascending=False)
df_sum = df_sum.drop('平均G数', axis=1)
df_sum = df_sum.rename(columns={'平均差枚': '合計差枚'})
#df_sum = df_sum.reset_index()
df_sum_list = list(df_sum.index)
df_sum_list

df_s = df.sort_values(['index', '日付'])

#print(df_s)
df_sum = df.groupby('index').sum()
df_sum = df_sum.sort_values(['平均差枚'], ascending=False)
df_sum = df_sum.drop('平均G数', axis=1)
df_sum = df_sum.rename(columns={'平均差枚': '合計差枚'})
#df_sum = df_sum.reset_index()
df_sum_list = list(df_sum.index)
#print(df_sum)
df_sum_list
cols = ['index','総差枚','平均差枚','平均G数','日付']
df_concat = pd.DataFrame(index=[], columns=cols)

for tenpo in df_sum_list:
    #record = pd.Series(['hoge', 'fuga'], index=df.columns)
    #record = df_s.query('index == @tenpo')
    record = df_s.query(f'index.str.contains("{tenpo}")', engine='python')
    df_concat = df_concat.append(record, ignore_index=True)

for tenpo_name in df_concat['index'].unique():
    record = df_concat.query(f'index.str.contains("{tenpo_name}")', engine='python')
    print(record)
    if len(record) != 3:
        df_concat = df_concat[df_concat['index'] != tenpo_name ]
#print(df_concat)

def f_str(x):
    #x.rstrip
    return str(x).replace('）', '').replace(')', '').replace('旧イベント日（', '').replace('-', '平常営業')
df_concat['イベ状況'] = df_concat['イベ状況'].map(f_str)
#print(df_concat)
def daisuu(x):
    x = int(x.split('/')[1])
    return x
def set_round(x):
    x = round(x, 1)
    return x

df_concat['台数'] = df_concat['勝率'].map(daisuu)
df = df[~df['日付'].isin([0])]
df_concat['平均G数'] = pd.to_numeric(df_concat['平均G数'], downcast='integer')
df_concat['平均差枚'] = pd.to_numeric(df_concat['平均差枚'], downcast='integer')
df_concat['総差枚'] = pd.to_numeric(df_concat['総差枚'], downcast='integer')
df_concat['出率'] = ((df_concat['平均G数'] * df_concat['台数'] * 3 ) + df_concat['総差枚'] ) / (df_concat['平均G数'] * df_concat['台数'] * 3 ) * 100 

df_concat['出率'] =  df_concat['出率'].map(set_round)
df_concat = df_concat.drop('台数',axis=1)

df = df_concat
print(df_concat)

df = df[df.duplicated(subset=["index"], keep=False)]
df = df.reindex(columns=['日付','index','総差枚','平均差枚','平均G数','イベ状況','勝率','出率'])


lists = df['index'].to_list()

samai_new_list = []
for x in lists:
    if x not in samai_new_list:
        samai_new_list.append(x)
    else:
        pass
text = f'''明日{tomorrow_str_tweet.lstrip('0')} 都内オススメ店舗⚡️
画像は{date_str}の合計の店舗平均差枚順㊙️
↓平均差枚順TOP7↓'''
tenpo_text = ''
for x in samai_new_list[:7]:
    tenpo_text =  tenpo_text + x.lstrip(' ') +'\n' 
texts = text + '\n' + tenpo_text + '\n' +'bit.ly/3vttcm8' + '\n' + '#スロット' + '\n'
print(texts)
samai_new_list = samai_new_list[:7]


rowOddColor = 'rgb(35, 35, 35)'
rowEvenColor = 'black'

#テーブルの作成
fig = go.Figure(data=[go.Table(
        columnwidth =  [7,14,5,4,5,6,6,4], #カラム幅の変更
        header=dict(values=df.columns, align='center', font_size=30,height = 50),
        cells=dict(values=df.values.T, align='center', font_size=30, height = 50,fill_color=[[rowOddColor, rowEvenColor]*11])
        )])
fig.update_layout(title={'text': f"♦️明日{tomorrow_str_tweet.lstrip('0')}のオススメ店舗　{date_str} 3回合計平均差枚順 TOP7♦️",'y':0.97,'x':0.5,'xanchor': 'center'})#タイトル位置の調整
fig.layout.title.font.size= 35 #タイトルフォントサイズの変更
#fig.write_image("a.png")
#fig.write_image("sample_table.jpg",height=600, width=800) #デーブルのサイズ変更

image_path = f"/Users/macbook/Desktop/tokyo_tomorrow_recommend/tokyo_img_2day_recommend_samai_{tomorrow_str_tweet}.png"
# Save the figure as a png image:

#py.image.save_as(fig, 'my_plot.png')/Users/macbook/Desktop/board_image.jpg
fig.update_layout(font={"family":"arial"}) 
fig.update_layout(template="plotly_dark")
fig.write_image(image_path,height=1285, width=1700)
upload_image(image_path,image_path)
# im = Image.open(image_path)
# im_new = crop_center(im, 850, 600)
# im_new.save(image_path, quality=100)


df_concat = pd.concat(df_lists,axis=1)
df=df_concat.drop('データ', axis=1)
df = df.T
try:
    df.columns = ['イベ状況','総差枚','平均差枚','平均G数','勝率','換金率・口コミ','過去の結果','集計対象','集計対象2','日付']
except:
    df.columns = ['イベ状況','総差枚','平均差枚','平均G数','勝率','換金率・口コミ','過去の結果','集計対象','日付']
#df=df.reindex(['状況','総差枚','平均差枚','NAN','平均G数','換金率・口コミ','過去の結果','集計対象','日付'])
df = df.drop('換金率・口コミ',axis=1)
df = df.drop('過去の結果', axis=1)
df = df.drop('集計対象',axis=1)
try:
    df = df.drop('集計対象2',axis=1)
except:
    pass
#df = df.drop('状況',axis=1)
#df = df.drop('NaN',axis=1)
df = df.dropna()
df = df[~df['日付'].isin([0])]
df['平均差枚'] = pd.to_numeric(df['平均差枚'], downcast='integer')
df['平均G数'] = pd.to_numeric(df['平均G数'], downcast='integer')
df = df.sort_values('平均差枚',axis=0,ascending=False)
df_r = df.reset_index()
df_r = df_r[~df_r['イベ状況'].str.contains('-')]
df_r = df_r[~df_r['イベ状況'].str.contains('曜日')]
df = df_r

#pd.set_option('print.max_rows', None)
# ①②をその日取材がある店舗分だけ繰り返す。
df_s = df.sort_values(['index', '日付'])
print(df_s)
df_sum = df.groupby('index').sum()
# 
df_sum = df_sum.sort_values(['平均G数'], ascending=False)
df_sum = df_sum.drop('平均G数', axis=1)
df_sum = df_sum.rename(columns={'平均差枚': '合計差枚'})
#df_sum = df_sum.reset_index()
df_sum_list = list(df_sum.index)
df_sum_list

df_s = df.sort_values(['index', '日付'])

#print(df_s)
df_sum = df.groupby('index').sum()
df_sum = df_sum.sort_values(['平均G数'], ascending=False)
df_sum = df_sum.drop('平均G数', axis=1)
df_sum = df_sum.rename(columns={'平均差枚': '合計差枚'})
#df_sum = df_sum.reset_index()
df_sum_list = list(df_sum.index)
#print(df_sum)
df_sum_list
cols = ['index','総差枚','平均差枚','平均G数','日付']
df_concat = pd.DataFrame(index=[], columns=cols)


for tenpo in df_sum_list:
    #record = pd.Series(['hoge', 'fuga'], index=df.columns)
    #record = df_s.query('index == @tenpo')
    record = df_s.query(f'index.str.contains("{tenpo}")', engine='python')
    df_concat = df_concat.append(record, ignore_index=True)

for tenpo_name in df_concat['index'].unique():
    record = df_concat.query(f'index.str.contains("{tenpo_name}")', engine='python')
    print(record)
    if len(record) != 3:
        df_concat = df_concat[df_concat['index'] != tenpo_name ]
#print(df_concat)

def f_str(x):
    #x.rstrip
    return str(x).replace('）', '').replace(')', '').replace('旧イベント日（', '').replace('-', '平常営業')
df_concat['イベ状況'] = df_concat['イベ状況'].map(f_str)
#print(df_concat)
def daisuu(x):
    x = int(x.split('/')[1])
    return x
def set_round(x):
    x = round(x, 1)
    return x

df_concat['台数'] = df_concat['勝率'].map(daisuu)
df = df[~df['日付'].isin([0])]
df_concat['平均G数'] = pd.to_numeric(df_concat['平均G数'], downcast='integer')
df_concat['平均差枚'] = pd.to_numeric(df_concat['平均差枚'], downcast='integer')
df_concat['総差枚'] = pd.to_numeric(df_concat['総差枚'], downcast='integer')
df_concat['出率'] = ((df_concat['平均G数'] * df_concat['台数'] * 3 ) + df_concat['総差枚'] ) / (df_concat['平均G数'] * df_concat['台数'] * 3 ) * 100 

df_concat['出率'] =  df_concat['出率'].map(set_round)
df_concat = df_concat.drop('台数',axis=1)

df = df_concat
print(df_concat)

df = df[df.duplicated(subset=["index"], keep=False)]
df = df.reindex(columns=['日付','index','総差枚','平均差枚','平均G数','イベ状況','勝率','出率'])


lists = df['index'].to_list()

game_new_list = []
for x in lists:
    if x not in game_new_list:
        game_new_list.append(x)
    else:
        pass
text = f'''明日{tomorrow_str_tweet.lstrip('0')} 都内高稼働店舗予想⚡️
画像は{date_str}の合計の店舗平均G数順㊙️
↓平均G数順TOP7↓'''
tenpo_text = ''
for x in game_new_list[:7]:
    tenpo_text =  tenpo_text + x.lstrip(' ') +'\n' 
texts = text + '\n' + tenpo_text + '\n' +'bit.ly/3vttcm8' + '\n' + '#スロット' + '\n'
print(texts)
game_new_list = game_new_list[:7]


rowOddColor = 'rgb(35, 35, 35)'
rowEvenColor = 'black'

#テーブルの作成
fig = go.Figure(data=[go.Table(
        columnwidth =  [7,14,5,4,5,6,6,4], #カラム幅の変更
        header=dict(values=df.columns, align='center', font_size=30,height = 50),
        cells=dict(values=df.values.T, align='center', font_size=30, height = 50,fill_color=[[rowOddColor, rowEvenColor]*11])
        )])
fig.update_layout(title={'text': f"♦️明日{tomorrow_str_tweet.lstrip('0')}のオススメ店舗　{date_str} 3回合計平均差枚順 TOP7♦️",'y':0.97,'x':0.5,'xanchor': 'center'})#タイトル位置の調整
fig.layout.title.font.size= 35 #タイトルフォントサイズの変更
#fig.write_image("a.png")
#fig.write_image("sample_table.jpg",height=600, width=800) #デーブルのサイズ変更

image_path = f"/Users/macbook/Desktop/tokyo_tomorrow_recommend/tokyo_img_2day_recommend_game_{tomorrow_str_tweet}.png"
# Save the figure as a png image:

#py.image.save_as(fig, 'my_plot.png')/Users/macbook/Desktop/board_image.jpg
fig.update_layout(font={"family":"arial"}) 
fig.update_layout(template="plotly_dark")
fig.write_image(image_path,height=1285, width=1700)
upload_image(image_path,image_path)
# im = Image.open(image_path)
# im_new = crop_center(im, 850, 600)
# im_new.save(image_path, quality=100)


recommend_tenpo = samai_new_list+ game_new_list
recommend_tenpo_list = list(dict.fromkeys(recommend_tenpo))
#print(recommend_tenpo_list)
for x in recommend_tenpo_list:
    print(x.lstrip(' '))


#明日の東京都オススメ記事

import os
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
import urllib
from bs4 import BeautifulSoup
import re
import math
import pyperclip
import csv
import codecs
import requests
import urllib.request as req
import openpyxl
import glob
from sklearn.datasets import  load_iris
import json
import time
import datetime

import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
from PIL import Image, ImageDraw, ImageFont
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.io as pio
import japanize_matplotlib
import datetime
from matplotlib.dates import MonthLocator



pio.templates.default = 'seaborn'
plt.rcParams['font.family'] = 'IPAexGothic'

# %matplotlib inline
# %config InlineBackend.figure_formats = {'png', 'retina'}

import matplotlib
import plotly

import cv2
import numpy as np
from PIL import Image

import gspread
import json

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 


print('ライブラリの読み込み完了')


#nのつく日
#ここからスタート
import datetime

import os
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
import urllib
from bs4 import BeautifulSoup
date_list = []
day_str_list= []
today = datetime.date.today () 
tomorrow_str = tomorrow.strftime('%Y-%m-%d')
tomorrow_str_tweet = tomorrow.strftime('%m月%d日')
tomorrow_str_blog_url = today.strftime('%Y/%m')
print(tomorrow_str[-1])
target_day_number = tomorrow_str[-1]

for i in range(54):
    belong_day = today - datetime.timedelta(days= i)
    belong_day_str = belong_day.strftime('%Y-%m-%d')
    day_str = belong_day.strftime('%m月%d日').lstrip('0')
    ##print(belong_day_str[-2:])
    if belong_day_str[-1] == tomorrow_str[-1]:
        if belong_day_str[-2:] == '31':
            continue
        date_list.append(belong_day_str)
        day_str_list.append(day_str)
date_str = ''
for date in day_str_list[:5]:
    date_str += date + ' '

date_list = date_list[:5]
print(date_str)
print(date_list)




#東京都記事反省用
import os
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
import urllib
from bs4 import BeautifulSoup
import re
import math
import pyperclip
import csv
import codecs
import requests
import urllib.request as req
import openpyxl
import glob
from sklearn.datasets import  load_iris
import json
import time
import datetime
from datetime import datetime, date, timedelta
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
from PIL import Image, ImageDraw, ImageFont
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.io as pio
import japanize_matplotlib
import datetime
import urllib.parse
from matplotlib.dates import MonthLocator

import urllib.parse
pio.templates.default = 'seaborn'
plt.rcParams['font.family'] = 'IPAexGothic'
# %matplotlib inline
# %config InlineBackend.figure_formats = {'png', 'retina'}

import matplotlib
import plotly

print('ライブラリの読み込み完了')

def get_concat_h_temp(im1, im2):
    dst = Image.new('RGB', (im1.width+100, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


class WordPress:
  def __init__(self, date, todoufuken):
    self.date = date
    self.todoufuken = todoufuken

def change_table_color_samai(x):
    x = int(x)
    if x > 3000:
        x = 'blue_7'+ str(x)
        return x
    elif 3000 > x > 2500:
        x = 'blue_6'+ str(x)
        return x
    elif 2500 > x > 2000:
        x = 'blue_5'+ str(x)
        return x
    elif 2000 > x > 1500:
        x = 'blue_4'+ str(x)
        return x
    elif 1500 > x > 1000:
        x = 'blue_3'+ str(x)
        return x
    elif 1000 > x > 500:
        x = 'blue_2'+ str(x)
        return x
    elif 500 > x > 0:
        x = 'blue_1'+ str(x)
        return x
    else:
        return x

def change_table_color_game(x):
    x = int(x)
    if x > 8000:
        x = 'blue_7'+ str(x)
        return x
    elif 8000 > x > 7000:
        x = 'blue_6'+ str(x)
        return x
    elif 7000 > x > 6000:
        x = 'blue_5'+ str(x)
        return x
    elif 6000 > x > 5000:
        x = 'blue_4'+ str(x)
        return x
    elif 5000 > x > 4000:
        x = 'blue_3'+ str(x)
        return x
    elif 4000 > x > 3000:
        x = 'blue_2'+ str(x)
        return x
    elif 2000 > x > 1000:
        x = 'blue_1'+ str(x)
        return x
    else:
        return x

def fraction_units(x):
    x = x.split('/')
    x = int(x[1])
    return x

def win_rate(x):
    x = x.split('/')
    x = int(x[0])
    return x

def set_round(x):
    x = round(x, 1)
    return x

def date_change(x):
    x = x.replace('2021-','').replace('2020-','').replace('-','/')
    return x

def upload_image(in_image_file_name, out_image_file_name):
    if os.path.exists(in_image_file_name):
        with open(in_image_file_name, 'rb') as f:
            binary = f.read()

        data = {
            "name": out_image_file_name,
            "type": 'image/png',
            "overwrite": True,
            "bits": binary
        }

        media_id = wp.call(media.UploadFile(data))['id']
        print(in_image_file_name.split('/')
              [-1], 'Upload Success : id=%s' % media_id)
        return media_id
    else:
        print(in_image_file_name.split('/')[-1], 'NO IMAGE!!')
import urllib.parse



#ここから
######

######
tenpo_kiji_text = ''
error_tenpo_name_list = []
for tenpo_name in recommend_tenpo_list:
    try:
        tenpo_name_decode = urllib.parse.quote(tenpo_name)
        kiji_texts =[]
        links = []
        urls = []
        days =[]
        tenpo_names = []
        tenpo_url_dict = {}
        df_lists = []
        image_concat_list= []
        from datetime import datetime, date, timedelta
        url = f'https://min-repo.com/?s={tenpo_name_decode}'
        #取材日データと機種データを取得する関数
        kiji =''
        urls_list = [f'https://min-repo.com/?s={tenpo_name_decode}',f'https://min-repo.com/page/2/?s={tenpo_name_decode}',f'https://min-repo.com/page/3/?s={tenpo_name_decode}']


        kiji_lists = []
        for url in urls_list:
            response = req.urlopen(url) #データを取得
            soup = BeautifulSoup(response, 'html.parser')
            kiji_lists += soup.find_all(class_='ichiran_title')
            

        for kiji in kiji_lists:
                text = kiji.text.replace('\n','')
                kiji_texts.append(text)

        for kiji_list in kiji_lists:
            r = kiji_list.find('a')
            temp = kiji_list.text
            try:
                tenpo_name = temp[6:]
                tenpo_name = tenpo_name.replace(')','').replace('(','').replace('店','').replace('本','本店').replace('本店館','本館').replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                day = '2021/' + str(temp[:5]).replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                day = datetime.strptime(day, '%Y/%m/%d')
                day_str  = day.strftime('%Y-%m-%d')
            except:
                tenpo_name = temp[12:]
                tenpo_name = tenpo_name.replace(')','').replace('(','').replace('店','').replace('本','本店').replace('本店館','本館').replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                day = '2020/' + str(temp[5:10]).replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                day = datetime.strptime(day, '%Y/%m/%d')
                day_str  = day.strftime('%Y-%m-%d')
            print(tenpo_name)
            print(day)
            url = r.get('href')
            if day_str in date_list:
                #print(tenpo_name)
                #print(url)
                #print(day_str)
                days.append(day_str)
                urls.append(url)
                tenpo_names.append(tenpo_name)
                tenpo_url_dict[tenpo_name]=url

        cols =['機種', '平均差枚', '平均G数','勝率','出率']
        df = pd.DataFrame(index=[], columns=cols)

        for ichiran_url ,tenpo_name ,str_day in zip(urls,tenpo_names,days):
            #print(url)
            #print(tenpo_name)
            #print(str_day)
            time.sleep(1)

            df_kisyu = pd.read_html(ichiran_url)[1]
            record  = df_kisyu[~df_kisyu['機種'].str.contains('機種')]
            record['日付'] = str_day
            record['出率'] = record['出率'].replace('%', '', regex=True).replace('-', '0', regex=True)
            record['出率'] = pd.to_numeric(record['出率'], downcast='integer')
            df = df.append(record, ignore_index=True)

            #df['台番'] = pd.to_numeric(df['台番'], downcast='integer')
            #df = df.sort_values('台番')
        df_kisyu_matome = df
        print(df_kisyu_matome)
        new_days_list = []
        for temp_day in days:
            temp_day_a = temp_day.replace('2021-','').replace('2020-','').replace('-','/')
            new_days_list.append(temp_day_a)
            print(temp_day_a)

        response = req.urlopen(url) #データを取得
        soup = BeautifulSoup(response, 'html.parser')
        todoufuken = soup.find(class_='todofuken')
        todoufuken.text

        import gspread
        import json
        #pd.set_option('print.max_rows', 8)

        #ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
        from oauth2client.service_account import ServiceAccountCredentials 

        #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        #認証情報設定
        #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/macbook/Desktop/python/共通config/twitteranalytics-jsonsercretkey.json', scope)

        #OAuth2の資格情報を使用してGoogle APIにログインします。
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_url('https://docs.google.com/spreadsheets/d/1PCaRKS0-vfqbFDuqNmMmGzrYm6dj4TyOGT6WNqdbbFg/edit#gid=1450792119')
        worksheet = workbook.worksheet('機種名変換シート')
        df = pd.DataFrame(worksheet.get_all_values())

        df.columns = list(df.loc[0, :])
        df.drop(0, inplace=True)
        df.reset_index(inplace=True)
        kisyu_convert_df = df
        print(kisyu_convert_df)

        def name_convert_change(kisyu_name):
            target_convert_df = kisyu_convert_df.query(f'みんレポ.str.contains(@kisyu_name)', engine='python')
            try:
                target_kisyu_name = target_convert_df.iloc[0,2]
                return target_kisyu_name
            except:
                #if kisyu_name != kisyu_name:
                time.sleep(1)
                new_kisyu_name = kisyu_name.replace('パチスロ　','').replace('ぱちスロ　','').replace('パチスロ ','').replace('パチスロ','').replace(' ','').replace('　','')
                #worksheet.append_row([kisyu_name,new_kisyu_name])
                #print(new_kisyu_name)
                return new_kisyu_name

        def name_convert_change2(kisyu_name):
            
            compare_kisyu_name = ''
            target_convert_df = kisyu_convert_df.query(f'みんレポ.str.contains(@kisyu_name)', engine='python')
            try:
                target_kisyu_name = target_convert_df.iloc[0,2]
                return target_kisyu_name
            except:
                if kisyu_name != compare_kisyu_name:
                    time.sleep(1)
                    new_kisyu_name = kisyu_name.replace('パチスロ　','').replace('ぱちスロ　','').replace('パチスロ ','').replace('パチスロ','').replace(' ','').replace('　','')
                    #worksheet.append_row([kisyu_name,new_kisyu_name])
                    #print(new_kisyu_name)
                    compare_kisyu_name = kisyu_name
                    return new_kisyu_name
                else:
                    new_kisyu_name = kisyu_name.replace('パチスロ　','').replace('ぱちスロ　','').replace('パチスロ ','').replace('パチスロ','').replace(' ','').replace('　','')
                    return new_kisyu_name

        def get_concat_h(im1, im2,im3):
            dst = Image.new('RGB', (im1.width*3, im1.height))
            dst.paste(im1, (0, 0))
            dst.paste(im2, (im1.width, 0))
            dst.paste(im3, (im1.width*2, 0))
            return dst


        kiji_texts =[]
        links = []
        urls = []
        days =[]
        tenpo_names = []
        tenpo_url_dict = {}
        df_lists = []
        image_concat_list= []
        from datetime import datetime, date, timedelta
        import urllib.parse

            
        for kiji_list in kiji_lists:
            r = kiji_list.find('a')
            temp = kiji_list.text
            try:
                tenpo_name = temp[6:]
                tenpo_name = tenpo_name.replace(')','').replace('(','').replace('店','').replace('本','本店').replace('本店館','本館').replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                day = '2021/' + str(temp[:5]).replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                day = datetime.strptime(day, '%Y/%m/%d')
                day_str  = day.strftime('%Y-%m-%d')
            except:
                tenpo_name = temp[12:]
                tenpo_name = tenpo_name.replace(')','').replace('(','').replace('店','').replace('本','本店').replace('本店館','本館').replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                day = '2020/' + str(temp[5:10]).replace(')','').replace('(','').replace(' ','').replace('月','').replace('火','').replace('水','').replace('木','').replace('金','').replace('土','').replace('日','')
                day = datetime.strptime(day, '%Y/%m/%d')
                day_str  = day.strftime('%Y-%m-%d')
            #print(tenpo_name)
            #print(day)
            url = r.get('href')
            if day_str in date_list:
                #print(tenpo_name)
                #print(url)
                #print(day_str)
                days.append(day_str)
                urls.append(url)
                tenpo_names.append(tenpo_name)
                tenpo_url_dict[tenpo_name]=url

        for url ,tenpo_name ,str_day in zip(urls,tenpo_names,days):
            #print(url)
            #print(tenpo_name)
            #print(str_day)
            #pd.set_option('print.max_rows', 8)
            ichiran_url = f'{url}?kishu=%E5%85%A8%E5%8F%B0'
            df_kisyu = pd.read_html(ichiran_url)[0]
            df = df_kisyu[~df_kisyu['機種'].str.contains('機種')]
            df['台番'] = pd.to_numeric(df['台番'], downcast='integer')
            df = df.sort_values('台番')
            df['台番'] = df['台番'].astype(str)
            convert_list = []
                #ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
            from oauth2client.service_account import ServiceAccountCredentials 

            #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

            #認証情報設定
            #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
            credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/macbook/Desktop/python/共通config/twitteranalytics-jsonsercretkey.json', scope)

            #OAuth2の資格情報を使用してGoogle APIにログインします。
            gc = gspread.authorize(credentials)
            workbook = gc.open_by_url('https://docs.google.com/spreadsheets/d/1PCaRKS0-vfqbFDuqNmMmGzrYm6dj4TyOGT6WNqdbbFg/edit#gid=1450792119')
            worksheet = workbook.worksheet('機種名変換シート')
            df_kisyu = pd.DataFrame(worksheet.get_all_values())

            df_kisyu.columns = list(df_kisyu.loc[0, :])
            df_kisyu.drop(0, inplace=True)
            df_kisyu.reset_index(inplace=True)
            kisyu_convert_df = df_kisyu
            for kisyu_name in df['機種']:
                kisyu_name = kisyu_name.replace(' ', '').replace('　', '')
                try:
                    target_low = kisyu_convert_df.query(f'みんレポ.str.contains("{kisyu_name}")', engine='python')
                except:
                    continue
                try:
                    convert_kisyu_name = target_low.iloc[0,2]
                    #print(convert_kisyu_name)
                    convert_list.append(convert_kisyu_name)
                except:
                    if kisyu_name != convert_kisyu_name:
                        new_kisyu_name = kisyu_name.replace('パチスロ　','').replace('ぱちスロ　','').replace('パチスロ ','').replace('パチスロ','').replace(' ','').replace('　','')
                        worksheet.append_row([kisyu_name,new_kisyu_name])
                        time.sleep(1)
                        print('追加',convert_kisyu_name)
                    convert_kisyu_name  =  kisyu_name
                    time.sleep(1)
                    convert_list.append(convert_kisyu_name)
            #print(len(convert_list))
            df = df.reset_index(drop=True)
            df['機種'] = pd.Series(convert_list)
            df = df.reindex(columns=['台番', '機種', '差枚','G数','出率'])
            #df['台番'] = pd.to_numeric(df['台番'], downcast='integer')
            #df = df.sort_values('台番')
            df['data'] = df['機種'].str.cat(df['台番'], sep='_')
            df_a = df.set_index('data')
            df_a['出率'] = df_a['出率'].str.replace('-', '0').str.strip('%')
            df_a = df_a[['差枚','G数','出率']]
            df_all = df_a.astype({'差枚':'int','G数':'int'})
            #df_completed = df_completed.drop('差枚', axis=1)

            df_completed_samai = df_all.drop('G数', axis=1)
            df_completed_samai = df_completed_samai.drop('出率', axis=1)

            df_len = math.floor(len(df_completed_samai)/3)
            df_1 = df_completed_samai[0:df_len]
            df_2 = df_completed_samai[df_len:df_len*2]
            df_3 = df_completed_samai[df_len*2:len(df_completed_samai)]
            
            for df ,i in zip([df_1,df_2,df_3],[1,2,3]):
                fig = ff.create_annotated_heatmap(z=df.values, x=list(df.columns),
                                                y=list(df.index), colorscale='Blues',
                                                hoverinfo='none',zauto=False,zmin=0,zmax=1500)
                fig.update_layout(height=4000, width=400,showlegend=False,font=dict(family='Arial',size=25),margin = dict(l = 300, r = 0, t = 100, b = 40))
                fig.update_layout(title={'text': f"{str_day}_{i}枚目",'y':0.996,'x':0.6,'xanchor': 'center'})#タイトル
                fig.update_layout(font={"family":"Arial"}) 
                fig.update_layout(template="plotly_dark",yaxis=dict(visible=True,autorange='reversed'))
                fig.write_image(f"/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{str_day}_{i}_差枚.png",height=4040, width=400)
                image_path = f"/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{str_day}_{i}_差枚.png"

                image_concat_list.append(image_path)

            #df_completed = df_completed.drop('G数', axis=1)
            df_completed_samai = df_all.drop('差枚', axis=1)
            df_completed_samai = df_completed_samai.drop('出率', axis=1)
            df_len = math.floor(len(df_completed_samai)/3)
            df_1 = df_completed_samai[0:df_len]
            df_2 = df_completed_samai[df_len:df_len*2]
            df_3 = df_completed_samai[df_len*2:len(df_completed_samai)]
            
            for df ,i in zip([df_1,df_2,df_3],[1,2,3]):
                fig = ff.create_annotated_heatmap(z=df.values, x=list(df.columns),
                                                y=list(df.index), colorscale='Blues',
                                                hoverinfo='none',zauto=False,zmin=4000,zmax=7500)
                fig.update_layout(height=4000, width=400,margin = dict(l = 0, r = 10, t = 100, b = 40),font=dict(family='Arial',size=27))
                fig.update_layout(font={"family":"Arial"}) 
                fig.update_layout(template="plotly_dark",yaxis=dict(visible=False,autorange='reversed'))
                fig.write_image(f"/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{str_day}_{i}_G数.png",height=4040, width=100)
                image_path = f"/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{str_day}_{i}_G数.png"
                image_concat_list.append(image_path)
                im1 = Image.open(f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{str_day}_{i}_差枚.png')
                im2 = Image.open(f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{str_day}_{i}_G数.png')
                get_concat_h_temp(im1, im2).save(f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{str_day}_{i}.png')

        for df ,i in zip([df_1,df_2,df_3],[1,2,3]):
            fig = ff.create_annotated_heatmap(z=df.values, x=list(df.columns),y=list(df.index), colorscale='Blues',hoverinfo='none',zauto=False,zmin=4000,zmax=7000)
            fig.update_layout(height=4000, width=400,margin = dict(l = 0, r = 10, t = 100, b = 40,  ),font=dict(family='Arial',size=27),newshape=dict(line=dict(color="cyan", width=4, dash="solid")))
            fig.update_layout(title={'text': f"G数",'y':0.996,'x':0.5,'xanchor': 'center'})#タイトル
            fig.update_layout(font={"family":"Arial"}) 
            fig.update_layout(template="plotly_dark",yaxis=dict(visible=False,autorange='reversed'))
            fig.write_image(f"/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{str_day}_{i}_G数.png",height=4040, width=100)
            image_path = f"/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{str_day}_{i}_G数.png"
            image_concat_list.append(image_path)


        for i in range(1,4):
                im1 = Image.open(f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{date_list[2]}_{i}.png')
                im2 = Image.open(f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{date_list[1]}_{i}.png')
                im3 = Image.open(f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{date_list[0]}_{i}.png')
                #im4 = Image.open(f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{date_list[1]}_{i}.png')
                #im5 = Image.open(f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{date_list[0]}_{i}.png')
                get_concat_h(im1, im2,im3).save(f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{date_list[0]}_{i}.jpg')


        from PIL import Image, ImageDraw, ImageFont
        #def recommend_image(todouhuken,write_image_context):

        write_image_context =f"""　　
            ◆{tenpo_name}◆
            {tomorrow_str_tweet} 予測分析
            過去５回分の傾向・分析まとめ

        """
        #元画像を読み込んでくる
        #image_path = r"C:\Users\81801\Desktop\twitter_anarytics_bot\recommend_syuzai_report\board_image.jpg" #win
        image_path = "/Users/macbook/Desktop/sumnail.png" #mac
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        #フォントを指定する（フォントファイルはWindows10ならC:\\Windows\\Fontsにあります）
        #フォントの読み込
        if os.name == 'nt':
            font_path = r"C:\Windows\Fonts\ラノベPOP.otf"
        elif os.name == 'posix':
            font_path = "/Users/macbook/Library/Fonts/GenEiGothicP-H-KL.otf"

        #sizeは文字サイズです（とりあえず適当に50）
        font = ImageFont.truetype(font_path, size=110)
        #文字を描く
        #最初の(0,0)は文字の描画を開f始する座標位置です　もちろん、(10,10)などでもOK
        #fillはRGBで文字の色を決めています
        draw.text((30,140), write_image_context, fill=(255,255,255), font=font,anchor='mm')
        image.save(f"/Users/macbook/Desktop/{tenpo_name}_{tomorrow_str_tweet}.png")
        sumnail_path =f"/Users/macbook/Desktop/{tenpo_name}_{tomorrow_str_tweet}.png"

        #image.show()    


        #機種一覧

        #pd.set_option('print.max_rows', None)
        # n= 0
        # for ichiran_url ,tenpo_name ,str_day in zip(urls,tenpo_names,days):
        #     print(url)
        #     print(tenpo_name)
        #     print(str_day)
        #     time.sleep(1)
        #     df_kisyu = pd.read_html(ichiran_url)[1]
        #     df_kisyu  = df_kisyu[~df_kisyu['機種'].str.contains('機種')]
        #     df_kisyu['機種'] = df_kisyu['機種'].map(name_convert_change)
            
        #     #df_kisyu['日付'] = str_day
        #     #df_kisyu['日付'] = df_kisyu['日付'].map(date_change)
        #     df_kisyu['出率'] = df_kisyu['出率'].replace('%', '', regex=True).replace('-', '0', regex=True)
        #     df_kisyu['出率'] = df_kisyu['出率'].astype('float')
        #     df_kisyu['平均G数'] = df_kisyu['平均G数'].astype('int')
        #     df_kisyu['平均差枚'] = df_kisyu['平均差枚'].astype('int')
        #     df_kisyu['平均G数'] = df_kisyu['平均G数'] - 6 
        #     df_kisyu['平均差枚'] = df_kisyu['平均差枚'] + 4
        #     df_kisyu['出率'] = df_kisyu['出率'] + 0.1
        #     df_kisyu = df_kisyu.sort_values('出率', ascending=False)
        #     #df_kisyu['出率'] = pd.to_numeric(record['出率'], downcast='integer') なぜか数値がずれる・・・・
        #     df_kisyu['平均差枚'] = df_kisyu['平均差枚'].map(change_table_color_samai)
        #     df_kisyu['平均G数'] = df_kisyu['平均G数'].map(change_table_color_game)
        #     print(df_kisyu)

        #     if n == 0:
        #         break
        # df_kisyu_text = df_kisyu.to_html(justify='justify-all',index=False)
        # completed_df_kisyu_text = df_kisyu_text.replace('<td>blue_1','<td class="color_blue_1">').replace('<td>blue_2','<td class="color_blue_2">').replace('<td>blue_3','<td class="color_blue_3">').replace('<td>blue_4','<td class="color_blue_4">').replace('<td>blue_5','<td class="color_blue_5">').replace('<td>blue_6','<td class="color_blue_6">').replace('<td>blue_7','<td class="color__blue_7">')
        # print('完了')


        n=0
        for url ,tenpo_name ,str_day in zip(urls,tenpo_names,days):
            #print(url)
            #print(tenpo_name)
            #print(str_day)
            ichiran_url = f'{url}?kishu=%E5%85%A8%E5%8F%B0'
            df_ichiran = pd.read_html(ichiran_url)[0]
            df_ichiran  = df_ichiran[~df_ichiran['機種'].str.contains('機種')]
            df_ichiran['機種'] = df_ichiran['機種'].map(name_convert_change2)
            df_ichiran['日付'] = str_day
            df_ichiran['日付'] = df_ichiran['日付'].map(date_change)
            df_ichiran['出率'] = df_ichiran['出率'].replace('%', '', regex=True).replace('-', '0', regex=True)
            df_ichiran['出率'] = pd.to_numeric(df_ichiran['出率'], downcast='integer')
            df_ichiran['差枚'] = pd.to_numeric(df_ichiran['差枚'], downcast='integer')
            df_ichiran['G数'] = pd.to_numeric(df_ichiran['G数'], downcast='integer')
            df_ichiran['G数'] =  df_ichiran['G数'] - 3 
            df_ichiran['差枚'] =  df_ichiran['差枚'] + 2
            df_ichiran['差枚'] = df_ichiran['差枚'].map(change_table_color_samai)
            df_ichiran['G数'] = df_ichiran['G数'].map(change_table_color_game)
            time.sleep(1)
            if n == 0:
                break
        ichiran_text = df_ichiran.to_html(justify='justify-all',index=False)
        completed_ichiran_text = ichiran_text.replace('<td>blue_1','<td class="color_blue_1">').replace('<td>blue_2','<td class="color_blue_2">').replace('<td>blue_3','<td class="color_blue_3">').replace('<td>blue_4','<td class="color_blue_4">').replace('<td>blue_5','<td class="color_blue_5">').replace('<td>blue_6','<td class="color_blue_6">').replace('<td>blue_7','<td class="color_blue_7">')
        print('完了')


        #②
        #pd.set_option('print.max_rows', 8)

        df_kisyu_matome['台数'] = df_kisyu_matome['勝率'].map(fraction_units)
        df_kisyu_matome['勝利台数'] = df_kisyu_matome['勝率'].map(win_rate)
        df_kisyu_matome['日付'] = df_kisyu_matome['日付'].map(date_change)
        df_kisyu_matome['平均差枚'] = pd.to_numeric(df_kisyu_matome['平均差枚'], downcast='integer')
        df_kisyu_matome['平均G数'] = pd.to_numeric(df_kisyu_matome['平均G数'], downcast='integer')
        df_kisyu_matome['総差枚'] = df_kisyu_matome['平均差枚']*df_kisyu_matome['台数']
        df_kisyu_matome['総G数'] = df_kisyu_matome['平均G数']*df_kisyu_matome['台数']
        df_kisyu_matome['集計回数'] = 1
        df_kisyu_matome

        cols =['機種', '台番', '差枚','G数','出率']
        ichiran_concat_df = pd.DataFrame(index=[], columns=cols)
        for url ,tenpo_name ,str_day in zip(urls,tenpo_names,days):
            print(url)
            print(tenpo_name)
            print(str_day)
            ichiran_url = f'{url}?kishu=%E5%85%A8%E5%8F%B0'
            df_ichiran = pd.read_html(ichiran_url)[0]
            record  = df_ichiran[~df_ichiran['機種'].str.contains('機種')]
            record['日付'] = str_day
            record['日付'] = record['日付'].map(date_change)
            record['出率'] = record['出率'].replace('%', '', regex=True).replace('-', '0', regex=True)
            record['出率'] = pd.to_numeric(record['出率'], downcast='integer')
            record['差枚'] = pd.to_numeric(record['差枚'], downcast='integer')
            record['G数'] = pd.to_numeric(record['G数'], downcast='integer')
            ichiran_concat_df = ichiran_concat_df.append(record, ignore_index=True)
            time.sleep(1)
        ichiran_concat_df

        ichiran_target_df_list = []
        # for target_day in days[:4]:
        #     print(target_day)
        target_day = temp_day_a[0]
        ichiran_pickup_df = ichiran_concat_df.query('日付.str.contains(@target_day)', engine='python')
        ichiran_pickup_df = ichiran_pickup_df[ichiran_pickup_df['差枚'] > 1000]
        ichiran_pickup_df_1 = ichiran_pickup_df[ichiran_pickup_df['G数'] > 7000]
        #print(ichiran_pickup_df_1)

        target_day = temp_day_a[1]
        ichiran_pickup_df = ichiran_concat_df.query('日付.str.contains(@target_day)', engine='python')
        ichiran_pickup_df = ichiran_pickup_df[ichiran_pickup_df['差枚'] > 1000]
        ichiran_pickup_df_2 = ichiran_pickup_df[ichiran_pickup_df['G数'] > 7000]
        #print(ichiran_pickup_df_2)

        target_day = temp_day_a[2]
        ichiran_pickup_df = ichiran_concat_df.query('日付.str.contains(@target_day)', engine='python')
        ichiran_pickup_df = ichiran_pickup_df[ichiran_pickup_df['差枚'] > 1000]
        ichiran_pickup_df_3 = ichiran_pickup_df[ichiran_pickup_df['G数'] > 7000]
        #print(ichiran_pickup_df_3)

        target_day = temp_day_a[3]
        ichiran_pickup_df = ichiran_concat_df.query('日付.str.contains(@target_day)', engine='python')
        ichiran_pickup_df = ichiran_pickup_df[ichiran_pickup_df['差枚'] > 1000]
        ichiran_pickup_df_4 = ichiran_pickup_df[ichiran_pickup_df['G数'] > 7000]
        #print(ichiran_pickup_df_4)

        ichiran_pickup_text = f"""<h2>過去4回の日別の単品で出てた台まとめ</h2>\n※差枚+1,000枚以上かつ回転数7000G以上を抽出\n日付をタップすると日付毎に台データが見れます\n[st-tab-content memo="全体を包むボックスです" type="button" myclass="st-radius"]
        [st-input-tab fontawesome="" text="{days[0]}" bgcolor="" bordercolor="#0999" color="" fontweight="" checked="checked"]
        [st-input-tab fontawesome="" text="{days[1]}" bgcolor="" bordercolor="#0999" color="" fontweight="" checked=""]
        [st-input-tab fontawesome="" text="{days[2]}" bgcolor="" bordercolor="#0999" color="" fontweight="" checked=""]
        [st-input-tab fontawesome="" text="{days[3]}" bgcolor="" bordercolor="#0999" color="" fontweight="" checked=""]
        [st-tab-main bgcolor="" bordercolor=""]

        {ichiran_pickup_df_1.to_html(justify='justify-all',index=False)}

        [/st-tab-main][st-tab-main bgcolor="" bordercolor=""]

        {ichiran_pickup_df_2.to_html(justify='justify-all',index=False)}

        [/st-tab-main][st-tab-main bgcolor="" bordercolor=""]

        {ichiran_pickup_df_3.to_html(justify='justify-all',index=False)}

        [/st-tab-main][st-tab-main bgcolor="" bordercolor=""]

        {ichiran_pickup_df_4.to_html(justify='justify-all',index=False)}

        [/st-tab-main]
        [/st-tab-content]"""
        #print(ichiran_pickup_df_2.to_html(justify='justify-all',index=False))


        def context_change_tenpo_name(df_temp,tenpo_name,day):
            global df
            #⬇️列のデータをインデックスに指定する
            df_temp.columns = ['データ', tenpo_name]
            #⬇️余計な文字の除く
            df_temp[tenpo_name] = df_temp[tenpo_name].str.replace('+','').str.replace('枚','').str.replace('G','').str.replace(',','')
            df1 = df_temp.append({'データ': '日付', tenpo_name: day}, ignore_index=True)
            if df1.loc[3, 'データ'] != '平均G数':
                    df1 = df1.append({'データ': '平均G数', tenpo_name: 0}, ignore_index=True)
            
            for i in range(len(df1)):
                if df1.loc[i, 'データ'] == '勝率':
                    df = df1.drop(i) 
            return df
        ave_samai_list = []
        ave_game_list = []
        sou_samai_list = []
        days.reverse()
        tenpo_names.reverse()
        urls.reverse()
        for url ,tenpo_name ,str_day in zip(urls,tenpo_names,days):
            print(url)
            df_matome = pd.read_html(url)[0]
            print(tenpo_name)
            context_change_tenpo_name(df_matome,tenpo_name,str_day)
            print(str_day)
            ave_samai = df_matome.query('データ == ["平均差枚"]').iloc[0,1]
            ave_game = df_matome.query('データ == ["平均G数"]').iloc[0,1]
            sou_samai = df_matome.query('データ == ["総差枚"]').iloc[0,1]
            ave_samai_list.append(ave_samai)
            ave_game_list.append(ave_game)
            sou_samai_list.append(sou_samai)
            #print(df)
            time.sleep(1)
            i += 1

        new_days_list_reverse = list(reversed(new_days_list))
        #print(new_days_list_reverse)

        slump_graph = '''<h2>直近5回の店舗平均差枚と平均G数グラフ</h2>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.3.0/Chart.bundle.min.js"></script>

        <div class="container" style="width:100%">
            <canvas id="canvas"></canvas>
        </div>
        <script>
        window.onload = function() {
            ctx = document.getElementById("canvas").getContext("2d");
            window.myBar = new Chart(ctx, {
                type: 'bar',
                data: barChartData,
                options: complexChartOption
            });
        };
        </script>



        <script>
        // とある4週間分のデータログ
        var barChartData = {
            labels: ''' + str(new_days_list_reverse) + ''',
            datasets: [
            {
                type: 'line',
                label: '平均差枚',
                data:'''+ str(ave_samai_list) +''',
                borderColor : "rgba(254,97,132,0.8)",
                        pointBackgroundColor    : "rgba(254,97,132,0.8)",
                        fill: false,
                yAxisID: "y-axis-1",// 追加
            },
            {
                type: 'bar',
                label: '平均G数',
                data:'''+ str(ave_game_list) +''',
                borderColor : "rgba(54,164,235,0.8)",
                backgroundColor : "rgba(54,164,235,0.5)",
                yAxisID: "y-axis-2",
            },
            ],
        };
        </script>



        <script>
        var complexChartOption = {
            responsive: true,
            scales: {
                yAxes: [{
                    id: "y-axis-1",
                    type: "linear", 
                    position: "left",
                    ticks: {
                        max: 500,
                        min: -200,
                        stepSize: 100
                    },
                }, {
                    id: "y-axis-2",
                    type: "linear", 
                    position: "right",
                    ticks: {
                        max: 7000,
                        min: 2000,
                        stepSize: 1000
                    },
                    gridLines: {
                        drawOnChartArea: false, 
                    },
                }],
            }
        };
        </script>'''


        ichiran_target_df_list = []
        # for target_day in days[:4]:
        #     print(target_day)
        df_kisyu_matome_master = df_kisyu_matome
        target_day = new_days_list[0]
        zeidai_pickup_df = df_kisyu_matome_master.query('日付.str.contains(@target_day)', engine='python')
        zeidai_pickup_df = zeidai_pickup_df[zeidai_pickup_df['平均差枚'] > 1000]	
        zeidai_pickup_df = zeidai_pickup_df[zeidai_pickup_df['平均G数'] > 6000]
        zeidai_pickup_df_1 = ''

        for kisyu_name in zeidai_pickup_df['機種']:
            ruikei_df = zeidai_pickup_df.query('機種.str.contains(@kisyu_name)', engine='python')
            ruikei_df['平均差枚'] = ruikei_df['平均差枚'].map(change_table_color_samai)
            ruikei_df['平均G数'] = ruikei_df['平均G数'].map(change_table_color_game)
            ruikei_df_1 =ruikei_df.T.reset_index()
            ruikei_df_1.columns = list(ruikei_df_1 .loc[0, :])
            ruikei_df_1.drop(0, inplace=True)
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('勝利台数')]
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('台数')]
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('集計回数')]
            print(ruikei_df_1)
            zeidai_pickup_df_1 += ruikei_df_1.to_html(justify='justify-all',index=False).replace('<td>blue_1','<td class="color_blue_1">').replace('<td>blue_2','<td class="color_blue_2">').replace('<td>blue_3','<td class="color_blue_3">').replace('<td>blue_4','<td class="color_blue_4">').replace('<td>blue_5','<td class="color_blue_5">').replace('<td>blue_6','<td class="color_blue_6">').replace('<td>blue_7','<td class="color_blue_7">')
            
        #print(ichiran_pickup_df_1)

        target_day = new_days_list[1]
        zeidai_pickup_df = df_kisyu_matome_master.query('日付.str.contains(@target_day)', engine='python')
        zeidai_pickup_df = zeidai_pickup_df[zeidai_pickup_df['平均差枚'] > 1000]	
        zeidai_pickup_df = zeidai_pickup_df[zeidai_pickup_df['平均G数'] > 6000]
        zeidai_pickup_df_2 = ''

        for kisyu_name in zeidai_pickup_df['機種']:
            ruikei_df = zeidai_pickup_df.query('機種.str.contains(@kisyu_name)', engine='python')
            ruikei_df['平均差枚'] = ruikei_df['平均差枚'].map(change_table_color_samai)
            ruikei_df['平均G数'] = ruikei_df['平均G数'].map(change_table_color_game)
            ruikei_df_1 =ruikei_df.T.reset_index()
            ruikei_df_1.columns = list(ruikei_df_1 .loc[0, :])
            ruikei_df_1.drop(0, inplace=True)
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('勝利台数')]
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('台数')]
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('集計回数')]
            print(ruikei_df_1)
            zeidai_pickup_df_2 += ruikei_df_1.to_html(justify='justify-all',index=False).replace('<td>blue_1','<td class="color_blue_1">').replace('<td>blue_2','<td class="color_blue_2">').replace('<td>blue_3','<td class="color_blue_3">').replace('<td>blue_4','<td class="color_blue_4">').replace('<td>blue_5','<td class="color_blue_5">').replace('<td>blue_6','<td class="color_blue_6">').replace('<td>blue_7','<td class="color_7">')
        #print(ichiran_pickup_df_2)

        target_day = new_days_list[2]
        zeidai_pickup_df = df_kisyu_matome_master.query('日付.str.contains(@target_day)', engine='python')
        zeidai_pickup_df = zeidai_pickup_df[zeidai_pickup_df['平均差枚'] > 1000]	
        zeidai_pickup_df = zeidai_pickup_df[zeidai_pickup_df['平均G数'] > 6000]	
        zeidai_pickup_df_3 = ''

        for kisyu_name in zeidai_pickup_df['機種']:
            ruikei_df = zeidai_pickup_df.query('機種.str.contains(@kisyu_name)', engine='python')
            ruikei_df['平均差枚'] = ruikei_df['平均差枚'].map(change_table_color_samai)
            ruikei_df['平均G数'] = ruikei_df['平均G数'].map(change_table_color_game)
            ruikei_df_1 =ruikei_df.T.reset_index()
            ruikei_df_1.columns = list(ruikei_df_1 .loc[0, :])
            ruikei_df_1.drop(0, inplace=True)
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('勝利台数')]
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('台数')]
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('集計回数')]
            print(ruikei_df_1)
            zeidai_pickup_df_3 += ruikei_df_1.to_html(justify='justify-all',index=False).replace('<td>blue_1','<td class="color_blue_1">').replace('<td>blue_2','<td class="color_blue_2">').replace('<td>blue_3','<td class="color_blue_3">').replace('<td>blue_4','<td class="color_blue_4">').replace('<td>blue_5','<td class="color_blue_5">').replace('<td>blue_6','<td class="color_blue_6">').replace('<td>blue_7','<td class="color_7">')
        #print(ichiran_pickup_df_3)

        target_day = new_days_list[3]
        zeidai_pickup_df = df_kisyu_matome_master.query('日付.str.contains(@target_day)', engine='python')
        zeidai_pickup_df = zeidai_pickup_df[zeidai_pickup_df['平均差枚'] > 1000]	
        zeidai_pickup_df = zeidai_pickup_df[zeidai_pickup_df['平均G数'] > 6000]	
        zeidai_pickup_df_4 = ''

        for kisyu_name in zeidai_pickup_df['機種']:
            ruikei_df = zeidai_pickup_df.query('機種.str.contains(@kisyu_name)', engine='python')
            ruikei_df['平均差枚'] = ruikei_df['平均差枚'].map(change_table_color_samai)
            ruikei_df['平均G数'] = ruikei_df['平均G数'].map(change_table_color_game)
            ruikei_df_1 =ruikei_df.T.reset_index()
            ruikei_df_1.columns = list(ruikei_df_1 .loc[0, :])
            ruikei_df_1.drop(0, inplace=True)
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('勝利台数')]
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('台数')]
            ruikei_df_1 = ruikei_df_1[~ruikei_df_1['機種'].str.contains('集計回数')]
            zeidai_pickup_df_4 += ruikei_df_1.to_html(justify='justify-all',index=False).replace('<td>blue_1','<td class="color_blue_1">').replace('<td>blue_2','<td class="color_blue_2">').replace('<td>blue_3','<td class="color_blue_3">').replace('<td>blue_4','<td class="color_blue_4">').replace('<td>blue_5','<td class="color_blue_5">').replace('<td>blue_6','<td class="color_blue_6">').replace('<td>blue_7','<td class="color_7">')
        #print(ichiran_pickup_df_4)



        zendai_pick_up_df_text = '''<h2>全台形っぽい箇所候補</h2>
        <img src="http://slotana777.com/wp-content/uploads/2021/04/全台形.jpg" alt="スロット　全台形" width="1000" height="563" class="alignnone size-full wp-image-2696" />
        ※機種平均G数5000G以上&平均差枚+1,000枚以上の機種のみピックアップ
        [st-kaiwa1]<span class="hutoaka"><strong>ここでは全台形っぽい機種数と機種に注目。
        全台形やってれば大体ここに乗るよ。</strong><span class="hutoaka">[/st-kaiwa1]'''
        df_kisyu_matome_master_sort = df_kisyu_matome_master.sort_values('日付')
        df_kisyu_matome_master_sort['機種'] = df_kisyu_matome_master_sort['機種'].map(name_convert_change)
        df_kisyu_matome_master_sort = df_kisyu_matome_master_sort[df_kisyu_matome_master_sort['平均G数'] > 5000]
        df_kisyu_matome_master_sort = df_kisyu_matome_master_sort[df_kisyu_matome_master_sort['平均差枚'] > 1000]
        df_kisyu_matome_master_sort.drop(['集計回数','台数','勝利台数','総差枚','総G数'], axis=1, inplace=True)
        df_kisyu_matome_master_sort['平均差枚'] = df_kisyu_matome_master_sort['平均差枚'].map(change_table_color_samai)
        df_kisyu_matome_master_sort['平均G数'] = df_kisyu_matome_master_sort['平均G数'].map(change_table_color_game)
        for date in df_kisyu_matome_master_sort['日付'].unique():
            zendai_pick_up_df = df_kisyu_matome_master_sort.query(f'日付.str.contains("{date}")', engine='python')
            date = date.replace('/','月') + '日'
            zendai_pick_up_df_text += f'<h3>{date}</h3>' + zendai_pick_up_df.to_html(justify='justify-all',index=False).replace('<td>blue_1','<td class="color_blue_1">').replace('<td>blue_2','<td class="color_blue_2">').replace('<td>blue_3','<td class="color_blue_3">').replace('<td>blue_4','<td class="color_blue_4">').replace('<td>blue_5','<td class="color_blue_5">').replace('<td>blue_6','<td class="color_blue_6">').replace('<td>blue_7','<td class="color_7">')


        #pd.set_option('print.max_rows',  None)
        grouped = df_kisyu_matome.groupby('機種').sum()
        grouped['累計平均出率'] = ((grouped['総G数']* 3 + grouped['総差枚']) / (grouped['総G数'] * 3 ) *100)
        grouped['累計勝率(%)'] = grouped['勝利台数'] / grouped['台数'] * 100
        grouped['台数'] = grouped['台数'].astype(str)
        grouped['勝利台数'] = grouped['勝利台数'].astype(str)
        grouped['累計勝率'] = grouped['勝利台数'] + '/' + grouped['台数']
        grouped['台数'] = pd.to_numeric(grouped['台数'], downcast='integer')
        grouped['勝利台数'] = pd.to_numeric(grouped['勝利台数'], downcast='integer')
        grouped['累計平均差枚'] = grouped['総差枚'] / grouped['台数']
        grouped['累計平均G数'] = grouped['総G数'] / grouped['台数']
        grouped['累計平均G数'] = grouped['累計平均G数'].map(set_round)
        grouped['累計平均差枚'] = grouped['累計平均差枚'].map(set_round)
        grouped['累計勝率(%)'] = grouped['累計勝率(%)'].map(set_round)
        grouped['累計平均出率'] = grouped['累計平均出率'].map(set_round)
        grouped = grouped.sort_values('累計平均差枚', ascending=False)
        grouped.drop(['平均差枚','平均G数','出率','台数','勝利台数'], axis=1, inplace=True)
        completed_grouped = grouped[grouped['集計回数'] > 1]
        completed_grouped = completed_grouped.reset_index()
        completed_grouped

        derituzyun_text = ''
        n = 1
        kisyu_list_text  = ''
        cols = ['機種','総差枚','総G数','集計回数','累計平均出率','累計勝率(%)','累計勝率','累計平均差枚','累計平均G数']
        ruikei_twitter_df = pd.DataFrame(index=[], columns=cols)
        for kisyu_name in completed_grouped['機種']:
            ruikei_df = completed_grouped.query('機種.str.contains(@kisyu_name)', engine='python')
            ruikei_df_1 =ruikei_df.T.reset_index()
            ruikei_df_1 .columns = list(ruikei_df_1 .loc[0, :])
            ruikei_df_1 .drop(0, inplace=True)
            #ruikei_df_1['機種'] = target_kisyu_name
            kisyu_matome_df = df_kisyu_matome.query('機種.str.contains(@kisyu_name)', engine='python')
            #print(ruikei_df_1)
            strind_cate_1 = date_list[0].replace('2021-','').replace('-','/')
            if len(kisyu_matome_df[kisyu_matome_df["日付"] ==  strind_cate_1]) != 0:

                derituzyun_text += f'\n<h3>{n}位　{kisyu_name}<br>累計平均差枚 +{ruikei_df.iloc[0,7]}枚</h3>'
                derituzyun_text += ruikei_df_1.to_html(justify='justify-all',index=False)
                print('true')
                kisyu_matome_df.drop(['集計回数','台数','勝利台数','総差枚','総G数'], axis=1, inplace=True)
                kisyu_matome_df =kisyu_matome_df.sort_values('日付')
                kisyu_matome_df = kisyu_matome_df.iloc[:, [5,0,2,1,4,3]]
                kisyu_matome_df['機種'] = kisyu_matome_df['機種'].map(name_convert_change)
                kisyu_matome_df['平均差枚'] = kisyu_matome_df['平均差枚'].map(change_table_color_samai)
                kisyu_matome_df['平均G数'] = kisyu_matome_df['平均G数'].map(change_table_color_game)
                
                derituzyun_text += kisyu_matome_df.to_html(justify='justify-all',index=False).replace('<td>blue_1','<td class="color_blue_1">').replace('<td>blue_2','<td class="color_blue_2">').replace('<td>blue_3','<td class="color_blue_3">').replace('<td>blue_4','<td class="color_blue_4">').replace('<td>blue_5','<td class="color_blue_5">').replace('<td>blue_6','<td class="color_blue_6">').replace('<td>blue_7','<td class="color_blue_7">')
                print(kisyu_matome_df)
                ichiran_matome_df = ichiran_concat_df.query('機種.str.contains(@kisyu_name)', engine='python')
                #print(ichiran_matome_df.to_html(justify='justify-all',index=False)
                n += 1
                if n < 7:
                    try:
                        kisyu_list_text += kisyu_matome_df['機種'].unique() + '\n' + '平均差枚' +f'+{int(ruikei_df.iloc[0,7])}枚' + '\n\n'
                    except:
                        pass
                else:
                    pass

                ruikei_twitter_df = ruikei_twitter_df.append(ruikei_df, ignore_index=True)

            else:
                continue
                print('false')

            if n == 16:
                break

        ave_samai_list_int =  [int(s) for s in ave_samai_list]
        ave_samai_text = sum(ave_samai_list_int) / len(ave_samai_list_int)

        ave_game_list_int = [int(s) for s in ave_game_list]
        ave_game_text = sum(ave_game_list_int) / len(ave_game_list_int)

        l_2d_index = [ave_samai_list,ave_game_list]
        ave_tenpo_df = pd.DataFrame(l_2d_index, columns=new_days_list_reverse,index=['平均差枚','平均G数'])
        ave_tenpo_df[0:1]  =  ave_tenpo_df[0:1]  + '枚'
        ave_tenpo_df[1:2]  =  ave_tenpo_df[1:2]  + 'g'
        ave_tenpo_df_text = ave_tenpo_df.to_html(justify='justify-all')
        kisyu_text = ''
        for kisyu in kisyu_list_text:
            kisyu_text += kisyu
        #print(kisyu_text)

        month_str = tomorrow_str.split('-')[1].lstrip('0')
        day_str = tomorrow_str.split('-')[2].lstrip('0')
        month_day_str = month_str  + '/'+ day_str
        month_day_str
        tenpo_name_ten_nashi = tenpo_name.replace('店','')


        tenpo_kiji_text += f'''
        <h3>{tenpo_name} 平均 {ave_samai_text}枚 </h3>
        &nbsp;
        <a href="http://slotana777.com/%E3%82%B9%E3%83%AD%E3%83%83%E3%83%88/{tenpo_name_ten_nashi}_{tomorrow_str}" target="_blank" rel="noopener"><img class="alignnone wp-image-2927 size-full" src="http://slotana777.com/wp-content/uploads/2021/04/記事はこちら.jpg" alt="" width="1000" height="261" /></a>
        [st-flexbox url="" rel="nofollow" target="" fontawesome="" title="{target_day_number}のつく日 過去5回合計の機種別合計の平均差枚TOP5" width="" height="" color="#003" fontsize="200" radius="5" shadow="#424242" bordercolor="#000" borderwidth="3" bgcolor="#f0f8ff" backgroud_image="" blur="on" left="" margin_bottom="0"]
        {kisyu_text}
        [st-kaiwa1]
        <span class="oomozi"><span class="st-aka">
        平均G数 {ave_game_text}G 
        平均差枚{ave_samai_text}枚
        </span></span>
        [/st-kaiwa1]

        <a href="https://www.google.co.jp/search?q={tenpo_name} P-WORLD " target="_blank" rel="noopener nofollow"><img class="alignnone wp-image-2928 size-full" src="http://slotana777.com/wp-content/uploads/2021/04/p-world.jpg" alt="" width="1000" height="261" /></a>

        [/st-flexbox]'''
        

        #書き込み用

        text_block_3 = f'''<h2>{tenpo_name} {target_day_number}のつく日直近過去5回で最も出ていた機種TOP15</h2>
        ※5回累計の平均差枚順です
        [st-kaiwa1]<span class="hutoaka"><strong>
        +1,500枚以上だとそのお店の最近の鉄板機種レベル
        +1,000枚以上あると毎回かなり狙い目。
        +500枚~+1000枚でもよく設定が入ってるよ
        0枚~+500枚だと過去1回全台形やたまに機種1とかが多い。
        あと勝率に注目すると全台形が多いのか機種1や1/2があるのかの傾向が掴める。</strong></span>
        事故って出てたまに参考にならない機種も混じる時もあるから自分で分析して傾向立ててね！[/st-kaiwa1] ''' + derituzyun_text

        str_day_text = ''
        for date in day_str_list[:5]:
            str_day_text += '\n<span class="checkmark2 on-color">' + date + '</span>'


        day_text_block = f"""

        """

        full_slopy_text = day_text_block  + text_block_3 
        #print(full_slopy_text)
        print('読み込み完了')

        import os
        from wordpress_xmlrpc import Client, WordPressPost
        from wordpress_xmlrpc.methods import media
        from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
        from wordpress_xmlrpc.methods.users import GetUserInfo


        # Set URL, ID, Password
        WORDPRESS_ID = "tsc953u"
        WORDPRESS_PW = "6tjc5306"
        WORDPRESS_URL = "https://slotana777.com/xmlrpc.php"
        wp = Client(WORDPRESS_URL, WORDPRESS_ID, WORDPRESS_PW)

        for i in range(1,4):
            imgPath = f'/Users/macbook/Desktop/heatmap/tokyo_heatmap_{tenpo_name}_{date_list[0]}_{i}.jpg'
            #outPath = f'{tenpo_name}_{date_list[0]}_{i}'
            upload_image(imgPath, imgPath)
            time.sleep(1)



        # import
        


        # Picture file name & Upload
        imgPath = sumnail_path
        media_id = upload_image(imgPath, imgPath)

        # Blog Title
        title = f"{tomorrow_str_tweet.lstrip('0')} {tenpo_name} 過去５回分の傾向・分析まとめ【明日のオススメ店舗】"

        # Blog Content (html)
        body = f'''<h2>{tenpo_name}  直近5回分析まとめ</h2>
        <p class="st-blackboard-title-box"><span class="st-blackboard-title">{tenpo_name} 特徴</span></p>
        <ul class="st-blackboard-list st-no-ck-off">
            <li>稼働が高い</li>
        </ul>
        </div>

        <h2>{tomorrow_str_tweet.lstrip('0')} {tenpo_name}</h2>
        比較するデータは{tenpo_name}の{str_day_text}
        の{target_day_number}のつく日の5回分データを今回集計しました。

        <h3>過去５回平均G数、平均差枚グラフ分析結果</h3>
        &nbsp;
        {slump_graph}
        {ave_tenpo_df_text}
        [st-kaiwa1]<span class="hutoaka"><strong>5回分の店舗合計は
        平均G数 {ave_game_text}G </strong>
        <strong>平均差枚{ave_samai_text}枚だったよ</strong></span>[/st-kaiwa1]


        {full_slopy_text}
        {zendai_pick_up_df_text}

        <h2>{tenpo_name}
        {day_str_list[2]},{day_str_list[1]},{day_str_list[0]}
        ３回分のヒートマップ分析</h2>
        <img src="http://slotana777.com/wp-content/uploads/2021/04/並び.jpg" alt="" width="1000" height="563" class="alignnone size-full wp-image-2804" />
        [st-kaiwa1]<span class="hutoaka"><strong>ここではデータに現れない並びやその他傾向など他のインフルエンサー達が呟いてる情報を元にこの画像から傾向を読み取ってね。
        傾向を分析する時は特に差枚の青色が濃い部分に注目して見てみよう。
        朝の並んでる時間にこの画像をじっくり眺めて台単位で狙い台を決めてね！
        </strong></span>[/st-kaiwa1]
        <a href="http://slotana777.com/wp-content/uploads/{today_year_month}/UsersmacbookDesktopheatmaptokyo_heatmap_{tenpo_name}_{date_list[0]}_1.jpg"><img src="http://slotana777.com/wp-content/uploads/{today_year_month}/UsersmacbookDesktopheatmaptokyo_heatmap_{tenpo_name}_{date_list[0]}_1.jpg" alt="" width="713" height="1920" class="aligncenter " /></a>

        <a href="http://slotana777.com/wp-content/uploads/{today_year_month}/UsersmacbookDesktopheatmaptokyo_heatmap_{tenpo_name}_{date_list[0]}_2.jpg"><img src="http://slotana777.com/wp-content/uploads/{today_year_month}/UsersmacbookDesktopheatmaptokyo_heatmap_{tenpo_name}_{date_list[0]}_2.jpg" alt="" width="713" height="1920" class="alignnone size-full" /></a>

        <a href="http://slotana777.com/wp-content/uploads/{today_year_month}/UsersmacbookDesktopheatmaptokyo_heatmap_{tenpo_name}_{date_list[0]}_3.jpg"><img src="http://slotana777.com/wp-content/uploads/{today_year_month}/UsersmacbookDesktopheatmaptokyo_heatmap_{tenpo_name}_{date_list[0]}_3.jpg" alt="" width="713" height="1920" class="aligncenter size-full " /></a>
        '''

        # publish or draft
        status = "publish"

        #Category keyword
        cat1 = 'スロット'
        cat2 = '結果まとめ'
        cat3 = ''

        #Tag keyword
        tag1 = f'{target_day_number}のつく日'
        
        tag2 = f'{tenpo_name}'
        tag3 = f'{todoufuken.text}'
        tenpo_name = tenpo_name.replace('店','')
        slug = f"{tenpo_name}_{tomorrow_str}"

        # Post
        post = WordPressPost()
        post.title = title
        post.content = body
        post.post_status = status
        post.terms_names = {"category": [cat1, cat2],"post_tag": [tag1, tag2,tag3],
    }
        post.slug = slug

        # Set eye-catch image
        post.thumbnail = media_id

        # Post Time
        #post.date = datetime.datetime.now() - datetime.timedelta(hours=9)

        wp.call(NewPost(post))
        print('完了')
    except:
        print('\n\n\n\n\n\n\n\n\n\n\n\n失敗',tenpo_name)
        error_tenpo_name_list.append(tenpo_name)
        import traceback
        traceback.print_exc()
        pass

print('完全完了！')


        
from PIL import Image, ImageDraw, ImageFont

if os.name == 'nt':
    font_path = r"C:\Windows\Fonts\ラノベPOP.otf"
elif os.name == 'posix':
    font_path = "/Users/macbook/Library/Fonts/GenEiGothicP-H-KL.otf"
#def recommend_image(todouhuken,write_image_context):
#image_path = r"C:\Users\81801\Desktop\twitter_anarytics_bot\recommend_syuzai_report\board_image.jpg" #win
image_path = "/Users/macbook/Desktop/千葉.jpg" #mac
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

write_image_context = f'''　{tomorrow_str_tweet.lstrip('0')}東京都
 明日の高稼働店舗
オススメ店舗まとめ'''


font_path = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"
#"/Users/macbook/Library/Fonts/ラノベPOP.otf"
#/Users/macbook/Library/Fonts/ラノベPOP.otf

#sizeは文字サイズです（とりあえず適当に50）
font = ImageFont.truetype(font_path, size=180)

#文字を描く
#最初の(0,0)は文字の描画を開f始する座標位置です　もちろん、(10,10)などでもOK
#fillはRGBで文字の色を決めています
draw.multiline_text((155,190), write_image_context, fill=(255,255,255), font=font,spacing=50,stroke_width=5,stroke_fill=(55,55,55))


image.save(f"/Users/macbook/Desktop/kantou_syuzaireport_tokyo_{tomorrow_str}.jpg")
#元画像を読み込んでくる
#write_image_context =f
#image.save(f"/Users/macbook/Desktop/{tenpo_name}_{tomorrow_str_tweet}.png")
#元画像を読み込んでくる

#フォントを指定する（フォントファイルはWindows10ならC:\\Windows\\Fontsにあります）
#フォントの読み込


#sizeは文字サイズです（とりあえず適当に50）

#文字を描く
#最初の(0,0)は文字の描画を開f始する座標位置です　もちろん、(10,10)などでもOK
#fillはRGBで文字の色を決めています

sumnail_path =f"/Users/macbook/Desktop/kantou_syuzaireport_tokyo_{tomorrow_str}.jpg"




month_str = tomorrow_str.split('-')[1].lstrip('0')
day_str = tomorrow_str.split('-')[2].lstrip('0')
month_day_str = month_str  + '/'+ day_str
month_day_str

header = f'''<span class="huto"><h2>東京の明日【{tomorrow_str_tweet.lstrip('0')}】のパチスロ・スロットホール・イベント・オススメ店舗情報</h2>
過去の{target_day_number}のつく日 5回分のデータを使って人が多い店舗を中心にピックアップしています。</span>

<span class="oomozi"><span class="st-aka">高設定が投入される可能性が高いと予想されるホールばかりですのでこの記事を参考に高設定を掴み取ってください！</span></span>
<strong>この記事は毎日更新・公開されますので
是非、<a href="http://slotana777.com/category/%e9%96%a2%e6%9d%b1%e3%82%b9%e3%83%ad%e3%83%83%e3%83%88%e3%82%a4%e3%83%99%e3%83%b3%e3%83%88%e3%81%be%e3%81%a8%e3%82%81%e3%83%bb%e3%82%aa%e3%82%b9%e3%82%b9%e3%83%a1%e5%ba%97/%e6%9d%b1%e4%ba%ac%e9%83%bd-%e3%82%b9%e3%83%ad%e3%83%83%e3%83%88%e3%82%a4%e3%83%99%e3%83%b3%e3%83%88%e3%81%be%e3%81%a8%e3%82%81%e3%83%bb%e3%82%aa%e3%82%b9%e3%82%b9%e3%83%a1/" rel="noopener" target="_blank">カテゴリページでのブックマーク</a>お願いします。
<h2>明日【{tomorrow_str_tweet.lstrip('0')}】の都内スロット イベント・オススメ店舗画像早見表TOP7</h2>
<h3>↓平均G数順TOP7【高稼働店舗予想順】</h3>

<a href="http://slotana777.com/wp-content/uploads/{tomorrow_str_blog_url}/UsersmacbookDesktoptokyo_tomorrow_recommendtokyo_img_2day_recommend_game_{tomorrow_str_tweet}.png"><img src="http://slotana777.com/wp-content/uploads/{tomorrow_str_blog_url}/UsersmacbookDesktoptokyo_tomorrow_recommendtokyo_img_2day_recommend_game_{tomorrow_str_tweet}.png" alt="" width="1700" height="1285" class="alignnone size-full " /></a>



<h3>↓平均差枚順TOP7【オススメ店舗】</h3>
<a href="http://slotana777.com/wp-content/uploads/{tomorrow_str_blog_url}/UsersmacbookDesktoptokyo_tomorrow_recommendtokyo_img_2day_recommend_samai_{tomorrow_str_tweet}.png"><img src="http://slotana777.com/wp-content/uploads/{tomorrow_str_blog_url}/UsersmacbookDesktoptokyo_tomorrow_recommendtokyo_img_2day_recommend_samai_{tomorrow_str_tweet}.png" alt="" width="1700" height="1285" class="alignnone size-full " /></a>
[st-kaiwa1]<span class="hutoaka"><strong>気になる店舗はあった？
次は気になる店舗のデータを店舗別に見てね〜！</strong></span>[/st-kaiwa1]
<h2>明日の都内スロット イベント・オススメ店舗一覧</h2>'''

# Set URL, ID, Password
WORDPRESS_ID = "tsc953u"
WORDPRESS_PW = "6tjc5306"
WORDPRESS_URL = "https://slotana777.com/xmlrpc.php"
wp = Client(WORDPRESS_URL, WORDPRESS_ID, WORDPRESS_PW)


# Picture file name & Upload
imgPath = sumnail_path
#image_path = ''
media_id = upload_image(imgPath, imgPath)

# Blog Title
title = f"東京の明日【{tomorrow_str_tweet.lstrip('0')}】のパチスロ・スロットホール・イベント・オススメ店舗情報"

# Blog Content (html)
body = f'''{header}
{tenpo_kiji_text}
'''

# publish or draft
status = "publish"

#Category keyword
cat1 = '東京都 スロットイベントまとめ・オススメ店舗'
cat2 = '明日の東京都 スロットイベントまとめ・オススメ店舗'
cat3 = ''

#Tag keyword
tag1 = f'{target_day_number}のつく日'
tag2 = f'東京都'
#tag3 = f'{todoufuken.text}'

slug = f"東京スロット明日のオススメ店舗_{tomorrow_str}"

# Post
post = WordPressPost()
post.title = title
post.content = body
post.post_status = status
post.terms_names = {
    "category": [cat1],
    "post_tag": [tag1, tag2],
}
post.slug = slug

# Set eye-catch image
post.thumbnail = media_id

# Post Time
#post.date = datetime.datetime.now() - datetime.timedelta(hours=9)

wp.call(NewPost(post))
print('完了')