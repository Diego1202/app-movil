import os
import shutil
import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from util import Alerts

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.alerts = Alerts()
        self.username = []
        self.ror_actual = ''
        self.welcome_label = Label(
            font_size='24sp',  # Tamaño de fuente
            color=(0, 0, 0, 1),  # Color negro (r, g, b, a)
            size_hint_y=None,  # No ajustar automáticamente la altura
            height=50,  # Altura de la etiqueta
            valign='top',  # Alineación vertical
        )
        layout.add_widget(self.welcome_label)

        # Tabla de datos usando MDDataTable
        self.data_tables = MDDataTable(
            size_hint=(1, 0.6),
            check=True,
            column_data=[
                ("ID", dp(20)),  # Asegúrate de que la primera columna es el ID
                ("File Path", dp(60)),
                ("Actions", dp(20))
            ],
            row_data=[],
        )
        self.data_tables.bind(on_check_press=self.on_check_press)
        layout.add_widget(self.data_tables)


        # Botón de eliminar
        self.delete_button = Button(
            text='Delete',
            size_hint=(1, 0.2),
            on_release=self.delete_selected_files
        )
        self.delete_button.opacity = 0
        self.delete_button.disabled = True
        layout.add_widget(self.delete_button)

        # Botón para abrir el explorador de archivos
        select_file_button = Button(text='Select File', size_hint=(1, 0.2), on_release=self.open_file_chooser)
        layout.add_widget(select_file_button)

        self.add_widget(layout)

    def on_start(self):
        self.data_tables.open()

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
            self.alerts.show_message("Error", "No file selected.")

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
        self.alerts.show_message("File Uploaded", f"The file has been uploaded to: {destination}")
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
        cursor.execute('SELECT id, file_path FROM files WHERE username=?', (self.username,))
        files = cursor.fetchall()
        conn.close()

        # Extraer los IDs y las rutas de archivo
        file_ids = [file[0] for file in files]
        file_paths = [file[1] for file in files]

        # Actualizar la vista de archivos
        self.data_tables.row_data = [(identi, file_path, "Delete") for identi, file_path in zip(file_ids, file_paths)]
        
        # Si no hay archivos, mostrar un mensaje
        if not file_paths:
            self.alerts.show_message("No Files", "No files have been uploaded by this user.")
    
    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        # Si hay filas seleccionadas, mostrar el botón de eliminar
        if current_row:
            self.ror_actual = current_row
            self.delete_button.opacity = 1
            self.delete_button.disabled = False
        else:
            self.delete_button.opacity = 0
            self.delete_button.disabled = True


    def delete_selected_files(self, instance):

        if self.ror_actual:
            file_id = self.ror_actual[0]
            file_path = self.ror_actual[1]

            # # Eliminar el archivo del sistema de archivos
            if os.path.exists(file_path):
                os.remove(file_path)

            # # Eliminar el archivo de la base de datos
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM files WHERE id=?', (file_id,))
            conn.commit()
            conn.close()

        # Volver a cargar los archivos del usuario
        self.load_user_files()

        # # Ocultar el botón de eliminar después de eliminar los archivos
        self.delete_button.opacity = 0
        self.delete_button.disabled = True

        self.alerts.show_message("Files Deleted", "The selected files have been deleted.")