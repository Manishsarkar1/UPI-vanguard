import pandas as pd
import joblib
from preprocess import preprocess
import click

#step1: Load model
model = joblib.load("../UPI-vanguard/models/Fraud_model.pkl")

#step2: Load and preprocess the data
X, _ = preprocess("../UPI-vanguard/data/upi_transactions.csv")

#step3: Predict fraud (anomalies)
predictions = model.predict(X) # -1 is anomaly, 1 is normal

#step4: Add prediction result to the dataframe
X['is_fraud'] = predictions
X['id_fraud'] = X['is_fraud'].apply(lambda x: True if x == -1 else False)

#step5: show some results
click.secho(f"Sample Transactions flagged as fraud:", fg='red')
click.secho(X[X['is_fraud'] == -1].head(10).to_string(index=False), fg='red')