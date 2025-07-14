import customtkinter as ctk
import pandas as pd

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

win = ctk.CTk()
win.geometry("1000x600")
win.title("📋 Transaction Logs Viewer")

title = ctk.CTkLabel(win, text="📋 UPI Transactions (Clean vs Fraud)", font=("Helvetica", 20))
title.pack(pady=10)

fraud_label = ctk.CTkLabel(win, text="🚨 Fraud Transactions", font=("Helvetica", 14))
fraud_label.pack(pady=5)
fraud_box = ctk.CTkTextbox(win, width=950, height=200, font=("Consolas", 11))
fraud_box.pack()

clean_label = ctk.CTkLabel(win, text="✅ Safe Transactions", font=("Helvetica", 14))
clean_label.pack(pady=5)
clean_box = ctk.CTkTextbox(win, width=950, height=200, font=("Consolas", 11))
clean_box.pack()

try:
    fraud_df = pd.read_csv("data/fraud_transactions.csv").tail(10)
    clean_df = pd.read_csv("data/clean_transactions.csv").tail(10)
    fraud_box.insert("0.0", fraud_df.to_string(index=False))
    clean_box.insert("0.0", clean_df.to_string(index=False))
except Exception as e:
    fraud_box.insert("0.0", f"Error loading data: {e}")
    clean_box.insert("0.0", "")

win.mainloop()
