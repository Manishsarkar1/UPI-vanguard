from preprocess import preprocess
from sklearn.ensemble import IsolationForest
import joblib
import click

#step1: preprocess the data
X, _ = preprocess("../UPI-vanguard/data/upi_transactions.csv")

#step2: train the isolation forest model
model = IsolationForest(
    n_estimators = 100,
    contamination = 0.05,
    random_state = 42
)
model.fit(X)

#step3:save the mdoel
joblib.dump(model, "../UPI-vanguard/models/Fraud_model.pkl")
click.secho(f"[👌] Model trained and saved as 'Fraud_model.pkl'", fg = 'blue')