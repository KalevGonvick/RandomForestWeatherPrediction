import requests
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.config import Config
import json
from kivy.uix.widget import Widget
import socket

#have a premade table of fixed length, just add in the data to the cells
#have a table with dynamically changing length with the data inside
#have it go to a new screen on button press which shows the data with either of the earlier options


######## BASIC HTTP CONNECTION ########
#endpoint url
URL = "http://192.168.0.30:5000"
PORT = 5000

###### USER INTERFACE ########
class ui(App):
    Config.set('graphics', 'width', '1600')
    Config.set('graphics', 'height', '600')

    def predict(self, instance, *args):

        print("predict button was pressed, this was the inputted airport: ", self.airport_txt.text)

        # gather the inputted values
        airport = self.airport_txt.text
        currentDate = datetime.date(datetime.now())

        if ((airport == "")):
            print("User inputted null values, not sending to main server")
        else:
            # put the parameters together
            PARAMS = {'airport': airport, 'date': currentDate}

            # send http request to server
            r = requests.get("http://127.0.0.1:5000" + "/getWeather", PARAMS)
            data = r.content.decode("utf-8").replace("'", '"')
            predictions = json.loads(data)
            print(predictions)

            # parse through the results, display on UI

            # create the popup
            # add the data depending on the number inputted by the user
            box = BoxLayout(orientation="vertical", spacing=20)
            results_box = BoxLayout(orientation="horizontal", spacing=20)
            Day1box = BoxLayout(orientation="vertical", spacing=10, padding=10)
            title = Label(text="Day 1", bold=True)
            label1 = Label(text="Min Temp: " + str(predictions["Day 1"]["Min Temperature"]), bold=False)
            label2 = Label(text="Max Temp: " + str(predictions["Day 1"]["Max Temperature"]), bold=False)
            label3 = Label(text="Avg Temp:" + str(predictions["Day 1"]["Avg Temperature"]), bold=False)
            label4 = Label(text="Min Humidity: "+ str(predictions["Day 1"]["Min Humidity"]), bold=False)
            label5 = Label(text="Max Humidity: "+ str(predictions["Day 1"]["Max Humidity"]), bold=False)
            label6 = Label(text="Avg Humidity: "+ str(predictions["Day 1"]["Avg Humidity"]), bold=False)
            label7 = Label(text="Min Pressure: "+ str(predictions["Day 1"]["Min Pressure"]), bold=False)
            label8 = Label(text="Max Pressure: "+ str(predictions["Day 1"]["Max Pressure"]), bold=False)
            label9 = Label(text="Avg Pressure: "+ str(predictions["Day 1"]["Avg Pressure"]), bold=False)
            Day1box.add_widget(title)
            Day1box.add_widget(label1)
            Day1box.add_widget(label2)
            Day1box.add_widget(label3)
            Day1box.add_widget(label4)
            Day1box.add_widget(label5)
            Day1box.add_widget(label6)
            Day1box.add_widget(label7)
            Day1box.add_widget(label8)
            Day1box.add_widget(label9)
            Day2box = BoxLayout(orientation="vertical", spacing=10, padding=10)
            title2 = Label(text="Day 2", bold=True)
            label12 = Label(text="Min Temp: " + str(predictions["Day 2"]["Min Temperature"]), bold=False)
            label22 = Label(text="Max Temp: " + str(predictions["Day 2"]["Max Temperature"]), bold=False)
            label32 = Label(text="Avg Temp:" + str(predictions["Day 2"]["Avg Temperature"]), bold=False)
            label42 = Label(text="Min Humidity: " + str(predictions["Day 2"]["Min Humidity"]), bold=False)
            label52 = Label(text="Max Humidity: " + str(predictions["Day 2"]["Max Humidity"]), bold=False)
            label62 = Label(text="Avg Humidity: " + str(predictions["Day 2"]["Avg Humidity"]), bold=False)
            label72 = Label(text="Min Pressure: " + str(predictions["Day 2"]["Min Pressure"]), bold=False)
            label82 = Label(text="Max Pressure: " + str(predictions["Day 2"]["Max Pressure"]), bold=False)
            label92 = Label(text="Avg Pressure: " + str(predictions["Day 2"]["Avg Pressure"]), bold=False)
            Day2box.add_widget(title2)
            Day2box.add_widget(label12)
            Day2box.add_widget(label22)
            Day2box.add_widget(label32)
            Day2box.add_widget(label42)
            Day2box.add_widget(label52)
            Day2box.add_widget(label62)
            Day2box.add_widget(label72)
            Day2box.add_widget(label82)
            Day2box.add_widget(label92)
            Day3box = BoxLayout(orientation="vertical", spacing=10, padding=10)
            title3 = Label(text="Day 3", bold=True)
            label13 = Label(text="Min Temp: " + str(predictions["Day 3"]["Min Temperature"]), bold=False)
            label23 = Label(text="Max Temp: " + str(predictions["Day 3"]["Max Temperature"]), bold=False)
            label33 = Label(text="Avg Temp:" + str(predictions["Day 3"]["Avg Temperature"]), bold=False)
            label43 = Label(text="Min Humidity: " + str(predictions["Day 3"]["Min Humidity"]), bold=False)
            label53 = Label(text="Max Humidity: " + str(predictions["Day 3"]["Max Humidity"]), bold=False)
            label63 = Label(text="Avg Humidity: " + str(predictions["Day 3"]["Avg Humidity"]), bold=False)
            label73 = Label(text="Min Pressure: " + str(predictions["Day 3"]["Min Pressure"]), bold=False)
            label83 = Label(text="Max Pressure: " + str(predictions["Day 3"]["Max Pressure"]), bold=False)
            label93 = Label(text="Avg Pressure: " + str(predictions["Day 3"]["Avg Pressure"]), bold=False)
            Day3box.add_widget(title3)
            Day3box.add_widget(label13)
            Day3box.add_widget(label23)
            Day3box.add_widget(label33)
            Day3box.add_widget(label43)
            Day3box.add_widget(label53)
            Day3box.add_widget(label63)
            Day3box.add_widget(label73)
            Day3box.add_widget(label83)
            Day3box.add_widget(label93)
            Day4box = BoxLayout(orientation="vertical", spacing=10, padding=10)
            title4 = Label(text="Day 4", bold=True)
            label14 = Label(text="Min Temp: " + str(predictions["Day 4"]["Min Temperature"]), bold=False)
            label24 = Label(text="Max Temp: " + str(predictions["Day 4"]["Max Temperature"]), bold=False)
            label34 = Label(text="Avg Temp:" + str(predictions["Day 4"]["Avg Temperature"]), bold=False)
            label44 = Label(text="Min Humidity: " + str(predictions["Day 4"]["Min Humidity"]), bold=False)
            label54 = Label(text="Max Humidity: " + str(predictions["Day 4"]["Max Humidity"]), bold=False)
            label64 = Label(text="Avg Humidity: " + str(predictions["Day 4"]["Avg Humidity"]), bold=False)
            label74 = Label(text="Min Pressure: " + str(predictions["Day 4"]["Min Pressure"]), bold=False)
            label84 = Label(text="Max Pressure: " + str(predictions["Day 4"]["Max Pressure"]), bold=False)
            label94 = Label(text="Avg Pressure: " + str(predictions["Day 4"]["Avg Pressure"]), bold=False)
            Day4box.add_widget(title4)
            Day4box.add_widget(label14)
            Day4box.add_widget(label24)
            Day4box.add_widget(label34)
            Day4box.add_widget(label44)
            Day4box.add_widget(label54)
            Day4box.add_widget(label64)
            Day4box.add_widget(label74)
            Day4box.add_widget(label84)
            Day4box.add_widget(label94)
            Day5box = BoxLayout(orientation="vertical", spacing=10, padding=10)
            title5 = Label(text="Day 5", bold=True)
            label15 = Label(text="Min Temp: " + str(predictions["Day 5"]["Min Temperature"]), bold=False)
            label25 = Label(text="Max Temp: " + str(predictions["Day 5"]["Max Temperature"]), bold=False)
            label35 = Label(text="Avg Temp:" + str(predictions["Day 5"]["Avg Temperature"]), bold=False)
            label45 = Label(text="Min Humidity: " + str(predictions["Day 5"]["Min Humidity"]), bold=False)
            label55 = Label(text="Max Humidity: " + str(predictions["Day 5"]["Max Humidity"]), bold=False)
            label65 = Label(text="Avg Humidity: " + str(predictions["Day 5"]["Avg Humidity"]), bold=False)
            label75 = Label(text="Min Pressure: " + str(predictions["Day 5"]["Min Pressure"]), bold=False)
            label85 = Label(text="Max Pressure: " + str(predictions["Day 5"]["Max Pressure"]), bold=False)
            label95 = Label(text="Avg Pressure: " + str(predictions["Day 5"]["Avg Pressure"]), bold=False)
            Day5box.add_widget(title5)
            Day5box.add_widget(label15)
            Day5box.add_widget(label25)
            Day5box.add_widget(label35)
            Day5box.add_widget(label45)
            Day5box.add_widget(label55)
            Day5box.add_widget(label65)
            Day5box.add_widget(label75)
            Day5box.add_widget(label85)
            Day5box.add_widget(label95)
            Day6box = BoxLayout(orientation="vertical", spacing=10, padding=10)
            title6 = Label(text="Day 6", bold=True)
            label16 = Label(text="Min Temp: " + str(predictions["Day 6"]["Min Temperature"]), bold=False)
            label26 = Label(text="Max Temp: " + str(predictions["Day 6"]["Max Temperature"]), bold=False)
            label36 = Label(text="Avg Temp:" + str(predictions["Day 6"]["Avg Temperature"]), bold=False)
            label46 = Label(text="Min Humidity: " + str(predictions["Day 6"]["Min Humidity"]), bold=False)
            label56 = Label(text="Max Humidity: " + str(predictions["Day 6"]["Max Humidity"]), bold=False)
            label66 = Label(text="Avg Humidity: " + str(predictions["Day 6"]["Avg Humidity"]), bold=False)
            label76 = Label(text="Min Pressure: " + str(predictions["Day 6"]["Min Pressure"]), bold=False)
            label86 = Label(text="Max Pressure: " + str(predictions["Day 6"]["Max Pressure"]), bold=False)
            label96 = Label(text="Avg Pressure: " + str(predictions["Day 6"]["Avg Pressure"]), bold=False)
            Day6box.add_widget(title6)
            Day6box.add_widget(label16)
            Day6box.add_widget(label26)
            Day6box.add_widget(label36)
            Day6box.add_widget(label46)
            Day6box.add_widget(label56)
            Day6box.add_widget(label66)
            Day6box.add_widget(label76)
            Day6box.add_widget(label86)
            Day6box.add_widget(label96)
            Day7box = BoxLayout(orientation="vertical", spacing=10, padding=10)
            title7 = Label(text="Day 7", bold=True)
            label17 = Label(text="Min Temp: " + str(predictions["Day 7"]["Min Temperature"]), bold=False)
            label27 = Label(text="Max Temp: " + str(predictions["Day 7"]["Max Temperature"]), bold=False)
            label37 = Label(text="Avg Temp:" + str(predictions["Day 7"]["Avg Temperature"]), bold=False)
            label47 = Label(text="Min Humidity: " + str(predictions["Day 7"]["Min Humidity"]), bold=False)
            label57 = Label(text="Max Humidity: " + str(predictions["Day 7"]["Max Humidity"]), bold=False)
            label67 = Label(text="Avg Humidity: " + str(predictions["Day 7"]["Avg Humidity"]), bold=False)
            label77 = Label(text="Min Pressure: " + str(predictions["Day 7"]["Min Pressure"]), bold=False)
            label87 = Label(text="Max Pressure: " + str(predictions["Day 7"]["Max Pressure"]), bold=False)
            label97 = Label(text="Avg Pressure: " + str(predictions["Day 7"]["Avg Pressure"]), bold=False)
            Day7box.add_widget(title7)
            Day7box.add_widget(label17)
            Day7box.add_widget(label27)
            Day7box.add_widget(label37)
            Day7box.add_widget(label47)
            Day7box.add_widget(label57)
            Day7box.add_widget(label67)
            Day7box.add_widget(label77)
            Day7box.add_widget(label87)
            Day7box.add_widget(label97)

            results_box.add_widget(Day1box)
            results_box.add_widget(Day2box)
            results_box.add_widget(Day3box)
            results_box.add_widget(Day4box)
            results_box.add_widget(Day5box)
            results_box.add_widget(Day6box)
            results_box.add_widget(Day7box)

            box.add_widget(results_box)

            content = box
            popup = Popup(title="Weather Prediction from the Server", content=content, auto_dismiss=False)


            # open the popup
            popup.open()

    def train(self, instance, *args):
        print("train button was pressed, this was the inputted airport: ", self.airport2_txt.text)

    def build(self):
        #build the recycleview

        box = BoxLayout(orientation="vertical", spacing=50, padding=10)
        weather_box = BoxLayout(orientation="vertical", spacing=20)

        #weather prediction section
        weather_txt = Label(text="Get Weather Prediction", font_size=30, bold=False, size_hint=(1,.2))
        #input text areas
        layout = GridLayout(cols=2,spacing=20)
        layout.add_widget(Label(text='AIRPORT CODE', font_size=25))
        self.airport_txt = TextInput(hint_text='Insert airport code here', font_size=25)
        layout.add_widget(self.airport_txt)

        #submit button
        find_weather_btn = Button(text="Predict Weather", on_press=self.predict, font_size= 30, size_hint=(1,1.8))
        #add all elements to the weather box
        weather_box.add_widget(weather_txt)
        weather_box.add_widget(layout)
        weather_box.add_widget(find_weather_btn)

        box.add_widget(weather_box)

        return box

ui().run()
