from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        register_button = Button(text='Register', on_release=self.go_to_register)
        login_button = Button(text='Login', on_release=self.go_to_login)

        layout.add_widget(register_button)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def go_to_login(self, instance):
        self.manager.current = 'login'
