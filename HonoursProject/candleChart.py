import plotly.graph_objects as go

import pandas as pd
from datetime import datetime


def candleChart(coin):
    df = pd.read_csv(f'APICryptoData{coin}.csv')

    fig1 = go.Figure(data=[go.Candlestick(x=df['RealTime'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])

    fig1.show()

