#scripts/generate_pdf.py
import json
from fpdf import FPDF
import os

# লোড করা JSON ডেটা
with open("signal.json", "r") as f:
    signals = json.load(f)

# PDF ক্লাস
class PDF(FPDF):
    def header(self):
        self.set_fill_color(40, 44, 51)  # Page background
        self.rect(0, 0, 210, 297, 'F')
        self.set_text_color(214, 248, 255)
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "AI Generated Trade Signals", ln=1, align="C")

    def add_table(self, data):
        col_widths = [28, 22, 20, 22, 20, 18, 18, 20, 18, 25, 22, 20, 20]
        headers = [
            "Symbol", "Buy Price", "Hold", "Sell Price", "Profit %", "Conf%", "Trend", "Strategy",
            "R:R", "Expiry", "Stop Loss", "Valid", "Accuracy"
        ]

        # Header styling
        self.set_font("Arial", "B", 9)
        self.set_fill_color(28, 28, 28)
        self.set_text_color(167, 167, 167)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, "C", fill=True)
        self.ln()

        # Body rows
        self.set_font("Arial", "", 8)

        for idx, row in enumerate(data):
            bg_color = (37, 44, 46) if idx % 2 == 0 else (44, 52, 54)
            self.set_fill_color(*bg_color)
            for i, key in enumerate([
                "symbol", "buy_price", "hold_duration", "sell_price", "estimated_profit", "confidence",
                "trend", "strategy", "risk_reward_ratio", "expiry_date", "stop_loss", "validity_duration", "past_accuracy"
            ]):
                text_color = (0, 255, 80) if key == "trend" and row[key] == "Uptrend" else \
                             (255, 162, 0) if key == "trend" and row[key] == "Downtrend" else (214, 248, 255)
                self.set_text_color(*text_color)
                self.cell(col_widths[i], 8, str(row[key]), 1, 0, "C", fill=True)
            self.ln()

# PDF তৈরি
pdf = PDF()
pdf.add_page()
pdf.add_table(signals)

# ফাইল সংরক্ষণ
os.makedirs("output", exist_ok=True)
pdf.output("output/ai_signals_report.pdf")
print("✅ PDF created successfully at output/ai_signals_report.pdf")
