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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)