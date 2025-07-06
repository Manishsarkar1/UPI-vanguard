import streamlit as st
import pandas as pd
import joblib
from scripts.preprocess import preprocess

#load the model
model = joblib.load("models/Fraud_model.pkl")

#title of the app
st.title("🫡 UPI Vanguard - Real-Time Fraud Detection")
st.markdown("Monitor and Flag suspicious UPI transactions in real-time using AI.")

#Load and preprocess the latest data
df, _ = preprocess("data/upi_transactions.csv")

#Predict fraud (anomalies)
preds = model.predict(df)
df['is_fraud'] = preds
df["is_fraud"] = df["is_fraud"].apply(lambda x: True if x == -1 else False)

#UI
st.subheader("❗ Transactions flagged as fraud")
st.dataframe(df[df["is_fraud"] == True], use_container_width=True)

#stats
st.markdown(f"**Total Transactions:** {len(df)}")
st.markdown(f"**Flagged as Fraud:** {df['is_fraud'].sum()}")