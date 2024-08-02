from database import create_db
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from register import RegisterScreen


class MyApp(App):
    def build(self):
        create_db()
        sm = ScreenManager()
        sm.add_widget(RegisterScreen(name='register'))
        return sm

if __name__ == '__main__':
    MyApp().run()
    
    
