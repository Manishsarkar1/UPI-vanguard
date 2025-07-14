import customtkinter as ctk
import pandas as pd
import joblib
import subprocess
from scripts.preprocess import preprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x500")
app.title("🛡️ UPI Guardian – Desktop Live Monitor")

# Load model
model = joblib.load("models/Fraud_model.pkl")

# Widgets
header = ctk.CTkLabel(app, text="🛡️ UPI Guardian – Live Fraud Detection", font=("Helvetica", 20))
header.pack(pady=10)

log_box = ctk.CTkTextbox(app, width=950, height=240, font=("Consolas", 12))
log_box.pack(pady=10)

status_label = ctk.CTkLabel(app, text="Status: --", font=("Helvetica", 16))
status_label.pack(pady=5)

reason_label = ctk.CTkLabel(app, text="Reason: --", font=("Helvetica", 12))
reason_label.pack(pady=2)

def load_and_predict():
    try:
        df_raw = pd.read_csv("data/upi_transactions.csv")
        df_encoded, _ = preprocess("data/upi_transactions.csv")

        latest_raw = df_raw.tail(1)
        latest_encoded = df_encoded.tail(1)
        cols = [c for c in latest_encoded.columns if c not in ["transaction_id", "timestamp", "is_fraud"]]

        prediction = model.predict(latest_encoded[cols])
        is_fraud = prediction[0] == -1

        # Show full logs
        log_box.delete("0.0", ctk.END)
        log_box.insert(ctk.END, df_raw.tail(10).to_string(index=False))

        # Status output
        if is_fraud:
            status_label.configure(text="🚨 Fraud Detected", text_color="red")
        else:
            status_label.configure(text="✅ Safe Transaction", text_color="green")

        # Reasoning
        row = latest_raw.iloc[0]
        reasons = []
        if row["amount"] > 9000:
            reasons.append("High amount")
        if row["device"] == "MacOS":
            reasons.append("Unusual device")
        if row["city"] in ["Kolkata", "Chennai"]:
            reasons.append("Less common location")
        if row["status"] in ["Failed", "Pending"]:
            reasons.append("Unstable status")

        reason_label.configure(text=f"Reason: {', '.join(reasons) if reasons else 'Looks normal'}")

    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="orange")

def auto_refresh():
    load_and_predict()
    app.after(2000, auto_refresh)  # Refresh every 2 seconds

# Run once + schedule
load_and_predict()
auto_refresh()

# Button to open external fraud/clean viewer
def open_fraud_viewer():
    subprocess.Popen(["python", "GUI/fraud_viewer.py"])

open_btn = ctk.CTkButton(app, text="📂 Show Fraud & Clean Logs", command=open_fraud_viewer)
open_btn.pack(pady=15)

app.mainloop()
