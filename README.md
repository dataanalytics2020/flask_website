![slomap_main_image_10s_gif](https://github.com/dataanalytics2020/flask_website/assets/117744645/c2fb4639-db6a-449f-b647-8c14d691e11d)


<br />

## サービスのURL

https://slo-map.com/

<br />

## サービス概要

### パチンコを知らない方へ

パチンコ店屋さんは過去の日のデータをWeb上に公開しています。
それをユーザーが見て出ている台はどの台だったのかを参考にして次のお店を選んだり、翌日に打つ台を選ぶ目安にしています。

ただ、複数日に渡っての集計や分析などより詳しい分析をするにはエクセルにまとめてやるしかないなど
手間の割に得られるリターンはかなり少なく、プロの中でもやっている人は極少数です。

また取材予定という概念が存在し、第三者のSNSを通じて
各店舗の出す日の予定などある程度の狙いがわかるような発信がXやWeb上で行われています。

### サービスへの想い
私自身、昔からパチスロのデータの分析をして年間収支を毎年プラスにするなどやっていましたが
そこのデータのまとめをだれでも簡単に出来ない事にモヤモヤを感じていました。

都内だけでもパチンコ店は約700店舗存在します。
そしてプロダクト名(スロマップ)にも入ってるマップを採用したのは
ライトユーザーでも直感的に家から近い店舗の中から選べるようにマップを採用しました。

このプロダクトは、パチンコのライトユーザーでも明日のお勧めのパチンコ店さんの
明日のお勧め店舗やその日の使えるデータの分析を、誰でも、いつでも、より簡単に見れるようにという想いから生まれました。

私自身がパチンコユーザーだからこそわかるライトユーザーに向けたこんなのがあったら便利だな・・・を具現化しているサイトです。

### 現在の収益状態とSEO対策・サイト改善分析について
Google Adsenseにも24年1月末に合格し、サーバー代含め現在黒字になっています。
インデックスされているページは現在12000ほどでPVのほとんどが検索流入です。
知人に使ってもらう事はまだしておらず、主にサーチコンソールとグーグルアナリティクスを使って
需要のある人気ページやアクセス数を分析し、機能の改善・追加などしています。

### サービスの現状と今後について
おかげ様で現在では一日のDAUが3~5000人、月間PVが16万前後にまで見た頂けるサイトになりました。
Twitterなどではまだプロモーションをあえて行っておらず、Nextjs,DRFともっとUIUXの改善を行ったのちに
プロモーションを行っていきたいと考えています。

最終的には今の10倍以上の月間300万PVくらいには成長させる事ができるサービスだと考えており、
あと2~3年をかけてサービスを成長させていく予定です。
最終的にはReact Nativeを使ってスマホアプリ化まで検討しています。

<br />

## アプリケーションのイメージ画像

<br />

## 機能一覧
| お知らせ機能(TOP画面) | 都道府県選択(TOP画面) |
| ---- | ---- |
| ![image](https://github.com/dataanalytics2020/flask_website/assets/117744645/438ba492-a8bf-4b2d-8cec-ae2fc2b17e27)| ![image](https://github.com/dataanalytics2020/flask_website/assets/117744645/e779d9d2-0fda-4b71-ab93-401f03728bdd) |
| ユーザーにサイトが改善されてる認知のために実装 | 都道府県選択も直感的に押せるように実装|

| お勧め機能リンク(TOP画面) | 明日の東京都お勧め店舗マップ表示機能(TOP画面) |
| ---- | ---- |
| ![Top画面](/docs/img/app-view/welcome_1.1.png) | ![ログイン画面](/docs/img/app-view/login_1.1.png) |
| 初心者や初訪問者に向けにまず触ってほしい機能リンクを表示 | TOP画面でサービスのコアになるマップ表示機能を東京都でサンプルとして表示、以下記事のサンプルを表示|

| 打ちたい機種から選ぶ(都道府県選択後画面) | 行きたい日付から選ぶ(都道府県選択後画面) |
| ---- | ---- |
| ![事業者選択画面](/docs/img/app-view/select-business_1.1.png) | ![請求書作成画面](/docs/img/app-view/create-invoice_1.1.png) |
| 画像を使って機種がわかりやすいように表示 | 日付に曜日をつけてわかりやすいように表示 |

| 取材から選ぶ(都道府県選択後画面) | 店舗から選ぶ(都道府県選択後画面) |
| ---- | ---- |
| ![請求書詳細画面](/docs/img/app-view/invoice-detail_1.1.png) | ![　PDF出力画面](/docs/img/app-view/print-invoice_1.1.png) |
| 行きたい取材が決まっている人向け |  行きたい店舗が決まっている人向け |

| 都道府県別日別記事機能➀(サムネイル) |　都道府県別日別記事機能➁(サムネイル) |
| ---- | ---- |
| ![請求書詳細画面](/docs/img/app-view/select-master_1.1.png) | ![　PDF出力画面](/docs/img/app-view/master-register-form_1.1.png) |
|出ていた店舗の店舗名と機種名の頻出ワードをワードクラウドを使ってサムネイルとして表示| マスタ情報の登録をすることで、請求書の作成時にデータを呼び出すことができます。 |

| 都道府県別日別記事機能③(店舗概要分析) |　都道府県別日別記事機能④(お勧め機種分析) |
| ---- | ---- |
| ![請求書詳細画面](/docs/img/app-view/select-master_1.1.png) | ![　PDF出力画面](/docs/img/app-view/master-register-form_1.1.png) |
|その店舗がどのくらい出ていたかを折れ線グラフと棒グラフで表示|過去3回分の過去データを使って出ていた機種を画像でわかりやすく表示|

<br />

## 使用技術

| Category          | Technology Stack                                     |
| ----------------- | --------------------------------------------------   |
| Frontend          | HTML/CSS,Bootstrap, jQuery, Chart.js , Vanilla.js   |
| Backend           | Flask, WordPress REST API                         |
| Library           | Selenium, Pillow, Pandas , BeautifulSoup,                       |
| Infrastructure    | WordPress, Heroku                          |
| Database          | MySQL(WordPress),Postgresql(Heroku)                                         |
| Monitoring        | Heroku                           |
| Environment setup | Venv , pip                                         |
| CI/CD             | Heroku                                       |
| Design            | Photoshop, Canva PRO                                     |
| etc.              | Git, GitHub ,VScode, Windows Task Scheduler |

<br />

## システム構成図



<br />

## ER図



<br />





## 以下個人用記録とコマンド備忘録

## 製作過程のスクショ一覧
### 2023/12/01時点のTOPページ
#### TOPページにお知らせページとラベル付き機能ボタンを追加
![image](https://github.com/dataanalytics2020/flask_website/assets/117744645/ff6e398f-384d-4c88-a2d8-81b3d86c48b0)
![image](https://github.com/dataanalytics2020/flask_website/assets/117744645/f3c5b676-7fcf-44e5-b0ba-9cf87a25e14a)
![image](https://github.com/dataanalytics2020/flask_website/assets/117744645/4fa2f908-bbb5-4200-bcc4-3f5a6249656d)
![image](https://github.com/dataanalytics2020/flask_website/assets/117744645/78c8a9d6-e4a8-401e-808b-486796ffaa89)

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


### エラーURL
http://127.0.0.1:5000/tomorrow_recommend/kitakantou/syuzai/%E3%82%B0%E3%83%A9%E3%83%B3%E3%83%89%E3%82%AA%E3%83%BC%E3%83%97%E3%83%B3(4%E6%97%A5%E7%9B%AE)

http://127.0.0.1:5000/tomorrow_recommend/minamikantou/syuzai/%E3%82%B0%E3%83%A9%E3%83%B3%E3%83%89%E3%82%AA%E3%83%BC%E3%83%97%E3%83%B3(4%E6%97%A5%E7%9B%AE)