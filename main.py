# main.py
import streamlit as st
import pandas as pd
import joblib
from scripts.preprocess import preprocess

st.set_page_config(page_title="UPI Guardian", layout="wide")

st.title("🛡️ UPI Guardian – Live Fraud Detection Dashboard")
st.markdown("This assistant monitors live UPI transactions and flags suspicious activity in real-time.")

# Load model
model = joblib.load("models/Fraud_model.pkl")

# Refresh block
placeholder = st.empty()

with placeholder.container():
    # Read raw data
    df_raw = pd.read_csv("data/upi_transactions.csv")
    latest_txn_raw = df_raw.tail(1)

    st.subheader("🧾 Recent Transactions")
    st.dataframe(df_raw.tail(5), use_container_width=True)

    # Preprocess for model
    df_encoded, _ = preprocess("data/upi_transactions.csv")
    txn = df_encoded.tail(1)
    cols_to_use = [col for col in txn.columns if col not in ["transaction_id", "timestamp", "is_fraud"]]
    prediction = model.predict(txn[cols_to_use])
    is_fraud = prediction[0] == -1

    # Show transaction
    st.subheader("🔍 Live Transaction Under Review")
    st.table(latest_txn_raw)

    # Prediction result
    if is_fraud:
        st.error("🚨 Suspicious Activity Detected!")
    else:
        st.success("✅ Transaction looks safe.")

    # Assistant reasoning
    reasons = []
    amount = latest_txn_raw["amount"].values[0]
    device = latest_txn_raw["device"].values[0]
    city = latest_txn_raw["city"].values[0]
    status = latest_txn_raw["status"].values[0]

    if amount > 9000:
        reasons.append("High amount")
    if device == "MacOS":
        reasons.append("Unusual device")
    if city in ["Kolkata", "Chennai"]:
        reasons.append("Less common location")
    if status in ["Failed", "Pending"]:
        reasons.append("Transaction not confirmed")

    if reasons:
        st.info(f"🧠 Assistant Insight: Flagged due to: {', '.join(reasons)}")

    # Avoid duplicate logs
    if "last_logged_id" not in st.session_state:
        st.session_state.last_logged_id = None

    current_txn_id = latest_txn_raw["transaction_id"].values[0]

    if current_txn_id != st.session_state.last_logged_id:
        st.session_state.last_logged_id = current_txn_id

        row_to_log = latest_txn_raw.copy()
        row_to_log["is_fraud"] = is_fraud
        target_file = "data/fraud_transactions.csv" if is_fraud else "data/clean_transactions.csv"

        try:
            with open(target_file, "a") as f:
                row_to_log.to_csv(f, header=f.tell() == 0, index=False)
        except FileNotFoundError:
            row_to_log.to_csv(target_file, mode="w", index=False)

# Manual refresh button (no infinite rerun)
if st.button("🔁 Refresh Now"):
    st.rerun()
