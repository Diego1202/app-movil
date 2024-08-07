from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class AuthScreen(Screen):
    def __init__(self, **kwargs):
        super(AuthScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        camera_button = Button(text='Login Camera', on_release=self.go_to_camera)
        register_button = Button(text='Register', on_release=self.go_to_register)
        login_button = Button(text='Login', on_release=self.go_to_login)
        # huella_button = Button(text='Login', on_release=self.go_to_huella)

        layout.add_widget(register_button)
        layout.add_widget(camera_button)
        layout.add_widget(login_button)
        # layout.add_widget(huella_button)

        self.add_widget(layout)

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def go_to_camera(self, instance):
        self.manager.current = 'camera'

    # def go_to_huella(self, instance):
    #     self.manager.current = 'huella'
