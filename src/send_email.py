import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(html_content, subject="New Rental Matches"):
    """
    Send an HTML email through Gmail SMTP using app-password auth.

    Required environment variables:
    - GMAIL_ADDRESS
    - GMAIL_APP_PASSWORD

    Optional environment variable:
    - RECIPIENT_EMAIL (defaults to GMAIL_ADDRESS)
    """
    gmail_address = os.getenv("GMAIL_ADDRESS")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL") or gmail_address

    if not gmail_address:
        raise ValueError("Missing GMAIL_ADDRESS environment variable.")
    if not gmail_app_password:
        raise ValueError("Missing GMAIL_APP_PASSWORD environment variable.")
    if not recipient_email:
        raise ValueError("Missing RECIPIENT_EMAIL and GMAIL_ADDRESS environment variables.")

    # Build a multipart email so we can provide HTML content cleanly.
    message = MIMEMultipart("alternative")
    message["From"] = gmail_address
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(html_content, "html"))

    # Use Gmail's SSL SMTP endpoint for encrypted transport.
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_address, gmail_app_password)
        smtp.sendmail(gmail_address, recipient_email, message.as_string())
