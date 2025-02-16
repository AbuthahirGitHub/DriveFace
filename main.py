from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
import cv2
import face_recognition
import os
from ftplib import FTP
from datetime import datetime
import tempfile

class FTPManager:
    def __init__(self, host, user, passwd):
        self.ftp = FTP(host)
        self.ftp.login(user=user, passwd=passwd)
        
    def list_images(self, directory='.'):
        """List all images in the FTP directory"""
        image_files = []
        for fname in self.ftp.nlst(directory):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_files.append(fname)
        return image_files
    
    def download_image(self, remote_path):
        """Download image to temp directory and return local path"""
        local_path = os.path.join(tempfile.gettempdir(), os.path.basename(remote_path))
        with open(local_path, 'wb') as f:
            self.ftp.retrbinary(f'RETR {remote_path}', f.write)
        return local_path

class GalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Add toolbar
        self.toolbar = MDTopAppBar(
            title="DriveFace Gallery",
            elevation=10,
            right_action_items=[
                ["refresh", lambda x: self.refresh_gallery()],
                ["server", lambda x: self.show_ftp_dialog()]
            ]
        )
        self.layout.add_widget(self.toolbar)
        
        # Add gallery list
        self.gallery_list = MDList()
        self.layout.add_widget(self.gallery_list)
        
        self.add_widget(self.layout)
        
        # FTP Dialog
        self.ftp_dialog = None
        self.ftp_manager = None
        
    def show_ftp_dialog(self):
        if not self.ftp_dialog:
            self.ftp_dialog = MDDialog(
                title="FTP Connection",
                type="custom",
                content_cls=BoxLayout(
                    orientation="vertical",
                    children=[
                        MDTextField(
                            hint_text="Host",
                            id="host"
                        ),
                        MDTextField(
                            hint_text="Username",
                            id="username"
                        ),
                        MDTextField(
                            hint_text="Password",
                            id="password",
                            password=True
                        )
                    ]
                ),
                buttons=[
                    MDRaisedButton(
                        text="CONNECT",
                        on_release=self.connect_ftp
                    )
                ]
            )
        self.ftp_dialog.open()
        
    def connect_ftp(self, *args):
        content = self.ftp_dialog.content_cls
        host = content.children[2].text
        user = content.children[1].text
        passwd = content.children[0].text
        
        try:
            self.ftp_manager = FTPManager(host, user, passwd)
            self.refresh_gallery()
            self.ftp_dialog.dismiss()
        except Exception as e:
            MDDialog(
                title="Error",
                text=f"Failed to connect: {str(e)}"
            ).open()
        
    def refresh_gallery(self):
        self.gallery_list.clear_widgets()
        if self.ftp_manager:
            for image in self.ftp_manager.list_images():
                self.gallery_list.add_widget(
                    OneLineListItem(
                        text=image,
                        on_release=lambda x, path=image: self.process_image(path)
                    )
                )
                
    def process_image(self, remote_path):
        if self.ftp_manager:
            local_path = self.ftp_manager.download_image(remote_path)
            # Process image for face detection here
            image = face_recognition.load_image_file(local_path)
            face_locations = face_recognition.face_locations(image)
            
            # Show results dialog
            MDDialog(
                title="Face Detection Results",
                text=f"Found {len(face_locations)} faces in {remote_path}"
            ).open()
            
            # Clean up temp file
            os.remove(local_path)

class FacesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Add toolbar
        self.toolbar = MDTopAppBar(
            title="Detected Faces",
            elevation=10
        )
        self.layout.add_widget(self.toolbar)
        
        # Add faces list
        self.faces_list = MDList()
        self.layout.add_widget(self.faces_list)
        
        self.add_widget(self.layout)

class DriveFaceApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        
        # Create screen manager
        self.sm = ScreenManager()
        
        # Add screens
        self.gallery_screen = GalleryScreen(name='gallery')
        self.faces_screen = FacesScreen(name='faces')
        
        self.sm.add_widget(self.gallery_screen)
        self.sm.add_widget(self.faces_screen)
        
        return self.sm
    
    def on_start(self):
        # Initialize database
        self.init_database()
        
    def init_database(self):
        conn = sqlite3.connect('driverface.db')
        c = conn.cursor()
        
        # Create tables if they don't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS faces
            (id INTEGER PRIMARY KEY,
             name TEXT,
             embedding BLOB,
             created_date TEXT)
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS photos
            (id INTEGER PRIMARY KEY,
             path TEXT,
             scan_date TEXT,
             faces_detected INTEGER)
        ''')
        
        conn.commit()
        conn.close()

if __name__ == '__main__':
    DriveFaceApp().run() 