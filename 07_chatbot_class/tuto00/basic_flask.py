from flask import Flask
from break_time import time_to_coffee

app = Flask(__name__)

print('쉬는 시간을 가질까요?')
print(time_to_coffee())


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello World!'


@app.route('/break')
def break_time():
    return 'python 에서 정상적인 출력이 나오면 10분간 쉬도록하겠습니다'


if __name__ == '__main__':
    app.run()
