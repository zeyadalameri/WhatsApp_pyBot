# WhatsApp Python Bot

A Python automation script for WhatsApp Web using Selenium. The bot opens WhatsApp Web, saves the browser session locally, monitors chats, detects new messages, and stores structured message data in JSON format.

## Features

- Automates WhatsApp Web using Selenium
- Saves browser session after QR login
- Monitors private and group chats
- Detects and logs new incoming messages
- Stores chat name, message text, and timestamp
- Uses JSON as a simple local data store
- Useful for learning browser automation and message monitoring workflows

## Tech Stack

- **Language:** Python
- **Automation:** Selenium
- **Browser:** Chrome / ChromeDriver
- **Storage:** JSON

## Project Structure

```text
.
├── bot.py              # Main automation script
├── messages.json       # Stored message logs
├── whatsapp_session/   # Local browser session data
└── .gitignore
```

## My Role

- Built the Python/Selenium automation script
- Implemented session persistence for WhatsApp Web
- Designed message monitoring and logging workflow
- Stored message data in structured JSON format

## Getting Started

1. Install Python dependencies:

```bash
pip install selenium
```

2. Make sure Chrome and ChromeDriver are installed and compatible.

3. Run the bot:

```bash
python bot.py
```

4. Scan the QR code on first login.

## Skills Demonstrated

- Python scripting
- Selenium browser automation
- Session persistence
- JSON logging
- Automation workflow design

## What I Learned

- Browser automation with Selenium
- Persisting login sessions across runs
- Extracting and storing structured data from web interactions
- Designing controlled automation prototypes

## Important Note

This project is intended for learning and controlled automation experiments. It should be used responsibly and in compliance with WhatsApp's terms and applicable privacy rules.

## Author

**Zeyad Alameri**  
Information Technology Graduate | Full-Stack Developer  
GitHub: [@zeyadalameri](https://github.com/zeyadalameri)
