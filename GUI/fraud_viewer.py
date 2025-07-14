import customtkinter as ctk
import pandas as pd
from pathlib import Path

# ── Theme Setup ─────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # Matches your main GUI

# ── File Paths ──────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FRAUD_CSV = DATA / "fraud_transactions.csv"
CLEAN_CSV = DATA / "clean_transactions.csv"

# ── App Window ──────────────────────────────────────────────
app = ctk.CTk()
app.title("📋 UPI Logs – Live Viewer")
app.geometry("1400x700")  # Increased width

header = ctk.CTkLabel(app, text="📋 UPI Transactions (Live Stream)", font=("Helvetica", 22))
header.pack(pady=10)

# ── Side-by-Side Frame ──────────────────────────────────────
frame = ctk.CTkFrame(app, fg_color="black")
frame.pack(fill="both", expand=True, padx=20, pady=10)

# ── Left Column (Fraud Transactions) ────────────────────────
left_col = ctk.CTkFrame(frame, fg_color="black")
left_col.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

fraud_label = ctk.CTkLabel(left_col, text="🚨 Fraud Transactions", text_color="red", font=("Helvetica", 16))
fraud_label.pack(pady=(0, 4))

fraud_box = ctk.CTkTextbox(
    left_col,
    width=670,
    height=580,
    font=("Consolas", 11),
    text_color="red",
    fg_color="black",
    border_color="red",
    border_width=1,
    wrap="none"  # Prevent line wrapping
)
fraud_box.pack()

# ── Right Column (Clean Transactions) ───────────────────────
right_col = ctk.CTkFrame(frame, fg_color="black")
right_col.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)

clean_label = ctk.CTkLabel(right_col, text="✅ Safe Transactions", text_color="cyan", font=("Helvetica", 16))
clean_label.pack(pady=(0, 4))

clean_box = ctk.CTkTextbox(
    right_col,
    width=670,
    height=580,
    font=("Consolas", 11),
    text_color="cyan",
    fg_color="black",
    border_color="cyan",
    border_width=1,
    wrap="none"  # Prevent line wrapping
)
clean_box.pack()

# ── Live Refresh Function ───────────────────────────────────
def refresh():
    try:
        if FRAUD_CSV.exists():
            fraud_df = pd.read_csv(FRAUD_CSV).tail(100)
            fraud_box.delete("0.0", ctk.END)
            fraud_box.insert(ctk.END, fraud_df.to_string(index=False))
        else:
            fraud_box.delete("0.0", ctk.END)
            fraud_box.insert(ctk.END, "No fraud transactions yet.")

        if CLEAN_CSV.exists():
            clean_df = pd.read_csv(CLEAN_CSV).tail(100)
            clean_box.delete("0.0", ctk.END)
            clean_box.insert(ctk.END, clean_df.to_string(index=False))
        else:
            clean_box.delete("0.0", ctk.END)
            clean_box.insert(ctk.END, "No clean transactions yet.")

    except Exception as e:
        fraud_box.delete("0.0", ctk.END)
        clean_box.delete("0.0", ctk.END)
        fraud_box.insert(ctk.END, f"Error reading fraud.csv: {e}")
        clean_box.insert(ctk.END, f"Error reading clean.csv: {e}")

    app.after(1000, refresh)  # refresh every 2 seconds

# ── Launch ──────────────────────────────────────────────────
refresh()
app.mainloop()
