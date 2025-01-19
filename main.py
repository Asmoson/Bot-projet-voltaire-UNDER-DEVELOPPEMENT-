import pytesseract
from PIL import Image, ImageEnhance, ImageGrab
from pynput import mouse

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

coordinates = []

def on_click(x, y, button, pressed):
    """Capture entre deux points"""
    if pressed and button == mouse.Button.left:
        coordinates.append((x, y))
        print(f"Clic en {x}, {y}")
        if len(coordinates) == 2:
            return False

print("Clique sur les coins de la zone a convertir")

with mouse.Listener(on_click=on_click) as listener:
    listener.join()

if len(coordinates) == 2:
    x1, y1 = coordinates[0]
    x2, y2 = coordinates[1]
    bbox = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

    screenshot = ImageGrab.grab(bbox)

    gray_image = screenshot.convert("L")


    enhancer = ImageEnhance.Contrast(gray_image)
    high_contrast_image = enhancer.enhance(2)

    threshold_image = high_contrast_image.point(lambda x: 0 if x < 128 else 255, "1")


    text = pytesseract.image_to_string(threshold_image, lang='eng+fra')
    print("Texte détecté :")
    print("-----------------------------------")
    print(text)
    print("-----------------------------------")
