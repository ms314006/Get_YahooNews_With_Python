import os
from flask import Flask, make_response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

@app.route("/index")
def index():
    strJson += 'Hi'

    resp = make_response(strJson) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
@app.route("/news/it")
def getNewsIt():
    req = requests.request('GET', 'https://tw.news.yahoo.com/tech-development',headers=headers)
    soup = BeautifulSoup(req.text)
    titleDom = soup.find_all('h3', class_='Mb(5px)')
    strJson = '{"data":['
    count = 0
    for title in titleDom:
        if (count == 10):
            break
        else:
            count += 1
        strJson += '{"title":"' + title.text + '",'
        contentReq = requests.request('GET', 'https://tw.news.yahoo.com/' + title.find('a')['href'],headers=headers)
        contentSoup = BeautifulSoup(contentReq.text)
        contentDom = contentSoup.find_all('p', class_='canvas-atom canvas-text Mb(1.0em) Mb(0)--sm Mt(0.8em)--sm')
        strJson += '"content":"'
        for content in contentDom:
            strJson += content.text
        strJson += '"},'
    strJson = strJson[:-1] + ']}'

    resp = make_response(strJson) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)