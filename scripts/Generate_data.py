import pandas as pd
import random
from datetime import datetime, timedelta
import os

#for generating fake UPI transactions
def generate_fake_UPI_transactions(n = 1000, save_directory = "../UPI-vanguard/data/upi_transactions.csv"):
    devices = ["Android", "IOS", "Windows", "MacOS"]
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]
    transactions_types = ["Send", "Receive", "Request"]
    status = ["Success", "Failed", "Pending"]

    data = []

    for i in range(n):
        # Generate a fake transaction
        # transaction_id is a string of 6 digits, timestamp is a random date in the past 100000 days,
        # sender_id and receiver_id are random integers between 1000 and 9999,
        # amount is a random float between 1.0 and 1000.0,
        # device is a random choice from the devices list, city is a random choice from the cities list,
        # transaction_type is a random choice from the transactions_types list,
        # status is a random choice from the status list

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
    #if not given the number of transactions, it will default to 1000
    #if not given the save directory, it will default to "../UPI-vanguard/data/upi_transactions.csv"
    #so you can call the function with just the number of transactions
    #or with both the number of transactions and the save directory
    generate_fake_UPI_transactions(n = 1000)
