import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import credentials, db

#IR GPIO
IR_SENSOR_PIN = 17

#Firebase 
cred = credentials.Certificate('path_to_your_service_account_key.json')  # Replace with the path to your Firebase JSON file
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-name.firebaseio.com/'  # Replace with your Firebase Realtime Database URL
})
ref = db.reference('ParkingSlot')

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

def check_parking_slot():
    if GPIO.input(IR_SENSOR_PIN) == GPIO.LOW:  # LOW means sensor is triggered, i.e., slot is occupied
        return "Occupied"
    else:
        return "Available"

def update_firebase(slot_status):
    ref.set({
        'status': slot_status
    })
    print(f"Data sent to Firebase: {slot_status}")

def main():
    setup()
    try:
        while True:
            slot_status = check_parking_slot()
            print(f"Parking Slot Status: {slot_status}")
            update_firebase(slot_status)
            time.sleep(10) 
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
