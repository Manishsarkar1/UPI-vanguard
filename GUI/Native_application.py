# GUI/Native_application.py
# -------------------------------------------------------------
# Live desktop dashboard built with customtkinter
# -------------------------------------------------------------
import sys, os, subprocess, pandas as pd, joblib
import customtkinter as ctk
from pathlib import Path

# ── Ensure project root is on sys.path ────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent   # …/UPI‑vanguard
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from scripts.preprocess import preprocess            # now import works

# ── Appearance / theme ───────────────────────────────────────
ctk.set_appearance_mode("dark")          # "light", "dark", or "system"
ctk.set_default_color_theme("blue")      # blue / green / dark‑blue …

# ── Paths ─────────────────────────────────────────────────────
DATA_DIR   = ROOT_DIR / "data"
MODEL_PATH = ROOT_DIR / "models" / "Fraud_model.pkl"
RAW_CSV    = DATA_DIR / "upi_transactions.csv"
FRAUD_CSV  = DATA_DIR / "fraud_transactions.csv"
CLEAN_CSV  = DATA_DIR / "clean_transactions.csv"

# ── Load ML model once ───────────────────────────────────────
model = joblib.load(MODEL_PATH)

# ── GUI Window ───────────────────────────────────────────────
app = ctk.CTk()
app.title("🛡️ UPI Guardian – Desktop Live Monitor")
app.geometry("1000x520")

title = ctk.CTkLabel(app, text="🛡️ UPI Guardian – Live Fraud Detection", font=("Helvetica", 20))
title.pack(pady=10)

log_box = ctk.CTkTextbox(app, width=960, height=250, font=("Consolas", 11))
log_box.pack(pady=5)

status_lbl  = ctk.CTkLabel(app, text="Status: --",  font=("Helvetica", 16))
reason_lbl  = ctk.CTkLabel(app, text="Reason: --", font=("Helvetica", 12))
status_lbl.pack(pady=4)
reason_lbl.pack(pady=2)

# Keep track of last‑seen txn to avoid duplicates
last_logged_id: str | None = None

# ── Core update routine ──────────────────────────────────────
def update_dashboard():
    global last_logged_id

    try:
        # ---------- load newest data ----------
        df_raw = pd.read_csv(RAW_CSV)
        latest_raw = df_raw.tail(1)
        txn_id = latest_raw["transaction_id"].values[0]

        # ---------- display last 10 rows ----------
        log_box.delete("0.0", ctk.END)
        log_box.insert(ctk.END, df_raw.tail(10).to_string(index=False))

        # ---------- preprocess + predict ----------
        df_enc, _ = preprocess(str(RAW_CSV))
        latest_enc = df_enc.tail(1)
        features = [c for c in latest_enc.columns if c not in ("transaction_id", "timestamp", "is_fraud")]
        is_fraud = model.predict(latest_enc[features])[0] == -1

        # ---------- UI status ----------
        if is_fraud:
            status_lbl.configure(text="🚨 Fraud Detected", text_color="red")
        else:
            status_lbl.configure(text="✅ Safe Transaction", text_color="green")

        # ---------- assistant reasoning ----------
        row = latest_raw.iloc[0]
        reasons = []
        if row["amount"] > 9000:                      reasons.append("High amount")
        if row["device"] == "MacOS":                  reasons.append("Unusual device")
        if row["city"] in ("Kolkata", "Chennai"):     reasons.append("Less‑common location")
        if row["status"] in ("Failed", "Pending"):    reasons.append("Unstable status")
        reason_lbl.configure(text="Reason: " + (", ".join(reasons) if reasons else "Looks normal"))

        # ---------- log to fraud/clean CSV once ----------
        if txn_id != last_logged_id:
            last_logged_id = txn_id
            target = FRAUD_CSV if is_fraud else CLEAN_CSV
            mode   = "a" if target.exists() else "w"
            latest_raw.assign(is_fraud=is_fraud).to_csv(target, mode=mode, index=False, header=not target.exists())

    except Exception as e:
        status_lbl.configure(text=f"Error: {e}", text_color="orange")

    # schedule next refresh (2000 ms)
    app.after(1000, update_dashboard)

# ── Button to open separate log viewer ───────────────────────
def open_viewer():
    subprocess.Popen([sys.executable, str(ROOT_DIR / "gui" / "fraud_viewer.py")])

viewer_btn = ctk.CTkButton(app, text="📂 Show Fraud / Clean Logs", command=open_viewer)
viewer_btn.pack(pady=12)

# ── Kick‑off first update and launch app ─────────────────────
update_dashboard()
app.mainloop()
