import json
import os
from datetime import datetime

class ParkingLot:
    def __init__(self, total_slots=5, file_name="parking_data.json"):
        self.total_slots = total_slots
        self.file_name = file_name
        self.slots = {}  # slot_no : {"car": str, "time": str}
        self.income = 0
        self.load_data()

    def park_car(self, car_number):
        if len(self.slots) >= self.total_slots:
            print("❌ Parking Full!")
            return

        # find nearest available slot
        for slot in range(1, self.total_slots + 1):
            if str(slot) not in self.slots:
                self.slots[str(slot)] = {
                    "car": car_number,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                print(f"✅ Car {car_number} parked at Slot {slot}")
                self.save_data()
                return

    def leave_car(self, car_number, fee=50):
        for slot, details in list(self.slots.items()):
            if details["car"] == car_number:
                print(f"🚗 Car {car_number} leaving Slot {slot}")
                self.income += fee
                del self.slots[slot]
                self.save_data()
                return
        print("❌ Car not found in parking!")

    def status(self):
        print("\n📊 Parking Status:")
        if not self.slots:
            print("All slots are free.")
        for slot, details in self.slots.items():
            print(f"Slot {slot} → Car {details['car']} (since {details['time']})")
        print(f"💰 Total Income: ${self.income}")

    def save_data(self):
        data = {"slots": self.slots, "income": self.income}
        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                data = json.load(f)
                self.slots = data.get("slots", {})
                self.income = data.get("income", 0)


# ---------------- DEMO -----------------
if __name__ == "__main__":
    lot = ParkingLot(total_slots=3)

    lot.park_car("GJ01AB1234")
    lot.park_car("MH12XY9999")
    lot.park_car("DL07PQ5555")
    lot.park_car("UP11CC8888")  # should show Full

    lot.status()

    lot.leave_car("MH12XY9999")
    lot.status()
