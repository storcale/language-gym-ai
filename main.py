import pyautogui
import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Example values for the number in the middle (adjust based on your screen)
x_number = 900  # X coordinate for the number
y_number = 350  # Y coordinate for the number
width_number = 100  # Width of the box around the number
height_number = 100  # Height of the box around the number

# Capture the number
screenshot_number = pyautogui.screenshot(region=(x_number, y_number, width_number, height_number))
screenshot_number.save("number.png")

# Example values for the words (all the white signs with letters)
x_words = 400  # X coordinate for the words region
y_words = 590  # Y coordinate for the words region
width_words = 1100  # Width to cover all the white signs
height_words = 100  # Height to cover the white signs

# Capture the words
screenshot_words = pyautogui.screenshot(region=(x_words, y_words, width_words, height_words))
screenshot_words.save("words.png")

# Load the screenshots
number_image = Image.open("number.png")
words_image = Image.open("words.png")

# Extract text from the number image
number_text = pytesseract.image_to_string(number_image, config='--psm 6')
print("Extracted Number:", number_text.strip())

# Extract text from the words image
words_text = pytesseract.image_to_string(words_image, config='--psm 6')
print("Extracted Words:", words_text.strip())

# Step 1: Clean the OCR Output
cleaned_number_text = re.sub(r'[^a-zA-Z]', '', number_text.strip().lower())
cleaned_words_text = re.sub(r'[^a-zA-Z\s]', '', words_text.strip().lower())

print("Cleaned Number:", cleaned_number_text)
print("Cleaned Words:", cleaned_words_text)

# Step 2: Match the Extracted Number to the Correct Word
# Define a dictionary for number words in Spanish
numbers_dict = {
    "uno": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "once": 11,
    "doce": 12,
    "trece": 13,
    "catorce": 14,
    "quince": 15,
    "dieciseis": 16,
    "diecisiete": 17,
    "dieciocho": 18,
    "diecinueve": 19,
    "veinte": 20,
}

# Check if the extracted number matches a number in Spanish
if cleaned_number_text in numbers_dict:
    number_value = numbers_dict[cleaned_number_text]
    print(f"Matched Number: {number_value}")
else:
    print("Number not recognized.")
    number_value = None

# Step 3: Identify the Correct Word Location and Click
if number_value is not None:
    for word in numbers_dict:
        if word in cleaned_words_text:
            word_position = cleaned_words_text.index(word)
            print(f"Found {word} at position {word_position}")
            
            # Assuming the words are laid out evenly, calculate the x position
            x_start = x_words
            x_spacing = 275  # Estimated width of each box
            word_index = cleaned_words_text.split().index(word)

            # Calculate the x position for the correct word
            x_click = x_start + word_index * x_spacing
            y_click = y_words + height_words // 2  # Vertical center of the word box

            # Click on the correct word
            pyautogui.click(x=x_click, y=y_click)
            print(f"Clicked on {word} at ({x_click}, {y_click})")
            break
    else:
        print("Correct word not found in extracted words.")
else:
    print("Could not find a matching word to click.")
