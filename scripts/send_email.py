#scripts/send_email.py
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_TO = os.getenv("EMAIL_To")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_email():
    msg = EmailMessage()
    msg['Subject'] = "📈 Daily Stock Signal Report"
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO 

    msg.set_content(
        """\
Hello,

Please find attached today's AI-generated stock signal report.
This report includes trend direction and confidence for selected DSE stocks.

Best regards,  
AI Signal Bot
"""
    )

    # Attach the PDF file
    pdf_path = "outputs/stock_report.pdf"
    with open(pdf_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(pdf_path)

    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # Send the email
    with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    print("✅ Email sent successfully!")

if __name__ == "__main__":
    send_email()
