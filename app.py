from flask import Flask, render_template, request
from datetime import date, timedelta
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

df  = pd.read_csv(r'csv\2022-12-09_touhou.csv')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
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
        target_day_list   
        concat_df_list = []
        urls = []
        for serch_date in target_day_list:
            search_url = url = f"https://ana-slo.com/{serch_date}-{user_data['tenpo-name']}-data/"
            urls.append(search_url)
            #search_response = requests.get(search_url)
            #print(search_response)
            # soup = BeautifulSoup(search_response.text, 'html.parser')
            # dfs = pd.read_html(str(soup))
            # for df in dfs:
            #     if '機種名' in list(df.columns):
            #         tmp_df = df
            #         tmp_df['店舗名'] = serch_tenpo_name
            #         tmp_df['機種名'
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
                concat_df[column_name] =concat_df[column_name].astype(int)
            except:
                pass

        concat_df = concat_df.reset_index()
        return render_template('values.html',
                                            user_data=user_data,\
                                            column_names=concat_df.columns.values, \
                                            row_data=list(concat_df.values.tolist()),\
                                            zip=zip)
    else:
        return render_template('index.html')

    #return render_template('index.html')


    # 
    # target_number = str(target_n_day)
    # print()
    # target_day_list = []
    # number = 0
    # for i in range(int(n_times)):
    #     while True:
    #         print(number)
    #         if target_number == str(date.today() - timedelta(days=number))[-1]:
    #             target_day = date.today() - timedelta(days=number)
    #             print('取得日',target_day)
    #             target_day_str = target_day.strftime('%Y-%m-%d')
    #             target_day_list.append(target_day_str)
    #             number += 1
    #             break
    #         else: 
    #             pass
    #         number += 1
    # target_day_list   
    # concat_df_list = []
    # urls = []
    # for serch_date in target_day_list:
    #     search_url = url = f"https://ana-slo.com/{serch_date}-{serch_tenpo_name}-data/"
    #     urls.append(search_url)
    #     #search_response = requests.get(search_url)
    #     #print(search_response)
    #     # soup = BeautifulSoup(search_response.text, 'html.parser')
    #     # dfs = pd.read_html(str(soup))
    #     # for df in dfs:
    #     #     if '機種名' in list(df.columns):
    #     #         tmp_df = df
    #     #         tmp_df['店舗名'] = serch_tenpo_name
    #     #         tmp_df['機種名'
    # with ThreadPoolExecutor(3) as executor:
    #     results = list(executor.map(requests.get, urls))
    # print(results)

    # concat_df_list = []
    # for search_response,date in zip(results, target_day_list):
    #     soup = BeautifulSoup(search_response.text, "lxml")
    #     elem = soup.select('#all_data_block')
    #     dfs = pd.read_html(str(elem))
    #     for df in dfs:
    #         if '機種名' in list(df.columns):
    #             tmp_df = df
    #             tmp_df['店舗名'] = serch_tenpo_name
    #             tmp_df['日付'] = date
    #             #tmp_df['機種名'] = tmp_df['機種名'].map(removal_text)
    #             break
    #     concat_df_list.append(df)

    # concat_df = pd.concat(concat_df_list,axis=0)
    # concat_df = concat_df.groupby(['日付','機種名']).mean().sort_values('差枚',ascending=False)
    # concat_df = concat_df[['G数','差枚']]
    # concat_df['差枚'] =concat_df['差枚'].astype(int)
    # concat_df['G数'] =concat_df['G数'].astype(int)
    # concat_df = concat_df.reset_index()
    # concat_df_html = concat_df.to_html(index=False)
    # return  concat_df_html

if __name__ == '__main__':
    app.run(debug=True)