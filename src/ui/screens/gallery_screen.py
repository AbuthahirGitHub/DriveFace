from kivy.uix.screenmanager import Screen
from kivymd.uix.grid import MDGridLayout
from src.utils.image_loader import ImageLoader
from src.face_recognition.detector import FaceDetector

class GalleryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_loader = ImageLoader()
        self.face_detector = FaceDetector()
        self.setup_ui()
    
    def setup_ui(self):
        self.grid = MDGridLayout(cols=3, adaptive_height=True)
        # Add UI components here 