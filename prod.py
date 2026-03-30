import requests
import time
import random

# BASE_URL = "https://ar.bhoomitra.space"
BASE_URL = "http://localhost:8000"

DEVICE_ID = "TU-1"

SYNC_URL = f"{BASE_URL}/api/device-sync/"
PUSH_URL = f"{BASE_URL}/api/push/"


def generate_random_data():
    return {
        "device_id": DEVICE_ID,
        "nitrogen": round(random.uniform(10, 200), 1),
        "phosphorus": round(random.uniform(10, 200), 1),
        "potassium": round(random.uniform(10, 200), 1),
        "temperature": round(random.uniform(20, 45), 1),
        "humidity": round(random.uniform(0, 80), 1)
    }


def device_sync():
    """Heartbeat + get sampling flag"""
    try:
        res = requests.post(SYNC_URL, json={"device_id": DEVICE_ID}, timeout=5)

        if res.status_code == 200:
            data = res.json()
            return data.get("sampling", False)

        print("Sync failed:", res.status_code)
        return False

    except Exception as e:
        print("Sync error:", e)
        return False


def send_data():
    """Send sensor data"""
    data = generate_random_data()
    print("📤 Sending data:", data)

    try:
        res = requests.post(PUSH_URL, json=data, timeout=5)
        print("Response:", res.status_code, res.text)
    except Exception as e:
        print("Push error:", e)


def run_device():
    sampling = False

    while True:
        # 🔁 Step 1: sync with server (heartbeat + config)
        sampling = device_sync()
        print("🧠 Sampling allowed:", sampling)

        # 📤 Step 2: send data only if allowed
        if sampling:
            send_data()
        else:
            print("⏸️ Sampling OFF — not sending data")

        # ⏱️ wait
        time.sleep(5)


if __name__ == "__main__":
    run_device()