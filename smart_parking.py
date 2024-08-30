import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import credentials, db

IR_SENSOR_PIN = 17

#Firebase 
cred = credentials.Certificate('smart-parking-89960-firebase-adminsdk-lwro9-5aa0cde6c1.json') 
firebase_admin.initialize_app(cred, {
    'databaseURL': 'smart-parking-89960-default-rtdb.firebaseio.com/' 
})
ref = db.reference('ParkingSlot')

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

def check_parking_slot():
    if GPIO.input(IR_SENSOR_PIN) == GPIO.LOW:  
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
