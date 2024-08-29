import RPi.GPIO as GPIO
import time
import requests

IR_SENSOR_PIN = 17

THINGSPEAK_API_KEY = '7ZCL1JMVZWHXRIF8'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

def check_parking_slot():
    if GPIO.input(IR_SENSOR_PIN) == GPIO.LOW:  
        return "Occupied"
    else:
        return "Available"

def update_thingspeak(slot_status):
    payload = {'api_key': THINGSPEAK_API_KEY, 'field1': slot_status}
    try:
        response = requests.get(THINGSPEAK_URL, params=payload)
        if response.status_code == 200:
            print(f"Data sent to ThingSpeak: {slot_status}")
        else:
            print(f"Failed to send data to ThingSpeak, status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    setup()
    try:
        while True:
            slot_status = check_parking_slot()
            print(f"Parking Slot Status: {slot_status}")
            update_thingspeak(1 if slot_status == "Occupied" else 0)
            time.sleep(15)
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
