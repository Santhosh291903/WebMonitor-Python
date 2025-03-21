import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER", "<Email id>")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "<App password>")
TO_EMAILS = ["<TO_EMAILS>"]

# Load website status
STATUS_FILE = "website_status.json"

def load_website_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {}

# Send end-of-day email
def send_end_of_day_email():
    website_status = load_website_status()

    if not website_status:
        print("✅ No website downtime recorded. Skipping email.")
        return

    # Inline CSS for the email
    css_style = """
    <style>
        body { font-family: Arial, sans-serif; }
        h2 { color: #2E86C1; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
    """

    email_content = f"""
    <html>
    <head>{css_style}</head>
    <body>
        <h2>Daily Website Status Report</h2>
        <table>
            <tr>
                <th>Website</th>
                <th>Downtime Count</th>
                <th>Downtime Periods</th>
            </tr>
    """

    for url, data in website_status.items():
        time_ranges = "<br>".join(data["time_ranges"]) if data["time_ranges"] else "No Downtime"
        email_content += f"""
            <tr>
                <td>{url}</td>
                <td>{data['down_count']}</td>
                <td>{time_ranges}</td>
            </tr>
        """

    email_content += """
        </table>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Daily Website Monitoring Report"
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(TO_EMAILS)

    msg.attach(MIMEText(email_content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, TO_EMAILS, msg.as_string())
        print("📧 End-of-day email sent successfully!")

        # Clear the old data after sending email
        with open(STATUS_FILE, "w") as f:
            json.dump({}, f)

        print("🗑️ Old website status data cleared.")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    send_end_of_day_email()
