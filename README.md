## 製作過程のスクショ一覧
### 2023/07/25時点取材予定マップ表示画面
![スクリーンショット 2023-07-25 045339](https://github.com/dataanalytics2020/flask_website/assets/117744645/21b8786e-4df0-41ac-a0bc-3ce15610a83d)
### 2023/07/16 時点の店舗N回分析結果画面
![image](https://github.com/dataanalytics2020/flask_website/assets/117744645/db0ea310-7eda-4fd7-8505-b29b9364bac0)
![image](https://github.com/dataanalytics2020/flask_website/assets/117744645/2366f448-bff7-4357-8529-e7068277646c)
![image](https://github.com/dataanalytics2020/flask_website/assets/117744645/fb145a27-a6b1-4c69-8a1c-d7d96245879c)
### 2023/07/08 時点の店舗N回分析結果画面
![2023-07-08_1](https://github.com/dataanalytics2020/flask_website/assets/117744645/3c1a98e2-f759-46f4-8ed3-4cea5e31e7a2)
![2023-07-08 051507](https://github.com/dataanalytics2020/flask_website/assets/117744645/06e42118-931a-4a57-876a-9581a4adbf99)

### 2023/07/06 時点のTOP画面
![スクリーンショット 2023-07-06 005740](https://github.com/dataanalytics2020/flask_website/assets/117744645/36a93bb8-257d-4a52-b0f4-be5082c684c3)
### 2023/07/04 時点のTOP画面
![スクリーンショット 2023-07-04 035103](https://github.com/dataanalytics2020/flask_website/assets/117744645/9f1da422-e147-4ce9-ae9b-0b996808402a)


# Flask チュートリアル
https://study-flask.readthedocs.io/ja/latest/01.html

## 仮想環境作成
python -m venv venv
## 仮想環境実行
.venv/Scripts/Activate.ps1


## ファイル作成
wsl mkdir -p flaskr/{static,templates} 
wsl touch manage.py requirements.txt
wsl touch flaskr/{__init__,views,models,config}.py
wsl touch flaskr/static/style.css
wsl touch flaskr/templates/{layout,show_entries}.html

## ライブラリ一括インストール
pip install -r requirements.txt


## サーバー起動
python app.py --reload

## postgressql起動コマンド
heroku pg:psql postgresql-cubic-54628 --app flask-mapwebsite

## Flaskのサンプルサイト
https://github.com/topics/flask-template

### アコーディオンのサンプルサイト
https://lmn-blog.com/jquery_accordion01/

参考動画 Udemy
https://www.udemy.com/share/107ggo3@Txcm81u9m0_R8WkgeEfxzhIgmQLev8Y-bo3XeWtZf-xpGNmtwNK2BWfe94n4SryHTg==/

