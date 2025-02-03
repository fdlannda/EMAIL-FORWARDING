import os
import time
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup  # To convert HTML to plain text
import telebot

# Telegram Bot Configuration
BOT_TOKEN = ''  # Enter your bot token
CHAT_ID = ''  # Enter your Chat ID
bot = telebot.TeleBot(BOT_TOKEN)

# Email Configuration
EMAIL = ''  # Enter your email
PASSWORD = ''  # Use an App Password for security
IMAP_SERVER = 'imap.gmail.com'  # Change to your email provider's IMAP server
CHECK_INTERVAL = 1  # Interval between checks (in seconds)

# Folder to store attachments
ATTACHMENT_FOLDER = "attachments"
if not os.path.exists(ATTACHMENT_FOLDER):
    os.makedirs(ATTACHMENT_FOLDER)

def clean_text(text):
    """Cleans text by removing invalid characters."""
    return ''.join(c if c.isalnum() else '_' for c in text)

def format_body_for_telegram(body):
    """Formats the message body so numbers/codes are easy to copy."""
    formatted_body = "\n".join(
        f"{line.strip()}" if line.strip().isdigit() else line
        for line in body.splitlines()
    )
    return formatted_body

def get_email_body(msg):
    """Extracts the email body, handling both plain text and HTML."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Extract email text (prioritizing text/plain, fallback to text/html)
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode(errors='ignore')
            elif content_type == "text/html" and not body:
                html = part.get_payload(decode=True).decode(errors='ignore')
                body = BeautifulSoup(html, "html.parser").get_text()
    else:
        body = msg.get_payload(decode=True).decode(errors='ignore')

    return body.strip()

def fetch_and_send_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")  # Select the inbox folder

        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Decode subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    from_ = msg.get("From")
                    to_ = msg.get("To")
                    
                    email_message = f"\U0001F4E7 *New Email*\n\n*From:* {from_}\n*To:* {to_}\n*Subject:* {subject}\n\n"

                    # Extract email content
                    body = get_email_body(msg)
                    if body:
                        formatted_body = format_body_for_telegram(body)
                        email_message += f"*Message Content:*\n{formatted_body}\n\n"

                    # Send message to Telegram
                    bot.send_message(CHAT_ID, email_message, parse_mode="Markdown")

                    # Process attachments if any
                    for part in msg.walk():
                        content_disposition = str(part.get("Content-Disposition"))
                        if "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                filename = clean_text(filename)
                                filepath = os.path.join(ATTACHMENT_FOLDER, filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                
                                # Send attachment to Telegram
                                with open(filepath, "rb") as f:
                                    bot.send_document(
                                        CHAT_ID, 
                                        f, 
                                        caption=f"\U0001F4CE *Attachment: {filename}*\n\n(From: {from_} To: {to_})"
                                    )

        mail.logout()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Bot is running. Waiting for new emails...")
    while True:
        try:
            fetch_and_send_emails()
        except Exception as e:
            print(f"Main error: {e}")
        time.sleep(CHECK_INTERVAL)
