import os
from flask import Flask, make_response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

@app.route("/taiwan/bingo")
def taiwanBingo():
    req = requests.request('GET', 'http://www.taiwanlottery.com.tw/Lotto/BINGOBINGO/drawing.aspx',headers=headers)

    soup = BeautifulSoup(req.text)
    strJson = '{"date":"' + soup.find(id="lblMonth").string + soup.find(id="lblDay").string  + '"'
    strJson += ',"period":"' + soup.find(id="lblBBDrawTerm").string  + '"'

    arrNum = soup.find_all("div",class_="ball_tx")
    strNum = ''
    for i in arrNum:
        strNum += i.text.replace(' ', '') + ","

    strJson += ',"number":"' + strNum[:-1]+ '"}'

    resp = make_response(strJson) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/korea/bingo")
def koreaBingo():
    req = requests.request('GET', 'http://www.645lotto.net/gameInfo.do?method=kenoWinNoList',headers=headers)

    soup = BeautifulSoup(req.text)
    arrTemp = soup.find_all("table",class_="tblType1 mt20")[0].tbody.find_all("tr")[0].find_all("td")

    strJson = '{"date":"' + arrTemp[0].text.replace('-','')[4:] + '"'
    strJson += ',"period":"' + arrTemp[1].text + '"'
    ballNum = arrTemp[2].text
    ballNum = ballNum[ballNum.index("numSort('") + 9:ballNum.index("');")]

    arrNum = []

    for i in range(len(ballNum)):
        if i%2!=0:
            continue
        arrNum.append(ballNum[i] + ballNum[i+1])

    arrNum.sort()
    strJson += ',"number":"' + ",".join(arrNum) + '"}'
    
    resp = make_response(strJson) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/america/powerball")
def americaPowerball():
    req = requests.request('GET', 'https://www.lotteryusa.com/powerball/',headers=headers)

    soup = BeautifulSoup(req.text)
    strJson = '{"date":"' + soup.time['datetime'].replace('-','')[4:] + '"'
    strJson += ',"period":""'

    arrNum = soup.find_all("ul",class_="draw-result")[0].find_all("li")
    strNum = ''
    for i in range(6):
        strNum += arrNum[i].text + ','
    strJson += ',"number":"' + strNum.replace('PB,','').replace(' ','')[:-1] + '"}'
    
    resp = make_response(strJson) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)