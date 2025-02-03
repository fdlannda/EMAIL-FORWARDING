import requests

# Enter your Telegram bot token
BOT_TOKEN = "..."

# API URL
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

# Send request to get updates
response = requests.get(url)

# Print response
print(response.json())
