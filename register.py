from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
import face_recognition
import numpy as np
from PIL import Image as PILImage
from io import BytesIO
from database import save_user

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        self.username = TextInput(hint_text='Username', multiline=False)
        self.password = TextInput(hint_text='Password', multiline=False, password=True)

        # Initialize camera
        self.camera = Camera(play=True, resolution=(640, 480))
        self.capture_button = Button(text='Capture Face', on_release=self.capture_face)
        register_button = Button(text='Create Account', on_release=self.register)
        back_button = Button(text='Back to Login', on_release=self.go_to_login)

        layout.add_widget(Label(text='Register your user'))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.camera)
        layout.add_widget(self.capture_button)
        layout.add_widget(register_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def capture_face(self, instance):
        texture = self.camera.texture
        if texture is None:
            print("No se pudo capturar la imagen: texture es None")
            return

        size = (int(texture.width), int(texture.height))
        pixels = texture.pixels

        if pixels is None:
            print("No se pudo capturar la imagen: pixels es Nones")
            return

        try:
            # Convert texture to PIL Image
            image = PILImage.frombytes(mode='RGBA', size=size, data=pixels)
            image = image.convert('RGB')  # Convert to RGB
        except Exception as e:
            print(f"Error al convertir datos de la cámara a imagen: {e}")
            return

        # Convert PIL Image to numpy array
        image_np = np.array(image)

        # Encode face
        face_encodings = face_recognition.face_encodings(image_np)
        if face_encodings:
            self.face_data = face_encodings[0].tobytes()  # Convert to bytes
            print("Face captured successfully")
        else:
            print("No face detected")

    def register(self, instance):
        username = self.username.text
        password = self.password.text
        if username and password and hasattr(self, 'face_data'):
            save_user(username, password, self.face_data)
            print("User registered successfully")
            self.manager.current = 'login'
        else:
            print("Username, password, and face capture are required")

    def go_to_login(self, instance):
        self.manager.current = 'login'
