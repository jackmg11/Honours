from mimetypes import init
from tkinter import E
from matplotlib.pyplot import show
from coinmarketstuff import Coin
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from apihonours import showGraph
from apihonours import apiCall
from apihonours import candleChart
from apihonours import showGraphVol
from lstm import LSTMFunc
from APITESTER import apicall23
from APITESTER import apicall_24_hour_percent
from sentiment import sentimentAverage

import json
import apihonours

coin = Coin()
with open("values.txt")as f:
    symbolNameConverter = json.load(f)
symbols = []
names = []
nameSymbolConverter = {}
for k,v in symbolNameConverter.items():
    symbols.append(v)
    names.append(k)
    nameSymbolConverter[v] = k
    
#print(symbolNameConverter)
def getItems(coin):
    zipp = zip(coin.nameList, coin.coinsOwned, coin.currencyList)
    items = [{"spalte1_SP":x,"spalte2_SP":str(y),"spalte3_SP":"£"+str(z)} for x,y,z in zipp]
    return items


class MainWindow(Screen):
    #Error message used on 3 pages 
    @staticmethod
    def show_error(message):
        

        PopupWindow = Popup(title="Error",content=Label(text=message), size_hint=(None,None),size=(400,400))

        PopupWindow.open()
        
        
            
class Table(BoxLayout):
    pass    
class Table3(BoxLayout):
    pass
class Table2(BoxLayout):
    pass
class SecondWindow(Screen):
    coin123 = NumericProperty(coin.myTotal)
    
    
    #loads graph of total coins in piechart
    def load_chart(self):
        coin.graph()
    #updates value of total coins owned
    def updateVal(self):
        coin.loadApiData()

        coinTotal = str(coin.myTotal)
        print(coinTotal)

        self.ids.total_display.text = "£"+ coinTotal
       

class AddRemove(Screen):
    #adds coins to coin total
    def add(self,k,v):
        try:
            k = k.text.strip()
            if coin.exists(k):
                coin.updateCoins1(k,float(v.text),"add")
                print(k,v)
                coin.process()
                coin.saveCoins()
                coin.loadLocalData()
            else:
                print("doesnt exist")
                MainWindow.show_error("Coin Doesnt Exists")
        except:
            MainWindow.show_error("Please Add coin amount")
                
        
    
    #removes coin from coin total 
    def remove(self,k,v):
        try:
            
            k = k.text.strip()
            if coin.exists(k):
                coin.updateCoins1(k,float(v.text),"remove")
                print(k,v)
                coin.process()
                coin.saveCoins()
                coin.loadLocalData
            else:
                MainWindow.show_error("Coin Doesnt Exists")
                print("doesnt exist")
        except:
            MainWindow.show_error("Please Add coin amount")
            
        
        
        
        

class ThirdWindow(Screen):
    def show_popup(self):
        
        show = Fifthwindow()
        popupWindow = Popup(title="Coins",content=show, size_hint=(0.85,0.85))
        
        popupWindow.open()
    
    def show_popup2(self):
        show2 = AddRemove()

        PopupWindow = Popup(title="Update Coin Total",content=show2, size_hint=(0.85,0.85))

        PopupWindow.open()
        #UPDATE
        
    def show_popup_candle(self):
        show2 = CandlePop()

        PopupWindow = Popup(title="Candle Chart",content=show2, size_hint=(0.9,0.9))

        PopupWindow.open()
        #UPDATE
    def show_popup_pricepred(self):
        show2 = PricePred()
        
        PopupWindow = Popup(title="Price Prediction",content=show2, size_hint=(0.85,0.85))
    
        PopupWindow.open()
        

    
class PricePred(Screen):
    def load_lstm(self,coin):
        
        try: 
            coinNoSpace = coin.text.replace(" ","")
            if self.doesFileExist(coinNoSpace):
                MainWindow.show_error("Incorrect input")
                
                
                
                LSTMFunc(coinNoSpace)
                
                
                
            else:
                apiCall(coinNoSpace)
                LSTMFunc(coinNoSpace)
                
                
        except:
            MainWindow.show_error("File Not Found")
   
        
    
   
                          
             
            
    @staticmethod
    def doesFileExist(coin):
        try:
            with open(f"ApiCryptoData{coin}.csv") as f:
                return True
        except FileNotFoundError:
            return False 
            
        
