from audioop import add
import matplotlib.pyplot as plt
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
class Coin:
  def __init__(self):
    self.data = None
    self.coins = None
    self.myTotal = 0
    self.globalNameList = []
    self.loadLocalData()
    self.LoadLocalCoins()
    self.nameList = []
    self.process()
    
    

  def storeLocalData(self):
    with open("data.txt","w") as f:
      json.dump(self.data,f)
   
  def LoadLocalCoins(self):
    try:
      with open("coins.txt","r") as f:
        self.coins = json.load(f)
        print("loaded Local Coins")
      if len(self.coins)<1:
        print("you need to create coins file")
        exit()
    except FileNotFoundError:
      print("you need to create coins file")
      exit()
      
      

  def loadLocalData(self):
    try:
      with open("data.txt","r") as f:
        self.data = json.load(f)
        print("Loaded Local")
      if len(self.data["data"]) <1:

        self.loadApiData()
        
      else:
        pass

    except FileNotFoundError:
      self.loadApiData()
  
  


  def loadApiData(self):
    print("Called Api")
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'5000',
      'convert':'GBP'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'b2246584-2198-44bf-890d-094be5f7a79f',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      self.data = json.loads(response.text)
      self.process()
      self.storeLocalData()
      
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
  def process(self):
    a = self.data["data"]


    
    self.nameList = []
    self.globalNameList = []
    self.symbolNameConverter = {}
    for k in self.coins.keys():

      self.nameList.append(k)  
    
    cleandata = []
    for i in a:
      self.globalNameList.append(i["name"].lower())
      self.symbolNameConverter[i["symbol"].lower()] = i["name"]
      if i["name"] in self.nameList:
          cleandata.append(i)
  
    

    
          
    
    name = []
    price = []
    dct = {}

    x = zip(name,price)
   
    for i in cleandata:
      name.append(i["name"])
      price.append(i["quote"]["GBP"]["price"])
      
    
    for name,price in x:
      dct[name]=price
    

    self.currencyList = []
    self.nameList = []
    self.coinsOwned = []

    for k,v in self.coins.items():
      self.currencyList.append(dct[k]*v)
      self.nameList.append(k)
      self.coinsOwned.append(v)
    

    
    amount = {"Bitcoin":0.01303729,"Ethereum":4.23188155,"Bitcoin Cash":1.505,"Litecoin":1.165,"Chainlink":2.76,"Stellar":544.30,"Uniswap":3.37,"Aave":0.63,"UMA":4.38,"Ethereum Classic":30.48,"OMG Network":20.59,"Numeraire":2.35,"Orchid":89.19,"Balancer":1.96,"The Graph":42.24,"Compound":0.15,"Monero":3.847,"Cardano":959,"Polkadot":8.1,"Ravencoin":1603.00,"Sushiswap":1.75,"PancakeSwap":16.4,"Binance Coin":0.0059209}

    
    


    self.myTotal = sum(self.currencyList)
    self.myTotal = round(self.myTotal,2)
    
    #return self.myTotal
    #print(self.myTotal)

    
    


  def exists(self,k):
    if k.lower() in self.symbolNameConverter:
      k = self.symbolNameConverter[k.lower()]
    if k.lower() in self.globalNameList:
      return True
    else:
      return False
    
 
  def graph(self):

    sizes = self.currencyList
    labels = self.nameList

    fig1, ax1 = plt.subplots(figsize=(6, 5))
    fig1.subplots_adjust(0.3,0,1,1)


    theme = plt.get_cmap('hsv')
    ax1.set_prop_cycle("color", [theme(1. * i / len(sizes)) for i in range(len(sizes))])

    _, _ = ax1.pie(sizes, startangle=90)

    ax1.axis('equal')

    total = sum(sizes)
    plt.legend(
        loc='upper left',
        labels=['%s, %1.1f%%' % (
            l, (float(s) / total) * 100) for l, s in zip(labels, sizes)],
        prop={'size': 11},
        bbox_to_anchor=(0.0, 1),
        bbox_transform=fig1.transFigure
    )

    plt.show()

  
    
  def updateCoins1(self,k,v,addremove):
    if k.lower() in self.symbolNameConverter:
      k = self.symbolNameConverter[k.lower()]
    k = k.lower().capitalize()
    if addremove == "remove":
      self.coins[k] = self.coins[k] - v
      self.saveCoins()
      self.process()
      self.loadLocalData()
    elif addremove == "add":
      self.coins[k] = self.coins[k] + v
      self.saveCoins()
      self.process()
      self.loadLocalData()
    





  def saveCoins(self):
    with open("coins.txt","w") as f:
      json.dump(self.coins,f)







      
    

    



if __name__=="__main__":
  ccc = Coin()
  #ccc.loadApiData()
  ccc.process()
  #ccc.graph()
  #ccc.updateCoins("Bitoin",0.01863129)
  
  ccc.saveCoins()



