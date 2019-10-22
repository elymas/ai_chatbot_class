# -*- coding: utf-8 -*-

import requests
from flask import Flask, request, Response

API_KEY = '{본인계정정보}'

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
    
    return chat_id, msg


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
    # 변수들을 딕셔너리 형식으로 묶음
    # 사용자에게 보내는 text는 사용자가 보낸 text와 똑같다
    # 똑같은 소리를 한다고 해서 Echo_bot
    params = {'chat_id': chat_id, 'text': text}
    
    # Url 에 params 를 json 형식으로 변환하여 전송
    # 메세지를 전송하는 부분
    response = requests.post(url, json=params)
    print(response)
    return response

    
# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()
                
        # parse_message 함수는 두가지 return 값을 가진다 (chat_id, msg)
        # 순서대로 chat_id, msg의 변수로 받아준다.
        chat_id, msg = parse_message(message)
        
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

