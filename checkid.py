import requests

# Masukkan bot token Anda
BOT_TOKEN = "7923488260:AAEn5U_3iXb7j_jhu6vnIjfLHicUMvl-7sw"

# API URL
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

# Kirim permintaan untuk mendapatkan pembaruan
response = requests.get(url)

# Cetak respon
print(response.json())
