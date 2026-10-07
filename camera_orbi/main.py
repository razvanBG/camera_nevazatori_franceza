import cv2
import numpy as np
import os
from gtts import gTTS
import time
from google import genai
from PIL import Image

GEMINI_API_KEY = "AIzaSyC3axp-3h2Vj3nBeLOag4Bc_eQSZNRddn0"
client = genai.Client(api_key=GEMINI_API_KEY)

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        return image_path
    return None
def read_prompt():
    with open("input.txt", "r") as file:
        prompt = file.read()
    return prompt
def describe_image(image_path):
    try:
        prompt = read_prompt()
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()
        image = Image.open(image_path)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[image, prompt]
        )
        return response.text if response else "I couldn't understand the image."
    except Exception as e:
        return f"Error: {str(e)}"

def speak_text(text):
    tts = gTTS(text=text, lang="fr")
    tts.save("output.mp3")
    os.system("start output.mp3") 

if __name__ == "__main__":
    while True:
        print("Capturing image...")
        image_path = capture_image()
        if image_path:
            print("Describing image...")
            description = describe_image(image_path)
            print("Description:", description)
            
            print("Speaking description...")
            speak_text(description)
            
            time.sleep(20)
            