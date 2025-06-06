from gpiozero import RGBLED, MotionSensor
from time import sleep
from picamzero import Camera
from datetime import datetime
from dotenv import load_dotenv
import os
import yagmail

# Initialize RGB LED, PIR motion sensor and Camera using GPIO Zero library
led = RGBLED(red=18, green=27, blue=22)  # RGB LED connected to GPIO pins 18 (Red), 27 (Green), 22 (Blue)
pir = MotionSensor(17)  # PIR sensor connected to GPIO pin 17
camera = Camera()

def email_auth():
    load_dotenv()
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    return email, password

def photo_folder():
    # Path to folder for saving photos
    photo_folder = "/home/haggard/Desktop/PIR_photos"

    # Check if photo folder exists
    if not os.path.exists(photo_folder):
        os.mkdir(photo_folder)
        
    return photo_folder

def motion_control():
    photo_count = 1
    folder = photo_folder()
    email, password = email_auth()
    yag_mail = yagmail.SMTP(email, password)
    try:
        # Continuously monitor for motion, take a picture and update LED color
        while True:
            if pir.motion_detected:  # Check for motion detected by PIR sensor
                led.color = (1, 0, 0)  # Set LED color to red (only Red)
                
                datetime_value = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                filename = f"image_{photo_count}_{datetime_value}.jpg"
                filepath = f"{folder}/{filename}"
                
                camera.take_photo(filepath) # Take a photo
                print("New photo has been taken")
                photo_count += 1
                yag_mail.send( # Send email with captured photo
                    to=email, 
                    subject="Motion Detection Alert!", 
                    contents="Motion was detected. Check attached image.",
                    attachments=filepath
                )
            else:
                led.color = (0, 0, 1)  # Set LED color to blue (only Blue)
            sleep(0.1)  # Short delay to reduce CPU load

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) to exit the loop gracefully
        led.off()
        print("Done")

motion_control()