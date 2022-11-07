import hashlib
import random
import string
from datetime import time, datetime, timezone, timedelta
import hashlib
import pandas as pd
import requests
import yfinance as yf
import psycopg2
import pytz
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, url_for, request, session, make_response, jsonify, json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/")
def index():
    try:
        conn = psycopg2.connect(dbname='dbname', user='user', password='password', host='host', port='port')
    except:
        print("I am unable to connect to the database")

    cur = conn.cursor()

    cur.execute("""SELECT * FROM tickers""") # GETTING A LIST OF TICKERS FROM DB
    tickers = list(cur.fetchall())

    # GROUPING THE TICKERS ACCORDING TO THE RISE IN PRICE COMPARED TO YESTERDAY'S CLOSE

    favorable_up = []
    favorable_down = []
    for ticker in tickers:
        ticker_yahoo = yf.Ticker(fav)
        data1 = ticker_yahoo.history()
        last_quote = data1['Close'].iloc[-1]
        tick_price = round(last_quote, 2)

        rate = 100 - (tick_price / last_tick) * 100
        if tick_price < last_tick:
            favorable_down.append(tuple([rate, fav[0], fav[1], fav[2]]))
        if tick_price > last_tick:
            favorable_up.append(tuple([rate, fav[0], fav[1], fav[2]]))

    favorable_up = favorable_up.sort(reverse=True)
    favorable_up = favorable_up[:5]
    favorable_down= favorable_down.sort(reverse=True)
    favorable_down = favorable_down[:5]

    # GETTING AN AVERAGE VALUE OF ALL THE TICKERS TO RENDER 1 LINE CHART
    
    frame = pd.DataFrame()
    for ticker in tickers:
        data = yf.download(tickers=fav, period="3d", interval="1m", auto_adjust=True)
        frame[ticker] = data['Close']

    frame['mean'] = frame.mean(axis=1)
    frame['time'] = range(1, frame.shape[0])

    mean_list = frame['mean'].tolist()
    time_list = frame['time'].tolist()

    cur.close()

    return render_template("index.html", mean_list = mean_list, time_list = time_list, favorable_up = favorable_up, favorable_down = favorable_down, tickers = tickers)

if __name__ == "__main__":
    app.run()
