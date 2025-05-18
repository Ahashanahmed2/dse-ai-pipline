# reports/generate_pdf.py

import json
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'AI Trading Signals Report', 0, 1, 'C')
        self.ln(10)

    def add_table(self, data):
        # Get all headers from the first signal
        headers = list(data[0].keys())

        # Set font
        self.set_font("Arial", 'B', 10)
        col_widths = [35] * len(headers)  # Dynamic width based on number of columns

        # Add headers
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, str(header), 1, 0, 'C', True)
        self.ln()

        # Add rows
        self.set_font("Arial", '', 10)
        for row in data:
            for i, key in enumerate(headers):
                self.cell(col_widths[i], 8, str(row[key]), 1, 0, 'C')
            self.ln()

def generate_pdf_report(signals, filename="output/ai_signals_report.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add table
    pdf.add_table(signals)
    pdf.output(filename)
    print(f"✅ PDF created at {filename}")

if __name__ == "__main__":
    with open("signal.json") as f:
        signals = json.load(f)
    
    generate_pdf_report(signals)