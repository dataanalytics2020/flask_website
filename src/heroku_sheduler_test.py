import requests
import json
import os
import datetime
from dotenv import load_dotenv
load_dotenv(".env")
print('ライブラリの読み込み完了')

def post_line_text(message,token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}
    post = requests.post(url ,headers = headers ,params=payload) 
    

token = os.getenv("SLOCHAN_LINE_TOKEN")
post_line_text('scheduler_test',token)

#python ./model/main.py
#python ./src/heroku_sheduler_test.py