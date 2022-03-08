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


coin = Coin()
zipp = zip(coin.nameList, coin.coinsOwned, coin.currencyList)
items = [{"spalte1_SP":x,"spalte2_SP":str(y),"spalte3_SP":"£"+str(z)} for x,y,z in zipp]

class MainWindow(Screen):
    pass


class Table(BoxLayout):
    pass
class SecondWindow(Screen):
    coin123 = NumericProperty(coin.myTotal)
    
    def load_chart(self):
        coin.graph()
    
    def updateVal(self):
        coin.loadApiData()

        ccc = str(coin.myTotal)
        print(ccc)

        self.ids.total_display.text = ccc
        print("hello")

class P(Screen):
    def runFunc(self,k,v): 
        coin.updateCoins(k.text,float(v.text))
        print(k,v)
        coin.saveCoins()

class ThirdWindow(Screen):
    def show_popup(self):
        show = ForthWindow()
        popupWindow = Popup(title="Coins",content=show, size_hint=(None,None),size=(600,600))

        popupWindow.open()
    
    def show_popup2(self):
        show2 = P()

        PopupWindow = Popup(title="Update Coin Total",content=show2, size_hint=(None,None),size=(400,400))

        PopupWindow.open()
    
 



    
class ForthWindow(Screen):
    pass



    

class WindowManager(ScreenManager):
    pass




   
class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = items



  
    


kv = Builder.load_file("Kivyfile.kv")






class MyMainApp(App):

    
    
    
    def build(self):
        #return SecondWindow()
        return kv
    

        

  
        


if __name__ =="__main__":
    MyMainApp().run()