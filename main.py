from database import create_db
from kivy.app import App


class MyApp(App):
    def build(self):
        create_db()

if __name__ == '__main__':
    MyApp().run()
    
    
