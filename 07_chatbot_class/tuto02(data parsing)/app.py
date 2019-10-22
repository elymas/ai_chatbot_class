# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import json

API_KEY = '{본인계정정보}'

# Flask 객체를 생성 __name__ 을 인수로 입력
app = Flask(__name__)


# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()

        # 메세지가 어떤식으로 들어오는지 json 파일로 저장
        with open('response.json', 'a+', encoding='UTF-8') as f:
            json.dump(message, f, indent=4, ensure_ascii=False)

        return Response('ok', status=200)
    else:
        return "Hello World!"


if __name__ == '__main__':
    app.run(port=5000)
