import pandas as pd
from pandas import read_csv
from matplotlib import pyplot as plt
import requests
import json 
from datetime import datetime

def Time_converter(time):
    time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d')
    return time
def Year_converter(time):
    time = datetime.utcfromtimestamp(time).strftime('%Y')
    return time
#Makes call tp API drops 2 cols and adds time conversion from unix time
def apiCall(Coinname):
    url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={Coinname}&tsym=GBP&limit=2000"
    a = requests.get(url)
    data = json.loads(a.text)
    
    Values = data["Data"]["Data"]
    
    df2 = pd.DataFrame(Values)
    df2["RealTime"]=df2["time"].apply(Time_converter)
    df2.drop("conversionType", inplace=True ,axis=1)
    df2.drop("conversionSymbol", inplace=True ,axis=1)
    df2.to_csv(f"ApiCryptoData{Coinname}.csv")
    return df2
    
#takes name of csv file
def loadData(file):
    return read_csv(file)




    
#takes days and coin and returns graph of both
def showGraph(days,coin): 
    data = loadData(f"ApiCryptoData{coin.strip()}.csv")
    data["Date"]=data["time"].apply(Time_converter)
   
   
    data1 = data.tail(days)
    graph = data1[[("Date"),"high"]]
    graph.plot(x="Date")
  
    plt.locator_params(axis="x",nbins=4)
    plt.show()

def showGraphVol(coin): 
    data = loadData(f"ApiCryptoData{coin.strip()}.csv")
    data["Date"]=data["time"].apply(Time_converter)
   
   
    data1 = data.tail(2000)
    graph = data1[[("Date"),"volumeto"]]
    graph.plot(x="Date")
  
    plt.locator_params(axis="x",nbins=4)
    plt.show()



"""def showGraph1(date,coin): 
    data = loadData(f"ApiCryptoData{coin}.csv")
    data["RealTime"]=data["time"].apply(Time_converter)
   
   
    data1 = data.tail(date)
    graph = data1[["RealTime","volumeto"]]
    graph.plot()
    plt.figure(300)
    plt.locator_params(axis="x",nbins=4)
    plt.show()"""

#showGraph1("eth")



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
