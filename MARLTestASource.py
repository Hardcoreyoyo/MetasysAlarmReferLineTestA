import requests
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

'''
連動網址：
https://notify-bot.line.me/oauth/authorize?response_type=code&client_id=Line設定取得&redirect_uri=本地端設定&scope=notify&state=NO_STATE
'''


def getNotifyToken(AuthorizeCode):
    body = {
        "grant_type": "authorization_code",
        "code": AuthorizeCode,
        "redirect_uri": '本地端設定',
        "client_id": 'Line設定取得',
        "client_secret": 'Line設定取得'
    }
    r = requests.post("https://notify-bot.line.me/oauth/token", data=body)
    return r.json()["access_token"]


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
    return r.status_code





@app.route('/', methods=['POST', 'GET'])
def hello_world():
    authorizeCode = request.args.get('code')
    token = getNotifyToken(authorizeCode)
    print(token)
    lineNotifyMessage(token, "恭喜你連動完成")
    return f"恭喜你，連動完成"


@app.route('/OutputText', methods=['POST', 'GET'])
def OutputText():
    if request.method == 'GET':
        return render_template('InputText.html')

    if request.method == 'POST':
        InputText = request.form["Text"]
        InputText = str(InputText)
        lineNotifyMessage("Line設定取得", InputText)
        return InputText



if __name__ == '__main__':
    app.run()
