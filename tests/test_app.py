import unittest
import os
import shutil
from pathlib import Path
from src.database.db_manager import DatabaseManager
from src.utils.image_loader import ImageLoader
from src.face_recognition.detector import FaceDetector
from src.face_recognition.recognizer import FaceRecognizer
from src.config.test_config import *

class TestDriveFace(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.db = DatabaseManager()
        self.image_loader = ImageLoader()
        self.face_detector = FaceDetector()
        self.face_recognizer = FaceRecognizer()
        
        # Copy test image to test directory
        if os.path.exists("1739665049339.jpg"):
            shutil.copy("1739665049339.jpg", TEST_IMAGE_DIR)
    
    def tearDown(self):
        # Clean up test data
        if os.path.exists(TEST_IMAGE_DIR):
            shutil.rmtree(TEST_IMAGE_DIR)
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
    
    def test_image_loading(self):
        """Test if images can be loaded correctly"""
        images = self.image_loader.load_images(TEST_IMAGE_DIR)
        self.assertTrue(len(images) > 0)
    
    def test_face_detection(self):
        """Test if faces can be detected in images"""
        test_image = Path(TEST_IMAGE_DIR) / "1739665049339.jpg"
        if test_image.exists():
            faces = self.face_detector.detect_faces(str(test_image))
            self.assertIsNotNone(faces)
    
    def test_database(self):
        """Test if database operations work"""
        # Test creating tables
        self.assertTrue(os.path.exists(self.db.db_path))
        
        # Test inserting an image
        cursor = self.db.conn.cursor()
        cursor.execute("INSERT INTO images (path) VALUES (?)", 
                      (str(Path(TEST_IMAGE_DIR) / "1739665049339.jpg"),))
        self.db.conn.commit()
        
        # Verify insertion
        cursor.execute("SELECT COUNT(*) FROM images")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

if __name__ == '__main__':
    unittest.main() 