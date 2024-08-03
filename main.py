from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from register import RegisterScreen
from login import LoginScreen
from home import HomeScreen
from database import create_db

class MyApp(App):
    def build(self):
        create_db()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(LoginScreen(name='login'))
        return sm

if __name__ == '__main__':
    MyApp().run()
