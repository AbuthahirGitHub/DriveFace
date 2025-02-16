from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList
from src.face_recognition.recognizer import FaceRecognizer

class FacesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.face_recognizer = FaceRecognizer()
        self.setup_ui()
    
    def setup_ui(self):
        self.face_list = MDList()
        # Add UI components here 