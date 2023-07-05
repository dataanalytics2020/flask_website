"# flask_website"
### 2023/07/06 時点のTOP画面
![スクリーンショット 2023-07-06 005740](https://github.com/dataanalytics2020/flask_website/assets/117744645/36a93bb8-257d-4a52-b0f4-be5082c684c3)
### 2023/07/04 時点のTOP画面
![スクリーンショット 2023-07-04 035103](https://github.com/dataanalytics2020/flask_website/assets/117744645/9f1da422-e147-4ce9-ae9b-0b996808402a)


# Flask チュートリアル
https://study-flask.readthedocs.io/ja/latest/01.html

## 仮想環境作成
python -m venv venv
## 仮想環境実行
.venv\Scripts\activate.bat


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

## Flaskのサンプルサイト
https://github.com/topics/flask-template

### アコーディオンのサンプルサイト
https://lmn-blog.com/jquery_accordion01/

参考動画 Udemy
https://www.udemy.com/share/107ggo3@Txcm81u9m0_R8WkgeEfxzhIgmQLev8Y-bo3XeWtZf-xpGNmtwNK2BWfe94n4SryHTg==/

