import hashlib
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException

def auth(credentials):
    
    username = credentials.username
    password = hashlib.md5(credentials.password.encode()).hexdigest()

    user = ['Shigeru', 'Ayako', 'Iroha', 'Kurumi', 'Satoru']
    pw = hashlib.md5('Yamazaki'.encode()).hexdigest()

    if (username not in user) or (password != pw):
        error = 'ユーザ名かパスワードが間違っています．'
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Basic"},
        )
    return username