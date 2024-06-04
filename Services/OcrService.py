import time
import requests
from PIL import Image
from io import BytesIO
import pytesseract


class ocrService:
    def __init__(self, urlImage):
        self.urlImage = urlImage

    def getText(self):
        response = requests.get(self.urlImage)
        image = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(image)
        return text