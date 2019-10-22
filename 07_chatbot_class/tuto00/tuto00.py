# -*- coding: utf-8 -*-
"""
목표 : 가장 기본적인 형태를 익혀봅시다.
"""

# flask 라이브러리 가져오기
from flask import Flask

# app 이라는 이름의 flask 객체 생성
app = Flask(__name__)

# 127.0.0.1:5000/ 에 들어오면 실행
@app.route('/', methods=['GET','POST'])
def receive_message():
    return 'Hello World!'

# 127.0.0.1:5000/Home 에 들어오면 실행
@app.route('/Home', methods=['GET','POST'])
def home():
    return 'My Sweet Home!'


if __name__ == '__main__':
    app.run()
