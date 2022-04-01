from fastapi import FastAPI, Depends, Form
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from glob import glob
from datetime import datetime
import numpy as np
import os
import psycopg2
import pandas as pd
import datetime
import pytz

import warnings
warnings.simplefilter('ignore')

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
                                      {'request': request,
                                       'username': username.upper()})


@app.post("/study")
async def study(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    
    # 認証
    username = auth(credentials)

    global loop_num
    global rand_music_paths
    global rand_img_paths

    # フォームからデータ取得
    data = await request.form()
    loop_num = int(data['loop_num'])

    music_paths = glob("./static/music/*")
    rand_music_paths = []
    rand_img_paths = []
    for num in np.random.randint(0, len(music_paths), loop_num):
        music_path = music_paths[num]
        rand_music_paths.append(os.path.split(music_path)[-1])

        img_path = ""
        if "dia" in music_path:
            img_path += 'dia'
        elif "spade" in music_path:
            img_path += 'dia'
        elif "heart" in music_path:
            img_path += 'heart'
        elif "club" in music_path:
            img_path += 'club'
        
        if ("01" in music_path)|("02" in music_path)|("03" in music_path)|("04" in music_path)|("05" in music_path)|("06" in music_path)|("07" in music_path)|("08" in music_path):
            img_path += "1.JPG"
        else:
            img_path += "2.JPG"
        rand_img_paths.append(img_path)
    
    return  templates.TemplateResponse(
        'study.html',
        {'request': request,
         'name': username, 
         'loop_num': loop_num,
         'rand_music_paths': rand_music_paths, 
         'rand_img_paths': rand_img_paths})


@app.get("/iteration/")
async def iteration(music: str, credentials: HTTPBasicCredentials = Depends(security), ):
    print('iteration')
    # 認証
    username = auth(credentials)

    db_url = "postgres://qwosamqjhsmjse:bdc36cd41f29cad53b026230c202df7ff08f34b0a1ede8a6334f134cc146f45f@ec2-44-194-92-192.compute-1.amazonaws.com:5432/d79ilntrh62i11"
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    music = music.split('.')[0]
    sql = f"SELECT {music} FROM ITERATION WHERE 学習者='{username}' ;"
    num = pd.read_sql(sql, conn)[music][0]

    if num == None:
        num = 1
    else:
        num += 1
    sql = f"UPDATE ITERATION SET {music} = {num} WHERE 学習者='{username}' ;"
    cur.execute(sql)
    conn.commit()

    return


@app.get("/history/")
async def history(loop: int, credentials: HTTPBasicCredentials = Depends(security), ):
    print("history")
    # 認証
    username = auth(credentials)

    db_url = "postgres://qwosamqjhsmjse:bdc36cd41f29cad53b026230c202df7ff08f34b0a1ede8a6334f134cc146f45f@ec2-44-194-92-192.compute-1.amazonaws.com:5432/d79ilntrh62i11"
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    sql = f"INSERT INTO HISTORY (学習者, 学習日, 再生回数) VALUES('{username}', '{now}', {loop}) ;"
    cur.execute(sql)
    conn.commit()

    return