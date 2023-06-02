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

df  = pd.read_csv(r'csv\2022-12-09_touhou.csv')

app = Flask(__name__)
bootstrap = Bootstrap(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SECRET_KEY'] = os.urandom(24)
# db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect("/東京都")


@app.route('/test', methods=['GET', 'POST'])
def test():
    print('test')
    return render_template('test.html')

@app.route('/<prefecture>', methods=['GET', 'POST'])
def test2(prefecture):
    tenpo_url_df:pd.DataFrame = pd.read_csv('csv/tenpo_url_flask_web_site.csv')
    group_name_list:list[str] ='''123,BBステーション,DAS,Dステーション,MGM,PIA,やすだ,ウエスタン,エスパス,\
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
        concat_df = concat_df.groupby(['日付','機種名']).mean().sort_values('差枚',ascending=False)#機種毎に集計
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
        gamesuu_list:str = str(groupby_samai_game_mean_df['G数'].tolist())
        concat_df = concat_df.rename(columns={'差枚': '平均差枚', 'G数': '平均G数'})

        record = [groupby_samai_game_mean_df['差枚'].tolist(),groupby_samai_game_mean_df['G数'].tolist()]
        print(record)
        ave_tenpo_df = pd.DataFrame(record, columns=target_day_list,index=['平均差枚','平均G数'])
        ave_tenpo_df[0:1]  =  ave_tenpo_df[0:1]  + '枚'
        ave_tenpo_df[1:2]  =  ave_tenpo_df[1:2]  + 'G'

        groupby_kisyubetu_df = pre_concat_df.groupby(['機種名']).sum()
        groupby_kisyubetu_df['総台数'] = pre_concat_df.groupby(['機種名']).size()
        groupby_kisyubetu_df = groupby_kisyubetu_df.reset_index(drop=False).reset_index().rename(columns={'index': '機種順位','ゲーム数': 'G数'})
        groupby_kisyubetu_df['機種順位'] = groupby_kisyubetu_df['機種順位'] + 1
        groupby_kisyubetu_df[['機種順位','機種名','総台数','G数','差枚']]
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
        groupby_kisyubetu_df['機種順位'] = list(range(1,len(groupby_kisyubetu_df)+1))
        groupby_kisyubetu_df['機種平均出率'] =(((groupby_kisyubetu_df['G数'] * 3) + groupby_kisyubetu_df['差枚']) / (groupby_kisyubetu_df['G数'] * 3) )*100
        groupby_kisyubetu_df['機種平均出率'] = groupby_kisyubetu_df['機種平均出率'].map(lambda x : round(x,1))
        groupby_kisyubetu_df['機種平均出率'] = groupby_kisyubetu_df['機種平均出率'].astype(str) + '%'
        groupby_kisyubetu_df = groupby_kisyubetu_df.rename(columns={'G数': '合計G数','差枚': '合計差枚'})
        groupby_kisyubetu_df = groupby_kisyubetu_df[['機種順位','機種名','勝率','機種平均出率','平均G数','平均差枚','合計差枚','合計G数','総台数']]
        groupby_kisyubetu_df['平均G数'] = groupby_kisyubetu_df['平均G数'].astype(str) + 'G'
        groupby_kisyubetu_df['平均G数'] = groupby_kisyubetu_df['平均差枚'].astype(str) + '枚'
        groupby_kisyubetu_df = groupby_kisyubetu_df[:5]

        return render_template('target_date_recommend_report.html',data=data,serch_number=serch_number,\
                                            user_data=user_data,\
                                            column_names=concat_df.columns.values, \
                                            row_data=list(concat_df.values.tolist()),\
                                            zip=zip,target_day_list_str=str(target_day_list),\
                                            target_day_list=target_day_list,\
                                            samai_list=samai_list,\
                                            gamesuu_list=gamesuu_list,\
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
        kisyubetu_master_df['機種順位'] = list(range(1,len(kisyubetu_master_df)+1))
        kisyubetu_master_df['機種平均出率'] =(((kisyubetu_master_df['G数'] * 3) + kisyubetu_master_df['差枚']) / (kisyubetu_master_df['G数'] * 3) )*100
        kisyubetu_master_df['機種平均出率'] = kisyubetu_master_df['機種平均出率'].map(lambda x : round(x,1))
        kisyubetu_master_df['機種平均出率'] = kisyubetu_master_df['機種平均出率'].astype(str) + '%'
        kisyubetu_master_df = kisyubetu_master_df.rename(columns={'G数': '合計G数','差枚': '合計差枚'})
        kisyubetu_master_df
        
        return render_template('values.html',
                                            user_data=user_data,\
                                            column_names=concat_df.columns.values, \
                                            row_data=list(concat_df.values.tolist()),\
                                            zip=zip,target_day_list=str(target_day_list))
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)