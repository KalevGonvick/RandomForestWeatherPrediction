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
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '900')
    def predict(self, instance, *args):

        print("predict button was pressed, this was the inputted airport: ", self.airport_txt.text)

        # gather the inputted values
        airport = self.airport_txt.text
        daysNum = self.days_txt.text
        currentDate = datetime.date(datetime.now())

        if ((airport == "") | (daysNum =="")):
            print("User inputted null values, not sending to main server")
        else:
            # put the parameters together
            PARAMS = {'airport': airport, 'days': daysNum, 'date': currentDate}

            # send http request to server
            r = requests.get("http://127.0.0.1:5000", PARAMS)
            print(r.content)
            #read results from server
            #data = r.json()

            # parse through the results, display on UI
            # fake data
            items = [
                {"color": (1, 1, 1, 1), "font_size": "20sp", "text": "white", "input_data": ["some", "random", "data"]},
                {"color": (.5, 1, 1, 1), "font_size": "30sp", "text": "lightblue", "input_data": [1, 6, 3]},
                {"color": (.5, .5, 1, 1), "font_size": "40sp", "text": "blue", "input_data": [64, 16, 9]},
                {"color": (.5, .5, .5, 1), "font_size": "70sp", "text": "gray", "input_data": [8766, 13, 6]},
                {"color": (1, .5, .5, 1), "font_size": "60sp", "text": "orange", "input_data": [9, 4, 6]},
                {"color": (1, 1, .5, 1), "font_size": "50sp", "text": "yellow", "input_data": [852, 958, 123]},
                {"color": (.5, .5, 1, 1), "font_size": "40sp", "text": "blue", "input_data": [64, 16, 9]},
                {"color": (.5, .5, .5, 1), "font_size": "70sp", "text": "gray", "input_data": [8766, 13, 6]},
                {"color": (1, .5, .5, 1), "font_size": "60sp", "text": "orange", "input_data": [9, 4, 6]},
                {"color": (1, 1, .5, 1), "font_size": "50sp", "text": "yellow", "input_data": [852, 958, 123]}
            ]

            # create the popup
            # add the data depending on the number inputted by the user
            box = BoxLayout(orientation="vertical")
            for item in items:
                name = "item" + str(item)
                l = Label(text=name)
                box.add_widget(l)

            label = Label(text=airport)
            back = Button(text="back")
            box.add_widget(label)
            box.add_widget(back)
            content = box
            popup = Popup(title="Weather Prediction from the Server", content=content, auto_dismiss=False)
            back.bind(on_press=popup.dismiss)

            # open the popup
            popup.open()

    def train(self, instance, *args):
        print("train button was pressed, this was the inputted airport: ", self.airport2_txt.text)

    def build(self):
        #build the recycleview

        box = BoxLayout(orientation="vertical", spacing=10, padding=10)
        weather_box = BoxLayout(orientation="vertical", spacing=20)
        training_box = BoxLayout(orientation="vertical", spacing=20)

        #weather prediction section
        weather_txt = Label(text="Get Weather Prediction", font_size=30)
        #input text areas
        layout = GridLayout(cols=2,spacing=20)
        layout.add_widget(Label(text='AIRPORT CODE'))
        self.airport_txt = TextInput(hint_text='Insert airport code here')
        layout.add_widget(self.airport_txt)

        layout.add_widget(Label(text='Number of Days'))
        self.days_txt = TextInput(hint_text='Insert number of days here')
        layout.add_widget(self.days_txt)
        #submit button
        find_weather_btn = Button(text="Predict Weather", on_press=self.predict)
        #add all elements to the weather box
        weather_box.add_widget(weather_txt)
        weather_box.add_widget(layout)
        weather_box.add_widget(find_weather_btn)


        #model training section
        training_txt = Label(text='Train model', font_size=30)
        #input fields
        layout2 = GridLayout(cols=2, spacing=20)
        layout2.add_widget(Label(text='AIRPORT CODE'))
        self.airport2_txt = TextInput(hint_text='Insert airport code here')
        layout2.add_widget(self.airport2_txt)

        #input start date
        layout2.add_widget(Label(text='Start Date'))
        self.startdate = TextInput(hint_text='Insert start date here (YYYY-MM-DD)')
        layout2.add_widget(self.startdate)
        #input end date
        layout2.add_widget(Label(text='End Date'))
        self.enddate = TextInput(hint_text='Insert end date here (YYYY-MM-DD)')
        layout2.add_widget(self.enddate)

        #submit button
        train_btn = Button(text="Train Model", on_press=self.train)

        # add all elements to the training box
        training_box.add_widget(training_txt)
        training_box.add_widget(layout2)
        training_box.add_widget(train_btn)


        box.add_widget(weather_box)
        box.add_widget(training_box)
        return box

ui().run()
