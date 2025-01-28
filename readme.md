# Email to Telegram Bot

This Python script is designed to monitor your email inbox for new messages and forward them to a specified Telegram chat. The bot also supports sending email attachments as Telegram documents.

## Features

- Fetches new (unread) emails from your inbox.
- Parses the email's subject, sender, recipient, and body.
- Formats email body for better readability in Telegram messages.
- Sends attachments as Telegram documents.

## Requirements

- Python 3.8+
- Gmail account (or other email providers with IMAP support)
- Telegram bot token

## Dependencies

Install the required Python libraries using the following command:

```bash
pip install beautifulsoup4 pyTelegramBotAPI
```

## Configuration

1. **Telegram Bot**
   - Create a bot using [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
   - Obtain your bot token.
   - Find your chat ID by messaging the bot and visiting `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`.

2. **Email Settings**
   - Use your email credentials (email address and app password).
   - Ensure IMAP is enabled for your email account.

3. **Script Variables**
   Update the following variables in the script:
   - `BOT_TOKEN`: Your Telegram bot token.
   - `CHAT_ID`: Your chat ID.
   - `EMAIL`: Your email address.
   - `PASSWORD`: Your email app password.

## How to Run

1. Clone this repository or copy the script.
2. Install dependencies as mentioned above.
3. Run the script:

```bash
python your_script_name.py
```

## File Structure

The script creates a folder named `attachments` in the current working directory to store email attachments.

## Notes

- This script uses Gmail's IMAP server (`imap.gmail.com`). If you're using a different email provider, update the `IMAP_SERVER` variable.
- For security reasons, always use an app password instead of your main email password.
- The email body is formatted for better readability in Telegram messages, particularly for numerical codes or structured text.

## Example Output

A Telegram message sent by the bot might look like this:

```
📧 *Email Baru*

*Dari:* sender@example.com
*Kepada:* your_email@gmail.com
*Subjek:* Test Email

*Isi Pesan:*
This is a test message.

12345
67890
```

Attachments are sent as documents with the following caption:

```
📎 *Lampiran: attachment_name.pdf*

(Dari: sender@example.com Kepada: your_email@gmail.com)
```

## Error Handling

The script includes error handling to ensure it continues running even if an error occurs. Errors are logged to the console.

## License

This project is open source and available under the MIT License.

