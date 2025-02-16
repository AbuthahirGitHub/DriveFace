import face_recognition
import numpy as np

class FaceRecognizer:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
    
    def add_face(self, face_image, name):
        encoding = face_recognition.face_encodings(face_image)[0]
        self.known_face_encodings.append(encoding)
        self.known_face_names.append(name)
    
    def recognize_face(self, face_image):
        encoding = face_recognition.face_encodings(face_image)[0]
        matches = face_recognition.compare_faces(self.known_face_encodings, encoding)
        
        if True in matches:
            index = matches.index(True)
            return self.known_face_names[index]
        return None 