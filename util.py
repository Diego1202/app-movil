from kivy.uix.popup import Popup
from kivy.uix.label import Label

class Alerts:
    def show_message(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.3),
                      auto_dismiss=True)
        popup.open()
