from gpiozero import RGBLED, MotionSensor
from time import sleep
from picamzero import Camera
from datetime import datetime
import os

# Initialize RGB LED, PIR motion sensor and Camera using GPIO Zero library
led = RGBLED(red=18, green=27, blue=22)  # RGB LED connected to GPIO pins 18 (Red), 27 (Green), 22 (Blue)
pir = MotionSensor(17)  # PIR sensor connected to GPIO pin 17
camera = Camera()

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
    datetime_value = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    try:
        # Continuously monitor for motion, take a picture and update LED color
        while True:
            if pir.motion_detected:  # Check for motion detected by PIR sensor
                led.color = (1, 0, 0)  # Set LED color to red (only Red)
                camera.take_photo(f"{folder}/image_{photo_count}_{datetime_value}.jpg") # Take a photo
                print("New photo has been taken")
                photo_count += 1
            else:
                led.color = (0, 0, 1)  # Set LED color to blue (only Blue)
            sleep(0.1)  # Short delay to reduce CPU load

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) to exit the loop gracefully
        led.off()
        print("Done")

motion_control()