import os
import time
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup  # Untuk mengubah HTML menjadi teks biasa
import telebot

# Konfigurasi Telegram Bot
BOT_TOKEN = '7923488260:AAEn5U_3iXb7j_jhu6vnIjfLHicUMvl-7sw'  # Masukkan token bot Anda
CHAT_ID = '5638861236'  # Masukkan Chat ID Anda
bot = telebot.TeleBot(BOT_TOKEN)

# Konfigurasi Email
EMAIL = 'anandaforwarding@gmail.com'  # Masukkan email Anda
PASSWORD = 'qzip lvus elkd rlbt'  # Gunakan App Password untuk keamanan
IMAP_SERVER = 'imap.gmail.com'  # Ganti dengan server IMAP penyedia email Anda
CHECK_INTERVAL = 1  # Waktu jeda antar pengecekan (dalam detik)

# Folder untuk menyimpan lampiran
ATTACHMENT_FOLDER = "attachments"
if not os.path.exists(ATTACHMENT_FOLDER):
    os.makedirs(ATTACHMENT_FOLDER)

def clean_text(text):
    """Membersihkan teks dari karakter yang tidak valid."""
    return ''.join(c if c.isalnum() else '_' for c in text)

def format_body_for_telegram(body):
    """Memformat isi pesan agar angka/kode mudah di-copy."""
    formatted_body = "\n".join(
        f"`{line.strip()}`" if line.strip().isdigit() else line
        for line in body.splitlines()
    )
    return formatted_body

def get_email_body(msg):
    """Mengambil isi pesan email, baik teks biasa maupun HTML."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Ambil teks email (prioritas text/plain, jika tidak ada gunakan text/html)
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
        mail.select("inbox")  # Pilih folder inbox

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
                    
                    email_message = f"📧 *Email Baru*\n\n*Dari:* {from_}\n*Kepada:* {to_}\n*Subjek:* {subject}\n\n"

                    # Mendapatkan isi email
                    body = get_email_body(msg)
                    if body:
                        formatted_body = format_body_for_telegram(body)
                        email_message += f"*Isi Pesan:*\n{formatted_body}\n\n"

                    # Kirim pesan ke Telegram
                    bot.send_message(CHAT_ID, email_message, parse_mode="Markdown")

                    # Proses lampiran jika ada
                    for part in msg.walk():
                        content_disposition = str(part.get("Content-Disposition"))
                        if "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                filename = clean_text(filename)
                                filepath = os.path.join(ATTACHMENT_FOLDER, filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                
                                # Kirim lampiran ke Telegram
                                with open(filepath, "rb") as f:
                                    bot.send_document(
                                        CHAT_ID, 
                                        f, 
                                        caption=f"📎 *Lampiran: {filename}*\n\n(Dari: {from_} Kepada: {to_})"
                                    )

        mail.logout()

    except Exception as e:
        print(f"Terjadi error: {e}")

if __name__ == "__main__":
    print("Bot sedang berjalan. Menunggu email baru...")
    while True:
        try:
            fetch_and_send_emails()
        except Exception as e:
            print(f"Error utama: {e}")
        time.sleep(CHECK_INTERVAL)
