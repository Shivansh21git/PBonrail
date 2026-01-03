import requests
import time
import random
import json

# Your API endpoint
API_URL = "https://ar.bhoomitra.space/api/push/"      # CHANGE IF NEEDED

DEVICE_ID = "TU-1"   # Change to your real device_id


def generate_random_data():
    return {
        "device_id": DEVICE_ID,
        "nitrogen": round(random.uniform(60, 250), 1),
        "phosphorus": round(random.uniform(60, 250), 1),
        "potassium": round(random.uniform(60, 250), 1),
        "temperature": round(random.uniform(20, 45), 1),
        "humidity": round(random.uniform(40, 80), 1)
    }


def send_demo_data():
    while True:
        data = generate_random_data()
        print("Sending:", data)

        try:
            res = requests.post(API_URL, json=data)
            print("Response:", res.status_code, res.text)
        except Exception as e:
            print("Error:", e)

        time.sleep(25)   # send every 3 seconds


if __name__ == "__main__":
    send_demo_data()
