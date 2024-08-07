from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.camera import Camera
import base64
import face_recognition
import numpy as np
from PIL import Image as PILImage
from database import get_user
from util import Alerts

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.alerts = Alerts()
        self.username = TextInput(hint_text='Username', multiline=False)
        self.password = TextInput(hint_text='Password', multiline=False, password=True)

        login_button = Button(text='Login', size_hint=(1, 0.4), on_release=self.login)
        register_button = Button(text='Back to Register',size_hint=(1, 0.4), on_release=self.go_to_register)
        home_button = Button(text='Regresar', size_hint=(1, 0.4), on_release=self.go_to_home)

        layout.add_widget(Label(text='Login', font_size='24sp',  # Tamaño de fuente
            color=(0, 0, 0, 1),  # Color negro (r, g, b, a)
            size_hint_y=None,  # No ajustar automáticamente la altura
            height=50,  # Altura de la etiqueta
            valign='top',  # Alineación vertical
            ))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_button)
        layout.add_widget(register_button)
        layout.add_widget(home_button)

        self.add_widget(layout)


    def login(self, instance):
        username = self.username.text
        password = self.password.text
        if username and password:
            user_data = get_user(username)
            if user_data and user_data[1] == password:
                print(user_data[0])
                self.manager.get_screen('welcome').set_username(user_data[0])
                self.manager.current = 'welcome' 
            else:
                self.alerts.show_message("Alerta","Username or password incorrect")
        else:
            self.alerts.show_message("Importante","Username, password, and face capture are required")

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def go_to_home(self, instance):
        self.manager.current = 'home'
