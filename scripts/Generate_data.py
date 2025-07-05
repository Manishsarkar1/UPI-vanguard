import pandas as pd
import random
from datetime import datetime, timedelta
import os

#for generating fake UPI transactions
def generate_fake_UPI_transactions(n = 1000, save_directory = "../data/upi_transactions.csv"):
    devices = ["Android", "IOS", "Windows", "MacOS"]
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]
    transactions_types = ["Send", "Receive", "Request"]
    status = ["Success", "Failed", "Pending"]

    data = []

    for i in range(n):
        trn = {
            "transaction_id": f"T{i:06d}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 100000))).strftime("%Y-%m-%d %H:%M:%S"),
            "sender_id": random.randint(1000, 9999),
            "receiver_id": random.randint(1000, 9999),
            "amount": round(random.uniform(1.0, 1000.0), 2),
            "device": random.choice(devices),
            "city": random.choice(cities),
            "transaction_type": random.choice(transactions_types),
            "status": random.choice(status)
        }
        # Now to avoid getting transactions as sender = receiver
        while trn["sender_id"] == trn["receiver_id"]:
            trn["receiver_id"] = random.randint(1000, 9999)
        data.append(trn)

    df = pd.DataFrame(data)

    # here we have to make sure that the directory exists
    os.makedirs(os.path.dirname(save_directory), exist_ok=True)

    df.to_csv(save_directory, index=False)
    print(f"Generated {n} fake UPI transactions and saved to {save_directory}")


if __name__ == "__main__":
    #Generate 1000 fake UPI transactions
    generate_fake_UPI_transactions(n = 1000)