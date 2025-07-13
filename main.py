import streamlit as st
import pandas as pd
import joblib
from scripts.preprocess import preprocess

# Load model and data
model = joblib.load("models/Fraud_model.pkl")
df, _ = preprocess("data/upi_transactions.csv")

# Track index in session state
if "index" not in st.session_state:
    st.session_state.index = 0

if "go_next" not in st.session_state:
    st.session_state.go_next = False
if "go_prev" not in st.session_state:
    st.session_state.go_prev = False

# Process button actions first
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("⬅️ Previous"):
        st.session_state.go_prev = True

with col2:
    if st.button("✅ Confirm as Legit"):
        st.success("Thanks! This will help us learn in future.")

with col3:
    if st.button("🚫 Report Fraud"):
        st.warning("Fraud reported. We'll take further action.")

with col4:
    if st.button("➡️ Next"):
        st.session_state.go_next = True

# Apply navigation actions after buttons are clicked
if st.session_state.go_next:
    if st.session_state.index + 1 < len(df):
        st.session_state.index += 1
    st.session_state.go_next = False

if st.session_state.go_prev:
    if st.session_state.index > 0:
        st.session_state.index -= 1
    st.session_state.go_prev = False

# Load current transaction AFTER button actions
txn = df.iloc[st.session_state.index:st.session_state.index + 1]
columns_to_use = [col for col in txn.columns if col != "is_fraud"]
prediction = model.predict(txn[columns_to_use])
is_fraud = prediction[0] == -1

st.title("🛡️ UPI Guardian – Smart Transaction Assistant")
st.markdown("Simulating real UPI transaction experience for Walmart consumers.")

# Display transaction info
st.subheader("🧾 Transaction Details")
st.table(txn)

# Display result
if is_fraud:
    st.markdown("🚨 **Flagged as Suspicious**")
else:
    st.markdown("✅ **Marked as Safe**")

# Explain reasoning (simulated logic)
reasons = []
if "amount" in txn.columns and txn["amount"].values[0] > 9000:
    reasons.append("High amount")
if "device" in txn.columns and txn["device"].values[0] == 2:
    reasons.append("Unusual device")
if "location" in txn.columns and txn["location"].values[0] > 3:
    reasons.append("Less common location")

if reasons:
    st.info(f"🧠 Assistant Insight: This transaction was flagged due to: {', '.join(reasons)}")
