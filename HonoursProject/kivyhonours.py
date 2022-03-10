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

from APITESTER import apicall23
from APITESTER import apicall_24_hour_percent


coin = Coin()
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
        if coin.exists(k.text):
            coin.updateCoins1(k.text,float(v.text),"add")
            print(k,v)
            coin.process()
            coin.saveCoins()
            coin.loadLocalData()
        else:
            print("doesnt exist")
            MainWindow.show_error("Coin Doesnt Exists")
            
            
        
    
    #removes coin from coin total 
    def remove(self,k,v):
        if coin.exists(k.text):
            coin.updateCoins1(k.text,float(v.text),"remove")
            print(k,v)
            coin.process()
            coin.saveCoins()
            coin.loadLocalData
        else:
            MainWindow.show_error("Coin Doesnt Exists")
            print("doesnt exist")
            
        
        
        
        

class ThirdWindow(Screen):
    def show_popup(self):
        
        show = Fifthwindow()
        popupWindow = Popup(title="Coins",content=show, size_hint=(None,None),size=(600,600))
        
        popupWindow.open()
    
    def show_popup2(self):
        show2 = P()

        PopupWindow = Popup(title="Update Coin Total",content=show2, size_hint=(None,None),size=(400,400))

        PopupWindow.open()
        #UPDATE
        
    def show_popup_candle(self):
        show2 = P()

        PopupWindow = Popup(title="Update Coin Total",content=show2, size_hint=(None,None),size=(400,400))

        PopupWindow.open()
        #UPDATE
    
        
    
 


class CandlePop(Screen):
    pass
    
class ForthWindow(Screen):
    #Takes number of days and coin and loads graph based on input
    def load_historical_week(self,coin):
        showGraph(7,coin)
    def load_historical_month(self,coin):
        showGraph(31,coin)
    def load_historical_year(self,coin):
        showGraph(365,coin)
        #### File Names ETH search Eth
    def apiCall1(self,coin):
        apiCall(coin)
    
  
    #searches for button ID given in kivy file and replaced button text with the value of coin and % change over 24 hours
    def searchButton1(self,coin):
        self.ids.btnb.text = str(apicall23(coin)) + "\n" + str(apicall_24_hour_percent(coin)) +"%"
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