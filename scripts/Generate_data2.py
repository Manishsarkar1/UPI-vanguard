import csv, random, time
from datetime import datetime

# Lists of readable values
devices = ["Android", "MacOS", "IOS"]
cities = ["Mumbai", "Delhi", "Chennai", "Bangalore", "Kolkata"]
txn_types = ["Send", "Receive", "Request"]
statuses = ["Success", "Failed", "Pending"]

# Field names for CSV
fieldnames = [
    "transaction_id", "timestamp", "sender_id", "receiver_id", "amount",
    "device", "city", "transaction_type", "status"
]

# Set starting ID
start_id = 0

# Make sure CSV has headers
try:
    with open("data/upi_transactions.csv", "x", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
except FileExistsError:
    # File exists already, get the next txn ID
    with open("data/upi_transactions.csv", "r") as f:
        lines = f.readlines()
        start_id = len(lines) - 1  # subtract header

# Start appending transactions live
with open("data/upi_transactions.csv", "a", newline="", buffering=1) as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    txn_id_counter = start_id
    while True:
        txn = {
            "transaction_id": f"T{txn_id_counter:06d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender_id": random.randint(1000, 9999),
            "receiver_id": random.randint(1000, 9999),
            "amount": round(random.uniform(50, 10000), 2),
            "device": random.choice(devices),
            "city": random.choice(cities),
            "transaction_type": random.choice(txn_types),
            "status": random.choice(statuses),
        }

        writer.writerow(txn)
        file.flush()  # 🚨 Ensures it's written to disk instantly
        print("✅ Generated:", txn)

        txn_id_counter += 1
        time.sleep(2)  # wait 2 seconds for next transaction