class Portfolio_pred(Screen):
    
    def getcoinvalues(self):
        with open("coins.txt","r") as f:
            file = json.load(f)
            lst1 =[]
            lst2 =[]
            for k,v in file.items():
                lst1.append(symbolNameConverter[k.lower()])
                lst2.append(v)
        return self.portfoliopred(lst1,lst2)
        
    def portfoliopred(self,coins,amount):
        
        totalval =[]
        for coin in coins:
            
            totalval.append(LSTMFunc(coin))
        coinamount =[]
        zipped = zip(totalval,amount)
        for val,am in zipped:
            coinamount.append(val*am)
        zipped2 = zip(coinamount,coins)
        totalcoins = {}
        for x,y in zipped2:
            totalcoins[y]=x
        lst1 = []
        lst2 =[]
        for k,v in totalcoins.items():
            lst1.append(k)
            lst2.append(v)
        zipp = zip(lst1,lst2)
        items1 = [{"item12":str(x),"item22":str(y)} for x,y in zipp]
        print(items1)
        return items1
        
    def refresh_RV(self):
        print("hello")
        self.ids.rv_id3.data = self.getcoinvalues()
        self.ids.rv_id3.refresh_from_data()
    

class CandlePop(Screen):
    
    def candleChart1(self,coin):
        #try:
            #print(coin.text)
            coinNoSpace = coin.text.replace(" ","")
            if coinNoSpace.upper() not in symbols:
                print(coinNoSpace)
                coinNoSpace = symbolNameConverter[coinNoSpace.lower()]
                
                candleChart(coinNoSpace)
                showGraphVol(coinNoSpace)
                
            else:
                candleChart(coinNoSpace.upper())
                showGraphVol(coinNoSpace.upper())
                
        
                
        #except:
            #MainWindow.show_error("File Not Found")
            
        
   
        
    
class ForthWindow(Screen):
    
    def marketsent(self):
        
        self.ids.btnb2.text = sentimentAverage()
            
    
        #except :
            #MainWindow.show_error("File Not Found")
        #### File Names ETH search Eth
    def apiCall1(self,coin):
        try:
            if coin.upper() not in symbols:
                coin = symbolNameConverter[coin.lower()]
                apiCall(coin)
            else:
                apiCall(coin.upper())
        except:
            MainWindow.show_error("File Not Found")
        
    def showWindowNews(self):
        show2 = popup6()
        
        PopupWindow = Popup(title="News",content=show2, size_hint=(0.85,0.85))
    
        PopupWindow.open()    
  
    #searches for button ID given in kivy file and replaced button text with the value of coin and % change over 24 hours
    def searchButton1(self,coin):
        try:
            print(nameSymbolConverter)
            if coin.upper() in symbols:
                
                coin = nameSymbolConverter[coin.upper()]
                #print(coin)
            price = apicall23(coin)
            percent24 = apicall_24_hour_percent(coin)         

            self.ids.btnb.text = "£"+ str(price) + "\n" + str(percent24) +"%"

            #self.ids.btnb.text = str(apicall23(coin)) + "\n" + str(apicall_24_hour_percent(coin)) +"%"
        except:
            MainWindow.show_error("Incorrect input")
    
    
    def show_porfolio_pred(self):

        show2 = Portfolio_pred()

        PopupWindow = Popup(title="Price Prediction",content=show2, size_hint=(0.9,0.9))

        PopupWindow.open()      
            
        
class Fifthwindow(Screen):
    def getItems(self):
        zipp = zip(coin.nameList, coin.coinsOwned, coin.currencyList)
        items = [{"spalte1_SP":x,"spalte2_SP":str(y),"spalte3_SP":"£"+str(round(z,2))} for x,y,z in zipp]
        return items
   
        
    
    def refresh_RV(self):
        self.ids.rv_id.data = self.getItems()
        self.ids.rv_id.refresh_from_data()
    
        
    
class popup6(Screen):
    def newslist(self):
        lst1 =[]
        lst2 = []
        for k,v in apihonours.news().items():
            lst1.append(k)
            lst2.append(v)

        zipp = zip(lst1,lst2)
        items = [{"item1":x,"item2":y} for x,y in zipp]
        #print(zipp)
        #print(items)
        return items  

    def refresh_RV(self):
        self.ids.rv_id1.data = self.newlist()
        self.ids.rv_id1.refresh_from_data()



            



    

class WindowManager(ScreenManager):
    pass




   
class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        
class RV1(RecycleView):
    def __init__(self, **kwargs):
        super(RV1, self).__init__(**kwargs)
    



  
    


kv = Builder.load_file("Kivyfile.kv")





class Crypto(App):

    
    
    
    def build(self):
        #return SecondWindow()
        return kv
    

        

  
        


if __name__ =="__main__":
    Crypto().run()
    