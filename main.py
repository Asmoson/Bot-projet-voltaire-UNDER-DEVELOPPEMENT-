import pytesseract
from PIL import Image, ImageEnhance, ImageGrab
from pynput import mouse
import requests
from time import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
url = "https://api.languagetoolplus.com/v2/check"




def on_click(x, y, button, pressed):
    """Capture entre deux points"""
    if pressed and button == mouse.Button.left:
        coordinates.append((x, y))
        print(f"Clic en {x}, {y}")
        if len(coordinates) == 2:
            return False

def attendre(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        None
    else :
        return False
    
def removelines(value):
    return value.replace('\n',' ')

for i in range(30):
    print("\n")


mode = int(input("Quel mode ?\n1)Evaluation\n2)Entrainement\n==>"))



while(True):
    coordinates = []

    for i in range(10):
        print("\n")

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


        text = removelines(pytesseract.image_to_string(threshold_image, lang='eng+fra'))
        

        print("\nTexte détecté :")
        print("-----------------------------------")
        print(text)
        print("-----------------------------------\n\n========== FAUTE ? ==========\n")

    data = {
        "text": text,
        "language": "fr"
    }
    response = requests.post(url, data=data)
    corrections = response.json()
    for match in corrections['matches']:
        print(f"Suggestion : {match['replacements'][0]['value']}")

    print("=============================")

    for i in range(mode):
        with mouse.Listener(on_click=attendre) as listener:
            listener.join()


# A faire :
"""
tjr quelques bugs sur la reconnaissance : accents, homoglyphes, appostrophes, tirets
clics en plus quand pop up
pouvoir avoir un retour si l'exo est bon ou non ?
utiliser une API de recherche internet pour recuperer la correction directement sur projet voltaire ?  
"""