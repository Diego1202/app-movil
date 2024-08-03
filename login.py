from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import face_recognition
from database import get_user_data
import numpy as np

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.username = TextInput(hint_text='Username', multiline=False)
        self.password = TextInput(hint_text='Password', multiline=False, password=True)
        self.login_button = Button(text='Login', on_release=self.login)
        back_button = Button(text='Back to Register', on_release=self.go_to_register)

        layout.add_widget(Label(text='Login'))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.login_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def login(self, instance):
        username = self.username.text
        password = self.password.text
        user_data = get_user_data(username)
        
        if user_data and user_data[1] == password:
            stored_face_data = user_data[2]
            if stored_face_data:
                stored_face_encoding = np.frombuffer(stored_face_data, dtype=np.float64)
                print("User logged in successfully")
                self.manager.current = 'home'
            else:
                print("Face data not found for the user.")
        else:
            print("Invalid username or password")

    def go_to_register(self, instance):
        self.manager.current = 'register'
