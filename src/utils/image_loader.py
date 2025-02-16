from PIL import Image
from pathlib import Path
import os

class ImageLoader:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png'}
        
    def load_images(self, directory):
        images = []
        for root, _, files in os.walk(directory):
            for file in files:
                if Path(file).suffix.lower() in self.supported_formats:
                    images.append(Path(root) / file)
        return images
    
    def create_thumbnail(self, image_path, size=(200, 200)):
        with Image.open(image_path) as img:
            img.thumbnail(size)
            thumbnail_path = Path('thumbnails') / image_path.name
            thumbnail_path.parent.mkdir(exist_ok=True)
            img.save(thumbnail_path)
            return thumbnail_path 