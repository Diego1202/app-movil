from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
# from kivy.uix.screenmanager import ScreenManager
from register import RegisterScreen
from login import LoginScreen
from auth import AuthScreen
from database import create_db
from face import LoginCameraScreen
from Home import HomeScreen
from Huella import RegHuellaScreen

class MyApp(MDApp):  # Inherit from MDApp
    def build(self):
        create_db()
        sm = ScreenManager()
        sm.add_widget(AuthScreen(name='home'))
        sm.add_widget(LoginCameraScreen(name='camera'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='welcome'))
        sm.add_widget(RegHuellaScreen(name='huella'))
        return sm

if __name__ == '__main__':
    MyApp().run()
