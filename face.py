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
from database import get_users
from util import Alerts

class LoginCameraScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginCameraScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.alerts = Alerts()

        self.camera = Camera(play=True, resolution=(640, 480))
        self.capture_button = Button(text='Capture Face', on_release=self.capture_face)
        back_button = Button(text='Regresar', on_release=self.go_to_home)
        print("L O G I N  F A C E")
        layout.add_widget(Label(text='Login'))
        layout.add_widget(self.camera)
        layout.add_widget(self.capture_button)
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
            print("No se pudo capturar la imagen: pixels es None")
            return
        try:
            # Convert texture to PIL Image
            image = PILImage.frombytes(mode='RGBA', size=size, data=pixels)
            image = image.convert('RGB')  # Convert to RGB
        except Exception as e:
            print("Error al convertir datos de la camara a imagen: ", e)
            return

        # Convert PIL Image to numpy array
        image_np = np.array(image)

        # Encode face
        face_encodings = face_recognition.face_encodings(image_np)
        if face_encodings:
            self.face_data = face_encodings[0].tobytes()  # Convert to bytes
            print("Face captured successfully")
            user_data = get_users()
            if user_data:
                try:
                    for user in user_data:
                        stored_face_data = base64.b64decode(user)  # Cambiar a posición correcta
                        current_face_encoding = np.frombuffer(self.face_data, dtype=np.float64)
                        stored_face_encoding = np.frombuffer(stored_face_data, dtype=np.float64)

                        matches = face_recognition.compare_faces([stored_face_encoding], current_face_encoding)
                        if matches[0]:

                            self.alerts.show_message("Succefull", f"Bienvenido {user}")
                            break
                            # Aquí deberías cambiar a la pantalla de inicio o la pantalla deseada
                        else:
                            self.alerts.show_message("Aviso", "Rostro sin identificar")
                except Exception as e:
                    self.alerts.show_message("Error", "Error processing face data: ", e)
            else:
                self.alerts.show_message("Aviso", "Uusuario no registrado")
        else:
            self.alerts.show_message("Importante", "Rostro no detectado")
        


    def go_to_home(self, instance):
        self.manager.current = 'home'
