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
import json

coin = Coin()
with open("values.txt")as f:
    symbolNameConverter = json.load(f)
symbols = []
for k,v in symbolNameConverter.items():
    symbols.append(v)
print(symbols)
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

        self.ids.total_display.text = coinTotal
       

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
        popupWindow = Popup(title="Coins",content=show, size_hint=(None,None),size=(600,600))
        
        popupWindow.open()
    
    def show_popup2(self):
        show2 = AddRemove()

        PopupWindow = Popup(title="Update Coin Total",content=show2, size_hint=(None,None),size=(400,400))

        PopupWindow.open()
        #UPDATE
        
    def show_popup_candle(self):
        show2 = CandlePop()

        PopupWindow = Popup(title="Candle Chart",content=show2, size_hint=(None,None),size=(400,400))

        PopupWindow.open()
        #UPDATE
    def show_popup_pricepred(self):
        show2 = PricePred()
        
        PopupWindow = Popup(title="Price Prediction",content=show2, size_hint=(None,None),size=(400,400))
    
        PopupWindow.open()
        
    
class PricePred(Screen):
    def load_lstm(self,coin):
        
        try: 
            coinNoSpace = coin.text.replace(" ","")
            if self.doesFileExist(coinNoSpace):
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
            
        


class CandlePop(Screen):
    
    def candleChart1(self,coin):
        try:  
        
            coinNoSpace = coin.text.replace(" ","")
        
            candleChart(coinNoSpace)
            showGraphVol(coinNoSpace)
        except:
            MainWindow.show_error("File Not Found")
   
        
    
class ForthWindow(Screen):
    #Takes number of days and coin and loads graph based on input
    def load_historical_week(self,coin):
        try:
            if coin.upper() not in symbols:
                coin = symbolNameConverter[coin.lower()]
                showGraph(7,coin)
                
        except:
            MainWindow.show_error("File Not Found")
            
    def load_historical_month(self,coin):
        try:
            if coin.upper() not in symbols:
                coin = symbolNameConverter[coin.lower()]
                showGraph(31,coin)
            else:
                showGraph(365,coin.upper())
        except:
            MainWindow.show_error("File Not Found")
    def load_historical_year(self,coin):
        try:
            if coin.upper() not in symbols:
                coin = symbolNameConverter[coin.lower()]
                showGraph(365,coin)
            else:
                showGraph(365,coin.upper())
        except :
            MainWindow.show_error("File Not Found")
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
        
    
  
    #searches for button ID given in kivy file and replaced button text with the value of coin and % change over 24 hours
    def searchButton1(self,coin):
        try :
            self.ids.btnb.text = str(apicall23(coin)) + "\n" + str(apicall_24_hour_percent(coin)) +"%"
        except:
            MainWindow.show_error("Incorrect input")
    def percentUpdate(self,coin):
        x = str(apicall_24_hour_percent(coin))
        return x
    
    
        
        
class Fifthwindow(Screen):
    def getItems(self):
        zipp = zip(coin.nameList, coin.coinsOwned, coin.currencyList)
        items = [{"spalte1_SP":x,"spalte2_SP":str(y),"spalte3_SP":"£"+str(z)} for x,y,z in zipp]
        return items
    
    def refresh_RV(self):
        self.ids.rv_id.data = self.getItems()
        self.ids.rv_id.refresh_from_data()
        
    
    
    
            



    

class WindowManager(ScreenManager):
    pass




   
class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        
    



  
    


kv = Builder.load_file("Kivyfile.kv")






class Crypto(App):

    
    
    
    def build(self):
        #return SecondWindow()
        return kv
    

        

  
        


if __name__ =="__main__":
    Crypto().run()