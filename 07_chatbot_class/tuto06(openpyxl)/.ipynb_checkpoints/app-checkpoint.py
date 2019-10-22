# -*- coding: utf-8 -*-

import requests
from flask import Flask, request, Response
from Tuto02 import find_user_row, user_counter
import numpy as np

API_KEY = '930278500:AAFQH3njUefoCC1iPb8wAQUQf2o2L-uGQyo'

app = Flask(__name__)


def parse_message(message):
    """
    telegram 에서 data 인자를 받아옴
    data 내부 구조를 이해해야 한다.
    
    Retuen :    
    chat_id = 사용자 아이디 코드
    msg = 사용자 대화 내용    
    """
    chat_id = message['message']['chat']['id']
    msg = message['message']['text']

    # 실습1 : 사용자 이름을 파싱
    last_name = message['message']['from']['last_name']
    first_name = message['message']['from']['first_name']
    user_name = last_name + first_name
    
    return chat_id, msg, user_name


def send_message(chat_id, text='hello'):
    """
    chat_id : 사용자 아이디 코드
    text : 사용자 대화내용

    Return :
    함수에 변수를 할당할때 text='hello' 라고 선언
    --> text에 관련된 값이 전달되지 않으면 hello를 default로 사용
    
    사용자에게 메세지를 보내는 내용의 함수   
    """
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
    params = {'chat_id': chat_id, 'text': '안녕!'}

    response = requests.post(url, json=params)
    print(response)
    return response


def send_welcome_msg(chat_id):
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)
    welcome_msg_set = ['어서와! 챗봇은 처음이지?', '안녕! 반가워 처음이지 챗봇은?', 'ㅎㅇ', '처음뵙겠습니다. 챗봇이라고합니다.']
    params = {'chat_id': chat_id, 'text': np.random.choice(welcome_msg_set)}
    requests.post(url, json=params)


# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()
                
        # parse_message 함수는 두가지 return 값을 가진다 (chat_id, msg)
        # 순서대로 chat_id, msg의 변수로 받아준다.
        
        # 실습1 : parse_message 함수를 수정하여 3가지 return 값을 가진다. 
        chat_id, msg, user_name = parse_message(message)
        user_row, is_welcome = find_user_row(chat_id, user_name)
        
        
        # 실습2 솔루션(3): 새로 정의한 함수 사용
        user_counter(user_row)

        if is_welcome:
            send_welcome_msg(chat_id)
            return Response('ok', status=200)

        # send_message 함수에 두가지 변수를 전달
        send_message(chat_id, msg)
        
        # 여기까지 오류가 없으면 서버상태 200 으로 반응
        return Response('ok', status=200)
    else:
        return 'Hello World!'


@app.route('/about')
def about():
  return 'About page'


if __name__ == '__main__':
    app.run(port = 5000)

