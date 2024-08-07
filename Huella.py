import base64
from kivymd.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from database import save_user

# Supuesto: Biblioteca de huellas dactilares
import fingerprint

class RegHuellaScreen(Screen):
    def __init__(self, **kwargs):
        super(RegHuellaScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.username = TextInput(hint_text='Username', multiline=False)

        home_button = Button(text='Regresar', size_hint=(1, 0.3), on_release=self.go_to_home)
        self.capture_fingerprint_button = Button(text='Capturar huella', size_hint=(1, 0.3), on_release=self.capture_fingerprint)
        register_button = Button(text='Crear cuenta', size_hint=(1, 0.3), on_release=self.register)

        layout.add_widget(Label(text='Register your user', font_size='24sp',  # Tamaño de fuente
            color=(0, 0, 0, 1),  # Color negro (r, g, b, a)
            size_hint_y=None,  # No ajustar automáticamente la altura
            height=50,  # Altura de la etiqueta
            valign='top',  # Alineación vertical
            ))
        layout.add_widget(self.username)
        layout.add_widget(self.capture_fingerprint_button)
        layout.add_widget(register_button)
        layout.add_widget(home_button)

        self.add_widget(layout)

    def capture_fingerprint(self, instance):
        # Falta funcion para obtener datos del sensor de huella
        fingerprint_data =  "dfds" #fingerprint.Fingerprint()
        if fingerprint_data:
            self.fingerprint_data = fingerprint_data
            print("Fingerprint captured successfully")
        else:
            print("No fingerprint detected")

    def register(self, instance):
        username = self.username.text
        if username and hasattr(self, 'fingerprint_data'):
            fingerprint_data_base64 = base64.b64encode(self.fingerprint_data).decode('utf-8')
            # save_user(username, fingerprint_data_base64)
            print("User registered successfully")
            self.manager.current = 'login'
        else:
            print("Username, and fingerprint capture are required")

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def go_to_home(self, instance):
        self.manager.current = 'home'
