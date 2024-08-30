import pyautogui
import pytesseract
from PIL import Image
import numpy as np
import cv2
import re
import json
import keyboard
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load numbers dictionary from JSON file
with open('numbers_dict.json', 'r', encoding='utf-8') as f:
    numbers_dict = json.load(f)

# Invert the dictionary to map numbers to words
number_to_word = {v: k for k, v in numbers_dict.items()}

def process_images():
    x_number = 900
    y_number = 350
    width_number = 100
    height_number = 100

    # Capture the number
    screenshot_number = pyautogui.screenshot(region=(x_number, y_number, width_number, height_number))
    screenshot_number.save("number.png")

    x_words = 400
    y_words = 590
    width_words = 1100
    height_words = 100

    # Capture the words
    screenshot_words = pyautogui.screenshot(region=(x_words, y_words, width_words, height_words))
    screenshot_words.save("words.png")

    # Load the screenshots
    number_image = Image.open("number.png")
    words_image = Image.open("words.png")

    # Extract text from the number image
    number_text = pytesseract.image_to_string(number_image, config='--psm 6')
    print("Extracted Number:", number_text.strip())

    # Extract bounding boxes and text from the words image
    words_data = pytesseract.image_to_data(words_image, output_type=pytesseract.Output.DICT)


    # Clean the extracted number text
    cleaned_number_text = re.sub(r'[^0-9]', '', number_text.strip().lower())

    try:
        number_value = int(cleaned_number_text)
        if number_value in number_to_word:
            number_word = number_to_word[number_value]
            print(f"Matched Number Word: {number_word}")
        else:
            print("Number out of expected range.")
            number_word = None
    except ValueError:
        print("Extracted number is not a valid integer.")
        number_word = None

    if number_word:
        for i, word in enumerate(words_data['text']):
            if word.lower() == number_word:
                # Get the bounding box for the word
                x1, y1, x2, y2 = (words_data['left'][i], words_data['top'][i],
                                  words_data['left'][i] + words_data['width'][i],
                                  words_data['top'][i] + words_data['height'][i])
                
                # Center of the bounding box
                x_click = x_words + (x1 + x2) // 2
                y_click = y_words + (y1 + y2) // 2

                # Click on the correct word
                pyautogui.click(x=x_click, y=y_click)
                print(f"Clicked on {number_word} at ({x_click}, {y_click})")
                break
        else:
            print("Could not find the correct word to click.")
    else:
        print("Could not find a matching word to click.")

# Run the script continuously until "Escape" key is pressed
print("Press 'Escape' to stop.")
while True:
    if keyboard.is_pressed('esc'):
        print("Escape key pressed. Exiting...")
        break

    process_images()
    time.sleep(0.5)

print("Script has stopped.")
