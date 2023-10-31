# サイトURL

https://www.slo-map.com/

## 製作過程のスクショ一覧

### 2023/10/30時点の記事用サンプルサムネ
![Word_Cloud_test](https://github.com/dataanalytics2020/flask_website/assets/117744645/1b9b992f-46ca-4022-948d-ae269090f298)

### 2023/10/26時点の明日のお勧めページ
#### googleアドセンス対策用の明日のお勧め店舗&機種ページ
![スクリーンショット 2023-10-26 022409](https://github.com/dataanalytics2020/flask_website/assets/117744645/a5069c76-1aad-41f1-896e-801d1199c3d6)
![スクリーンショット 2023-10-26 022350](https://github.com/dataanalytics2020/flask_website/assets/117744645/6ab2f3f7-2997-4ec8-8edc-96c507e89c92)
![スクリーンショット 2023-10-26 022330](https://github.com/dataanalytics2020/flask_website/assets/117744645/5ed43f5a-184d-465c-9db0-2c5af1e14662)


### 2023/09/30時点のTOPページ
#### 都道府県マップから選択できるように機能追加
![slomap_Capture http___127 0 0 1_5000_ 20230930](https://github.com/dataanalytics2020/flask_website/assets/117744645/6bf1d3ee-e606-4165-94c3-9c1d89b19d51)
### 2023/09/26時点のエリア別選択ページ
#### エンドポイント　/tomorrow-recommend/kyushu/
![スクリーンショット 2023-09-27 020331](https://github.com/dataanalytics2020/flask_website/assets/117744645/095938dc-14a5-4098-b4a4-82b884151d7a)
### 2023/08/18時点の明日のお勧め店舗画面
#### エンドポイント　/top
![20230818_top](https://github.com/dataanalytics2020/flask_website/assets/117744645/779d3147-ab77-4b3a-be7f-f0ad6dc22eec)
### 2023/08/09時点の明日のお勧め店舗画面
#### エンドポイント　/tomorrow-recommend/
![スクリーンショット 2023-08-09 002916](https://github.com/dataanalytics2020/flask_website/assets/117744645/1a46e321-431e-4110-b4f8-d852a74f438c)

#### エンドポイント　/tomorrow-recommend/<area_name>
![スクリーンショット 2023-08-09 002931](https://github.com/dataanalytics2020/flask_website/assets/117744645/63b823b9-fe38-4aa3-9944-4804c9534bb8)

#### エンドポイント　/tomorrow-recommend/<area_name>/<date>-data
![スクリーンショット 2023-08-09 002948](https://github.com/dataanalytics2020/flask_website/assets/117744645/3059c471-e7c0-475f-8c96-2a13d77f24af)
### 2023/08/05時点の店舗N回分析結果画面アップデート
生javascriptとjqueryのデータテーブルライブラリを使ってテーブルの行検索機能と差枚に応じたヒートマップで差枚がわかるようにアップデートしました。
仕様サンプル動画リンク
https://github.com/dataanalytics2020/flask_website/assets/117744645/1d1511e0-2732-409c-880a-2b0e5522d7dd
![スクリーンショット 2023-08-05 025445](https://github.com/dataanalytics2020/flask_website/assets/117744645/e96ad36e-e491-45eb-bb15-83209ecd7937)

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

## サーバー起動
python app.py --reload


## ファイル作成
wsl mkdir -p flaskr/{static,templates} 
wsl touch manage.py requirements.txt
wsl touch flaskr/{__init__,views,models,config}.py
wsl touch flaskr/static/style.css
wsl touch flaskr/templates/{layout,show_entries}.html

## ライブラリ一括インストール
pip install -r requirements.txt




## postgressql起動コマンド
heroku pg:psql postgresql-cubic-54628 --app flask-mapwebsite

## Flaskのサンプルサイト
https://github.com/topics/flask-template

### アコーディオンのサンプルサイト
https://lmn-blog.com/jquery_accordion01/

参考動画 Udemy
https://www.udemy.com/share/107ggo3@Txcm81u9m0_R8WkgeEfxzhIgmQLev8Y-bo3XeWtZf-xpGNmtwNK2BWfe94n4SryHTg==/

### ナビゲーションバーサンプルサイト
https://www.webopixel.net/lab/sample/17/fixed-sidebar/01/#

### GitHub Issueを用いた開発手順
https://zenn.dev/ogakuzuko/articles/2250f7c7331106
#### ブランチの切り方
```git checkout -b 新規ブランチ名_#issue番号```

#### キリの良いところで適宜コミット
```git commit -m "コミットメッセージ #issue番号"```

#### push
```git push origin HEAD```

### mainブランチに切り替えてmainブランチの内容をプルする
```
git checkout main
git pull origin main
```

### ローカルにある作業ブランチを削除する
```git branch -d 作業ブランチ名 ```
### 最後にherokuも更新
```git push heroku main```