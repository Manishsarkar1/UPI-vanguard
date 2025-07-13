import csv, random, time
from datetime import datetime

def generate_transaction():
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender_id": random.randint(1000, 9999),
        "receiver_id": random.randint(1000, 9999),
        "amount": round(random.uniform(10, 100000), 2),
        "device": random.choice([0, 1, 2]),
        "location": random.choice([0, 1, 2, 3, 4, 5]),
        "transaction_type": random.randint(0, 2),
        "status": random.choice([0, 1])  # fail/success
    }

# Continuous write
with open("data/upi_transactions.csv", "a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "timestamp", "sender_id", "receiver_id", "amount",
        "device", "location", "transaction_type", "status"
    ])
    while True:
        txn = generate_transaction()
        writer.writerow(txn)
        print("✅ Generated:", txn)
        time.sleep(2)  # new txn every 2 sec
