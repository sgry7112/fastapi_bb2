from fastapi import FastAPI, Depends, Form
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from glob import glob
from datetime import datetime
import numpy as np
import os
import sqlite3

from auth import auth


app = FastAPI(
    title='bb_english',
    description='bb_english',
)
security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')
jinja_env = templates.env

    
@app.get("/")
def login(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # 認証
    username = auth(credentials)
    return templates.TemplateResponse('index.html',
                                      {'request': request})


@app.post("/study")
async def study(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    
    # 認証
    username = auth(credentials)

    global name
    global loop_num
    global rand_music_paths
    global rand_img_paths

    # フォームからデータ取得
    data = await request.form()
    name = str(data['name'])
    loop_num = int(data['loop_num'])

    music_paths = glob("./static/music/*")
    rand_music_paths = []
    rand_img_paths = []
    for num in np.random.randint(0, len(music_paths), loop_num):
        music_path = music_paths[num]
        rand_music_paths.append(os.path.split(music_path)[-1])

        img_path = ""
        if "ダイヤ" in music_path:
            img_path += 'ダイヤ'
        elif "スペード" in music_path:
            img_path += 'スペード'
        elif "ハート" in music_path:
            img_path += 'ハート'
        elif "クラブ" in music_path:
            img_path += 'クラブ'
        
        if ("01" in music_path)|("02" in music_path)|("03" in music_path)|("04" in music_path)|("05" in music_path)|("06" in music_path)|("07" in music_path)|("08" in music_path):
            img_path += "1.JPG"
        else:
            img_path += "2.JPG"
        rand_img_paths.append(img_path)
    
    return  templates.TemplateResponse(
        'study.html',
        {'request': request,
         'name': name, 
         'loop_num': loop_num,
         'rand_music_paths': rand_music_paths, 
         'rand_img_paths': rand_img_paths})


@app.post("/history")
async def history(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # 認証
    print('ttest')
    conn = sqlite3.connect('./db.sqlite3')
    c = conn.cursor()
    now = datetime.now()
    sql = f"insert into satoru (時刻, 内容) values('{now}', 'test') ;"
    c.execute(sql)
    conn.commit()
    return {'hello': 'world'}
