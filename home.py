import os
import shutil
import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

class FileEntry(RecycleDataViewBehavior, BoxLayout):
    """Clase para mostrar la entrada de archivo en la tabla."""
    
    def __init__(self, delete_callback, **kwargs):
        super(FileEntry, self).__init__(**kwargs)

        # Layout para la entrada de archivo
        layout = BoxLayout(size_hint_y=None, height=40)

        # Etiqueta para mostrar la ruta del archivo
        self.file_label = Label(size_hint_x=0.8)
        layout.add_widget(self.file_label)

        # Botón para eliminar el archivo
        delete_button = Button(text='Delete', size_hint_x=0.2)
        delete_button.bind(on_release=self.delete_file)
        layout.add_widget(delete_button)

        self.add_widget(layout)

        self.delete_callback = delete_callback  # Callback para eliminar archivos

    def delete_file(self, instance):
        file_path = self.file_label.text  # Obtener la ruta del archivo desde la etiqueta
        self.delete_callback(file_path)  # Llamar al callback para eliminar el archivo

class FileListView(RecycleView):
    """Clase que representa la lista de archivos subidos."""
    def __init__(self, delete_callback, **kwargs):
        super(FileListView, self).__init__(**kwargs)
        self.data = []
        self.viewclass = FileEntry  # Establece la clase que se usará para las entradas
        self.delete_callback = delete_callback  # Callback para eliminar archivos

    def update_files(self, files):
        self.data = [{'file_label': file} for file in files]  # Actualiza los datos para mostrar la ruta del archivo
        self.refresh_from_data()  # Refresca la vista para mostrar los nuevos datos

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.username = ''
        self.welcome_label = Label()
        layout.add_widget(self.welcome_label)

        # Botón para abrir el explorador de archivos
        select_file_button = Button(text='Select File', on_release=self.open_file_chooser)
        layout.add_widget(select_file_button)

        # RecycleView para mostrar los archivos
        self.file_list_view = FileListView(delete_callback=self.delete_file)
        layout.add_widget(self.file_list_view)

        self.add_widget(layout)

    def set_username(self, username):
        self.welcome_label.text = f"Welcome, {username}!"
        self.username = username 
        self.load_user_files()  # Cargar archivos del usuario al iniciar

    def open_file_chooser(self, instance):
        # Crear un layout para el FileChooser y el botón
        layout = BoxLayout(orientation='vertical')

        # Obtener la ruta del directorio del usuario
        user_home = os.path.expanduser("~")

        # Crear el FileChooser y establecer el directorio inicial al directorio del usuario
        file_chooser = FileChooserListView(path=user_home)
        layout.add_widget(file_chooser)

        # Botón para seleccionar el archivo
        select_button = Button(text='Select', size_hint_y=None, height=50)
        select_button.bind(on_release=lambda *args: self.load_file(file_chooser))

        layout.add_widget(select_button)

        # Crear el Popup con el layout
        self.popup = Popup(title="Select a file", content=layout, size_hint=(0.9, 0.9))
        self.popup.open()

    def load_file(self, file_chooser):
        selected = file_chooser.selection
        if selected:
            selected_file = selected[0]
            self.store_file(selected_file)
        else:
            self.show_popup("Error", "No file selected.")

    def store_file(self, selected_file):
        # Crear la ruta de la carpeta del usuario
        user_folder = os.path.join("upload", self.username)
        os.makedirs(user_folder, exist_ok=True)  # Crear la carpeta si no existe

        # Obtener el nombre del archivo
        file_name = os.path.basename(selected_file)

        # Crear la ruta completa donde se almacenará el archivo
        destination = os.path.join(user_folder, file_name)

        # Copiar el archivo a la carpeta del usuario
        shutil.copy(selected_file, destination)

        # Almacenar el archivo en la base de datos
        self.save_file_to_db(destination)

        # Actualizar la lista de archivos
        self.load_user_files()  # Actualiza los archivos del usuario después de almacenar el nuevo archivo

        # Mostrar un mensaje y cerrar el popup
        self.show_popup("File Uploaded", f"The file has been uploaded to: {destination}")
        self.popup.dismiss()

    def save_file_to_db(self, file_path):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO files (username, file_path) VALUES (?, ?)", (self.username, file_path))
        conn.commit()
        conn.close()

    def load_user_files(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT file_path FROM files WHERE username=?', (self.username,))
        files = cursor.fetchall()
        conn.close()

        # Extraer solo las rutas de archivo
        file_paths = [file[0] for file in files]

        # Actualizar la vista de archivos
        self.file_list_view.update_files(file_paths)

        # Si no hay archivos, mostrar un mensaje
        if not file_paths:
            self.show_popup("No Files", "No files have been uploaded by this user.")

    def delete_file(self, file_path):
        # Eliminar el archivo del sistema de archivos
        if os.path.exists(file_path):
            os.remove(file_path)

        # Eliminar el archivo de la base de datos
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM files WHERE file_path=?', (file_path,))
        conn.commit()
        conn.close()

        # Volver a cargar los archivos del usuario
        self.load_user_files()

        self.show_popup("File Deleted", f"The file has been deleted: {file_path}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()
